"""知恵袋・発言小町の定量分析。python3 -I qa_analysis.py > qa_out.md"""
import sys,os,collections,statistics
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
C=jl('chiebukuro.jsonl');K=jl('komachi.jsonl')
def uniq(rows):
    s=set();o=[]
    for r in rows:
        if r['url'] in s: continue
        s.add(r['url']);o.append(r)
    return o
HITS={'将来の不安':330482,'お金':529294,'仕事':900736,'恋愛・結婚':289675,'健康・メンタル':56670,'人間関係':248764,'自分らしさ':2114,'（参考）占い':60319}
def st(v):
    v=[x for x in v if x is not None]
    return (len(v),statistics.mean(v),statistics.median(v)) if v else (0,0,0)
print('# 知恵袋・発言小町 集計\n')
print('## A. 知恵袋 テーマ別（検索ヒット件数はREADME-qa.md値、サンプルは `theme:` 行 各10件・関連度順）\n')
print('| テーマ | ヒット件数 | サンプルn | 閲覧数 平均 | 閲覧数 中央値 | 回答数 平均 | 回答数 中央値 |\n|---|---|---|---|---|---|---|')
th=collections.defaultdict(list)
for r in C:
    if r['keyword'].startswith('theme:'): th[r['keyword'].split(':')[1].split('|')[0]].append(r)
for t,h in sorted(HITS.items(),key=lambda x:-x[1]):
    rs=th.get(t,[])
    if not rs: print(f'| {t} | {h:,} | 0(未取得) | - | - | - | - |');continue
    n,vm,vd=st([r['views'] for r in rs]);_,am,ad=st([r['answers'] for r in rs])
    print(f'| {t} | {h:,} | {n} | {vm:,.0f} | {vd:,.0f} | {am:.1f} | {ad:.0f} |')
tot=sum(v for k,v in HITS.items() if '参考' not in k)
print(f'\nヒット件数の比（占い以外7テーマ合計={tot:,}）: '+' / '.join(f'{k} {v/tot*100:.1f}%' for k,v in sorted(HITS.items(),key=lambda x:-x[1]) if '参考' not in k))
print('\n注: ヒット件数は検索語依存（1テーマ1語、AND検索）。「仕事 悩み」は語が一般的で大きく出る。サンプルは10件ずつで、閲覧数は質問の古さ・露出に左右される。')
# detailed concerns: 占い系キーワードを除いた相談本文
DIV=('占い','運勢','数秘','タロット','星占い','ライフパス')
def is_div(r): 
    k=r['keyword'].replace('theme:','');return any(d in k for d in DIV)
Cn=uniq([r for r in C if not is_div(r)]);Kn=uniq([r for r in K if not is_div(r)])
print(f'\n## B. 相談本文の悩みの中身（占い系キーワード行を除外。知恵袋 n={len(Cn)}、発言小町 n={len(Kn)}）\n')
print('知恵袋の本文は70件のみ詳細取得、他は検索結果の要約(短文)。分類は title+text への辞書マッチ（複数該当あり、未該当は「分類できず」）。\n')
TH={
'将来の不安':{
 '老後・この先が見えない不安':['老後','年金','この先','先が見えない','先行き','定年','一人で生きて','20年後','10年後'],
 '仕事・収入・お金への不安':['仕事','就職','転職','給料','収入','お金','貯金','年収'],
 '結婚・家族・孤独への不安':['結婚','独身','子供','子ども','孤独','家族'],
 '年齢・焦り':['30代','40代','歳','年齢','もう遅い'],
 '眠れない・精神的につらい':['眠れ','死にたい','つらい','辛い','しんどい','鬱','うつ']},
'お金':{
 '貯金ができない・足りない':['貯金','貯蓄','お金が足り','足りない','生活費','赤字','家計'],
 '収入が少ない・給料':['収入','給料','年収','手取り','月収','給与'],
 '老後資金・年金':['老後','年金','老後資金'],
 '副業・投資・稼ぎたい':['副業','投資','NISA','稼ぎ','稼げ'],
 '借金・ローン':['借金','ローン','奨学金','返済'],
 '子育て・教育費':['教育費','学費','養育費','子供の','子どもの']},
'仕事':{
 '転職すべきか迷う':['転職','辞めたい','退職','辞める'],
 '向いている仕事・やりたいことがわからない':['向いて','適職','やりたい','天職','何をしたい'],
 '職場の人間関係・上司':['上司','同僚','人間関係','パワハラ','職場'],
 '仕事が見つからない・無職':['見つから','無職','就職','就活','未経験'],
 '待遇・キャリアアップ':['給料','昇進','資格','スキル','キャリア','年収']},
'恋愛・結婚':{
 '結婚できない・婚活':['結婚','婚活','独身'],
 '相手の気持ちがわからない・連絡':['気持ち','連絡','LINE','ライン','既読','脈'],
 '片思い・好きな人':['片思い','好きな人','好き','告白'],
 '復縁・別れ':['復縁','別れ','元彼','元カノ','振られ'],
 '不倫・浮気':['不倫','浮気']},
'人間関係':{
 '職場の人間関係':['職場','上司','同僚','会社'],
 '友人・ママ友':['友達','友人','ママ友','仲間'],
 '家族・親':['親','母','父','家族','義'],
 '疲れた・距離の取り方':['疲れ','距離','ストレス','切った','離れ']},
'健康・メンタル':{
 '鬱・精神疾患':['鬱','うつ','障害','統合失調','パニック','適応'],
 '自己肯定感・自信がない':['自己肯定','自信','自分が嫌い','劣等'],
 '不安・眠れない':['不安','眠れ','不眠','動悸'],
 '生きづらさ・孤独':['生きづら','孤独','死にたい','つらい','辛い']},
'自分らしさ・生き方':{
 '自分がわからない・やりたいことがない':['自分がわからない','やりたい','何がしたい','わからない','目標'],
 '生き方・人生の意味に迷う':['生き方','人生','生きる','意味'],
 '自己肯定感が低い':['自己肯定','自信','劣等']},
}
# theme assignment: from 'theme:' keyword when present; others by keyword mapping
KW={'将来が不安':'将来の不安','将来 不安':'将来の不安','将来 不安 眠れない':'将来の不安','生きるのがつらい 将来':'将来の不安',
 '転職 迷う':'仕事','自分に向いている仕事 わからない':'仕事','仕事 辞めたい 先が見えない':'仕事','仕事 辞めたい':'仕事','転職 不安 30代':'仕事','向いている仕事 わからない':'仕事',
 '恋愛 不安 30代':'恋愛・結婚','結婚 できない 不安 30代':'恋愛・結婚','恋愛 不安':'恋愛・結婚',
 '人間関係 疲れた':'人間関係','人生 迷子':'自分らしさ・生き方','自分がわからない 何をしたいか':'自分らしさ・生き方','生き方 迷う':'自分らしさ・生き方','孤独 不安':'健康・メンタル'}
TMAP={'将来の不安':'将来の不安','お金':'お金','仕事':'仕事','恋愛・結婚':'恋愛・結婚','健康・メンタル':'健康・メンタル','人間関係':'人間関係','自分らしさ':'自分らしさ・生き方'}
def theme(r):
    k=r['keyword']
    if k.startswith('theme:'): return TMAP[k.split(':')[1].split('|')[0]]
    return KW.get(k)
allrows=[(r,'知恵袋') for r in Cn]+[(r,'発言小町') for r in Kn]
by=collections.defaultdict(list)
for r,src in allrows:
    t=theme(r)
    if t: by[t].append((r,src))
used=set()
for t,dic in TH.items():
    rs=by.get(t,[])
    print(f'### {t}（n={len(rs)}。知恵袋{sum(1 for _,s in rs if s=="知恵袋")}・小町{sum(1 for _,s in rs if s=="発言小町")}）\n')
    if not rs: print('該当データなし\n');continue
    cnt=collections.Counter();none=0;pick=collections.defaultdict(list)
    for r,src in rs:
        txt=r['title']+' '+r['text']
        h=classify(txt,dic)
        if not h: none+=1
        for x in h: cnt[x]+=1;pick[x].append((r,src))
    print('| 悩みの中身 | 件数 | 割合 |\n|---|---|---|')
    for k,v in cnt.most_common(): print(f'| {k} | {v} | {v/len(rs)*100:.0f}% |')
    print(f'| 分類できず | {none} | {none/len(rs)*100:.0f}% |')
    print('\n辞書: '+' / '.join(f'{k}=[{",".join(v)}]' for k,v in dic.items())+'\n')
    print('代表的な引用:')
    q=0
    for k,_ in cnt.most_common():
        for r,src in pick[k]:
            if r['url'] in used or len(r['title'])<8: continue
            used.add(r['url']);print(f'- [{k}/{src}] 「{mask(r["title"])[:60]}」'+(f' ／本文: {mask(r["text"])[:70]}' if r['text'] and not r['text'].startswith(r['title'][:15]) else ''));q+=1;break
        if q>=3:break
    print()
# overall by-source stats for non-uranai consults
print('## C. 全相談（占い系除く）の閲覧数・回答数\n')
print('| 出典 | n | 閲覧数 平均 | 閲覧数 中央値 | 回答(レス)数 平均 | 中央値 |\n|---|---|---|---|---|---|')
for name,rows in [('知恵袋',Cn),('発言小町',Kn)]:
    n,vm,vd=st([r['views'] for r in rows]);_,am,ad=st([r['answers'] for r in rows])
    print(f'| {name} | {len(rows)} | '+(f'{vm:,.0f} | {vd:,.0f}' if n else '取得なし(閲覧数非表示) | -')+f' | {am:.1f} | {ad:.0f} |')
print('\n## D. 参考: 占い系キーワード行（比較用）\n')
D=uniq([r for r in C if is_div(r)]);DK=uniq([r for r in K if is_div(r)])
for name,rows in [('知恵袋',D),('発言小町',DK)]:
    n,vm,vd=st([r['views'] for r in rows]);_,am,ad=st([r['answers'] for r in rows])
    print(f'- {name} n={len(rows)} 閲覧 '+(f'平均{vm:,.0f}/中央値{vd:,.0f}' if n else '取得なし')+f'、回答 平均{am:.1f}/中央値{ad:.0f}')
