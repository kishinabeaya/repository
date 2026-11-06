#!/usr/bin/env python3
"""PreToolUse: L3（禁止）操作と、未承認の公開をブロックする。
exit 2 でブロックし、stderr の理由がClaudeに伝わる。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISIONS = ROOT / "company" / "decisions"
PUBLISHED = ROOT / "company" / "content" / "published"

BASH_RULES = [
    (r"\brm\s+(-[a-zA-Z]*[rRf][a-zA-Z]*\s+)+(/|~|\.|\*|company\b|\.git\b)(\s|/|$)", "広範囲の削除は禁止（L3）"),
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s--force-with-lease\b|\s\+\S)", "force pushは禁止（L3）"),
    (r"\bgit\s+(reset\s+--hard|clean\s+-[a-zA-Z]*f|filter-branch|filter-repo)\b", "履歴・作業内容を破壊する操作は禁止（L3）"),
    (r"(^|[\s;&|])(cat|less|head|tail|more|grep|cp|mv)\s+[^|;&]*\.env\b", "秘密情報ファイルの読み出しは禁止（L3）"),
    (r"\b(curl|wget|http|httpie)\b[^|;&]*(\s-X\s*(POST|PUT|PATCH|DELETE)|\s--data|\s-d\s|\s-F\s|\s--form|\s--upload-file|\s-T\s)",
     "外部へのデータ送信はCEO承認が必要（L2）。下書きまでに留め、承認依頼を出してください"),
    (r"\b(npm|pnpm|yarn)\s+publish\b|\bgh\s+(release\s+create|repo\s+(edit|delete|create))\b|\bvercel\b.*--prod|\bnetlify\s+deploy\b.*--prod",
     "外部への公開・リリースはCEO承認が必要（L2）"),
]


def block(reason: str) -> None:
    print(f"[AI COMPANY OS ガード] ブロックしました: {reason}", file=sys.stderr)
    sys.exit(2)


def resolve(p: str) -> Path:
    path = Path(p)
    return (path if path.is_absolute() else ROOT / path).resolve()


def inside(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base.resolve())
        return True
    except ValueError:
        return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Bash":
        cmd = ti.get("command", "")
        for pattern, reason in BASH_RULES:
            if re.search(pattern, cmd):
                block(reason)
        if re.search(r"(>|\btee\b|\brm\b|\bmv\b|\bsed\s+-i)[^|;&]*company/decisions/", cmd):
            block("決定ログ（company/decisions/）はシェルで変更できません。新しい決定は Write ツールで新規作成してください")
        if re.search(r"(>|\btee\b|\bcp\b|\bmv\b)[^|;&]*company/content/published/", cmd):
            block("公開済みフォルダへはシェルで書き込めません。/approve の手順で Write ツールを使ってください")
        sys.exit(0)

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        fp = ti.get("file_path") or ti.get("notebook_path") or ""
        if not fp:
            sys.exit(0)
        path = resolve(fp)
        if re.search(r"(^|/)\.env(\.|$)", str(path)):
            block("秘密情報ファイル（.env）は編集できません（L3）")
        if inside(path, DECISIONS) and path.name != ".gitkeep":
            if tool != "Write" or path.exists():
                block("決定ログは追記のみです。既存の決定は変更できません。新しい決定ファイルを作成してください（L3）")
        if inside(path, PUBLISHED) and path.name != ".gitkeep":
            if tool != "Write":
                block("公開済みファイルは編集できません。修正版は新しい承認を経て公開してください")
            m = re.search(r"decision:\s*(D-\d{4})", ti.get("content", ""))
            if not m or not (DECISIONS / f"{m.group(1)}.md").exists():
                block("公開済みフォルダには、CEO承認の決定ID（decision: D-xxxx、実在するもの）を含むファイルしか置けません（L2）")
    sys.exit(0)


if __name__ == "__main__":
    main()
