import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in ("scripts", "intake"):
    p = os.path.join(ROOT, sub)
    if p not in sys.path:
        sys.path.insert(0, p)


def read(path, mode="r"):
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        return f.read()
