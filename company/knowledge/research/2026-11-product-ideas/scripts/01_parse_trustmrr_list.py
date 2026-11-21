"""TrustMRR カテゴリAPIの取得JSON(cat/<slug>_<page>.json)を、1つのCSV(中間)にまとめる。
使い方: python3 -I 01_parse_trustmrr_list.py <jsonディレクトリ> <出力csv>
各行に、カテゴリ、ページ番号、カテゴリ総数、層の重み(weight)を付ける。
重みの考え方: 1ページ目(上位30件)は自分自身(重み1)。それ以外の取得ページは、残り(総数-30)を、取得行数で等分に代表させる。
"""
import csv, glob, json, os, re, sys
d, out = sys.argv[1], sys.argv[2]
rows = {}
tot = {}
for f in sorted(glob.glob(os.path.join(d, '*.json'))):
    m = re.match(r'(.+)_(\d+)\.json$', os.path.basename(f))
    cat, page = m.group(1), int(m.group(2))
    j = json.load(open(f))
    if 'startups' not in j:
        continue  # 'Too many requests' 等
    tot[cat] = j['total']
    rows.setdefault(cat, []).extend((page, s) for s in j['startups'])
w = csv.writer(open(out, 'w', newline='', encoding='utf-8'))
w.writerow(['name','slug','category','list_page','category_total','weight','description','total_revenue_usd','mrr_usd','last30d_revenue_usd','merchant_of_record','on_sale','asking_price_usd','url'])
for cat, lst in rows.items():
    other = [x for x in lst if x[0] != 1]
    wt_other = ((tot[cat] - 30) / len(other)) if other else 0
    for page, s in lst:
        wt = 1.0 if page == 1 else wt_other
        w.writerow([s.get('name'), s.get('slug'), cat, page, tot[cat], round(wt, 3),
                    (s.get('description') or '').replace('\n', ' ')[:300],
                    round(s.get('currentTotalRevenue') or 0, 2), round(s.get('currentMrr') or 0, 2),
                    round(s.get('currentLast30DaysRevenue') or 0, 2),
                    s.get('isMerchantOfRecord'), s.get('onSale'), s.get('askingPrice'),
                    'https://trustmrr.com/startup/' + str(s.get('slug'))])
print(sum(len(v) for v in rows.values()), 'rows', len(rows), 'categories')
