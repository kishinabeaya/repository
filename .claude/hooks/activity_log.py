#!/usr/bin/env python3
"""PostToolUse: ファイル変更を company/logs/activity.jsonl に記録する。
Bashコマンドは記録しない（CEO決定 2026-11-06）。git commit 自体がログに残り、
未コミット変更が永久に発生するため。コマンド履歴はGitのコミット履歴で追える。
"""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "company" / "logs" / "activity.jsonl"

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}
entry = {"ts": datetime.now().isoformat(timespec="seconds"), "tool": tool}
if "agent_type" in data:
    entry["agent"] = data["agent_type"]
if tool == "Bash":
    sys.exit(0)
fp = ti.get("file_path") or ti.get("notebook_path") or ""
try:
    fp = str(Path(fp).resolve().relative_to(ROOT))
except ValueError:
    pass
entry["file"] = fp
try:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
except OSError:
    pass
sys.exit(0)
