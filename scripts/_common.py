"""AI COMPANY OS 共通ユーティリティ（標準ライブラリのみ使用）"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPANY = ROOT / "company"


def read_frontmatter(path: Path) -> dict:
    """Markdown先頭の --- で囲まれた簡易YAML（key: value）を読む。"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if "#" in val and not val.startswith(("'", '"')):
            val = val.split(" #", 1)[0].strip()
        if val.startswith("[") and val.endswith("]"):
            data[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            data[key] = val.strip("'\"")
    return data
