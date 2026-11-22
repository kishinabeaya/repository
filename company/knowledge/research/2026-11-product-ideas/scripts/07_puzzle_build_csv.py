"""謎解き関連: BOOTH(商品JSON)・note(ハッシュタグAPI)・Amazon(検索結果HTML)・itch.io(既存CSV再利用) -> puzzle-products.csv
使い方: python3 -I 07_puzzle_build_csv.py <work_dir> <existing_itch_csv> <out_csv>"""
import re,html,json,glob,sys,csv,os
w,itch,out=sys.argv[1:4]
KEY=re.compile(r'謎解き|ナゾトキ|脱出|謎とき|なぞとき|リドル|謎')
rows=[]
def add(**k):
    base=dict(source='',query='',rank_in_result='',item_id='',name='',price='',price_unit='JPY',is_free='',count_metric='',count_value='',rating='',kind_observed='',puzzle_keyword_in_name_or_tags='',url='',note='')
    base.update(k); rows.append(base)
# BOOTH: 検索ごとの上位8件(欲しい物リスト順)。検索順位は各検索HTMLの出現順
qs={1:'謎解き',2:'脱出ゲーム',3:'ナゾトキ',4:'リアル脱出',5:'謎解きキット'}
seen=set()
for i,q in qs.items():
    t=open(f'{w}/pz/booth_{i}.html').read()
    ids=[]
    for m in re.finditer(r'data-product-id="(\d+)"',t):
        if m.group(1) not in ids: ids.append(m.group(1))
    for rk,pid in enumerate(ids[:8],1):
        p=f'{w}/bj/{pid}.json'
        if not os.path.exists(p): continue
        d=json.load(open(p))
        pr=re.sub(r'[^\d]','',d['price'].split('~')[0]) or '0'
        tags=[x['name'] for x in d['tags']]
        var=[v.get('name') for v in d['variations']]
        add(source='BOOTH',query=q,rank_in_result=rk,item_id=pid,name=d['name'],price=int(pr),is_free='yes' if int(pr)==0 else 'no',
            count_metric='wish_lists_count',count_value=d['wish_lists_count'],kind_observed=d['category']['name'],
            puzzle_keyword_in_name_or_tags='yes' if KEY.search(d['name']+' '.join(tags)) else 'no',url='https://booth.pm/ja/items/'+pid,
            note=('価格は最安バリエーション(~付き)' if '~' in d['price'] else '')+('; 重複(複数検索に出現)' if pid in seen else ''))
        seen.add(pid)
# note: ハッシュタグ「謎解き」hot順5ページ + 「謎解きキット」1ページ
n=0
for f,tag in [(f'{w}/note_h{p}.json','謎解き') for p in range(1,6)]+[(f'{w}/note_n6.json','謎解きキット')]:
    if not os.path.exists(f): continue
    try: d=json.load(open(f))['data']['notes']
    except Exception: continue
    for x in d:
        n+=1
        add(source='note',query='#'+tag,rank_in_result=n,item_id=x['key'],name=x['name'],price=x['price'],is_free='yes' if x['price']==0 else 'no',
            count_metric='like_count(スキ)',count_value=x['like_count'],kind_observed=x['type'],
            puzzle_keyword_in_name_or_tags='yes' if KEY.search(x['name']) else 'no',url=f"https://note.com/{x['user']['urlname']}/n/{x['key']}",
            note='ハッシュタグhot順。price>0は有料記事(または有料部分あり)')
# Amazon
for f,q in [('amz_a.html','謎解き キット'),('amz_0bae.html','謎解き 本 脱出')]:
    t=open(f'{w}/{f}').read()
    pos=0
    chunks=t.split('data-component-type="s-search-result"')
    for ci in range(1,len(chunks)):
        blk=chunks[ci]
        head=chunks[ci-1]
        ha=re.findall(r'data-asin="(\w{10})"',head[-600:])
        asin=re.search(r'(\w{10})',ha[-1]) if ha else None
        s=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','|',blk[:30000])); s=re.sub(r'(\|\s*)+','|',s)
        parts=s.split('|')
        title=next((p for p in parts if len(p)>6 and not p.startswith(' class')),'')
        rc=re.search(r'aria-label="([\d,.万]+) レーティング',blk[:30000]) or re.search(r'5つ星のうち[\d.]+\|\(([\d,.万]+)\)',s)
        rt=re.search(r'5つ星のうち([\d.]+)',s)
        pr=re.search(r'USD\s*([\d,.]+)',s)
        bs=re.search(r'ベストセラー(\d+)位\s*\|?-?\s*([^|]*)',s)
        pos+=1
        if not rc and not pr: continue
        add(source='Amazon.co.jp',query=q,rank_in_result=pos,item_id=asin.group(1) if asin else '',name=title.strip()[:120],
            price=pr.group(1).replace(',','') if pr else '',price_unit='USD(取得環境の表示。円ではない)',is_free='no' if pr else '',
            count_metric='評価件数',count_value=rc.group(1).replace(',','') if rc else '',rating=rt.group(1) if rt else '',
            kind_observed=('ベストセラー%s位 %s'%(bs.group(1),bs.group(2).strip()) if bs else ''),
            puzzle_keyword_in_name_or_tags='yes' if KEY.search(title) else 'no',url='https://www.amazon.co.jp/dp/'+asin.group(1) if asin else '',
            note='検索結果の表示順(関連度順。売上順ではない)')
# itch.io: 既存CSV再利用
if os.path.exists(itch):
    for r in csv.DictReader(open(itch,encoding='utf-8')):
        if re.search(r'puzzle|mystery|escape|謎|パズル|detective',r['genre']+' '+r['title'],re.I):
            pr=r['price_listed']
            add(source='itch.io(既存CSV再利用)',query='popular listing(既存)',rank_in_result=r['rank_in_page'],item_id=r['game_id'],name=r['title'],price=pr,price_unit='USD',
                is_free='yes' if pr in ('$0','Free','無料') else '',count_metric='rating_count',count_value='取得できず',kind_observed=r['genre'],
                puzzle_keyword_in_name_or_tags='',url=r['url'],note='既存の一覧(T-0032系)から、ジャンル/題名に puzzle/mystery 等を含む行のみ。今回の再取得は429で失敗')
with open(out,'w',newline='',encoding='utf-8') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
import collections
print(collections.Counter(r['source'] for r in rows))
