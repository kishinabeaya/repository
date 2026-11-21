#!/usr/bin/env python3
"""工程の担当と所要分数を記録する（「9割」の測定用）。標準ライブラリのみ。
使い方: python3 log_step.py --order ORD-0001 --step build --actor claude --minutes 25 --note "LPを生成"
工程: intake(受付) requirements(要件確認) build(制作) qa(検証) delivery(納品) revision(修正対応) payment(入金確認)
      日本語名でも指定できる。担当: claude / ceo。記録先: ../tracking/steps.jsonl（--file で変更）
形式: {"order_id","step","actor","minutes","note"}。個人情報（氏名・連絡先・住所）は書かない。"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import ACTORS, JA2ID, ORDER_RE, STEPS, find_pii  # noqa: E402

DEFAULT_FILE = os.path.join(os.path.dirname(HERE), "tracking", "steps.jsonl")


def make_record(order_id, step, actor, minutes, note=""):
    if not ORDER_RE.match(str(order_id)):
        raise ValueError("order_id は英数字・ハイフン・下線のみ（個人名は使わない）")
    step = JA2ID.get(step, step)
    if step not in STEPS:
        raise ValueError("step は %s のどれか" % "、".join("%s(%s)" % kv for kv in STEPS.items()))
    if actor not in ACTORS:
        raise ValueError("actor は claude か ceo")
    try:
        minutes = float(minutes)
    except (TypeError, ValueError):
        raise ValueError("minutes は数字で")
    if not (0 <= minutes <= 1440):
        raise ValueError("minutes は 0〜1440")
    note = (note or "").strip()
    if find_pii(note):
        raise ValueError("note に個人情報（メール・電話・郵便番号など）らしき記載があります。書き換えてください")
    if len(note) > 200:
        raise ValueError("note は200字まで")
    return {"order_id": order_id, "step": step, "actor": actor,
            "minutes": int(minutes) if minutes == int(minutes) else minutes, "note": note}


def append_record(path, rec):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="工程の記録")
    ap.add_argument("--order", required=True)
    ap.add_argument("--step", required=True)
    ap.add_argument("--actor", required=True)
    ap.add_argument("--minutes", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--file", default=DEFAULT_FILE)
    args = ap.parse_args(argv)
    try:
        rec = make_record(args.order, args.step, args.actor, args.minutes, args.note)
    except ValueError as e:
        print("記録できませんでした: %s" % e, file=sys.stderr)
        return 1
    append_record(args.file, rec)
    print("記録しました: %s %s %s %s分" % (rec["order_id"], rec["step"], rec["actor"], rec["minutes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
