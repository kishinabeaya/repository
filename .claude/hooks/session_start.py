#!/usr/bin/env python3
"""SessionStart: 会社の現状をセッション冒頭の文脈に読み込ませる。"""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = subprocess.run(
    [sys.executable, str(root / "scripts" / "status.py"), "--brief"],
    capture_output=True, text=True, cwd=root,
)
print("あなたはこのリポジトリのChief of Staffです（CLAUDE.md参照）。現在の会社の状況:")
print(out.stdout.strip() or "(状況を取得できませんでした)")
