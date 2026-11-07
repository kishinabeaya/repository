"""ココナラ レビューの定量分析。python3 -I coconala_analysis.py > coconala_out.md"""
import sys,os,csv,re,collections,statistics
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
rev=jl('coconala-reviews.jsonl')
seen=set();R=[]
for r in rev:
    if r['text'] in seen: continue
    seen.add(r['text']);R.append(r)
N=len(R)
THEME={
'恋愛・復縁・片思い':['恋愛','復縁','片思い','片想い','彼氏','彼女','彼と','彼の','好きな人','元彼','元カレ','相手の気持ち','お相手','不倫','パートナー','恋','結婚','婚活','ツインレイ','ソウルメイト','連絡'],
'仕事・転職・キャリア':['仕事','転職','就職','職場','職業','適職','天職','キャリア','会社','上司','起業','独立','副業','退職','お仕事'],
'お金・金運':['お金','金運','収入','貯金','財運','経済','金銭','借金','資産','年収'],
'将来・人生':['将来','人生','先行き','進むべき','道標','生き方','岐路','進路'],
'運勢・年運(今年/来年)':['来年','運勢','今年','年運','2026','2027','1年'],
'人間関係':['人間関係','友人','友達','同僚','職場の人','人付き合い','対人','ママ友','親友'],
'家族・子育て':['家族','母親','お母','父親','お父','両親','親子','子供','子ども','娘','息子','旦那','夫婦','主人','義母','義父','義理','離婚','妊活','妊娠','育児','不登校'],
'健康・メンタル':['健康','体調','病気','鬱','うつ病','メンタル','不安で眠','ストレス','心の病','病院','治療'],
'自分の性格・適性・才能':['性格','適性','才能','自分らしさ','自分自身','使命','魂','本質','自己','持って生まれ','生まれ持った','資質','強み','自分のこと','自分を知'],
}
SAT={
'当たっていた・的中':['当たって','当たり','的中','言い当て','その通り','図星','ドンピシャ','一致','びっくり','驚'],
'気持ちが楽になった・安心':['楽になり','楽になっ','気持ちが軽','心が軽','軽くなり','軽くなっ','安心','救われ','癒','落ち着','スッキリ','すっきり','前向き','心が温か','涙','元気が出','希望'],
'背中を押された・勇気':['背中を押','後押し','勇気','一歩踏み出','踏み出'],
'具体的な行動・アドバイスがわかった':['具体的','アドバイス','何をすれば','やるべき','行動','道筋','方向性','指針','ヒント','気づ','気付','参考にな','考え方','視点'],
'丁寧・早い・寄り添い':['丁寧','早い','早く','迅速','スピーディ','親身','寄り添','優しい','優しく','真摯','わかりやすい','分かりやすい','詳しく','細かく','細やか','対応'],
'また頼みたい・リピート':['リピ','またお願い','また相談','また鑑定','また依頼','またよろしく','また宜しく','また利用','次回','機会があれば','おすすめ','オススメ','何度'],
}
def pct(a,b=None): return f'{a/(b or N)*100:.1f}%'
tc=collections.Counter();sc=collections.Counter();ex={}
ntheme0=0;nsat0=0;theme_of=[];multi=0
for r in R:
    t=classify(r['text'],{k:v for k,v in THEME.items()})
    s=classify(r['text'],SAT)
    r['T']=t;r['S']=s
    if not t:ntheme0+=1
    if not s:nsat0+=1
    for k in t:tc[k]+=1
    for k in s:sc[k]+=1
print(f'# ココナラ レビュー集計（ユニーク本文 N={N}、生{len(rev)}件）\n')
print('## 1. 相談テーマ（複数該当あり。本文に語が出た件数）\n')
print('| テーマ | 件数 | 割合(N比) |\n|---|---|---|')
for k,v in tc.most_common(): print(f'| {k} | {v} | {pct(v)} |')
print(f'| 分類できず | {ntheme0} | {pct(ntheme0)} |')
print('\n**注意**: 辞書は本文に語が出たかの判定で、相談内容そのものではなく感想文の中の言及を拾う。「今後」「未来」は感想の定型句のため除外した。')
# strict (恋愛 etc. specific words) share among classified
print('\n辞書:')
for k,v in THEME.items(): print(f'- {k}: {", ".join(v)}')
print('\n## 2. 満足の理由（複数該当あり）\n')
print('| 満足の理由 | 件数 | 割合(N比) |\n|---|---|---|')
for k,v in sc.most_common(): print(f'| {k} | {v} | {pct(v)} |')
print(f'| 分類できず | {nsat0} | {pct(nsat0)} |')
print('\n辞書:')
for k,v in SAT.items(): print(f'- {k}: {", ".join(v)}')
# frequent words: regex tokens of kanji/katakana runs, stoplist
STOP=set('鑑定 ありがとうございました ありがとうございます ありがとう 今回 とても 本当 思います 感じ ました こと ので よう さん 先生 様'.split())
tok=collections.Counter()
for r in R:
    ws=set(re.findall(r'[一-龥]{2,6}|[ァ-ヴー]{3,8}',r['text']))
    for w in ws:
        if w not in STOP: tok[w]+=1
EXC=set('鑑定 今回 本当 非常 大変 感謝 以上 自分 本当 回答 結果 内容 時間 対応 場合 気持 的確 的中 当日'.split())
print('\n## 3. 頻出語上位40（語を含むレビュー件数。漢字2〜6字/カタカナ3〜8字の連続を抽出、定型語を一部除外）\n')
print('| 語 | 件数 |\n|---|---|')
n=0
for w,c in tok.most_common(300):
    if w in EXC or w.endswith('ました') or w.endswith('ます'): continue
    print(f'| {w} | {c} |');n+=1
    if n>=40:break
print('\n## 4. 代表的な引用（各分類3件、最初に該当した中で70〜160字の本文を等間隔に抽出、冒頭110字、固有名は機械マスク）\n')
used=set()
def quotes(key,idx):
    c=[r for r in R if key in r[idx] and 70<=len(r['text'])<=160]
    if not c: return []
    step=max(1,len(c)//3)
    c=[r for r in c if r['text'] not in used]
    step=max(1,len(c)//3)
    o=[c[i*step] for i in range(3) if i*step<len(c)]
    used.update(r['text'] for r in o)
    return o
print('### テーマ別')
for k in THEME:
    print(f'**{k}**')
    for r in quotes(k,'T'): print(f'- 「{mask(r["text"])[:110]}」')
print('\n### 満足理由別')
for k in SAT:
    print(f'**{k}**')
    for r in quotes(k,'S'): print(f'- 「{mask(r["text"])[:110]}」')
# services
svc=list(csv.DictReader(open(os.path.join(BASE,'coconala-services.csv'),encoding='utf-8')))
byid=collections.defaultdict(list)
for r in R: byid[r['service_id']].append(r)
print('\n## 5. サービス別（reviews 取得できたサービス）\n')
print('theme列はタイトル機械分類（README準拠）。レビュー件数=サービス評価件数(service_reviews)。\n')
agg=collections.defaultdict(lambda:[0,0,0,[]])
for s in svc:
    th=s['theme'] or 'その他・不明'
    for t in th.replace('その他/不明','その他・不明').split('/'):
        a=agg[t];a[0]+=1;a[1]+=int(s['service_reviews'] or 0);a[3].append(int(s['price']))
print('| タイトルのテーマ | 出品数 | 評価件数合計 | 1出品あたり評価件数(中央値) | 価格中央値(円) |\n|---|---|---|---|---|')
revs=collections.defaultdict(list)
for s in svc:
    for t in (s['theme'] or 'その他/不明').replace('その他/不明','その他・不明').split('/'): revs[t].append(int(s['service_reviews'] or 0))
for t,a in sorted(agg.items(),key=lambda x:-x[1][1]):
    print(f'| {t} | {a[0]} | {a[1]:,} | {statistics.median(revs[t]):.0f} | {statistics.median(a[3]):,.0f} |')
print('\n### 評価件数 上位15サービス（取得したレビュー本文の主テーマ=本文辞書で最多のテーマ）\n')
print('| id | 価格 | 評価件数 | タイトルのテーマ | 本文の最多テーマ(取得n) | タイトル(先頭40字) |\n|---|---|---|---|---|---|')
for s in sorted(svc,key=lambda x:-int(x['service_reviews'] or 0))[:15]:
    rs=byid.get(s['id'],[]);c=collections.Counter(t for r in rs for t in r['T'])
    top=c.most_common(1)[0][0] if c else '-'
    print(f'| {s["id"]} | {int(s["price"]):,} | {int(s["service_reviews"]):,} | {s["theme"]} | {top}({len(rs)}) | {mask(s["title"])[:40]} |')
# price bands vs reviews
print('\n### 価格帯と評価件数\n\n注: 「円/分」の分単価が混在（列で区別なし）。\n')
bands=[(0,500),(501,1000),(1001,3000),(3001,5000),(5001,10000),(10001,10**9)]
print('| 価格帯 | 出品数 | 評価件数合計 | 中央値 |\n|---|---|---|---|')
for lo,hi in bands:
    x=[int(s['service_reviews'] or 0) for s in svc if lo<=int(s['price'])<=hi]
    print(f'| {lo:,}〜{hi if hi<10**9 else ""} | {len(x)} | {sum(x):,} | {statistics.median(x) if x else 0:.0f} |')
# review-text theme by service-weighted? 主テーマ: 取得レビュー全体のテーマを価格帯別に
print('\n### 取得レビュー本文のテーマ割合を価格帯別に（レビュー単位）\n')
price={s['id']:int(s['price']) for s in svc}
print('| 価格帯 | n | '+' | '.join(THEME)+' |\n|---|---|'+'---|'*len(THEME))
for lo,hi in bands:
    rs=[r for r in R if r['service_id'] in price and lo<=price[r['service_id']]<=hi]
    if not rs: continue
    print(f'| {lo:,}〜{hi if hi<10**9 else ""} | {len(rs)} | '+' | '.join(pct(sum(1 for r in rs if k in r['T']),len(rs)) for k in THEME)+' |')
