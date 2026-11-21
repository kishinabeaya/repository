#!/usr/bin/env python3
"""ココナラのメッセージにそのまま貼れる質問票を出力する。
使い方: python3 make_questionnaire.py homepage|lp|automation|data"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = ("homepage", "lp", "automation", "data")


def build(kind):
    if kind not in TYPES:
        raise ValueError("種類は %s のどれかです" % ", ".join(TYPES))
    parts = []
    for name in ("common", kind):
        with open(os.path.join(HERE, "questionnaire_%s.txt" % name), encoding="utf-8") as f:
            parts.append(f.read().rstrip("\n"))
    return "\n\n".join(parts) + "\n"


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        sys.stdout.write(build(argv[1]))
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
