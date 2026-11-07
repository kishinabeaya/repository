#!/usr/bin/env python3 -I
"""collect.py の出力（キャッシュdirのlisting-rows.json / detail-rows.json）から CSV・JSONL・集計表を作る。
使い方: python3 -I build.py <キャッシュdir> <raw dir>
"""
import sys, os, re, json, csv, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cats import CONSULT_PARENTS
CACHE, RAW = sys.argv[1], sys.argv[2]
rows = json.load(open(f'{CACHE}/listing-rows.json'))
det = json.load(open(f'{CACHE}/detail-rows.json'))

def form(title, cat, extra=''):
    t = title + ' ' + extra
    if re.search(r'添削|校正|リライト|赤入れ|フィードバック|チェック|ブラッシュアップ|レビュー', t): return '添削・校正・チェック'
    if re.search(r'電話|通話|ビデオ通話|ビデオチャット|Zoom|zoom|ZOOM|オンライン面談|オンライン相談|音声通話|ボイスチャット', t): return '通話・ビデオ相談'
    if re.search(r'相談|聞き|アドバイス|カウンセリング|コーチング|鑑定|占|悩み|傾聴|愚痴|話し相手|模擬面接|面接対策|診断|指導|レッスン', t): return 'チャット・テキスト相談/指導'
    return '制作・代行（ファイル等の納品）'

def family(parent, f):
    if f == '添削・校正・チェック': return '添削系'
    if f in ('通話・ビデオ相談', 'チャット・テキスト相談/指導') or parent in CONSULT_PARENTS: return '相談・指導系'
    return '制作代行系'

def band(p, unit='円'):
    if unit == '円/分': return '分単価(円/分、電話・チャット時間制)'
    if p == '' : return '価格不明'
    for hi, n in [(1000,'0-999円'),(3000,'1,000-2,999円'),(5000,'3,000-4,999円'),(10000,'5,000-9,999円'),(30000,'10,000-29,999円'),(100000,'30,000-99,999円')]:
        if p < hi: return n
    return '100,000円以上'
BANDS = ['0-999円','1,000-2,999円','3,000-4,999円','5,000-9,999円','10,000-29,999円','30,000-99,999円','100,000円以上','分単価(円/分、電話・チャット時間制)','価格不明']

out = []; reviews = []
for r in rows:
    d = det.get(r['service_id'])
    j = d['jsonld'] if d else {}
    title = j.get('name') or r['title']
    mp = r['min_price_yen']
    if d and j.get('offers', {}).get('price') is not None and mp == '': mp = j['offers']['price']
    f = form(title, r['category'])
    cp = os.path.join(CACHE, f"svc-{r['service_id']}.html" if d else f"cat-{r['category_id']}.html")
    fa = datetime.datetime.fromtimestamp(os.path.getmtime(cp)).strftime('%Y-%m-%dT%H:%M:%S')
    proxy = r['service_rating_count'] * mp if (mp != '' and r['price_unit'] == '円') else ''
    ag = j.get('aggregateRating', {})
    o = dict(r); o.update(title=title, min_price_yen=mp,
        rating_count_detail=ag.get('reviewCount', ''),
        seller_total_sales=d['seller_total_sales'] if d else '取得せず',
        favorites=d['favorites'] if d else '取得せず', delivery_days=(d['delivery_days'] or '取得できず') if d else '取得せず',
        options_text=(d['options_text'] or 'なし/取得できず') if d else '取得せず',
        provision_text=(d['provision_text'] or '取得できず') if d else '取得せず',
        delivery_form=f, service_family=family(r['parent_category'], f), price_band=band(mp, r['price_unit']),
        proxy_lower_bound_yen=proxy, detail_page_fetched='yes' if d else 'no', fetched_at=fa)
    o.pop('url'); o['url'] = r['url']
    out.append(o)
    if d:
        seller = j.get('offers', {}).get('seller', {}).get('name', '')
        for rv in j.get('review', []):
            body = rv.get('reviewBody', '') or ''
            for nm in (seller, rv.get('author', {}).get('name', '')):
                if nm and len(nm) >= 2: body = body.replace(nm, '[名前]')
            reviews.append(dict(service_id=r['service_id'], category_id=r['category_id'], category=r['category'],
                service_title=title, rating=rv.get('reviewRating', {}).get('ratingValue'), date=rv.get('datePublished'), text=body.strip()))
cols = list(out[0].keys())
with open(f'{RAW}/coconala-all-categories.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(out)
with open(f'{RAW}/coconala-all-reviews.jsonl', 'w', encoding='utf-8') as fh:
    for rv in reviews: fh.write(json.dumps(rv, ensure_ascii=False) + '\n')

# ---- 集計 ----
uniq = {}
for o in out: uniq.setdefault(o['service_id'], o)
U = list(uniq.values())
def agg(key):
    g = collections.defaultdict(lambda: [0, 0, 0, 0])
    for o in U:
        a = g[key(o)]; a[0] += 1; a[1] += o['service_rating_count']
        if o['proxy_lower_bound_yen'] != '': a[2] += o['proxy_lower_bound_yen']; a[3] += 1
    return g
def table(title, g, order=None):
    keys = order or sorted(g, key=lambda k: -g[k][2])
    s = f'\n### {title}\n| 区分 | サービス数 | 評価件数合計 | 代理指標合計(円) | 代理指標の算出対象数 | 1サービス平均の評価件数 | 全体に占める代理指標 |\n|---|---|---|---|---|---|---|\n'
    tot = sum(v[2] for v in g.values())
    for k in [k for k in keys if k in g]:
        a = g[k]; s += f'| {k} | {a[0]:,} | {a[1]:,} | {a[2]:,} | {a[3]:,} | {a[1]/a[0]:.1f} | {a[2]/tot*100:.1f}% |\n'
    return s
md = f'\n(重複除去後のサービス数 {len(U)}、全行 {len(out)})\n'
md += table('親カテゴリ別', agg(lambda o: o['parent_category']))
md += table('カテゴリ別（代理指標の降順）', agg(lambda o: f"{o['category']}({o['category_id']})"))
md += table('価格帯別（最低表示価格）', agg(lambda o: o['price_band']), BANDS)
md += table('提供形態別（タイトル等のキーワード機械分類）', agg(lambda o: o['delivery_form']))
md += table('系統別（添削系・相談指導系・制作代行系）', agg(lambda o: o['service_family']))
md += '\n### 評価件数の上位30サービス（全カテゴリ横断、評価件数順）\n| 順 | カテゴリ | タイトル | 最低価格 | 評価件数 | 代理指標(円) | 出品者の総販売実績 |\n|---|---|---|---|---|---|---|\n'
for i, o in enumerate(sorted(U, key=lambda o: -o['service_rating_count'])[:30], 1):
    md += f"| {i} | {o['category']} | {o['title'][:40]} | {o['min_price_yen']} | {o['service_rating_count']:,} | {o['proxy_lower_bound_yen']} | {o['seller_total_sales']} |\n"
md += '\n### 代理指標の上位30サービス（全カテゴリ横断）\n| 順 | カテゴリ | タイトル | 最低価格 | 評価件数 | 代理指標(円) |\n|---|---|---|---|---|---|\n'
for i, o in enumerate(sorted([o for o in U if o['proxy_lower_bound_yen'] != ''], key=lambda o: -o['proxy_lower_bound_yen'])[:30], 1):
    md += f"| {i} | {o['category']} | {o['title'][:40]} | {o['min_price_yen']:,} | {o['service_rating_count']:,} | {o['proxy_lower_bound_yen']:,} |\n"
dets = [o for o in U if o['detail_page_fetched'] == 'yes']
md += f'\n### 件数\n- 全行 {len(out)} / 重複除去 {len(U)} / 詳細ページ取得 {len(dets)} / レビュー本文 {len(reviews)}件（{len(set(r["service_id"] for r in reviews))}サービス） / 価格不明 {sum(1 for o in U if o["min_price_yen"]=="")}\n'
open(f'{CACHE}/aggregate.md', 'w', encoding='utf-8').write(md)
print(md[:3000])
