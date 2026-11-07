import csv,statistics as st,collections,sys
R="/home/user/repository/company/knowledge/research/2026-11-proven-sellers/raw/"
def med(x): return int(st.median(x)) if x else ''
print("## Kindle/本 ベストセラー（カテゴリ別・各ページ上位30件）")
print("| カテゴリ | 件数 | 価格中央値(円) | 評価数 中央値 | 評価数 最大 | 評価数500以上 | 評価数 取得できず |")
print("|---|---|---|---|---|---|---|")
k=list(csv.DictReader(open(R+"kindle-bestsellers.csv",encoding='utf-8')))
g=collections.OrderedDict()
for x in k: g.setdefault(x['category'],[]).append(x)
for c,v in g.items():
    p=[int(x['price_jpy']) for x in v if x['price_jpy']]; rc=[int(x['rating_count']) for x in v if x['rating_count']]
    print(f"| {c} | {len(v)} | {med(p)} | {med(rc)} | {max(rc) if rc else ''} | {sum(1 for r in rc if r>=500)} | {len(v)-len(rc)} |")
print("\n## BOOTH（欲しい物リスト順、クエリ別・上位6件）")
print("| クエリ(種別) | 件数 | 価格中央値(円) | wish数 中央値 | wish数 最大 |")
print("|---|---|---|---|---|")
b=list(csv.DictReader(open(R+"booth-top.csv",encoding='utf-8')))
g=collections.OrderedDict()
for x in b: g.setdefault((x['query'],x['query_type']),[]).append(x)
for (q,t),v in g.items():
    p=[int(x['price_jpy']) for x in v if x['price_jpy']]; w=[int(x['wish_lists_count']) for x in v]
    print(f"| {q}({'カテゴリ' if t=='cat' else '検索語'}) | {len(v)} | {med(p)} | {med(w)} | {max(w)} |")
print("\nBOOTH 取得件の親カテゴリ内訳:",dict(collections.Counter(x['parent_category'] or x['category'] for x in b)))
print("\n## note 有料記事（ハッシュタグAPI、price>0）")
print("| ハッシュタグ | 有料記事数 | 価格中央値(円) | スキ数 中央値 | スキ数 最大 |")
print("|---|---|---|---|---|")
n=list(csv.DictReader(open(R+"note-paid.csv",encoding='utf-8')))
g=collections.OrderedDict()
for x in n: g.setdefault(x['hashtag'],[]).append(x)
for c,v in g.items():
    p=[int(x['price_jpy']) for x in v]; l=[int(x['like_count']) for x in v]
    print(f"| {c} | {len(v)} | {med(p)} | {med(l)} | {max(l)} |")
print("\nnote フォロワー数取得済み:",sum(1 for x in n if x['follower_count']),"件")
