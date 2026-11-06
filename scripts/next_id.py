#!/usr/bin/env python3
"""次のIDを表示する。使い方: python3 scripts/next_id.py T|D|A
T=タスク(company/tasks)  D=決定(company/decisions)  A=承認依頼(company/inbox/ceo)
"""
import re
import sys

from _common import COMPANY

DIRS = {"T": COMPANY / "tasks", "D": COMPANY / "decisions", "A": COMPANY / "inbox" / "ceo"}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1].upper() not in DIRS:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    prefix = sys.argv[1].upper()
    pattern = re.compile(rf"^{prefix}-(\d{{4}})")
    nums = [int(m.group(1)) for p in DIRS[prefix].glob(f"{prefix}-*") if (m := pattern.match(p.name))]
    print(f"{prefix}-{max(nums, default=0) + 1:04d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
