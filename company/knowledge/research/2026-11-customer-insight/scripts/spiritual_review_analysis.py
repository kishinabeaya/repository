#!/usr/bin/env python3
"""T-0013 スピリチュアル商材レビュー分析（標準ライブラリのみ）。
使い方: python3 -I spiritual_review_analysis.py  -> 集計をstdoutへ。--dump <dir> で検証用の一覧を書き出す。
機械分類（正規表現）+ 人手確認の上書き（MANUAL_*）の2段階。"""
import json, re, os, sys, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', 'raw')

def load_unique():
    rows = [json.loads(l) for l in open(os.path.join(BASE, 'spiritual-goods-reviews.jsonl'), encoding='utf-8')]
    seen = set(); uniq = []
    for x in rows:
        if x['text'] in seen: continue
        seen.add(x['text']); x['uid'] = len(uniq); x['t'] = re.sub(r'\s+', ' ', x['text']); uniq.append(x)
    return rows, uniq

def has(t, pats): return any(re.search(p, t) for p in pats)
def which(t, d): return [k for k, p in d.items() if has(t, p)]

# ---------- 1. 変化 ----------
CHANGE_CAND = ['変化を感じ','効果があ','効果を感じ','すっきり','スッキリ','軽くな','体感','変化(?!な)','叶','眠れ','ぐっすり',
               '良くなっ','よくなっ','改善','楽になっ','前向きに','解消','消え','なくなり','効いた','効きま','実感']
# 変化なし・まだ・期待のみ（陰性）
NOCHANGE = ['(変化|体感|効果|実感|自覚)(は|が|も)?(まだ)?(あまり|特に|全く|全然|それほど)?(なかっ|無かっ|ありません|ない|無い|出来て(い)?ません|できて(い)?ません|感じられ(て)?(い)?ませ|分かりにくい)',
            'まだ(効果|変化|実感)','(変化|効果)はなかった','鈍感なので']
EVENT_STRONG = ['復縁(でき|し|が|に至|まで導)(?!るま)','連絡(が|を)?(来|きま|きた|き$|ありま)','臨時収入','当選','契約率','妊娠|授かり|受胎','逆告白','告白がありました','お付き合いして',
                '会えました','会うことが出来','再会','仲直り(でき|し)','食事(に|へ)(誘|行|OK)','誘われ','LINE(が|の)?(増|復活|繋が)','電話が来','ロト','ボーナス',
                '離婚に進','結婚の話','ばったり','すれ違','既読がつ','プロデュース','頂き物が','入金','契約書を整え','有給を取って','会いに来','話題提供が増','からの.{0,4}LINEが増','お金が入','昇給|昇進|内定|採用が決']
EVENT_VAGUE = ['ラッキー','引き寄せ','好転(?!反応)','運が良く','いい流れ|良い流れ','流れが急に動','人生が動き','良いこと|いいこと','シンクロ','偶然','状況が(良|変)']
BODY = ['(体|身体|からだ|体全体)(が|の|も|は)?(軽|楽|ぽか|温|だる|ほぐ|調子|緩|整|スッキリ|すっきり)','体調','肩','腰','痛(み|く|が|い)','頭(が|の)?(軽|痛|スッキリ|すっきり)','頭痛','むくみ','蕁麻疹','症状','(?<![熱])熱(が|っ|い)|発熱','疲れ(が)?(取|とれ|抜)|疲れにくく|疲れを感じ','ぽかぽか|ポカポカ|温か(く|い)|温ま','ピリピリ|ビリビリ','怠|だるさ','足(が|の)(軽|むくみ|痛|具合)|脚(が|の)|ふくらはぎ','胃','お腹|下腹','肌','食欲','持病','不調','(?<![ぁ-ん])コリ|こり(が|も)','咳','難聴','息苦し','神経']
SLEEP = ['眠れ|眠り|ぐっすり|熟睡|睡眠|寝つき|寝れ|目覚め|起きられ|起床|眠気']
MIND = ['(気持ち|心|気分|頭|こころ).{0,8}(軽|スッキリ|すっきり|楽|落ち着|穏やか|安定|明る|整)','(スッキリ|すっきり)','不安(が|は)?(消|なくな|減|無く|ない)','落ち着','穏やか','安心','癒','もやもや.{0,6}(消|スッキリ)','イライラ.{0,10}(減|少な|なくな)','ネガティブ.{0,12}(減|なくな)','気付き|気づき|腑に落ち','悩み.{0,6}(消|解決|なくな)']
POS = ['前向き','元気','やる気','自信','希望','明るく','ポジティブ','活力','勇気','ワクワク','笑顔']
ACTION = ['行動(力|が|できる|する|し)','動けるよう|動けた|動き出','踏み出','決断|決意|覚悟','挑戦','勇気(が|を)出|勇気を振り絞|勇気を持','話し合(う|え|い)(?!ま)','連絡してみ|声をかけ|誘ってみ','転職活動','始め(まし|た)','辞め']

def change_flags(t):
    f = {}
    f['neg'] = has(t, NOCHANGE)
    f['event'] = has(t, EVENT_STRONG)
    f['vague'] = has(t, EVENT_VAGUE)
    f['body'] = has(t, BODY); f['sleep'] = has(t, SLEEP)
    f['mind'] = has(t, MIND) or has(t, POS)
    f['action'] = has(t, ACTION)
    return f

# ---------- 2. リピート ----------
# (a1) 反復購入の明示（本人が過去にも買った／継続していると書いている）
REPEAT_A1 = ['(?<![0-9０-９一])(?:[2-9２-９二三四五六七八九十]|[0-9０-９]{2})(?:回目|度目|回め|度め)|(?:二|２|2)回めの|(?:一|１|1)(?:回|度)目','リピ(ート|ーター)(?!(し|す)(たい|たく|ます|よう|てみ|させて頂きたい|させていただきたい))','何(度|回)(も|か)(お世話|依頼|お願い|利用|頼|受け|相談|購入|鑑定|施術|助け|リピ|申し込)|数回|複数回','毎月|毎週|毎日のように','定期的に|定期的な',
 '継続(して|し|中|的)','(前回|前々回|前回の|以前|先日|過去|去年|昨年|前に|一度目|1度目).{0,25}(お願い(し|いた)|依頼(し|いた)|購入|利用|受け(て|た|まし)|鑑定|施術|頂|いただ|お世話)','回を重ね|回毎|毎回(お願い|依頼|ヒーリング|受け|頼|施術|鑑定)','常連','ずっと(お世話|お願い|利用|頼)','長期(に|間)?(渡|わた)り','[0-9０-９]+年(前から|来)','久しぶり(に)?(お願い|依頼|利用|鑑定)','再度(お願い|依頼|利用)','またまた','続けて(お願い|依頼|受け|い(る|ます))|続けています|続けていま']
# (a2) 反復の暗示（「今回も」等。単独では購入履歴の確証にならない）
REPEAT_A2 = ['(今回|この度|今日|本日|毎度|いつも)も(?:大変)?(?:ありがとう|お世話|助か|素晴ら|丁寧|よろしく|お願い)','いつもお世話','いつもありがとう','いつも(助け|救)','お世話になっております|お世話になってます|お世話になっています','また(お世話|お願い)(に|し)(なり|ます)']
# (b) 次回意向・社交辞令
REPEAT_B = ['また(お願い|依頼|利用|機会|ご縁|お世話|相談|よろしく|是非|ぜひ|宜しく)','次回(も|は)?(よろしく|お願い|依頼|宜しく)','機会が(あれば|ありましたら)','ぜひまた|是非また','引き続き(よろしく|お願い|宜しく)','今後(とも|も)(よろしく|宜しく|お願い)','これからも(よろしく|宜しく|お願い)','また(何か|分からない|悩み|困った|必要)']
# 継続理由
REASON = {
 '変化・効果を感じたから': ['効果を?(感じ|実感)','体感','変化','良くな(って|り)','改善','軽く','スッキリ|すっきり','楽に','当た(って|る|り)','叶','好転','助かって'],
 '安心・信頼': ['安心','信頼','頼り|頼れ|頼って','寄り添','心強い','支え','お人柄','親身','相談しやすい|話しやすい'],
 '相談相手・話を聞いてほしい': ['相談(相手|できる)|話を聞い|聞いてくれ|聞いていただ|話せる|愚痴|主治医|かかりつけ'],
 '習慣・メンテナンス': ['メンテナンス|定期的|習慣|日課|毎月|毎週|ルーティン|調子が悪くなると|調子が悪い時|困った(時|とき)'],
 '家族・他者のため': ['家族|母|父|娘|息子|夫|旦那|主人|友人|親友|妻|子供|子ども|彼女'],
 '価格・手軽さ': ['お安|手頃|リーズナブル|価格|料金|1,?000円|お値段|コスパ'],
 '他メニュー・オプション': ['他の(メニュー|サービス)|オプション|別の(メニュー|サービス)|他メニュー'],
}
# ---------- 4. 購入前の状況 ----------
SIT = {
 '仕事・職場': ['仕事|職場|転職|上司|同僚|会社|職|キャリア|就活'],
 '恋愛・パートナー': ['彼氏|彼女|彼(?!ら)|恋愛|復縁|片思い|片想い|別れ|失恋|結婚|離婚|不倫|パートナー|婚活|音信不通|お相手'],
 '家族・子ども': ['家族|母|父|娘|息子|夫|旦那|主人|子供|子ども|子育て|育児|親(?!切|身|し)|妻|兄弟|姉妹|義'],
 '人間関係': ['人間関係|友人|友達|人付き合い|対人|ママ友|いじめ|職場の人'],
 '体調・不調': ['体調|不調|症状|痛|病|眠れ|疲|だる|しんど|不眠|更年期|うつ|鬱|パニック|自律神経|頭痛'],
 '悩み・不安・つらさ': ['悩|不安|辛い|つらい|苦し|しんどい|落ち込|絶望|どん底|藁にも|心配|焦|もやもや|モヤモヤ|イライラ|不満|寂し|孤独|孤立|心細'],
 'お金': ['お金|金運|収入|借金|生活費|経済'],
}
TIMING_PRE = ['(悩ん|困っ|苦しん|迷っ|落ち込ん|辛かっ|つらかっ|不安だっ|不安で|心配で|焦っ|疲れ(て|果て)|眠れ(ず|なく|ない日)|どん底|藁にも|限界|行き詰|詰んで|限界)','(を|が)?(相談|お願い)(したく|したくて|させていただき|させて頂き)','きっかけ','気になって','探して','(つらい|辛い|大変な)時期','本当にきつ']
LONELY = ['孤独','寂し|淋し','独り|ひとり(ぼっち|で抱え)|一人(ぼっち|で抱え|で悩|で考え)','友(達|人)がいな|友達が少な|相談(できる|する)(人|相手)が(い)?な|話(せる|を聞いてくれる)(人|相手)が(い)?な|誰にも(相談|言え|話せ)','人に(相談|話)できな|話せる(人|相手)']

# ---------- 人手確認（全文を読んで判定した上書き）----------
# 具体的な現実の出来事（本人または代理依頼の相手に起きたと書かれているもの。真偽は未検証）
MANUAL_EVENT = {4,13,60,84,395,950,1083,1749,1819,1820,1822,2142,2148,2149,2155,2435,2439,2480,2484,2501,2503,2508,2510,2527,2530,2559,2560,2561,2567,2568,
 2569,2572,2574,2576,2577,2579,2582,2585,2589,2590,2594,2595,2597,2599,2601,2604,2609,2610,2613,2615,2618,2619,2620,2622,2624,2626,2627,2628,2629,2630,2631,
 2635,2636,2641,2642,2644,2645,2649,2651,2655,2656,2737}
# 正規表現で拾ったが、出来事の報告ではない（未発生・否定・無関係）
MANUAL_EVENT_EXCLUDE = {2175,2431,2433,2528,2563,2830,2852,2646,2565,2430,2443,2639,2657,2654}

MANUAL_REPEAT_EXCLUDE = {297, 1116, 2724}   # 反復購入ではない（自己クリーニング継続・過去の経験・体調の記述）

# 変化の分類で使う補助
ANTIC = ['楽しみ','期待','様子(を)?(見|み)','観察','願っ','いいな|良いな|ばいいな','祈っ','信じて','兆し|兆候']
UNSPEC_POS = ['(効果|体感|変化).{0,6}(感じ(た|まし|られ(て|た|る|ま)|て|る)|実感(でき|し|して)|あり(まし|ます)|あった|が出)','(感じ|実感)(して|でき|られ)(い)?(ます|ました|ている)','よく効|効きます|効果的|効果が(あり|高|すぐ)','体感(あり|が(あり|強|得))','変化(が|も)?(あり|感じ)','運氣が良く|運気が良く','良い兆し']
GENERAL = ['良くな(って|り|っ)','よくな(って|り|っ)','改善','変化し','クリア','なくなりました','減(って|り|っ)','消え(て|ま)','進んで','前進','整(って|い|っ)']

def classify_change(x):
    """主分類（排他・優先順）。戻り値 (primary, multi-label set)。"""
    t = x['t']; uid = x['uid']; f = change_flags(t)
    ev = (uid in MANUAL_EVENT) or (f['event'] and uid not in MANUAL_EVENT_EXCLUDE)
    if uid in MANUAL_EVENT_EXCLUDE: ev = False
    labels = set()
    if ev: labels.add('event')
    if f['vague']: labels.add('vague')
    if f['action']: labels.add('action')
    if f['body']: labels.add('body')
    if f['sleep']: labels.add('sleep')
    if f['mind']: labels.add('mind')
    antic = has(t, ANTIC)
    pos_past = has(t, UNSPEC_POS)
    general = has(t, GENERAL)
    if f['neg'] and not (labels & {'event','body','sleep','mind'}): primary = 'none_or_antic'
    elif ev: primary = 'event'
    elif f['action'] and not (labels & {'body','sleep'}): primary = 'action'
    elif labels & {'body','sleep'} and not (antic and not pos_past and not has(t, ['軽く(なり|なっ)','眠れ(まし|た)','ぐっすり','楽に(なり|なっ)(まし|た|て)','なくなり','痛み','治'])): primary = 'body'
    elif 'mind' in labels and not (antic and not pos_past and not has(t, ['スッキリ|すっきり','軽く(なり|なっ)','落ち着(き|い)(まし|た|て)','安心(し|でき)'])): primary = 'mind'
    elif 'vague' in labels: primary = 'vague'
    elif pos_past or general: primary = 'unspecified'
    elif antic: primary = 'none_or_antic'
    else: primary = 'other'
    return primary, labels

def repeat_class(x):
    t = x['t']
    if x['uid'] in MANUAL_REPEAT_EXCLUDE:
        return 'b' if has(t, REPEAT_B) else 'none'
    if has(t, REPEAT_A1): return 'a1'
    if has(t, REPEAT_A2): return 'a2'
    if has(t, REPEAT_B): return 'b'
    return 'none'

def reasons(t):
    return [k for k, p in REASON.items() if has(t, p)]

# ---------- 購入前の状況 ----------
# 購入前（依頼時点）の悩み・状況を述べる文脈
PRE = ['(悩ん|困っ|苦しん|迷っ|落ち込ん|辛かっ|つらかっ|不安(だっ|で)|心配(で|だっ)|焦っ|疲弊|疲れ(て|果て)(い|きっ)|眠れ(ず|なく|ない)|どん底|藁にも|すがる思い|限界|行き詰|きつかっ|悩み(が|を)|不調(が|で|を)|体調(が|不良)(悪|で|が続)|落ち込み|限界)',
       '(お願い|依頼|相談|申し込み|申込み)(し|いた|致し|させて).{0,3}(のは|きっかけ|理由)','(ので|ため|たくて|ところ|そこで).{0,6}(お願い|依頼|相談|申し込|申込)','(悩み|不安|不調|体調不良|トラブル|問題|状況).{0,12}(お願い|依頼|相談|申し込|申込)',
       '(つらい|辛い|大変な|きつい)(時期|状況|時|日々)','(探して|探していた)','(トラブル|問題)(が|を)(起き|あり|抱え|続い)','(人間関係|職場|家族|夫婦|子育て|育児|恋愛|仕事).{0,14}(悩|困|辛|つら|苦し|疲|トラブル)']
LONELY_PAT = ['孤独','寂し|淋し','(独り|ひとり|一人)(ぼっち|で抱え|で悩|で考え|で頑張|きり)','友(達|人)(が|も)(い)?(な|少な)|周(り|囲)に(相談|話)(できる|せる)?(人|相手)','相談(できる|する|出来る)(人|相手)(が|も)(い)?(な|少)','話(せる|を聞いてくれる|を聞いてもらえる)(人|相手)(が|も)(い)?(な|少)','誰にも(相談|言え|話せ|話し|打ち明)','人に(相談|話)(できな|出来な|しづら|しにく)','身近(な人|に)(に)?(相談|話)','話しづらい|話しにくい|言えない']
TRIGGER = {
 '悩み・不安・つらさの自覚（一般）': ['悩|不安|辛い|つらい|苦し|落ち込|どん底|藁にも|すがる|心配|焦|疲弊|限界|行き詰'],
 '体調不良・症状': ['体調|不調|症状|痛|眠れ|不眠|更年期|疲れ|だる|しんど|具合'],
 '恋愛・復縁・相手の気持ち': ['彼氏|彼女|彼(?!ら)|恋愛|復縁|片思い|片想い|別れ|失恋|不倫|音信不通|お相手|相手の気持ち|縁結び'],
 '仕事・金銭': ['仕事|職場|転職|上司|同僚|会社|収入|お金|金運|借金|生活'],
 '家族・子ども・夫婦': ['家族|母|父|娘|息子|夫|旦那|主人|子供|子ども|子育て|育児|夫婦|義|親(?!切|身|し)'],
 '人間関係': ['人間関係|友人|友達|人付き合い|対人|ママ友|いじめ|周りの人'],
 'トラブル・不運・原因が分からない出来事': ['トラブル|不運|立て続け|続けて(起|悪)|原因(が|を)?(分か|わか|知り)|説明がつかな|おかしい|原因不明|物理的な原因|憑|祟|霊障|厄|呪'],
 '転機・節目': ['転機|節目|厄年|本厄|新年|年明け|引っ越|離婚後|出産|退職|転職|独立|新しい人生|ターニング'],
 '口コミ・紹介・他サービスで効果': ['他のサービス|別のサービス|他の方|紹介|評判|口コミ|SNS|YouTube|友人に|知人|おすすめ(され|を見)|勧められ'],
 'お試し・好奇心・価格が手頃': ['お試し|初めて|興味|気になって|気になっていた|お安|手頃|リーズナブル|1,?000円|500円|ワンコイン'],
 '緊急・急に': ['急に|突然|急遽|緊急|至急|当日|すぐに(お願い|頼|対応)'],
}

# 孤独・相談相手の不在に触れる本文（全文を読んで人手で選定。正規表現では取りこぼし・誤検出があったため）
LONELY_A = [353, 1061, 1076, 2360, 2676, 2711]          # 話せる相手・理解者・相談相手の不在を直接述べる
LONELY_B = [917, 1554, 1642, 1651, 1925, 2683]                 # 孤独感・「一人ではない」・居場所のなさ
LONELY_C = [1395, 1842, 1846]                            # 愚痴・不満を聞いてもらえたことへの言及
# 批判・負担・依存の兆候（人手確認済み）
CRITICAL = [746, 689, 1827, 1934]
DEPEND_PAT = ['何度も(同じ|相談|依頼)|同じ(事|こと)(を)?(何度|繰り返し)','頼り切','依存','やめられ','ジプシー','お金ばかり','毎日(のように)?(占|相談|鑑定)','毎日ヒーリング|毎日のようにお願い','進展もない','お金を使','高額|高い(と|気が|です|けど)|値段が','追加料金|勧められ|勧誘']

TITLE_TERMS = ['叶','変わ','変化','浄化','ブロック解除|ブロック','波動','開運','運気|運勢','金運','復縁','縁結び|ご縁','霊視|霊能','除霊|憑依|エーテルコード','祈祷|ご祈祷|祈願','護符|お守り','引き寄せ','願望|実現','即|最短|当日','効果|効く','好転','幸せ|幸運','エネルギー|氣|気功','癒','チャクラ','遠隔','ヒーリング','厄|お祓い|祓','先祖|供養','治|症状|痛み|不調|病|改善']

def price_bins(prices):
    bins = [(0,500,'~500円'),(501,1000,'501~1,000円'),(1001,3000,'1,001~3,000円'),(3001,5000,'3,001~5,000円'),(5001,10000,'5,001~10,000円'),(10001,30000,'10,001~30,000円'),(30001,10**9,'30,001円~')]
    return [(lab, sum(1 for p in prices if lo <= p <= hi)) for lo, hi, lab in bins]

def pct(a, b): return '%.1f%%' % (100.0 * a / b) if b else '-'

def main():
    import statistics
    rows, u = load_unique(); N = len(u)
    L = []; P = L.append
    P('全行 %d / 重複除去後 %d / サービス数 %d' % (len(rows), N, len(set(x['service_id'] for x in u))))
    # 1 変化
    cand = [x for x in u if has(x['t'], CHANGE_CAND) or x['uid'] in MANUAL_EVENT]
    cls = {x['uid']: classify_change(x) for x in cand}
    cnt = collections.Counter(p for p, _ in cls.values())
    P('\n## 1. 変化 候補(機械抽出) %d件 = %s of %d' % (len(cand), pct(len(cand), N), N))
    for k in ['event','action','body','mind','vague','unspecified','none_or_antic','other']: P('  %s: %d' % (k, cnt[k]))
    pos = [x for x in cand if cls[x['uid']][0] not in ('none_or_antic', 'other')]
    P('  変化を述べる(正): %d (%s)' % (len(pos), pct(len(pos), N)))
    ml = collections.Counter(l for x in pos for l in cls[x['uid']][1])
    P('  multi-label(正のみ): %s' % dict(ml))
    ev = [x for x in pos if 'event' in cls[x['uid']][1]]
    P('  event を含む: %d / サービス別: %s' % (len(ev), collections.Counter(x['service_id'] for x in ev).most_common(6)))
    # 2 リピート
    rc = {x['uid']: repeat_class(x) for x in u}
    rcnt = collections.Counter(rc.values())
    P('\n## 2. リピート a1=%d a2=%d b=%d none=%d' % (rcnt['a1'], rcnt['a2'], rcnt['b'], rcnt['none']))
    a1 = [x for x in u if rc[x['uid']] == 'a1']
    rs = collections.Counter(r for x in a1 for r in reasons(x['t']))
    P('  a1 理由(multi): %s' % dict(rs))
    P('  a1 理由なし: %d' % sum(1 for x in a1 if not reasons(x['t'])))
    # 3 仮説
    posids = {x['uid'] for x in pos}
    both_a1 = sum(1 for i in posids if rc[i] == 'a1'); both_a12 = sum(1 for i in posids if rc[i] in ('a1', 'a2')); both_any = sum(1 for i in posids if rc[i] != 'none')
    nonpos = [x for x in u if x['uid'] not in posids]
    P('\n## 3. 正の変化 %d件のうち a1=%d (%s) a1+a2=%d (%s) b含む何か=%d (%s)' % (len(posids), both_a1, pct(both_a1, len(posids)), both_a12, pct(both_a12, len(posids)), both_any, pct(both_any, len(posids))))
    P('  非変化 %d件のうち a1=%d (%s) a1+a2=%d (%s)' % (len(nonpos), sum(1 for x in nonpos if rc[x['uid']] == 'a1'), pct(sum(1 for x in nonpos if rc[x['uid']] == 'a1'), len(nonpos)), sum(1 for x in nonpos if rc[x['uid']] in ('a1','a2')), pct(sum(1 for x in nonpos if rc[x['uid']] in ('a1','a2')), len(nonpos))))
    P('  a1 %d件のうち変化(正)を述べる: %d (%s)' % (len(a1), sum(1 for x in a1 if x['uid'] in posids), pct(sum(1 for x in a1 if x['uid'] in posids), len(a1))))
    for k in ['event','body','mind','unspecified']:
        s = [x for x in pos if cls[x['uid']][0] == k]
        P('  主分類 %s %d件 のうち a1=%d (%s)' % (k, len(s), sum(1 for x in s if rc[x['uid']] == 'a1'), pct(sum(1 for x in s if rc[x['uid']] == 'a1'), len(s))))
    # 4 購入前
    pre = [x for x in u if has(x['t'], PRE)]
    P('\n## 4. 購入前の状況(PRE一致) %d件 (%s)' % (len(pre), pct(len(pre), N)))
    tr = collections.Counter(k for x in pre for k in which(x['t'], TRIGGER))
    P('  きっかけ/状況(multi): %s' % dict(tr.most_common()))
    sit_any = [x for x in u if has(x['t'], list(sum(SIT.values(), [])))]
    P('  状況語(SIT)を含む(時制不問): %d (%s)' % (len(sit_any), pct(len(sit_any), N)))
    P('  SIT別(時制不問): %s' % {k: sum(1 for x in u if has(x['t'], p)) for k, p in SIT.items()})
    P('  孤独A=%d B=%d C=%d / "孤独"語=%d "寂し|淋し"=%d' % (len(LONELY_A), len(LONELY_B), len(LONELY_C), sum(1 for x in u if '孤独' in x['t']), sum(1 for x in u if re.search('寂し|淋し', x['t']))))
    dep = [x for x in u if has(x['t'], DEPEND_PAT)]
    P('  批判・負担・依存の兆候(機械) %d件 / 人手確認 %s' % (len(dep), CRITICAL))
    # 5 タイトル・価格
    svc = list(csv.DictReader(open(os.path.join(BASE, 'spiritual-goods-services.csv'), encoding='utf-8')))
    P('\n## 5. サービス %d件' % len(svc))
    for plat in ['coconala', 'booth']:
        s = [r for r in svc if r['platform'] == plat]; pr = [int(r['price']) for r in s if r['price']]
        P(' %s n=%d 中央値=%s 平均=%.0f 最小=%d 最大=%d' % (plat, len(s), statistics.median(pr), statistics.mean(pr), min(pr), max(pr)))
        P('  価格帯: %s' % price_bins(pr))
        P('  タイトル語: %s' % {t[:10]: sum(1 for r in s if re.search(t, r['title'])) for t in TITLE_TERMS})
    # 補足集計
    posids2 = {x['uid'] for x in pos}
    evs = [x for x in pos if 'event' in cls[x['uid']][1]]
    T = {'お金':'臨時収入|当選|ロト|ボーナス|配当|頂き物|入金|契約率|収入|くじ','恋愛・対人':'彼|連絡|復縁|再会|お付き合い|告白|結婚|仲直り|LINE|誘|会え|離婚|主人|デート|ばったり|電話|人間関係','仕事':'仕事|プロデュース|契約|転職|フリマ|商品が売れ|書類','妊娠・家族':'妊娠|授かり|母|家族|娘'}
    ct = collections.Counter(([k for k, p in T.items() if re.search(p, x['t'])] or ['その他'])[0] for x in evs)
    P('\n## 補足')
    P('  出来事の種類(先頭一致): %s' % dict(ct))
    P('  出来事72件のうち サービス1400270(恋愛占い)=%d' % sum(1 for x in evs if x['service_id'] == '1400270'))
    ex = [x for x in u if x['service_id'] != '1400270']; px = [x for x in ex if x['uid'] in posids2]
    P('  1400270を除く: N=%d 正の変化=%d  a1率(正の変化)=%s a1率(それ以外)=%s' % (len(ex), len(px), pct(sum(1 for x in px if rc[x['uid']] == 'a1'), len(px)), pct(sum(1 for x in ex if x['uid'] not in posids2 and rc[x['uid']] == 'a1'), len(ex) - len(px))))
    a1s = [x for x in u if rc[x['uid']] == 'a1']; na1 = [x for x in u if rc[x['uid']] != 'a1']
    P('  正の変化率: a1の中=%s  a1以外=%s' % (pct(sum(1 for x in a1s if x['uid'] in posids2), len(a1s)), pct(sum(1 for x in na1 if x['uid'] in posids2), len(na1))))
    fr = [x for x in u if re.search('初めて|はじめて|初回|初依頼|初利用', x['t']) and rc[x['uid']] != 'a1']
    P('  初回言及(a1除く) %d件: 正の変化=%s / 次回意向(b)=%s' % (len(fr), pct(sum(1 for x in fr if x['uid'] in posids2), len(fr)), pct(sum(1 for x in fr if rc[x['uid']] == 'b'), len(fr))))
    P('  サービス別レビュー数(重複除去後)上位: %s' % collections.Counter(x['service_id'] for x in u).most_common(5))
    print('\n'.join(L))
    return rows, u, cand, cls, pos, rc, pre

if __name__ == '__main__':
    main()
