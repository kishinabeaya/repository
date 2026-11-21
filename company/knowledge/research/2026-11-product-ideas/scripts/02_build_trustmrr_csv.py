"""中間CSV(01の出力)と、詳細.mdの一部サンプルを結合して raw/trustmrr.csv を作る。
使い方: python3 -I 02_build_trustmrr_csv.py <list.csv> <mdディレクトリ> <出力csv>
【設計】列 design_cc_class は、収益の集計には使わない。分類基準(キーワード、名前+説明文に対して):
  B = 物理・人手・サービス型の語を含む(agency, consulting, done-for-you, hardware, physical, shipping, marketplace, supplement, coaching, concierge, 受託 等)
  A = それ以外(説明文があるもの。ソフト/デジタル配信で完結しうる、と設計上みなす)
  U = 説明文なし(判定不能)
これは説明文のキーワードによる粗い設計上の分類であり、実際にClaude Codeで作れる・運営できることを示さない。
"""
import csv, os, re, sys
lst, mdd, out = sys.argv[1:4]
B_WORDS = ['agency','consult','done-for-you','done for you','hardware','physical','shipping','marketplace','supplement','coaching','concierge','freelanc','devices','device ','manufactur','fulfillment','wholesale','restaurant','clinic','staffing','recruiting firm','custom development','dev shop','we build','our team of']
def cls(name, desc):
    if not desc: return 'U'
    t = (name + ' ' + desc).lower()
    return 'B' if any(w in t for w in B_WORDS) else 'A'
def md_fields(slug):
    p = os.path.join(mdd, slug + '.md')
    if not os.path.exists(p): return {}
    t = open(p, encoding='utf-8').read()
    def g(label):
        m = re.search(r'^- ' + label + r': (.+)$', t, re.M)
        return re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', m.group(1)).strip() if m else ''
    months = re.findall(r'^\| (\d{4}-\d{2}) \| \$([\d,]+) \|$', t.split('### Monthly revenue timeline')[1].split('\n\n')[0] if '### Monthly revenue timeline' in t else '', re.M)
    first = next((m for m, v in months if int(v.replace(',', '')) > 0), '')
    return {'founded': g('Founded date'), 'country': g('Country'), 'pricing_model': g('Pricing model')[:200],
            'audience': g('Audience type'), 'funding': g('Funding'), 'founder_listed': 'あり' if g('Founder') else 'なし',
            'est_users': g('Estimated user count'), 'months_in_timeline': str(len(months)), 'first_revenue_month_in_timeline': first,
            'insight': g('Value proposition')[:200]}
rows = list(csv.DictReader(open(lst, encoding='utf-8')))
cols = ['name','category','list_page','category_total','weight','currency','total_revenue_usd','mrr_usd','last30d_revenue_usd','description','url',
        'pricing_model','audience','funding','founded','country','founder_listed','est_users','months_in_timeline','first_revenue_month_in_timeline','insight','on_sale','asking_price_usd','design_cc_class','slug']
w = csv.DictWriter(open(out, 'w', newline='', encoding='utf-8'), fieldnames=cols)
w.writeheader()
for r in rows:
    o = {k: r.get(k, '') for k in cols}
    o['currency'] = 'USD'
    o.update(md_fields(r['slug']))
    o['design_cc_class'] = cls(r['name'], r['description'])
    w.writerow(o)
print(len(rows))
