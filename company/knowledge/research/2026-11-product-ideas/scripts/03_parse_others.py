"""Chromeウェブストア、Gumroad、itch.io の保存HTMLを解析して、CSVにする。
使い方: python3 -I 03_parse_others.py <cwsディレクトリ> <grディレクトリ> <itchディレクトリ> <出力raw>
"""
import csv, glob, html, json, os, re, sys
cws, gr, itch, out = sys.argv[1:5]
# ---- Chrome ----
ENTRY = re.compile(r'\["([a-p]{32})","https://[^"]*","((?:[^"\\]|\\.)*)",([0-9.]+),(\d+),')
rows = []; seen = set()
for f in sorted(glob.glob(os.path.join(cws, '*.html'))):
    cat = os.path.basename(f)[:-5]
    cat = re.sub(r'^(productivity|lifestyle|make_chrome_yours)_', lambda m: m.group(1) + '/', cat)
    h = open(f, encoding='utf-8').read()
    n = 0
    for m in ENTRY.finditer(h):
        eid = m.group(1)
        tail = h[m.end():m.end() + 1500]
        site = re.search(r'"https?://[^"]*",(?:\d|null)', tail)
        u = re.search(r'\["([a-z_]+/[a-z_]+)",null,\d+\],\d+,\d+,(\d+)', tail)
        if eid in seen and False: continue
        n += 1
        name = json.loads('"' + m.group(2) + '"')
        rows.append({'category': cat, 'rank_in_page': n, 'ext_id': eid, 'name': name, 'rating': round(float(m.group(3)), 2),
                     'rating_count': int(m.group(4)), 'users_bucket': u.group(2) if u else '',
                     'free_or_paid': '取得できず', 'developer_type': '取得できず',
                      'url': 'https://chromewebstore.google.com/detail/' + eid})
with open(os.path.join(out, 'chrome-extensions.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('chrome', len(rows), len({r['ext_id'] for r in rows}))
# ---- Gumroad ----
rows = []
for f in sorted(glob.glob(os.path.join(gr, '*.html'))):
    cat = os.path.basename(f)[:-5]
    h = open(f, encoding='utf-8').read()
    d = json.loads(html.unescape(re.search(r'data-page="([^"]*)"', h).group(1)))
    sr = d['props']['search_results']
    for i, p in enumerate(sr['products'], 1):
        rows.append({'taxonomy': cat, 'taxonomy_total_products': sr['total'], 'rank_best_sellers_sort': i, 'name': p['name'],
                     'seller': p['seller']['name'], 'native_type': p.get('native_type'), 'price_usd': (p.get('price_cents') or 0) / 100,
                     'pay_what_you_want': p.get('is_pay_what_you_want'), 'recurrence': p.get('recurrence') or '',
                     'rating_count': (p.get('ratings') or {}).get('count'), 'rating_avg': (p.get('ratings') or {}).get('average'),
                     'sales_count': '取得できず', 'url': p['url'].split('?')[0]})
with open(os.path.join(out, 'gumroad-top.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('gumroad', len(rows))
# ---- itch ----
rows = []
for f in sorted(glob.glob(os.path.join(itch, '*.html'))):
    src = os.path.basename(f)[:-5]
    h = open(f, encoding='utf-8').read()
    if 'game_cell' not in h: continue
    tags = list(re.finditer(r'<div[^>]*class="game_cell[ "][^>]*>', h))
    for i, tg in enumerate(tags, 1):
        c = h[tg.end(): tags[i].start() if i < len(tags) else len(h)]
        gid = re.search(r'data-game_id="(\d+)"', tg.group(0)).group(1)
        t = re.search(r'<a[^>]*data-label="game:\d+:title"[^>]*>', c)
        href = re.search(r'href="([^"]*)"', t.group(0)).group(1) if t else ''
        tt = re.search(r'data-label="game:\d+:title"[^>]*>([^<]*)<', c)
        pv = re.search(r'class="price_value">([^<]*)<', c)
        au = re.search(r'class="game_author"><a[^>]*>([^<]*)<', c)
        ge = re.search(r'class="game_genre">([^<]*)<', c)
        rows.append({'source_page': src, 'rank_in_page': i, 'game_id': gid, 'title': html.unescape(tt.group(1)) if tt else '',
                     'price_listed': pv.group(1) if pv else '(価格表示なし)', 'genre': html.unescape(ge.group(1)) if ge else '',
                     'author': html.unescape(au.group(1)) if au else '', 'rating_count': '取得できず(一覧に表示なし)',
                     'solo_dev': '取得できず', 'url': href})
with open(os.path.join(out, 'itch-top.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('itch', len(rows))
