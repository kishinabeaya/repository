#!/usr/bin/env python3
"""クラウドワークスの公開の案件一覧（ログイン不要）から、予算・契約数などを集める（T-0037）。
GETのみ。ログイン・応募・問い合わせはしない。間隔を置く。確認ページが返ったら打ち切る。
使い方: python3 crowdworks_collect.py <出力CSV>
"""
import csv
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime

QUERIES = [
    "AI導入", "AI活用 業務効率化", "営業代行", "テレアポ", "ホームページ制作", "LP制作",
    "事務代行", "経理代行", "広告運用", "SNS運用代行", "データ入力", "データ分析 集計",
    "採用 代行", "業務改善", "システム開発", "Webサイト 構築", "資料作成", "補助金",
    "リスト作成", "ライティング",
]
PAGES = 2
UA = "Mozilla/5.0"


def fetch(q: str, page: int) -> str | None:
    url = ("https://crowdworks.jp/public/jobs/search?keywords="
           + urllib.parse.quote(q) + "&order=new&page=" + str(page))
    r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "30", url],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def parse(t: str):
    m = re.search(r'id="vue-container" data="([^"]*)"', t)
    if not m:
        return None, None
    d = json.loads(html.unescape(m.group(1)))
    sr = d.get("searchResult", {})
    return sr.get("job_offers", []), sr.get("page", {})


def main() -> int:
    out = sys.argv[1]
    seen = {}
    blocked = 0
    log = []
    for q in QUERIES:
        for p in range(1, PAGES + 1):
            t = fetch(q, p)
            time.sleep(1.5)
            if not t:
                blocked += 1
                if blocked >= 3:
                    break
                continue
            offers, page = parse(t)
            if offers is None:
                blocked += 1
                if blocked >= 3:
                    break
                continue
            blocked = 0
            for o in offers:
                jo = o["job_offer"]
                if jo["id"] in seen:
                    continue
                pay = o.get("payment", {})
                kind, lo, hi = "", None, None
                if "fixed_price_payment" in pay:
                    kind = "固定報酬"
                    lo = pay["fixed_price_payment"].get("min_budget")
                    hi = pay["fixed_price_payment"].get("max_budget")
                elif "hourly_payment" in pay:
                    kind = "時給"
                    lo = pay["hourly_payment"].get("min_hourly_wage")
                    hi = pay["hourly_payment"].get("max_hourly_wage")
                elif "task_payment" in pay:
                    kind = "タスク"
                    lo = pay["task_payment"].get("task_price")
                    hi = lo
                else:
                    kind = ",".join(pay.keys()) or "不明"
                ent = o.get("entry", {}).get("project_entry", {})
                cl = o.get("client", {})
                seen[jo["id"]] = {
                    "query": q,
                    "id": jo["id"],
                    "title": jo["title"][:90],
                    "category_id": jo.get("category_id"),
                    "payment_kind": kind,
                    "min": lo,
                    "max": hi,
                    "num_contracts": ent.get("num_contracts"),
                    "hope_number": ent.get("project_contract_hope_number"),
                    "released": jo.get("last_released_at", "")[:10],
                    "expired_on": jo.get("expired_on"),
                    "client_certified": cl.get("is_employer_certification"),
                    "client_is_company": bool(re.search(r"株式会社|有限会社|合同会社|\(株\)|Inc|LLC", cl.get("username", ""))),
                }
            log.append((q, p, len(offers), (page or {}).get("total_entries")))
        if blocked >= 3:
            print("連続3回失敗のため打ち切り", file=sys.stderr)
            break
    rows = list(seen.values())
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["id"])
        w.writeheader()
        w.writerows(rows)
    print("取得日時:", datetime.now().isoformat(timespec="seconds"))
    print("件数:", len(rows))
    for q, p, n, tot in log:
        print(f"  {q} p{p}: {n}件 (検索ヒット総数 {tot})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
