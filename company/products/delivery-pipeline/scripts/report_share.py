#!/usr/bin/env python3
"""CEOの作業の割合を集計する（工程ベースと時間ベース）。標準ライブラリのみ。
使い方: python3 report_share.py [--file ../tracking/steps.jsonl] [--order ORD-0001]
工程ベース: (order_id, step, actor) の組を1件と数え、ceoの件数 ÷ 全件数（参考値。CEOの工程は受付・納品・入金確認の転記や確認なので、件数では高く出る）。
時間ベース: ceoの minutes の合計 ÷ 全 minutes の合計。目標は 10% 以下（D-0023）。"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import ACTORS, STEPS  # noqa: E402

DEFAULT_FILE = os.path.join(os.path.dirname(HERE), "tracking", "steps.jsonl")
TARGET = 0.10


def load(path):
    """(記録のリスト, 読めなかった行の説明のリスト)"""
    recs, bad = [], []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r["actor"] not in ACTORS or r["step"] not in STEPS:
                    raise ValueError("actor/step が不正")
                r["minutes"] = float(r["minutes"])
                if r["minutes"] < 0:
                    raise ValueError("minutes が負")
                str(r["order_id"])
                recs.append(r)
            except (ValueError, KeyError, TypeError) as e:
                bad.append("%d行目: %s" % (n, e))
    return recs, bad


def summarize(recs):
    units = {(r["order_id"], r["step"], r["actor"]) for r in recs}
    ceo_units = sum(1 for u in units if u[2] == "ceo")
    tot_min = sum(r["minutes"] for r in recs)
    ceo_min = sum(r["minutes"] for r in recs if r["actor"] == "ceo")
    per_step = {}
    for r in recs:
        d = per_step.setdefault(r["step"], {"claude": 0.0, "ceo": 0.0})
        d[r["actor"]] += r["minutes"]
    return {
        "units": len(units), "ceo_units": ceo_units,
        "step_share": (ceo_units / len(units)) if units else None,
        "total_min": tot_min, "ceo_min": ceo_min,
        "time_share": (ceo_min / tot_min) if tot_min > 0 else None,
        "per_step": per_step,
        "orders": len({r["order_id"] for r in recs}),
    }


def pct(x):
    return "データなし" if x is None else "%.1f%%" % (x * 100)


def judge(x):
    if x is None:
        return "判定できません"
    return "目標内（10%以下）" if x <= TARGET else "目標超過（10%超）"


def render(s, bad=()):
    L = ["# CEOの作業の割合", "",
         "- 注文数: %d 件" % s["orders"],
         "- 工程ベース（参考）: %s（CEO %d 件 / 全 %d 件）。CEOの工程は、転記・確認・入金確認に限る前提のため、件数の割合は高く出ます。CEOの記録に、それ以外の作業がないかを見てください" % (pct(s["step_share"]), s["ceo_units"], s["units"]),
         "- 時間ベース（目標の判定に使う）: %s（CEO %g 分 / 全 %g 分）→ %s" % (pct(s["time_share"]), s["ceo_min"], s["total_min"], judge(s["time_share"])),
         "", "## 工程ごとの所要分", "", "| 工程 | Claude Code（分） | CEO（分） |", "|---|---|---|"]
    for k, ja in STEPS.items():
        d = s["per_step"].get(k)
        if d:
            L.append("| %s | %g | %g |" % (ja, d["claude"], d["ceo"]))
    if bad:
        L += ["", "## 読めなかった行（集計に含めていません）"] + ["- " + b for b in bad]
    L += ["", "注意: 所要分はCEOとClaude Codeの自己申告の記録です。記録の漏れがあると、割合は変わります。"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="CEOの割合の集計")
    ap.add_argument("--file", default=DEFAULT_FILE)
    ap.add_argument("--order")
    args = ap.parse_args(argv)
    if not os.path.exists(args.file):
        print("記録ファイルがありません: %s" % args.file, file=sys.stderr)
        return 1
    recs, bad = load(args.file)
    if args.order:
        recs = [r for r in recs if r["order_id"] == args.order]
    sys.stdout.write(render(summarize(recs), bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
