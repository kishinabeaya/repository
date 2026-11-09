#!/usr/bin/env python3 -I
"""T-0025 集計。使い方: python3 -I t25_build.py <ココナラ全カテゴリCSV> <キャッシュdir> <出力raw dir>
出力: coconala-companion.csv / coconala-companion-reviews.jsonl / coconala-fortune-detail.csv / coconala-new-entrants.csv / t25-tables.md
購入者名・出品者名は保存しない（レビューのauthorは捨てる。本文中の出品者表示名は[名前]に置換）。"""
import sys, os, re, csv, json, html as H, statistics as st, collections, datetime as dt
CSV_, CACHE, RAW = sys.argv[1:4]
SNAP = dt.date(2026, 11, 9)   # 詳細ページ取得日
LIST_SNAP = '2026-11-07'
F = {'660': '仕事運・仕事占い', '656': '恋愛占い', '658': 'スピリチュアル鑑定'}
rows = list(csv.DictReader(open(CSV_, encoding='utf8')))
by = {}
for r in rows: by.setdefault(r['category_id'], []).append(r)
targets = {}
for l in open(os.path.join(CACHE, 'targets.csv')).read().split('\n'):
    if l: a, b = l.split(','); targets[a] = b
targets.setdefault('3598316', 'companion_top45')
def txt(s): return re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', ' ', re.sub(r'<style.*?</style>|<script.*?</script>', '', s, flags=re.S)))).strip()
def num(s): return int(s.replace(',', ''))
QUAL = re.compile(r'公認心理師|臨床心理士|心理カウンセラー|産業カウンセラー|キャリアコンサルタント|国家資格|精神保健福祉士|社会福祉士|看護師|医師|保育士|認定|資格|ライセンス|修了|取得')
CAREER = re.compile(r'経験|歴\d*年|\d+年|元[^\s]{1,8}|現役|勤務|在籍|キャリア|実績|スナック|ホスト|ママ|ホステス|接客|カウンセリング')
def parse(sid):
    p = os.path.join(CACHE, f'svc-{sid}.html')
    if not os.path.exists(p): return None
    h = open(p, encoding='utf8').read()
    i = h.find('"@type": "Product"')
    if i < 0: return None
    s = h.rfind('<script', 0, i); e = h.find('</script>', i)
    try: j = json.loads(h[h.find('>', s)+1:e])
    except Exception: return None
    t = txt(h); d = {'jsonld': j}
    m = re.search(r'評価 ([\d.]+) \(([\d,]+)\) 販売実績 ([\d,]+) 件', t)
    d['page_rating_score'] = m.group(1) if m else ''; d['page_rating_count'] = num(m.group(2)) if m else ''
    d['service_sales'] = num(m.group(3)) if m else ''
    m = re.search(r'総販売実績： ?([\d,]+)件', t); d['seller_total_sales'] = num(m.group(1)) if m else ''
    m = re.search(r'サービス内容 購入時のお願い(?: よくある質問)? 評価・感想 (.{0,30}?) お気に入り\(', t); d['accept_text'] = m.group(1) if m else ''
    m = re.search(r'提供形式 ([^ ]+)', t); d['provision'] = m.group(1) if m else ''
    m = re.search(r'手法 (.{1,40}?) (?:性別|高評価のレビュー|スタイル|ジャンル)', t); d['method'] = m.group(1) if m else ''
    m = re.search(r'お届け日数 (.{1,40}?) (?:初回返答時間|スタイル|$)', t); d['delivery_days'] = m.group(1) if m else ''
    m = re.search(r'初回返答時間 (.{1,20}?) ', t); d['first_reply'] = m.group(1) if m else ''
    m = re.search(r'出品者プロフィール (.{1,80}?) 出品者ランク', t); d['seller_display'] = m.group(1) if m else ''
    m = re.search(r'出品者ランク： (\S+)', t); d['seller_rank'] = m.group(1) if m else ''
    m = re.search(r'お気に入り\(([\d,]+)\)', t); d['favorites'] = num(m.group(1)) if m else ''
    m = re.search(r'サービス内容 (.*?) (?:購入時のお願い|よくある質問|評価・感想 \d)', t[t.find('ココナラの安心保証'):])
    d['desc'] = j.get('description', '')
    d['qual_flag'] = 'あり' if QUAL.search(d['desc']) else 'なし'
    d['career_flag'] = 'あり' if CAREER.search(d['desc']) else 'なし'
    d['desc_len'] = len(d['desc'])
    return d
def scrub(text, disp):
    names = set()
    if disp:
        for tok in re.split(r'[｜|/／・\s☆★♡✨⭐︎()（）【】]+', disp):
            if len(tok) >= 2: names.add(tok)
        names.add(disp)
    for n in sorted(names, key=len, reverse=True): text = text.replace(n, '[名前]')
    return text
def form(d, r):
    pv = d['provision']
    if r['price_unit'] == '円/分':
        if '電話' in pv and 'チャット' in pv: return '電話+チャット'
        if '電話' in pv: return '電話'
        if 'チャット' in pv: return 'チャット'
        return pv or '取得できず'
    return pv or '円建て（提供形式取得できず）'
lk = {r['service_id']: r for r in rows}
det = {}; reviews = []
for sid in targets:
    d = parse(sid)
    if d: det[sid] = d
# 話し相手
comp_rows = []
comp_ids = [x['service_id'] for x in by['51'] if targets.get(x['service_id'], '').startswith('companion')]
for sid in comp_ids:
    if sid not in det: continue
    r, d = lk[sid], det[sid]
    comp_rows.append(dict(service_id=sid, rank_in_category=r['rank_in_category'], group=targets[sid], title=r['title'],
        price_yen=r['min_price_yen'], price_unit=r['price_unit'], form=form(d, r), accept_text=d['accept_text'],
        delivery_days=d['delivery_days'], first_reply=d['first_reply'], rating_count_listing=r['service_rating_count'],
        rating_count_page=d['page_rating_count'], rating_score=d['page_rating_score'], service_sales=d['service_sales'],
        seller_total_sales=d['seller_total_sales'], seller_rank=d['seller_rank'], favorites=d['favorites'],
        method_attr=d['method'], profile_qualification_text=d['qual_flag'], profile_career_text=d['career_flag'], reviews_in_page=len(d['jsonld'].get('review', [])), url=r['url']))
w = csv.DictWriter(open(os.path.join(RAW, 'coconala-companion.csv'), 'w', newline='', encoding='utf8'), fieldnames=list(comp_rows[0].keys())); w.writeheader(); w.writerows(comp_rows)
# レビュー
rev_n = collections.Counter(); rv = open(os.path.join(RAW, 'coconala-companion-reviews.jsonl'), 'w', encoding='utf8')
nrev = 0
for sid, d in det.items():
    r = lk[sid]; seen = set()
    for x in d['jsonld'].get('review', []):
        body = x.get('reviewBody', '') or ''
        if not body.strip(): continue
        rec = dict(service_id=sid, category=r['category'], group=targets[sid], date=x.get('datePublished', ''),
                   rating=(x.get('reviewRating') or {}).get('ratingValue', ''), text=scrub(body, d['seller_display']))
        rv.write(json.dumps(rec, ensure_ascii=False) + '\n'); nrev += 1; rev_n[(sid)] += 1
rv.close()
# 占い・悩み相談 詳細
fd = []
for sid, d in det.items():
    g = targets[sid]
    if not (g.startswith('top5_') and g != 'top5_51') and not g.startswith('fortune_lt100'): continue
    r = lk[sid]
    fd.append(dict(service_id=sid, category_id=r['category_id'], category=r['category'], group=g, rank_in_category=r['rank_in_category'], title=r['title'],
        price_yen=r['min_price_yen'], price_unit=r['price_unit'], form=form(d, r), accept_text=d['accept_text'], delivery_days=d['delivery_days'],
        rating_count_listing=r['service_rating_count'], rating_count_page=d['page_rating_count'], rating_score=d['page_rating_score'],
        service_sales=d['service_sales'], seller_total_sales=d['seller_total_sales'], seller_rank=d['seller_rank'], favorites=d['favorites'],
        method_attr=d['method'], profile_qualification_text=d['qual_flag'], profile_career_text=d['career_flag'], reviews_in_page=len(d['jsonld'].get('review', [])), url=r['url']))
if fd:
    w = csv.DictWriter(open(os.path.join(RAW, 'coconala-fortune-detail.csv'), 'w', newline='', encoding='utf8'), fieldnames=list(fd[0].keys())); w.writeheader(); w.writerows(fd)
# 新規参入（一覧の評価件数<100の詳細取得分）
ne = []
for sid, d in det.items():
    r = lk[sid]
    if int(r['service_rating_count']) >= 100: continue
    revs = [x for x in d['jsonld'].get('review', []) if x.get('datePublished')]
    dates = sorted(dt.date.fromisoformat(x['datePublished']) for x in revs)
    page_n = d['page_rating_count'] if d['page_rating_count'] != '' else None
    complete = (page_n is not None and len(dates) >= page_n and len(dates) > 0)
    first = dates[0] if dates else None
    tenth = dates[9] if len(dates) >= 10 else None
    ne.append(dict(service_id=sid, category=r['category'], group=targets[sid], price_yen=r['min_price_yen'], price_unit=r['price_unit'],
        rating_count_listing=r['service_rating_count'], rating_count_page=page_n if page_n is not None else '',
        reviews_with_date=len(dates), all_reviews_captured='yes' if complete else 'no',
        listing_date='取得できず', first_review_date=first.isoformat() if first else '', last_review_date=dates[-1].isoformat() if dates else '',
        days_first_review_to_snapshot=(SNAP-first).days if first else '', days_first_to_last=(dates[-1]-first).days if first else '',
        days_first_to_10th=(tenth-first).days if tenth else '', seller_total_sales=d['seller_total_sales'], service_sales=d['service_sales'], url=r['url']))
if ne:
    w = csv.DictWriter(open(os.path.join(RAW, 'coconala-new-entrants.csv'), 'w', newline='', encoding='utf8'), fieldnames=list(ne[0].keys())); w.writeheader(); w.writerows(ne)
# ---- 集計表 ----
out = []
def P(s=''): out.append(s)
def q(vals, ps=(0, .25, .5, .75, 1)):
    v = sorted(vals); n = len(v)
    return [v[min(n-1, int(round(p*(n-1))))] for p in ps]
P(f'## 取得件数\n- 詳細取得: {len(det)}サービス / 対象{len(targets)}')
P(f'- 話し相手の詳細取得: {len(comp_rows)} / レビュー本文(JSON-LD, 空本文除く) 全体: {nrev}、話し相手のみ: {sum(v for k,v in rev_n.items() if targets[k].startswith("companion"))}')
# 話し相手の分単価
pm = [int(r['price_yen']) for r in comp_rows if r['price_unit'] == '円/分']
P(f'\n## 話し相手 分単価（円/分、一覧の最低表示価格、n={len(pm)}）')
P(f'- 最小・25%・中央・75%・最大: {q(pm)} / 平均 {st.mean(pm):.1f}')
c = collections.Counter(pm); P('- 値ごとの件数: ' + ', '.join(f'{k}円:{v}' for k, v in sorted(c.items())))
P('\n### 話し相手 提供形態'); 
for k, v in collections.Counter(r['form'] for r in comp_rows).most_common(): P(f'- {k}: {v}')
P('\n### 話し相手 受付形態テキスト'); 
for k, v in collections.Counter(r['accept_text'] for r in comp_rows).most_common(): P(f'- {k or "取得できず"}: {v}')
P('\n### 話し相手 納期・返答')
for k, v in collections.Counter(r['delivery_days'] or '表示なし' for r in comp_rows).most_common(8): P(f'- お届け日数 {k}: {v}')
P('\n### 話し相手 経歴・資格テキストの有無（サービス説明文の機械分類。プロフィールページ未取得）')
P('- 構造化属性「手法」の表示: ' + ', '.join(f'{k or "表示なし"}:{v}' for k, v in collections.Counter(r['method_attr'] for r in comp_rows).most_common()))
P(f"- 資格に関する語あり: {sum(r['profile_qualification_text']=='あり' for r in comp_rows)} / {len(comp_rows)}; 経歴に関する語あり: {sum(r['profile_career_text']=='あり' for r in comp_rows)} / {len(comp_rows)}")
rc = [int(r['rating_count_listing']) for r in comp_rows]; ts = [r['seller_total_sales'] for r in comp_rows if r['seller_total_sales'] != '']
P(f'\n### 話し相手 評価件数(一覧) {q(rc)} / 出品者総販売実績(n={len(ts)}) {q(ts)}')
# 占い価格帯
P('\n## 占い3カテゴリ 1回払い（円建て）の価格帯別（一覧の最低表示価格、各カテゴリ上位60件、n=円建てのみ）')
bands = [('〜1,000円', 0, 1000), ('1,001〜3,000円', 1001, 3000), ('3,001〜5,000円', 3001, 5000), ('5,001〜10,000円', 5001, 10000), ('10,001円〜', 10001, 10**9)]
def band(p):
    for n, lo, hi in bands:
        if lo <= p <= hi: return n
fr = [r for cid in F for r in by[cid] if r['price_unit'] == '円']
P(f'- 円建て {len(fr)} 件 / 占い3カテゴリ全 {sum(len(by[c]) for c in F)} 件（残りは分単価）')
P('| 価格帯 | サービス数 | 評価件数合計 | 評価件数 中央値 | 評価0〜99件 | 100〜999件 | 1,000件以上 |'); P('|---|---|---|---|---|---|---|')
for n, lo, hi in bands:
    v = [int(r['service_rating_count']) for r in fr if band(int(r['min_price_yen'])) == n]
    P(f'| {n} | {len(v)} | {sum(v)} | {st.median(v) if v else "-"} | {sum(x<100 for x in v)} | {sum(100<=x<1000 for x in v)} | {sum(x>=1000 for x in v)} |')
P('\n### カテゴリ別（円建て、評価100未満の件数）')
P('| カテゴリ | 円建て | うち評価100未満 | 分単価 | 分単価で評価100未満 |'); P('|---|---|---|---|---|')
for cid, nm in F.items():
    a = [r for r in by[cid] if r['price_unit'] == '円']; b = [r for r in by[cid] if r['price_unit'] == '円/分']
    P(f"| {nm} | {len(a)} | {sum(int(r['service_rating_count'])<100 for r in a)} | {len(b)} | {sum(int(r['service_rating_count'])<100 for r in b)} |")
P('\n### 評価100未満（円建て）の価格帯別内訳')
P('| 価格帯 | 件数 | 評価件数の最小〜最大 |'); P('|---|---|---|')
for n, lo, hi in bands:
    v = [int(r['service_rating_count']) for r in fr if band(int(r['min_price_yen'])) == n and int(r['service_rating_count']) < 100]
    P(f'| {n} | {len(v)} | {(min(v), max(v)) if v else "-"} |')
# 新規参入
P('\n## 新規参入（一覧の評価件数<100）')
P('| 区分 | 上位60件中の評価100未満 | うち詳細取得 | 全レビュー取得 | 最初の評価日あり |'); P('|---|---|---|---|---|')
grp = {'話し相手(51)': ['51'], '占い3カテゴリ': list(F), '悩み相談 他6カテゴリ(参考)': ['693', '53', '50', '676', '692', '647']}
for nm, cids in grp.items():
    lt = [r for cid in cids for r in by[cid] if int(r['service_rating_count']) < 100]
    got = [x for x in ne if x['service_id'] in {r['service_id'] for r in lt}]
    P(f"| {nm} | {len(lt)} | {len(got)} | {sum(x['all_reviews_captured']=='yes' for x in got)} | {sum(bool(x['first_review_date']) for x in got)} |")
P('\n### 評価件数(一覧)0件の出品 / 評価日付の観測')
for nm, cids in grp.items():
    lt = [r for cid in cids for r in by[cid] if int(r['service_rating_count']) < 100]
    z = sum(int(r['service_rating_count']) == 0 for r in lt)
    P(f'- {nm}: 評価0件 {z} / 評価1〜9件 {sum(1<=int(r["service_rating_count"])<10 for r in lt)} / 10〜49件 {sum(10<=int(r["service_rating_count"])<50 for r in lt)} / 50〜99件 {sum(50<=int(r["service_rating_count"])<100 for r in lt)}')
ok_ = [x for x in ne if x['all_reviews_captured'] == 'yes']
P(f'\n- 全レビューの日付が取得できた新規参入(評価100未満): {len(ok_)} 件')
v = [x['days_first_review_to_snapshot'] for x in ok_]
if v: P(f'  - 最初の評価日〜取得日(2026-11-09)の日数 分位(最小/25/50/75/最大): {q(v)}')
v = [x['days_first_to_10th'] for x in ok_ if x['days_first_to_10th'] != '']
if v: P(f'  - 最初の評価〜10件目の評価の日数(n={len(v)}): {q(v)}')
v = [x['days_first_to_last'] for x in ok_]
if v: P(f'  - 最初の評価〜最後の評価の日数: {q(v)}')
open(os.path.join(RAW, 't25-tables.md'), 'w', encoding='utf8').write('\n'.join(out))
print('\n'.join(out))
