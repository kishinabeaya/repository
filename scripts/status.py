#!/usr/bin/env python3
"""会社の現状サマリーを表示する。使い方: python3 scripts/status.py [--brief]"""
import sys
from datetime import date

from _common import COMPANY, read_frontmatter

ORDER = ["planned", "in_progress", "review", "rejected", "waiting_approval", "blocked", "done"]
PRIO = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def load_tasks():
    tasks = []
    for p in sorted((COMPANY / "tasks").glob("T-*.md")):
        fm = read_frontmatter(p)
        fm.setdefault("id", p.stem)
        tasks.append(fm)
    return tasks


def main() -> int:
    brief = "--brief" in sys.argv
    today = date.today().isoformat()
    tasks = load_tasks()
    by_id = {t["id"]: t for t in tasks}

    counts = {s: 0 for s in ORDER}
    for t in tasks:
        counts[t.get("status", "planned")] = counts.get(t.get("status", "planned"), 0) + 1

    open_tasks = [t for t in tasks if t.get("status") != "done"]
    overdue = [t for t in open_tasks if t.get("due") and t["due"] < today]

    def ready(t):
        if t.get("status") not in ("planned", "in_progress", "rejected"):
            return False
        return all(by_id.get(d, {}).get("status") == "done" for d in t.get("depends_on", []) or [])

    actionable = sorted(
        (t for t in open_tasks if ready(t)),
        key=lambda t: (PRIO.get(t.get("priority", "P3"), 3), t.get("due") or "9999"),
    )
    pending = [
        (p.stem, read_frontmatter(p))
        for p in sorted((COMPANY / "inbox" / "ceo").glob("A-*.md"))
    ]
    pending = [(i, fm) for i, fm in pending if fm.get("status", "pending") == "pending"]
    reports = sorted((COMPANY / "reports" / "daily").glob("*.md"))

    print(f"# AI COMPANY OS 現状 ({today})")
    print("タスク: " + " / ".join(f"{s}={counts[s]}" for s in ORDER if counts.get(s)) if tasks else "タスク: なし")
    print(f"CEO承認待ち: {len(pending)}件")
    for i, fm in pending:
        print(f"  - {i}: {fm.get('title', '')} (task {fm.get('task', '-')})")
    if overdue:
        print(f"期限切れ: {len(overdue)}件")
        for t in overdue:
            print(f"  - {t['id']} {t.get('title', '')} [{t.get('owner', '?')}] due {t['due']}")
    print(f"着手可能: {len(actionable)}件")
    for t in actionable[: 3 if brief else 10]:
        print(f"  - {t['id']} {t.get('priority', '')} {t.get('title', '')} [{t.get('owner', '?')}] {t.get('status')}")
    if not brief:
        for s in ("in_progress", "review", "rejected", "waiting_approval", "blocked"):
            items = [t for t in tasks if t.get("status") == s]
            if items:
                print(f"{s}:")
                for t in items:
                    print(f"  - {t['id']} {t.get('title', '')} [{t.get('owner', '?')}]")
    print(f"最新の日報: {reports[-1].relative_to(COMPANY.parent) if reports else 'なし'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
