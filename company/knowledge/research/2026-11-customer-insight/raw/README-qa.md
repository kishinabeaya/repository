# raw/README-qa.md  Q&A・相談サイト 生データ収集メモ

- 取得日: 2026-11-07。方法: curl（GETのみ、ログイン・POSTなし、1.3秒間隔、UA=通常ブラウザ）。合計リクエスト数: 150（上限）。
- 投稿者名・IDは保存していない。textは冒頭300字まで。
- 知恵袋: 検索 `https://chiebukuro.yahoo.co.jp/search?p=<kw>`（1ページ10件、&page=2で次頁）を解析。title/summary/回答数/閲覧数/質問日時/カテゴリを取得。うち70件は詳細ページ（JSON内questionText）から本文を取得（text_source=detail）。それ以外は検索結果の要約文（text_source=search-summary、短い）。
- 発言小町: `https://komachi.yomiuri.co.jp/search/?text=<kw>` のJSON-LDからtitle/本文冒頭（サイト側で約100字に省略済み）/レス数/投稿日。閲覧数は表示なし（null）。ジャンル別の件数比較は未実施。
- 件数: chiebukuro.jsonl 400行（ユニークURL 367）、komachi.jsonl 180行。
- 取得できなかったもの: 子育て・家族テーマの件数比較とサンプル（リクエスト上限のため未取得）。発言小町のテーマ別トピック数（検索ヒット件数の保存をしていない）。知恵袋の占い系キーワードのヒット件数（1件を除き未保存）。回答本文は保存していない。

## テーマ別 相談件数の比較（知恵袋・検索ヒット件数 totalHits）
数え方: 各テーマ1つの検索語で `search?p=<語>` を実行し、ページ内の totalHits を記録（同日・同方式）。複数語はAND検索。検索語の選び方に依存するため、あくまで同条件の目安で、テーマの母数そのものではない。1テーマ1語のみで、同義語は含まない。

| テーマ | 検索語 | ヒット件数 |
|---|---|---|
| 将来の不安 | 将来 不安 | 330,482 |
| お金 | お金 不安 | 529,294 |
| 仕事 | 仕事 悩み | 900,736 |
| 恋愛・結婚 | 恋愛 悩み | 289,675 |
| 健康・メンタル | メンタル 悩み | 56,670 |
| 人間関係 | 人間関係 悩み | 248,764 |
| 自分らしさ | 自己肯定感 生き方 | 2,114 |
| （参考）占い | 占い 当たる | 60,319 |

注意: 「仕事 悩み」等の件数は検索語の一般性に左右される。「メンタル 悩み」「自己肯定感 生き方」は語が狭く、テーマ全体より小さく出る。各テーマのサンプルは jsonl の keyword が `theme:<テーマ>|<検索語>` の行（各10件、検索の関連度順。閲覧数順ではない）。

## キーワード別 件数（知恵袋 jsonl行数、ページ数分）

| keyword | 行数 |
|---|---|
| 占い 当たる | 10 |
| 占い 依存 | 10 |
| 占い 不安 | 10 |
| 数秘術 | 10 |
| 星占い | 10 |
| 来年 運勢 | 10 |
| 2027年 運勢 | 10 |
| 占い 有料 価値 | 10 |
| 占い師 相談 内容 | 10 |
| 占い 当たらない | 10 |
| 占い 電話占い 高い | 10 |
| 将来が不安 | 10 |
| 転職 迷う | 10 |
| 恋愛 不安 30代 | 10 |
| 自分に向いている仕事 わからない | 10 |
| 人間関係 疲れた | 10 |
| 人生 迷子 | 10 |
| 生きるのがつらい 将来 | 10 |
| 結婚 できない 不安 30代 | 10 |
| 仕事 辞めたい 先が見えない | 10 |
| 自分がわからない 何をしたいか | 10 |
| タロット 悩み 相談 | 10 |
| 占い 数秘術 当たる | 10 |
| 運勢 2027 | 10 |
| 占い 頼りすぎ やめたい | 10 |
| 占い 何を聞けばいい | 10 |
| 将来 不安 眠れない | 10 |
| 転職 不安 30代 | 10 |
| 占い 恋愛 不安 | 10 |
| 占い 仕事 転職 | 10 |
| ライフパス ナンバー | 10 |
| 占い 詐欺 高額 | 10 |
| 占い 無料 有料 違い | 10 |
| theme:将来の不安|将来 不安 | 10 |
| theme:お金|お金 不安 | 10 |
| theme:仕事|仕事 悩み | 10 |
| theme:恋愛・結婚|恋愛 悩み | 10 |
| theme:健康・メンタル|メンタル 悩み | 10 |
| theme:人間関係|人間関係 悩み | 10 |
| theme:自分らしさ|自己肯定感 生き方 | 10 |

## 発言小町 キーワード別 件数

| keyword | 行数 |
|---|---|
| 占い | 20 |
| 占い 不安 | 10 |
| 占い師 | 10 |
| 数秘術 | 10 |
| 運勢 | 10 |
| タロット | 10 |
| 将来 不安 | 20 |
| 人生 迷子 | 10 |
| 転職 迷う | 10 |
| 人間関係 疲れた | 20 |
| 恋愛 不安 | 10 |
| 向いている仕事 わからない | 10 |
| 生き方 迷う | 10 |
| 仕事 辞めたい | 10 |
| 孤独 不安 | 10 |

## 知恵袋 閲覧数 上位15（取得分のみ）

- 62,384閲覧/3回答 占いって何を聞くべき・・・？！ 占いって何を聞いたらいいんでしょう？ 来週、1年前から予... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1031689890
- 49,883閲覧/4回答 占いで絶対に引越ししてはいけない時期に引越しをした…と言われてしまいました。 １ヶ月前に引越し... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1319475583
- 28,055閲覧/6回答 仕事がみつからない。先が見えなくて不安で死にたくなります。 前の会社を辞め1年半以上経ちます。... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1047448435
- 27,698閲覧/2回答 タロット占いって当たるんですか？ もし当たるとしたらどういう仕組み？ 当たらないんだとしたらな... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10306764300
- 20,682閲覧/4回答 星ひとみさんの占いを月額390円で入会しました。その月には退会して、翌月からは引き落としがないはずだ https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11309109836
- 20,063閲覧/3回答 ゲッターズ飯田の占いって当たりますか？ アンチとかではなく、私も信じてここ数年本を買っています。 https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13317395418
- 20,021閲覧/4回答 30代の男性って、好きな人・恋人との連絡頻度は比較的低い方ですか？一日にどのくらい連絡取り合い... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14277632744
- 17,388閲覧/10回答 お金が足りず毎日不安です。 4人家族(小1、幼稚園年少の子あり)私は専業主婦で旦那のお給料は月30万 https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12297724222
- 12,833閲覧/4回答 占いって何を聞けばいいんですか？ 友人と、生まれて初めて占い師さんに占ってもらうことになりましたが何 https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14109532904
- 12,203閲覧/5回答 来年の2025年の運勢が最悪すぎて不安です。 私は八白土星、火星人プラス、金の鳳凰座です。どの... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11308707756
- 11,142閲覧/11回答 占いをとても信じます。 占いに頼ることがやめられません。 特に恋愛です。 運勢とか相性とか 相... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14179366994
- 11,095閲覧/5回答 占いで、面白いサイトありますか？ 占い好きなんです。 無料で楽しめる占いサイトを教えてください。 https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12128465837
- 9,295閲覧/1回答 電話占い師の方に質問です 正直キツく無いですか？ なかなか稼げないとか 相談内容がしんどいとか リア https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14217734119
- 8,575閲覧/5回答 占いって当たらないですよね？？何も根拠がないのに、最近占いに振り回されて辛いです。当たらなかっ... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10318901525
- 8,325閲覧/4回答 占いで結婚する年齢や時期を言い当てられた人で、当たったことがある人はいますか？ 何歳で結婚す... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14301600759

## 知恵袋 回答数 上位10（取得分のみ）

- 20回答/7,551閲覧 30代で未経験事務に転職するには それなりにパソコンスキルが必要でしょうか？ 今まで肉体労働... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11276968541
- 17回答/420閲覧 将来が不安で仕方なく資格マニアになりそうです。 大きめの銀行勤めサラリーマン34歳です。 たく... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11330907806
- 16回答/772閲覧 恋愛占いの練習にご協力頂ける方募集！ 初心者であることをご理解いただいた上で、ご協力いただけ... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10317869505
- 13回答/411閲覧 占いって全くなんの意味もないですよね。 占いは詐欺だとかスピリチュアルなんかないとかそういった... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11318881756
- 13回答/164閲覧 将来の不安について。19歳女です。 現在音楽大学に通っています。私は最近、ずっと将来の不安で眠れませ https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10306602070
- 12回答/105閲覧 30代、40代以上の独身者が増加したのは何が原因ですか？ https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10331476050
- 12回答/2,239閲覧 受験と恋愛について悩んでます。 私は今高2で今同い年の他校のいい感じになっている人がいます。私... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13322425523
- 12回答/690閲覧 不倫をしている人は皆、自己肯定感が低いのですか？ わたしはしていますが、自分の考え、生き方、これまで https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10310378130
- 11回答/152閲覧 将来が不安で2人目を産むか悩んでいます。 目を通して下さりありがとうございます。1児の母です、... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11330859691
- 11回答/139閲覧 30代後半独身女性、安定した職業に就き、独身友達と気軽に旅行に行き、子供も欲しくない、側から見... https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13326376558

## 発言小町 レス数 上位10（取得分のみ）

- 180レス 勤務時間を増やして欲しい！と話したのですが… https://komachi.yomiuri.co.jp/topics/id/1245000/
- 158レス 年収500万の彼氏との将来に不安があります。 https://komachi.yomiuri.co.jp/topics/id/1250361/
- 145レス 老人になりたくありません https://komachi.yomiuri.co.jp/topics/id/791695/
- 138レス 霊能者の占い https://komachi.yomiuri.co.jp/topics/id/1249513/
- 132レス 子どもが欲しい自分（男）と育てる自信がない彼女 https://komachi.yomiuri.co.jp/topics/id/1198466/
- 125レス あなたの生き甲斐は、なんですか？ https://komachi.yomiuri.co.jp/topics/id/1115042/
- 114レス 「論理的じゃない人」って実質最強だと思いませんか？ https://komachi.yomiuri.co.jp/topics/id/1233739/
- 89レス 人生に迷ったときはどちらの道を選びますか？ https://komachi.yomiuri.co.jp/topics/id/675548/
- 83レス 転職のお誘いに乗るか（16年勤めてる現職を辞めるか） https://komachi.yomiuri.co.jp/topics/id/1230813/
- 82レス 子どもを望むということ https://komachi.yomiuri.co.jp/topics/id/1217763/
