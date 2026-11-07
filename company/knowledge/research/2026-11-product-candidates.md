# 商品候補の調査と推奨（T-0001）

作成: strategist 2026-11-06 / 対応: KR1 / D-0001（最速の収益化）・D-0002（予算ゼロ）

## 0. 調査の制約（先に読むこと）
- 調査環境の制約で booth.pm / note.com / help-note.com へは直接アクセスできなかった（ネットワーク許可外）。販売ページ・ランキング・レビュー数を**直接確認できていない**。
- 以下の手数料は Web 検索結果（公式ヘルプを引用した要約）経由であり、**CEOが出品前に各公式ページで最終確認すること**。
- 需要の証拠は「確認できた事実」だけを書く。確認できないものは「未検証」とした。**どの候補も、実売数での需要は未検証**。これが本調査の最大の弱点である。

## 1. 無料で出品できる販売チャネルと手数料

| チャネル | 初期/月額 | 販売手数料（確認できた範囲） | 出典 | 備考 |
|---|---|---|---|---|
| note（有料記事・マガジン） | 0円 | 事務手数料（購入者の決済手段で変動。クレカ5%、携帯キャリア15%、PayPay・Amazon Pay 7%、PayPal 6.5%、noteポイント10%）＋プラットフォーム利用料（売上から事務手数料を引いた額の10%）。振込手数料270円/回。例: 1,000円をクレカ購入→手数料計145円、手元855円（振込手数料前） | [note公式ヘルプ](https://www.help-note.com/hc/ja/articles/360011358873-コンテンツを販売する際に引かれる手数料)（検索結果経由） | 文章系に最適。ファイル添付は有料記事内で可能（未検証） |
| BOOTH | 0円（出品・ショップ開設無料と複数記事が記載） | サービス利用料は 5.6%＋45円/取引（2025-10-28に22円→45円へ改定との報道）。2026年の比較記事に「+22円」の記載もあり情報が割れる→**公式で要確認** | [GameBusiness 2025-07-24](https://www.gamebusiness.jp/article/2025/07/24/24711.html)、[QUASA](https://quasa.io/ja/media/boothkasuzurika-1000jpydlfan-mai-hagu-ding-23jpychai-gacan-ru) | デジタル商品（PDF/Excel/Notionリンク）向き。低単価だと固定45円の比率が大きい |
| ココナラ | 出品無料（根拠不明確・未検証） | 販売手数料22%（税込）。公式お知らせでは27.5%→22%に改定と案内（年の記載なし）。購入者側にも別途5.5%の手数料の情報あり | [ココナラお知らせ](https://coconala.com/news/532)、[atsoho解説](https://atsoho.com/blog/coconala-fee-2026-breakdown) | 手数料が高い。個別対応が発生しCEO負担大 |
| Gumroad | 0円 | 直接販売10%＋$0.50、カード処理費は別（2.9%＋$0.30との記述）。Discover経由は30%。日本の銀行へ全銀で入金できる旨の報道あり（時期未確認） | [swell.is](https://www.swell.is/content/gumroad-pricing)、[Gumroad公式ヘルプ](https://gumroad.com/help/article/13-getting-paid)、[TechCrunch](https://techcrunch.com/?p=907446) | 日本語UI・日本の消費税対応は未検証。第三者情報が多い |
| BASE（スタンダード） | 月額0円 | 決済手数料3.6%＋40円＋サービス利用料3%（計6.6%＋40円）。振込手数料250円。デジタルコンテンツ特有の条件は未検証 | [shopowner-support](https://www.shopowner-support.net/attracting_customers/retail/netshop/thebase/)、[imitsu](https://imitsu.jp/cost/hp-design/base-commission) | 手数料は安いが自前集客。ショップ設計の手間 |
| STORES | 未調査 | 未検証 | — | 検索回数節約のため割愛 |

## 2. 候補と採点（各5点満点・合計30点）
評価軸は `company/playbooks/market-research.md`。「需要」は実売の直接確認ができていないため、**最大でも3点**に抑えた（周辺情報のみ）。

| # | 候補 | チャネル | 速さ | 初期費用0 | 需要の証拠 | AI制作 | CEO作業 | 規約リスク | 合計 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 業務別 生成AIプロンプト集＋活用ガイド（PDF/記事） | note（＋BOOTH） | 5 | 5 | 3 | 5 | 4 | 4 | **26** |
| 2 | Excel/スプレッドシート業務テンプレ（見積書・請求書・在庫・家計簿など）セット | BOOTH | 4 | 5 | 3 | 4 | 4 | 4 | **24** |
| 3 | Notionテンプレート（業務管理・学習管理など） | BOOTH | 4 | 5 | 3 | 3 | 3 | 4 | **22** |
| 4 | 特定層向けノウハウ電子書籍（note有料記事。例: AI活用の副業入門） | note | 4 | 5 | 2 | 5 | 4 | 3 | **23** |
| 5 | 文章作成代行（ブログ・商品説明）サービス | ココナラ | 3 | 5 | 2 | 4 | 1 | 4 | **19** |
| 6 | ブラウザ小ツール（計算機・文字数カウンタ等）＋有料版 | GitHub Pages＋BOOTH | 2 | 5 | 1 | 4 | 3 | 4 | **19** |
| 7 | Canvaテンプレート | BOOTH/Canva | 2 | 3 | 2 | 2 | 2 | 3 | **14** |
| 8 | 税務・法律・医療系の解説書（インボイス対応ガイド等） | note | 4 | 5 | 2 | 3 | 4 | 1 | **19** |

採点根拠（需要の証拠）:
- #1: noteが販売先として挙げられ、初期費用0〜3,000円・売れたときのみ手数料が発生と解説する国内記事がある（[aipicks](https://aipicks.jp/mag/prompt-template-selling-start-guide)）。ココナラに「ChatGPTプロンプト集」の出品が存在する（[ココナラ出品例](https://coconala.com/services/4200427)）。ただし**販売数・ランキングは未検証**。供給が多く競合が多いことは確かだが、数は未検証。
- #2: BOOTHに売上管理テンプレート（980円）の出品が存在することを確認（[BOOTH出品例](https://booth.pm/en/items/8635053)）。販売数は未検証。
- #3: BOOTHにNotionテンプレート（業務管理系・ウェルネス系）の出品が複数存在（[例1](https://booth.pm/en/items/8104193)、[例2](https://booth.pm/en/items/8192285)）。販売数は未検証。Notion公式マーケットプレイスは審査に数か月かかる場合あり（[Notion](https://www.notion.com/ja/help/selling-on-marketplace)）ので不採用。Notionは複製用ページの公開作業が増え、CEO/ビルダー側の手間が大きい。
- #4〜#8: 需要の確認ができず未検証。

## 3. 推奨（1案）

### 推奨: 業務別 生成AIプロンプト集＋すぐ使える活用ガイド（note有料記事、BOOTHに同内容を併売）
- **ターゲット**: 個人事業主・小規模事業者・会社員で、ChatGPT/Claude等は使えるが「業務で何を指示すればよいか」分からない人。
- **商品概要**: 職種別（営業メール、議事録、見積・請求の文面、SNS投稿、求人文、問い合わせ返信など）のコピペ可能プロンプト30〜50本＋入力例＋出力例＋使い方。特定1業種に絞る方が競合と差別化できる（業種は未決。CEOの得意分野があれば優先）。
- **競合との違い**: 単発のプロンプト羅列ではなく、「作業手順を通して使えるセット」にする（海外解説の指摘: [dodopayments](https://dodopayments.com/blogs/sell-ai-prompts-online)）。日本語・日本の商習慣に合わせた例を入れる。
- **想定価格帯**: 500〜1,500円（推定。類似商品の価格は直接確認できておらず**未検証**。BOOTHの売上管理テンプレが980円という事実のみ確認）。最終決定はCEO（L2）。
- **チャネル**: note（手数料はクレカ購入で約14.5%。1,000円で手元855円）。BOOTH併売は任意。
- **最初の1件までの道筋（目安）**:
  - Day1-3: 構成決定→Builder/Creatorが本文作成、Analystが品質・事実確認
  - Day4: 商品ページ文案・無料サンプル記事を作成
  - Day5: CEOがnoteアカウント設定・口座登録・特商法表記を確認し出品（L2承認）
  - Day6〜: 無料サンプル記事・X等の無料SNSで告知。**自前の読者がいない場合、初売上は遅れる可能性が高い**（最大リスク）

### 代替案A: Excel/スプレッドシート業務テンプレセット（BOOTH）
- 理由: 中身が具体的で「買う理由」が明確。AIがPythonで生成可能（要検証）。BOOTHは固定45円がかかるため価格は500円以上に。
- 選ばなかった理由: 動作検証の手間と、画面付き商品ページの作成が必要で、#1よりやや遅い（需要の証拠は同程度）。

### 代替案B: 特定層向けノウハウ電子書籍（note有料記事）
- 理由: 制作が最速。CEOの経験・実体験があれば強い。
- 選ばなかった理由: 一般的な内容では差別化が難しく、需要の証拠が最も弱い。

## 4. 選ばなかった案と理由
| 案 | 理由 |
|---|---|
| #3 Notionテンプレート | 複製用ページの公開・管理の手間が大きく、公式マーケットは審査数か月。需要は未検証 |
| #5 ココナラ代行 | 手数料22%、個別対応が継続しCEOの作業時間（KR6）を圧迫 |
| #6 ブラウザ小ツール | 無料ツールが飽和しており課金が難しい。収益化まで時間がかかる |
| #7 Canvaテンプレ | Canvaアカウントの制約・AIでの制作が難しい。無料出品の条件が未検証 |
| #8 税務・法律・医療系 | 資格・誤情報リスクが高い（評価軸の規約リスク1点）。再検討するなら専門家の確認が必要 |

## 5. 未検証事項
- すべての候補で、**実際の販売数・ランキング・レビュー数は確認できていない**（booth.pm/note.comに接続不可）。CEOまたは次回のネットワーク許可後に、noteの有料記事（「ChatGPT プロンプト」等）とBOOTHの人気順上位の販売数・価格帯を確認することを推奨。
- BOOTHの現行手数料（+22円か+45円か）。ココナラの出品無料可否。GumroadとBASEのデジタル商品の細部、STORESの手数料。
- noteでの有料記事内ファイル添付可否、価格帯の相場。

## 6. 出典一覧
- https://www.help-note.com/hc/ja/articles/360011358873-コンテンツを販売する際に引かれる手数料
- https://www.gamebusiness.jp/article/2025/07/24/24711.html
- https://quasa.io/ja/media/boothkasuzurika-1000jpydlfan-mai-hagu-ding-23jpychai-gacan-ru
- https://coconala.com/news/532
- https://atsoho.com/blog/coconala-fee-2026-breakdown
- https://www.swell.is/content/gumroad-pricing
- https://gumroad.com/help/article/13-getting-paid
- https://www.shopowner-support.net/attracting_customers/retail/netshop/thebase/
- https://imitsu.jp/cost/hp-design/base-commission
- https://aipicks.jp/mag/prompt-template-selling-start-guide
- https://coconala.com/services/4200427
- https://booth.pm/en/items/8635053 , https://booth.pm/en/items/8104193 , https://booth.pm/en/items/8192285
- https://www.notion.com/ja/help/selling-on-marketplace
- https://dodopayments.com/blogs/sell-ai-prompts-online
