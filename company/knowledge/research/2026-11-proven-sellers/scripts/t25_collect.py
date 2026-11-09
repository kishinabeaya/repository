#!/usr/bin/env python3 -I
"""T-0025 詳細ページ取得（GETのみ・ログインなし・間隔1.5秒・上限200リクエスト・確認ページは間隔を伸ばし連続3回で打ち切り）。
使い方: python3 -I t25_collect.py <ココナラ全カテゴリCSV> <キャッシュdir> [probe_count_already]
対象: (A)話し相手(51)の一覧順位上位45 + 評価100未満の全件 (B)占い3+悩み相談7の各カテゴリ、評価件数上位5
      (C)占い3カテゴリの評価100未満の全件。重複は1回だけ取得。
"""
import sys, os, csv, time, subprocess, re
CSV_, CACHE = sys.argv[1], sys.argv[2]
LIMIT = 200
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
F = ['660', '656', '658']; C = ['693', '53', '51', '50', '676', '692', '647']
rows = list(csv.DictReader(open(CSV_, encoding='utf8')))
by = {}
for r in rows: by.setdefault(r['category_id'], []).append(r)
targets = []; seen = set()
def add(r, grp):
    if r['service_id'] in seen: return
    seen.add(r['service_id']); targets.append((r['service_id'], grp))
for r in by['51'][:45]: add(r, 'companion_top45')
for r in by['51']:
    if int(r['service_rating_count']) < 100: add(r, 'companion_lt100')
for cid in F + C:
    if cid == '51': continue
    for r in sorted(by[cid], key=lambda r: (-int(r['service_rating_count']), int(r['rank_in_category'])))[:5]: add(r, f'top5_{cid}')
for cid in F:
    for r in by[cid]:
        if int(r['service_rating_count']) < 100: add(r, f'fortune_lt100_{cid}')
LOG = os.path.join(CACHE, 'requests.log')
def nreq(): return sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
def ok(p): return os.path.exists(p) and os.path.getsize(p) > 100000 and '"@type": "Product"' in open(p, encoding='utf8').read()
print('targets', len(targets), flush=True)
wait = 1.5; fails = 0
for sid, grp in targets:
    p = os.path.join(CACHE, f'svc-{sid}.html')
    if ok(p): continue
    if nreq() >= LIMIT - 2: print('limit'); break
    time.sleep(wait)
    r = subprocess.run(['curl', '-s', '-m', '40', '-A', UA, '-o', p, '-w', '%{http_code}', f'https://coconala.com/services/{sid}'], capture_output=True, text=True)
    open(LOG, 'a').write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {r.stdout} {sid}\n")
    if ok(p):
        fails = 0; wait = 1.5
    else:
        fails += 1; wait = wait * 2
        print('NOT OK', sid, r.stdout, 'fails', fails, flush=True)
        if os.path.exists(p): os.rename(p, p + '.bad')
        if fails >= 3: print('abort: 3 consecutive'); break
print('done req', nreq(), flush=True)
open(os.path.join(CACHE, 'targets.csv'), 'w').write('\n'.join(f'{a},{b}' for a, b in targets))
