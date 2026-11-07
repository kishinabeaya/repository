#!/usr/bin/env python3 -I
"""ココナラ全カテゴリの実績データ収集（GETのみ・ログインなし・間隔1.5秒・上限200リクエスト）。
使い方: python3 -I collect.py <キャッシュdir> <出力raw dir> [listing|detail|all]
キャッシュdirに取得済みHTMLがあれば再取得しない（リクエスト数に数えない）。
"""
import sys, os, re, json, csv, time, subprocess, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cats import CATS, CONSULT_PARENTS
CACHE, RAW = sys.argv[1], sys.argv[2]
MODE = sys.argv[3] if len(sys.argv) > 3 else 'all'
LIMIT = 200
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
os.makedirs(CACHE, exist_ok=True); os.makedirs(RAW, exist_ok=True)
LOG = os.path.join(CACHE, 'requests.log')
def nreq():
    return sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
def fetch(url, fname):
    p = os.path.join(CACHE, fname)
    if os.path.exists(p) and os.path.getsize(p) > 100000:
        return open(p, encoding='utf8').read()
    if nreq() >= LIMIT: raise SystemExit('request limit')
    time.sleep(1.5)
    r = subprocess.run(['curl', '-s', '-A', UA, '-o', p, '-w', '%{http_code}', url], capture_output=True, text=True)
    open(LOG, 'a').write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {r.stdout} {url}\n")
    return open(p, encoding='utf8').read() if os.path.exists(p) else ''
def num(s): return int(s.replace(',', ''))
def txt(s): return re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', ' ', s))).strip()

def full_title(b, t):
    m = re.search(r'<img[^>]*alt="([^"]+)"[^>]*service_images|service_images[^>]*alt="([^"]+)"', b)
    a = (m.group(1) or m.group(2)) if m else ''
    return re.sub(r' イメージ\d+$', '', txt(a)) if a else (txt(t.group(1)) if t else '')

def parse_listing(h, cid, parent, cname):
    """一覧ページの2種類のレイアウト（ブロック型 c-serviceBlockItem / リスト型 c-serviceListItem）に対応。"""
    rows = []
    if 'class="c-serviceBlockItem c-searchPageItemBlock' in h:
        parts = h.split('class="c-serviceBlockItem c-searchPageItemBlock')[1:]; layout = 'block'
    else:
        parts = h.split('class="c-serviceListItem c-searchPageItemList')[1:]; layout = 'list'
    for i, b in enumerate(parts, 1):
        m = re.search(r'href="/services/(\d+)"', b)
        if not m: continue
        if layout == 'block':
            t = re.search(r'c-serviceBlockItemContent_title[^>]*>(.*?)</div>', b, re.S)
            title = full_title(b, t)
        else:
            o = re.search(r'ColContentHeader_overview[^>]*>(.*?)</div>', b, re.S)
            c = re.search(r'ColContentHeader_catchphrase[^>]*>(.*?)</div>', b, re.S)
            title = (txt(o.group(1)) if o else '') + (' / ' + txt(c.group(1)) if c else '')
        sc = re.search(r'PriceRating_score[^>]*>\s*([\d.]+)', b)
        ct = re.search(r'PriceRating_count[^>]*>(.*?)</span>', b, re.S)
        pi = b.find('Price_price')
        pr = re.search(r'<strong[^>]*>([\d,]+)</strong>\s*(円/分|円)?', b[pi:]) if pi >= 0 else None
        unit = (pr.group(2) or '円') if pr else ''
        cnt = re.search(r'\(([\d,]+)\)', txt(ct.group(1))) if ct else None
        rows.append(dict(category_id=cid, parent_category=parent, category=cname, layout=layout, rank_in_category=i,
            service_id=m.group(1), title=title, min_price_yen=num(pr.group(1)) if pr else '', price_unit=unit,
            quote_required='見積り必須' if '見積り必須' in b else '', rating_score=sc.group(1) if sc else '',
            service_rating_count=num(cnt.group(1)) if cnt else 0, url=f"https://coconala.com/services/{m.group(1)}"))
    return rows

def parse_detail(h):
    d = {}
    m = re.search(r'"@type": "Product".*?</script>', h, re.S)
    j = {}
    i = h.find('"@type": "Product"')
    if i >= 0:
        s = h.rfind('<script', 0, i); e = h.find('</script>', i)
        try: j = json.loads(h[h.find('>', s)+1:e])
        except Exception: j = {}
    d['jsonld'] = j
    t = txt(re.sub(r'<style.*?</style>|<script.*?</script>', '', h, flags=re.S))
    m = re.search(r'総販売実績： ?([\d,]+)件', t); d['seller_total_sales'] = num(m.group(1)) if m else ''
    m = re.search(r'お気に入り\(([\d,]+)\)', t); d['favorites'] = num(m.group(1)) if m else ''
    m = re.search(r'お届け日数 (.{1,40}?) (?:初回返答時間|スタイル|$)', t); d['delivery_days'] = m.group(1) if m else ''
    m = re.search(r'提供形式 (.{1,120}?) (?:デザイン|基本対応範囲|無料修正|お届け日数)', t); d['provision_text'] = m.group(1) if m else ''
    m = re.search(r'有料オプション (.{1,200}?) [\d,]+ 円 購入画面', t); d['options_text'] = m.group(1) if m else ''
    m = re.search(r'現在(\d+)人がお願い中', t); d['in_progress_now'] = m.group(1) if m else ''
    return d

def main():
    listing_csv = os.path.join(RAW, 'listing-rows.json')
    allrows = []
    if MODE in ('listing', 'all'):
        for cid, parent, cname in CATS:
            h = fetch(f'https://coconala.com/categories/{cid}', f'cat-{cid}.html')
            rows = parse_listing(h, cid, parent, cname)
            print(cid, cname, len(rows), 'req', nreq(), flush=True)
            allrows += rows
        json.dump(allrows, open(os.path.join(CACHE, 'listing-rows.json'), 'w'), ensure_ascii=False)
    if MODE in ('detail', 'all'):
        allrows = json.load(open(os.path.join(CACHE, 'listing-rows.json')))
        bycat = {}
        for r in allrows: bycat.setdefault(r['category_id'], []).append(r)
        order = []
        for k in (0, 1, 2):
            for cid, _, _ in CATS:
                rs = sorted(bycat.get(cid, []), key=lambda r: (-r['service_rating_count'], r['rank_in_category']))
                if len(rs) > k: order.append(rs[k])
        det = {}
        for r in order:
            if nreq() >= LIMIT - 1 and not os.path.exists(os.path.join(CACHE, f"svc-{r['service_id']}.html")): break
            h = fetch(r['url'], f"svc-{r['service_id']}.html")
            if not h: continue
            det[r['service_id']] = parse_detail(h)
            print('detail', r['service_id'], det[r['service_id']]['seller_total_sales'], 'req', nreq(), flush=True)
        json.dump(det, open(os.path.join(CACHE, 'detail-rows.json'), 'w'), ensure_ascii=False)
main()
