"""T-0033 集計(標準ライブラリのみ)。使い方: python3 -I 08_aggregate_t0033.py <raw_dir> > aggregate-t0033.md"""
import csv,sys,statistics as st,collections,re
raw=sys.argv[1]
R=list(csv.DictReader(open(raw+'/rakkoma-sites.csv',encoding='utf-8')))
P=list(csv.DictReader(open(raw+'/puzzle-products.csv',encoding='utf-8')))
def f(x):
    try: return float(x)
    except: return None
def q(v,p):
    v=sorted(v); k=(len(v)-1)*p; a=int(k); b=min(a+1,len(v)-1); return v[a]+(v[b]-v[a])*(k-a)
def dist(v):
    if not v: return '-'
    return f"n={len(v)} / 中央値 {st.median(v):,.0f} / 上位10%水準(P90) {q(v,.9):,.0f} / 最大 {max(v):,.0f} / 月3万円以上 {sum(1 for x in v if x>=30000)}件({100*sum(1 for x in v if x>=30000)/len(v):.1f}%)"
def pct(n,d): return f"{n}件 ({100*n/d:.1f}%)" if d else '-'
print("# 集計（T-0033）。自動生成。売りに出された案件の自己申告値。全体の代表ではない\n")
print(f"## A. ラッコM&A 受付中の案件一覧（2026-11-22取得、project_type=1の一覧、全{len(R)}件）\n")
c=collections.Counter(r['kind'] for r in R); print("### 種類別の件数（一覧のアイコンによる）\n|種類|件数|\n|---|---|"); [print(f"|{k}|{v}|") for k,v in c.most_common()]
print("\n### 月間利益（直近月、一覧に表示された自己申告値）の分布。分母は「月間利益の記載がある案件」\n|区分|分布|\n|---|---|")
groups=[('全体',R)]+[(k,[r for r in R if r['kind']==k]) for k in c]
for name,g in groups:
    v=[f(r['profit_latest']) for r in g if f(r['profit_latest']) is not None]
    print(f"|{name}（全{len(g)}件中、記載あり{len(v)}件）|{dist(v)}|")
print("\n### 月間利益（平均＝過去の月の平均。一覧に表示）\n|区分|分布|\n|---|---|")
for name,g in groups:
    v=[f(r['profit_avg']) for r in g if f(r['profit_avg']) is not None]
    print(f"|{name}（平均値の記載あり{len(v)}件）|{dist(v)}|")
print("\n### 月間売上（直近月）\n|区分|分布|\n|---|---|")
for name,g in groups:
    v=[f(r['rev_latest']) for r in g if f(r['rev_latest']) is not None]
    print(f"|{name}（記載あり{len(v)}件）|{dist(v)}|")
allp=[r for r in R if f(r['profit_latest']) is not None]
print(f"\n- 直近月の利益が0円以下: {pct(sum(1 for r in allp if f(r['profit_latest'])<=0),len(allp))}（記載ありの案件中）。月間利益の記載なし: {len(R)-len(allp)}件")
print("\n### 売却希望価格\n|区分|分布|\n|---|---|")
for name,g in groups:
    v=[f(r['price_jpy']) for r in g if f(r['price_jpy'])]
    if v: print(f"|{name}（n={len(v)}）|中央値 {st.median(v):,.0f}円 / P90 {q(v,.9):,.0f}円 / 最大 {max(v):,.0f}円 / 30万円未満 {pct(sum(1 for x in v if x<300000),len(v))}|")
print("\n### 売却希望価格が月間利益の何か月分か（倍率）。利益が正の案件のみ\n|区分|直近月利益で割る|平均利益で割る|\n|---|---|---|")
for name,g in groups:
    a=[f(r['price_over_profit_latest']) for r in g if f(r['price_over_profit_latest'])]
    b=[f(r['price_over_profit_avg']) for r in g if f(r['price_over_profit_avg'])]
    s=lambda v: f"n={len(v)} / 中央値 {st.median(v):.1f}か月 / 25%-75% {q(v,.25):.1f}-{q(v,.75):.1f}" if v else '-'
    print(f"|{name}|{s(a)}|{s(b)}|")
print("\n### 月間利益の帯（直近月、記載あり案件）\n|帯|件数|\n|---|---|")
bands=[('0円以下',-10**12,1),('1〜9,999円',1,10000),('1万〜2.9万円',10000,30000),('3万〜9.9万円',30000,100000),('10万円以上',100000,10**12)]
v=[f(r['profit_latest']) for r in allp]
for n,lo,hi in bands: print(f"|{n}|{sum(1 for x in v if lo<=x<hi)}|")
print("\n### 月間利益3万円以上の案件の内訳（直近月基準）\n|種類|件数|価格中央値|\n|---|---|---|")
hi=[r for r in allp if f(r['profit_latest'])>=30000]
for k in c:
    g=[r for r in hi if r['kind']==k]
    if g: print(f"|{k}|{len(g)}|{st.median([f(r['price_jpy']) for r in g]):,.0f}円|")
print("\n### SNS・YouTube等アカウント案件のプラットフォーム（題名のキーワードによる粗い分類。未分類は空）\n|プラットフォーム|件数|\n|---|---|")
pc=collections.Counter(r['account_platform_by_title'] or '(題名から判別できず)' for r in R if r['kind'].startswith('SNS'))
[print(f"|{k}|{v}|") for k,v in pc.most_common()]
D=[r for r in R if r['detail_fetched']=='yes']
print(f"\n## B. 個別ページを取得した案件（サイト・アプリで直近月売上>0、{len(D)}件。全体の一部。取得対象の選び方に偏りあり）\n")
print("### 種類（ページ上の表示）\n|種類|件数|\n|---|---|"); [print(f"|{k}|{v}|") for k,v in collections.Counter(r['type_label'] for r in D).most_common()]
rm=collections.Counter(); 
for r in D:
    for m in set(x.strip() for x in r['revenue_model'].split(' / ')): rm[m]+=1
print("\n### 収益モデル別の件数（複数選択あり。1案件が複数に数えられる）と、その案件の直近月利益の中央値\n|収益モデル|件数|利益中央値(円/月)|月3万円以上|\n|---|---|---|---|")
for k,n in rm.most_common():
    g=[f(r['profit_latest']) for r in D if k in [x.strip() for x in r['revenue_model'].split(' / ')] and f(r['profit_latest']) is not None]
    print(f"|{k}|{n}|{st.median(g):,.0f}|{sum(1 for x in g if x>=30000)}/{len(g)}|" if g else f"|{k}|{n}|-|-|")
cc=collections.Counter()
for r in D:
    for m in set(x.strip() for x in r['category'].split('/') if x.strip()): cc[m]+=1
print("\n### ジャンル（カテゴリ）別の件数（複数選択あり）と利益中央値\n|ジャンル|件数|利益中央値(円/月)|\n|---|---|---|")
for k,n in cc.most_common(15):
    g=[f(r['profit_latest']) for r in D if k in [x.strip() for x in r['category'].split('/')] and f(r['profit_latest']) is not None]
    print(f"|{k}|{n}|{st.median(g):,.0f}|" if g else f"|{k}|{n}|-|")
print("\n### 運営期間（運営開始時期〜2026-11）。個別ページ取得案件のみ\n|項目|値|\n|---|---|")
ms=[]
for r in D:
    m=re.match(r'(\d{4})年(\d\d)月',r['start_month'])
    if m: ms.append((2026-int(m.group(1)))*12+(11-int(m.group(2))))
if ms: print(f"|n|{len(ms)}|\n|中央値|{st.median(ms):.0f}か月|\n|25%-75%|{q(ms,.25):.0f}-{q(ms,.75):.0f}か月|\n|1年未満|{pct(sum(1 for x in ms if x<12),len(ms))}|\n|3年以上|{pct(sum(1 for x in ms if x>=36),len(ms))}|")
print("\n### 運営状況\n|状況|件数|\n|---|---|"); [print(f"|{k}|{v}|") for k,v in collections.Counter(r['status'] for r in D).items()]
print("\n### PV/月（直近）\n"); v=[f(r['pv_latest']) for r in D if f(r['pv_latest']) is not None]; print(f"n={len(v)} / 中央値 {st.median(v):,.0f} / P90 {q(v,.9):,.0f}" if v else '-')
w=[r for r in D if r['workload_text']]
print(f"\n### 運営工数（本文に時間の記載があった案件のみ。自由記述の抜粋）\n- 記載あり {len(w)}/{len(D)}件（構造化された欄は無い。自由記述の正規表現抽出のため漏れあり）")
for r in w: print(f"  - {r['id']}: {r['workload_text']}")
print("\n### 利益が月3万円以上のWebサイト・アプリ案件（個別ページ取得分、最大30件）\n|ID|種類|収益モデル|直近月利益|平均利益|価格|倍率(直近)|運営開始|\n|---|---|---|---|---|---|---|---|")
for r in sorted([r for r in D if f(r['profit_latest']) and f(r['profit_latest'])>=30000],key=lambda r:-f(r['profit_latest']))[:30]:
    print(f"|{r['id']}|{r['type_label']}|{r['revenue_model'][:30]}|{f(r['profit_latest']):,.0f}|{r['profit_avg'] or '-'}|{r['price_jpy']}|{r['price_over_profit_latest'] or '-'}|{r['start_month']}|")
print("\n## C. 謎解き関連\n")
B=[r for r in P if r['source']=='BOOTH']
print(f"### BOOTH（5つの検索語×欲しい物リスト順の上位8件、重複除くと{len({r['item_id'] for r in B})}件。商品JSONを取得）\n")
seenb={}
for r in B: seenb.setdefault(r['item_id'],r)
BU=list(seenb.values())
print("|種類(BOOTHカテゴリ)|件数|無料|謎解き系の語を含む|欲しい物リスト中央値|\n|---|---|---|---|---|")
for k,n in collections.Counter(r['kind_observed'] for r in BU).most_common():
    g=[r for r in BU if r['kind_observed']==k]
    print(f"|{k}|{n}|{sum(1 for r in g if r['is_free']=='yes')}|{sum(1 for r in g if r['puzzle_keyword_in_name_or_tags']=='yes')}|{st.median([f(r['count_value']) for r in g]):,.0f}|")
print("\n価格帯別（BOOTH、上位8件×5検索）\n\n|価格帯|件数|\n|---|---|")
def band(p):
    return '無料' if p==0 else '1〜499円' if p<500 else '500〜999円' if p<1000 else '1,000〜1,999円' if p<2000 else '2,000円以上'
bc=collections.Counter(band(f(r['price'])) for r in BU)
for k in ['無料','1〜499円','500〜999円','1,000〜1,999円','2,000円以上']: print(f"|{k}|{bc.get(k,0)}|")
core=[r for r in BU if r['puzzle_keyword_in_name_or_tags']=='yes' and 'TRPG' not in r['kind_observed']]
print("\n謎解き系の語（謎解き・ナゾトキ・脱出など）を題名かタグに含み、カテゴリがTRPG以外のもの（BOOTH）\n\n|ID|商品|種類|価格|欲しい物リスト|\n|---|---|---|---|---|")
for r in sorted(core,key=lambda r:-f(r['count_value'])): print(f"|{r['item_id']}|{r['name'][:36]}|{r['kind_observed']}|{r['price']}円(最安)|{r['count_value']}|")
cw=[f(r['count_value']) for r in BU]; print(f"\n- 欲しい物リスト（40商品中の重複除く{len(BU)}件）: 中央値 {st.median(cw):,.0f} / 最大 {max(cw):,.0f}。注意: 上位は『謎解き』のタグを付けたクトゥルフ神話TRPGシナリオが多く、謎解きキットそのものではない。")
cwc=[f(r['count_value']) for r in core]
if cwc: print(f"- 上の『謎解き系・TRPG以外』{len(core)}件: 欲しい物リスト 中央値 {st.median(cwc):,.0f} / 最大 {max(cwc):,.0f}。欲しい物リスト数は購入数ではない。")
N=[r for r in P if r['source']=='note']
NU={}
for r in N: NU.setdefault(r['item_id'],r)
N=list(NU.values()); paid=[r for r in N if f(r['price'])>0]
print(f"\n### note（ハッシュタグ#謎解き hot順5ページ＋#謎解きキット1ページ、重複除き{len(N)}件。検索APIは403のため不使用）\n")
print(f"- 無料 {len(N)-len(paid)}件 / 価格が付いたもの {len(paid)}件（{100*len(paid)/len(N):.1f}%）。スキ数 全体の中央値 {st.median([f(r['count_value']) for r in N]):.0f} / 最大 {max(f(r['count_value']) for r in N):.0f}")
if paid:
    pv=[f(r['price']) for r in paid]; print(f"- 有料の価格: 中央値 {st.median(pv):,.0f}円 / 最大 {max(pv):,.0f}円。スキ数の中央値 {st.median([f(r['count_value']) for r in paid]):.0f}")
    print("\n|価格|スキ|題名|謎解き系語|\n|---|---|---|---|")
    for r in sorted(paid,key=lambda r:-f(r['count_value']))[:15]: print(f"|{r['price']}|{r['count_value']}|{r['name'][:40]}|{r['puzzle_keyword_in_name_or_tags']}|")
print("\n note: スキ数は購入数ではない。有料記事の販売数は非公開。")
A=[r for r in P if r['source']=='Amazon.co.jp']; AU={}
for r in A: AU.setdefault(r['item_id'] or r['name'],r)
A=list(AU.values())
ac=[f(r['count_value']) for r in A if f(r['count_value']) is not None]
print(f"\n### Amazon.co.jp（検索2ページ＋1ページは確認ページ、重複除き{len(A)}件。価格はUSD表示（取得環境のため。円ではない）。順位は関連度順の表示順で、売上順ではない）\n")
print(f"- 評価件数: 取得できた{len(ac)}件、中央値 {st.median(ac):.0f} / 最大 {max(ac):.0f}。100件以上: {sum(1 for x in ac if x>=100)}件")
print("\n|ベストセラー表示のあるもの|評価件数|評価|価格(USD)|\n|---|---|---|---|")
for r in A:
    if r['kind_observed']: print(f"|{r['name'][:40]} {r['kind_observed']}|{r['count_value']}|{r['rating']}|{r['price']}|")
print("\n評価件数の多い順 上位10\n\n|商品|評価件数|評価|USD|\n|---|---|---|---|")
for r in sorted([r for r in A if f(r['count_value']) is not None],key=lambda r:-f(r['count_value']))[:10]: print(f"|{r['name'][:44]}|{r['count_value']}|{r['rating']}|{r['price']}|")
print("\n### itch.io: 今回の再取得は 429(Too Many Requests)で取得できず。既存CSV(itch-top.csv、popularの一覧の一部)から Puzzle ジャンル等 5件のみ再掲（価格のみ、評価件数なし）")
