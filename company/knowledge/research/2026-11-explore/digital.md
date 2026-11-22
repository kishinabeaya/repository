# 領域5 探索：コンテンツ・ソフトウェア・データ・API・アプリ・ツール・自動化・AIネイティブ（T-0044 / D-0030）

作成: strategist 2026-11-22 / WebSearch 38回（上限40）/ 実行（営業・出品・登録・支出）は未実施。提案のみ。

## 0. 読み方・制約
- 区分: 【事実】=出典で確認した事実（ただし下記の制約あり）、【傾向】=公開データから読み取れる傾向、【仮説】=未検証、【検証】=確かめ方。算術は【算術】。
- **取得方法の制約:** 本書の外部データはすべて **WebSearchの要約経由**。原典ページ・PDFの本文は未確認（要約文に出た数字のみ使用）。各行のURLは検索結果に出たもの。調査日はすべて 2026-11-22。事業者（プラットフォーム運営者）の自己申告は「自己申告」と明記。
- 売上・購入数が非公開のものは「不明」。SNS反応・競合の存在だけでは需要ありとしない。
- 許認可欄は確認できた範囲。弁護士の確認ではない。
- 既存調査（T-0017/0022/0031/0034）の結論は引き継いでいない。再利用したのはプロジェクト内の生データ集計のみ（company/knowledge/research/2026-11-product-ideas/raw/aggregate-output.md、TrustMRR等の収益データ。2026年取得）。

## 1. 発見の過程（どこで「お金が動いている」ことを探したか）
一覧・統計・プラットフォーム公表値から探した。思いつきではない。
| 探した場所 | 得たもの |
|---|---|
| TrustMRR（検証済み収益のあるSaaS/アプリ約2,690事業。プロジェクト内集計） | 収益分布（下記2） |
| RevenueCat State of Subscription Apps 2026、Adapty | アプリ課金の分布・日本の成長 |
| BOOTH「3Dモデルカテゴリ取引白書2026」（pixiv） | 年間取扱高104億円 |
| Shopify開発者向け収益分配ページ、Apify公式、ElevenLabs公式、Roblox経済白書、Voicy 10周年発表、pixivFANBOX 8周年、Substack統計、Mercor関連報道、入札情報サービス比較 | 各プラットフォームで実際に払われた額 |
| KDP/YouTube/Etsy/TPT/Apple/DLsite/noteの規約・報道 | 飽和・規制（下記3） |
| 既存調査 company/knowledge/research/2026-11-proven-sellers/substitution-and-ai.md（T-0023） | AI代替で需要・求人が減った領域のデータ |

## 2. 収益分布の実績（個人・少人数が実際に稼げる割合）— 結論：「上位集中。中央値は小さい」
| 市場 | 数字 | 出典・区分 |
|---|---|---|
| SaaS/アプリ（TrustMRR、検証済み、重み付き） | 直近30日収益の中央値$9、収益0が44.8%、$10,000以上は3.0%。収益が正の事業だけなら中央値$149、$10,000以上5.4% | company/knowledge/research/2026-11-product-ideas/raw/aggregate-output.md 【事実】（自己登録の標本。母集団代表ではない。1ページ目上位だけだと中央値$7,136と大きく違う＝標本の取り方で見え方が変わる） |
| サブスクアプリ | 中央50%のアプリが月収益$16〜$429。2025年に新規アプリの17%が月$1,000（MRR）超え（2024年は19%）。2020年以前のアプリが全課金売上の69%、2025年以降のアプリは3% | https://www.revenuecat.com/state-of-subscription-apps-2026/ 、9to5mac https://9to5mac.com/2026/03/04/new-report-looks-into-the-sustainability-of-the-subscription-app-market-for-2026/ 【事実】（17%は二次報道の数字） |
| Steamゲーム（2025） | 66%が収益$1,000未満、約20,000本中$100万超は約300本（Gamalytic/Alinea推定） | https://80.lv/articles/steam-earned-usd16b-in-2025-but-nearly-half-of-19-000-games-got-under-10-reviews 【傾向】（第三者推定） |
| Roblox | DevEx参加29,000超、参加者の中央値は12か月で$1,440。上位1,000の平均$110万 | https://about.roblox.com/newsroom/2025/12/how-roblox-impacts-the-global-economy 【事実】（自己申告） |
| Gumroad | 月$1,000超は5%未満、中央値月$72（推計値） | https://insightraider.com/en/data/gumroad-statistics-2026 【傾向】（公開評価数×単価からのモデル推計。公式ではない） |
| Teachers Pay Teachers | 売上の81%が上位1%（2020年研究） | https://spencergreenhalgh.com/2020-Koehler-et-al-TPT.pdf 【事実】（古い） |
| Chrome拡張 | 70.4%が利用者100人以下、中央値18人。有料転換は0.5〜3%程度の報告が多い | https://konabayev.com/blog/extension-monetization-statistics-2026/ 、https://extensionbooster.net/blog/chrome-extension-first-sale-solo-dev-revenue-guide/ 【傾向】（個人ブログ・事例。大標本なし） |
| Substack | 有料購読500万超。年$100万超のライター50人超。1,000有料購読超の媒体は10,000 | https://sacra.com/research/substack 、https://www.tubefilter.com/2025/03/12/substack-five-million-paid-subscribers-journalist-reporter-newsletter/amp/ 【傾向】（二次情報） |
| Voicy | 収益上位100人の年間売上は平均約700万円、6割超のチャンネルが「収益化」（定義不明）、累計流通総額50億円超 | https://www.oricon.co.jp/pressrelease/3003513/ 【事実】（自己申告。上位100人の平均であり一般のパーソナリティではない。中央値は不明） |

**収益が立つまでの期間:** 公開された信頼できる中央値は見つからず「不明」。TrustMRRの詳細ページ標本（18件）では「最初の収益月まで3〜12か月」の記載が複数あったが、標本が小さく代表ではない【傾向】。

## 3. AI生成による飽和・規制・ポリシー（実績データ）
| 領域 | 内容 | 出典 | 区分 |
|---|---|---|---|
| Kindle/KDP | AI生成の申告義務（2023年9月〜）、新規タイトルは1日3冊まで。2026年9月付の報道は、2023〜2026年の自費出版小説約14,000冊の約20%にAI痕跡、点数19.2倍に対し総売上8.9倍と紹介（英語圏の小説・宗教書。日本の電子書籍ではない） | https://authorsguild.org/news/amazon-adds-to-kdp-generative-ai-policy-caps-daily-self-publishing-uploads/ 、https://technews.tw/2026/09/20/ai-disrupts-publishing-industry/ | 【事実】規約／【傾向】販売分析（二次報道） |
| YouTube | 2025-07-15「繰り返し的コンテンツ」を「inauthentic content」に改称、量産・同一ナレーション等は収益化対象外。AI全面禁止ではない | https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/ | 【事実】 |
| Etsy | 2026年10月、AI生成の編み図・レシピ・設計図等の機能的な指示書を禁止。デジタルアートは申告で可。出品者の売上30〜50%減の声（掲示板中心、検証不能） | https://valueaddedresource.net/etsy-bans-ai-patterns/ （検索結果より）、https://www.digitaltrends.com/computing/etsy-sellers-are-quitting-as-ai-slop-floods-the-handmade-marketplace/ | 【事実】規約／【未検証】売上減 |
| Teachers Pay Teachers | 2026年10月、AI生成教材の禁止方針を報道（TPT自称でAI品は売上の「ごく一部」） | https://www.chalkbeat.org/2026/10/15/teachers-pay-teachers-to-ban-ai-generated-teaching-resources/ | 【事実】 |
| Apple App Store | 2026年6月、ガイドライン4.3を強化（「既に広く出回るものと区別できないアプリは不可」等）。AI製アプリそのものを名指しする条文は確認できず | https://macrumors.com/2026/06/09/app-store-guidelines-low-quality-apps/ 、https://newly.app/guides/guideline-4-3-spam-rejection | 【事実】 |
| DLsite | 2023年にAI生成作品を一時停止、2024年2月にAI生成フロア新設、1サークル月2作品等の上限（現在も同じかは未確認） | https://automaton-media.com/en/nongaming-news/20230512-18862/ | 【事実】（古い可能性） |
| note | AI記事の一律禁止規定は検索では確認できず。2025-08から学習対価還元、2026-11-18にAI回答での参照実績に応じた還元を発表 | https://www.advertimes.com/?p=564388 | 【事実】（規約本文は未確認） |
| Google検索 | Pew（米国成人900人、2025年3月）：AI要約ありでリンクのクリック率8%、なしで15%。Googleは方法論に異議 | https://9to5google.com/2025/07/23/google-ai-overview-link-click-study/ | 【傾向】 |
| Adobe Stock | 画像ポートフォリオの約47.85%が生成AI（2025年4月分析）。寄稿者の売上半減の投稿は掲示板の逸話のみ | https://community.adobe.com/questions-38/drastic-decrease-in-monthly-earnings-317425 | 【未検証】 |
| 代替の影響（既存T-0023） | フリーランス市場：ライティング求人-33%（Upwork、Bloomberry）、Chegg会員-5%・株価-99%（2021比）など。成果物を単価で受注する仕事は減少 | company/knowledge/research/2026-11-proven-sellers/substitution-and-ai.md | 【事実】（掲載数であり収入ではない） |

**読み取り（傾向）:** 「AIで大量に作れる成果物（電子書籍・テンプレ・素材・汎用アプリ）」は、プラットフォーム側が規制し、売上は上位に集中する。一方、**プラットフォームが手数料を取って払い続けている領域（Apify、Shopify、BOOTH 3D、ElevenLabs、Roblox）は、個別の個人の収益は不明でも、市場全体の支払額は増えている**。

## 4. 案（15件）
共通の注記: 「初期資金」はすべてゼロ円前提で書く。アカウント作成・本人確認・名義開示・銀行/Stripe連携は **L2（CEO承認）** で、CEO本人の作業。

### 案1. Apify Store向け「日本のWebサイト対象データ取得Actor」（従量課金・レンタル）
- **誰が・何に・なぜ:** データを継続取得したい開発者・企業・AIエージェント利用者が、サイト仕様変更に追従するスクレイパーの利用料を払う。開発者は自作・保守の手間を買う。
- **収益構造:** Apifyが売上の20%を取る（レンタル課金時）、開発者へ月次払い。単価は自分で設定。粗利は計算コストを除きほぼ全額。継続収益あり。
- **実績の根拠:** Apify自己申告で開発者への累計支払$400万超、2025年9月単月$563,000（前年の6倍）、トップ層は月$10,000超（MRR）、Store掲載8,000超 https://natlawreview.com/press-releases/apify-bets-1m-independent-developers-building-ais-missing-tools 、https://help.apify.com/en/articles/8684010-how-does-actor-monetization-work 【事実（自己申告）】。個々のActorの売上分布は**不明**。日本向けActorの需要は**未検証の仮説**。
- **初回売上までの経路と期間:** Actor公開→Store検索での利用→従量課金。期間は**不明**（根拠なし）。
- **到達性:** Apify Store内の検索・掲載が主。外部集客不要の可能性。実績ある無料の方法は掲載のみ。
- **AI代替:** 中。買い手がAIでスクレイパーを書ける。しかし対象サイトの変更追従・IP/ブロック対策・稼働保証は継続作業で、代替しにくい。**日本語サイト固有の知識**は弱い優位。
- **許認可・規制:** 対象サイトの利用規約・著作権・個人情報の取り扱いに注意（法務確認が必要）。個人情報を含むデータ取得は対象外とすべき。
- **初期資金とCEOの作業:** 0円。Apifyアカウント作成・支払受取設定（L2）。開発はBuilderが可能。
- **最大の弱点:** 個人の収益分布が非公開。トップに集中する可能性が高い（Apify自身が「最上位は月$10,000超」としか言わない）。
- **検証:** Apify Storeで日本向けの既存Actor（リスト検索）の利用数・評価・価格を調べ、需要の見える領域に1本出す。基準：公開後30日で有料実行が発生したか。

### 案2. プラットフォーム連携アプリ・プラグイン（Shopifyアプリ／kintoneプラグイン／WordPress有料テーマ・プラグイン）
- **誰が・何に・なぜ:** 既存のプラットフォームを使う事業者が、足りない機能（受注連携、帳票、通知等）を月額/買い切りで買う。すでにプラットフォームに払っている顧客に、追加で払う。
- **収益構造:** Shopify：開発者は生涯売上最初の$1,000,000まで100%保持、以降85%（2025-01-01以降分） https://shopify.dev/docs/apps/launch/distribution/revenue-share 。WordPressテーマ例：SWELLは17,600円買い切り（https://www.xserver.ne.jp/news_detail.php?view_id=10486 に掲載確認）。kintone：有料プラグインのライセンス管理方法が公式に公開 https://cybozu.dev/ja/kintone/tips/development/plugins/development-plugin/plugin-license-management/ 。
- **実績の根拠:** Shopifyは2025年に開発者へ$13億超を支払ったと自己申告（内訳不明） https://help.shopify.com/en/partners/how-to-earn 【事実（自己申告）】。kintone個人事業主がプラグイン販売を行う事例のインタビューはあるが売上額は**不明**。SWELLの累計販売数・収益も**不明**。
- **初回売上までの経路と期間:** アプリストア審査→掲載→インストール。期間は**不明**。審査に数日〜数週間かかる（推定）。
- **到達性:** 公式アプリストア内の検索が主。ゼロ予算の実績ある方法は掲載と、事業者コミュニティでの紹介。
- **AI代替:** 中〜低。AIでコードは書けるが、**プラットフォームの審査通過・API追従・サポートと保守**は継続的に必要。買い手は「動作保証された既製品」に払う。
- **許認可・規制:** 各ストアの規約。決済・個人情報を扱う場合は個人情報保護法に注意。
- **初期資金とCEOの作業:** 0円（Shopifyパートナーは無料と案内。kintoneの開発者環境は無料枠の有無を未確認）。アカウント作成・本人確認（L2）。
- **最大の弱点:** Shopifyの個人開発者の収益分布が不明。日本の中小Shopify事業者向けニッチの需要は未確認。ストアの順位競争。
- **検証:** ストアの既存アプリで日本語対応・レビュー数が少ないが課金されている機能領域を探す（レビュー数は購入数の代替にならないので、価格表示とインストール順位のみ参照）。1機能の簡易版を無料で出し、有料プランへの転換有無を見る。

### 案3. 官公需・補助金・業界公開情報の通知・検索サービス（日本の中小事業者向け・月額）
- **誰が・何に・なぜ:** 入札や補助金を探す中小事業者・個人事業主が、毎朝の新着通知・期限リマインドに月額を払う。
- **収益構造:** 実例：「入札みはり」は無料／月980円／月1,980円 https://www.aspicjapan.org/asu/article/72528 の説明で確認（検索要約）。大手有料サービスは別価格帯（不明）。継続収益あり。
- **実績の根拠:** サービスが有料プランで提供されている事実は確認。契約数・売上は**不明**。公的データ（中小企業庁の官公需情報ポータル等）を使うサービスが存在。個人運営が成立しているかは**不明**。
- **初回売上までの経路と期間:** 既存サービスが埋めていない業種・地域に絞った通知サービスを作り、事業者団体・業界掲示で案内。期間は不明。
- **到達性:** 業種別の検索（「〇〇業 入札 通知」）、商工会・業界団体。ゼロ予算の実績は未確認。
- **AI代替:** 中。公開データの要約はAIで可能。しかし**継続的な収集・網羅性・通知配信・更新**は自動化が必要で、買い手のAIでは日次運用しにくい。
- **許認可・規制:** データ利用規約（公的データの二次利用条件）。補助金の「申請代行」は行政書士法に抵触しうるため対象外。情報提供のみ。
- **初期資金とCEOの作業:** 0円（ホスティングの無料枠で開始と仮定。要確認）。決済導入（Stripe等）はL2。
- **最大の弱点:** 無料の公的サービスと既存有料サービスが多く、競合に対する差別化が難しい。契約数が不明。
- **検証:** 特定1業種（例：建設以外のニッチ）で、通知の簡易版を無料で作り、20〜30社に案内して有料意向（事前申込）を取る。基準：事前払いの申込が出るか。

### 案4. BOOTH向けVRChat・3D周辺の「ツール・ギミック・テクスチャ・スクリプト」販売
- **誰が・何に・なぜ:** VRChatユーザー・アバター制作者が、アバターの衣装・改変・ギミック（Unity用スクリプト、ツール）を買う。
- **収益構造:** BOOTHの手数料率は今回未確認（不明）。買い切り。
- **実績の根拠:** BOOTH 3Dモデルカテゴリの2025年取扱高約104億円（前年約58億円、+179%）、注文約774万件、注文者約28.1万人、最多価格帯5,000〜6,999円、年10万円以上購入者が増加 https://koubo.jp/press-release/prtimes/c35885_r460 、https://www.moguravr.com/booth-3d-2025-white-paper/ 【事実】（pixiv発表）。**販売者数・上位集中度・平均売上は不明**。
- **初回売上までの経路と期間:** 出品→BOOTH内検索・VRChatコミュニティ。期間は不明。
- **到達性:** BOOTH内ランキング／検索、VRChatコミュニティ。ゼロ予算の実績あり（プラットフォーム内検索）だが、新規は埋もれやすい（推定）。
- **AI代替:** 中。コード系ギミックはAIで作りやすく**供給が増える**。3Dモデリング自体はAIだけでは困難（推定）。コミュニティでの信用・表現（デザイン）が差別化。
- **許認可・規制:** BOOTH規約、素材の著作権・ライセンス。AI生成物のBOOTH規約は未確認。
- **初期資金とCEOの作業:** 0円。アカウント・振込設定（L2）。Unity/VRChat知識が必要で、CEOに経験がなければ立ち上げが重い。
- **最大の弱点:** 市場が大きくても個人の分配は不明。制作スキル（3D・Unity）が必要。
- **検証:** BOOTHのカテゴリで「ツール・ギミック」の人気商品の価格帯を調べ、1つの小さなUnityツールを作る前に、作者コミュニティで需要を聞く（反応数は需要の証拠にならないので、事前予約・購入意思を基準にする）。

### 案5. ニッチ法人向けマイクロSaaS（日本語・特定業務）
- **誰が・何に・なぜ:** 特定業務（帳票作成、見積、予約管理等）の小規模事業者が、業務時間の削減のために月額を払う。
- **収益構造:** 月額$9〜$49程度が多い（TrustMRR詳細標本18件の価格設定より、aggregate-output.md）。継続収益あり。
- **実績の根拠:** TrustMRR（検証済み収益）で収益が正の事業の中央値は直近30日$149、$10,000以上は5.4%（集計は上記2）【事実（標本）】。日本の個人開発SaaSでMRR100万円に達した例は、今回の検索では**見つからず（不明）**。海外例：Bannerbear（約1年無収入の後にMRR$10,000）https://gigazine.net/news/20210201-bootstrapped-saas/ 【事実】。
- **初回売上までの経路と期間:** TrustMRR標本では最初の収益まで3〜12か月の記載が複数（標本小）。
- **到達性:** 業界ごとのコミュニティ・検索。到達方法ごとの実績データは不明。
- **AI代替:** 高〜中。「AIで自作する」「汎用AIで済ませる」へ代替されやすい。差別化は**業務固有のデータ連携・法令対応・導入サポート**。
- **許認可・規制:** 業務により異なる（会計・労務・個人情報）。
- **初期資金とCEOの作業:** 0円で開始可能（無料ホスティング）。決済導入はL2。営業はCEOの対面不要でも可。
- **最大の弱点:** 収益が立つまで時間がかかる傾向。上位に収益が集中。
- **検証:** 特定業務の担当者10社に、手作業の実態をヒアリングし、プロトタイプへの事前申込（有料）を取る。基準：有料前払いの申込が出るか。

### 案6. 収益のある小規模SaaS・サイトの買収（有料案・参考）
- **誰が・何に:** 買い手が、すでに顧客と収益のあるSaaSの権利を買い、運営して利益を得る。
- **収益構造:** Acquire.comの掲載の中央値は希望価格約$19万、売上の約2〜2.4倍、利益の約3.6〜4倍（BigIdeasDB、掲載価格であり成約価格ではない）https://bigideasdb.com/state-of-saas-valuations-2026 。成約の中央値は利益の約3.9倍（同社引用）。
- **実績の根拠:** 買収市場が存在することは確認。個別の収益再現性は**不明**。
- **初回売上までの経路:** 買収後すぐ売上が入るが、購入資金が必要。
- **AI代替:** 買収先による（AIで置き換えられるSaaSは価値が下がる）。
- **初期資金:** **購入資金が必要（予算ゼロの制約により実行不可）。有料案（参考）。**
- **最大の弱点:** 資金ゼロと矛盾。**案の対象外ではなく、参考として記載**。
- **検証:** 実行しない。資金制約が解除された場合にのみ再検討。

### 案7. 日本語ニッチのモバイルアプリ（買い切り／サブスク）
- **誰が・何に・なぜ:** 特定の用途（学習、記録、管理）の個人が、広告なし・機能解放のために少額を払う。
- **収益構造:** 買い切り・サブスク・広告。App Storeの手数料（15〜30%、一般論）。
- **実績の根拠:** 上記2の分布：中央50%が月$16〜$429、1,000ドル超は新規の17%。Adaptyは「最も成長が速い市場は日本」と記載（検索要約）https://adapty.io/ja/state-of-in-app-subscriptions/ 【傾向】。日本の個人開発者の具体的月収は今回の検索では**不明**（資格過去問アプリも数字なし）。
- **初回売上までの経路と期間:** ストア審査→公開。期間は不明。
- **到達性:** ストア検索（ASO）。ゼロ予算の実績はあるが、数字は不明。
- **AI代替:** 高。AIでアプリを量産でき、Apple 4.3(b)の「区別できないアプリ」規制の対象になりうる。
- **許認可・規制:** App Store審査、個人情報、アプリ内課金規約。
- **初期資金とCEOの作業:** **Apple Developer Programは年額の有料（金額は今回未確認）で、予算ゼロの制約と衝突。有料案（参考）。** Google Playは登録料がかかる（金額未確認）。
- **最大の弱点:** 年額費用、審査、飽和。個人の中央値は小さい。
- **検証:** 実行しない（費用）。Webアプリで先に需要を測る方が低コスト。

### 案8. 専門資格者によるAI学習用の専門評価・データ作成ワーク（Mercor等）
- **誰が・何に・なぜ:** AI開発企業が、専門家の判断（法律・医療・金融・開発）を学習・評価に使うため、時間単価で支払う。
- **収益構造:** 掲載レート：医師$115〜150/時、弁護士$100〜150/時、投資銀行$100〜130/時、ソフトウェア$70〜150/時（Second Talent集計。2026年10月）https://www.secondtalent.com/resources/domain-expert-ai-trainer-rates/ 。Mercorの平均は$97〜110（記事により異なる）。**時間給であり、継続収益ではない**。
- **実績の根拠:** Mercorで約30,000人が時給で報酬を得ている（二次報道） https://advisorperspectives.com/articles/2026/02/03/some-ai-gig-workers-1-000-hour-can-last 【事実（報道）】。「案件が最近減った」という不満の報告もあり、**継続性は不明**。日本語の専門家需要は**不明**。
- **初回売上までの経路と期間:** 応募→審査→案件。期間は不明。
- **到達性:** プラットフォームへの応募。
- **AI代替:** （この事業は「AI学習用」なので、代替の逆）。専門資格・責任の所在が必要で、AI単独では置き換わらない部分。ただし、**いずれAIが専門家の作業を置き換える意図**があるとの指摘（fourweekmba）。
- **許認可・規制:** 資格の保有が前提。守秘義務・利益相反に注意。
- **初期資金とCEOの作業:** 0円。**CEO（または資格者本人）の資格・本人確認・作業時間が必要（AI社員では不可）。**
- **最大の弱点:** 労働集約。資格が前提。誤分類訴訟（プラットフォームへの）などリスク。事業ではなく**個人の副業**に近い。
- **検証:** CEOが保有資格・専門性を持つ場合のみ。持たない場合は対象外。応募1件で審査通過の有無を見る。

### 案9. 自分の声のProfessional Voice Clone をElevenLabs Voice Libraryに登録（利用ごとの報酬）
- **誰が・何に・なぜ:** 動画・ナレーション制作者がAI音声の利用料を払い、声の提供者に報酬が分配される。
- **収益構造:** 報酬は利用量に比例（レートは今回未確認）。Stripe Connectで払い出し。
- **実績の根拠:** ElevenLabs自己申告で、ボイス提供者の累計報酬$2,200万（2025年11月時点$1,100万から約6か月で倍増）、報酬を得ている提供者は10,400人超 https://elevenlabs.io/blog/22-million-earned-by-voice-creators-on-elevenlabs 【事実（自己申告）】。【算術】$22M÷10,400≒約$2,100/人（累計・平均。分布は上位集中の可能性が高く、中央値は不明）。**日本語の声の需要は不明**。
- **初回売上までの経路と期間:** 声の登録・審査→ライブラリで利用。期間は不明。
- **到達性:** プラットフォーム内検索。
- **AI代替:** 該当せず（AIに声を売る事業）。ただし他のAI声との競合は増える。
- **許認可・規制:** 声は本人のもの。本人の同意・肖像/声の権利。
- **初期資金とCEOの作業:** 0円。**CEO（または声を提供する人）の声・本人確認・同意が必要。**
- **最大の弱点:** 声の提供者本人が必要。個人の収益は不明で、$2,100は平均にすぎない。
- **検証:** 声の提供者がいる場合のみ。日本語ライブラリの既存ボイスの数・種類を調べ、空きがあるかを確認。

### 案10. 音声配信プレミアム（Voicy等）
- **誰が・何に・なぜ:** リスナーが、専門家・著名人の話を聴くために月額を払う。
- **収益構造:** プレミアムリスナー（月額）、有料放送、ライブの差し入れ（2026-07〜）。
- **実績の根拠:** 上位100人の年間売上平均約700万円、6割超のチャンネルが収益化（定義不明）、累計流通総額50億円超（自己申告） https://www.oricon.co.jp/pressrelease/3003513/ 。中央値・下位の収益は**不明**。
- **初回売上までの経路と期間:** 既存オーディエンスがないと難しい（推定）。期間は不明。
- **到達性:** 既存フォロワー・プラットフォーム内。ゼロから集める実績は**不明**。
- **AI代替:** 低（本人の声・体験・人柄）。ただし**本人が必要**。
- **許認可・規制:** プラットフォームの審査（未確認）。
- **初期資金とCEOの作業:** 0円。**CEO本人の声・顔出し/名義が必要。**
- **最大の弱点:** オーディエンスなしでは収益が立たない。AI社員では代替できない。
- **検証:** 既存フォロワーを持つ専門家との提携の可能性を探る（案としては、他者との提携が前提）。

### 案11. pixivFANBOX／note メンバーシップ（既存の専門性・オーディエンス前提）
- **誰が・何に・なぜ:** ファンが、クリエイターの継続的な作品・知見への支援として月額を払う。
- **収益構造:** FANBOX：支援額の10%がpixiv（一般向け。成人向けは2025-09-01から12.9%との記載）。noteメンバーシップ：手数料は今回未確認。
- **実績の根拠:** FANBOX：ユーザー1,500万、登録クリエイター30万、過去1年で140万人が初めて支援（2026年4月発表の8周年データ。https://koubo.jp/article/74736 、検索要約経由）【事実（自己申告）】。note：メンバーシップで売上が発生したクリエイター数が前年同月比100.5%（2025年11月）、売れている有料記事（各分類上位20%）の実用ノウハウ平均価格1,842円 https://hashout.jp/?p=14330 【傾向（二次報道）】。**クリエイター別の収益分布は不明**。
- **初回売上までの経路と期間:** 既存オーディエンスの有無で大きく変わる。期間は不明。
- **到達性:** 既存SNS・ブログ。ゼロからの実績は不明。
- **AI代替:** 汎用情報は高。**本人の体験・一次データ・創作物は低〜中**。
- **許認可・規制:** プラットフォーム規約。特定の内容（医療・投資助言等）は規制。
- **初期資金とCEOの作業:** 0円。アカウント・名義（L2）。
- **最大の弱点:** オーディエンスがなければ売上が立たない。収益は上位に集中。
- **検証:** 既存オーディエンスがある第三者（専門家）と共同で、有料会員の事前申込を取る。

### 案12. 専門家監修の「業務ドリル・テンプレート」（人が作ったと明示、特定資格・特定業務）
- **誰が・何に・なぜ:** 教師・実務担当者が、準備時間を減らすために教材・書式を買う（TPT、BOOTH、Gumroad）。
- **収益構造:** 買い切り。Gumroadの上位商品の価格中央値は$33.75（教育カテゴリは$99、いずれも上位36件の標本）（aggregate-output.md）。
- **実績の根拠:** TPTでは売上の81%が上位1%に集中（2020年）。Gumroadは月$1,000超が5%未満（推計）。個人が継続的に稼ぐ割合は**小さい**【傾向】。日本の教材販売の実績は今回の検索では**不明**。
- **初回売上までの経路と期間:** 出品→プラットフォーム検索。期間は不明。
- **到達性:** プラットフォーム内検索、実務コミュニティ。
- **AI代替:** **高**。買い手がAIで同じ物を作れる。TPT・Etsyが2026年10月にAI生成物を禁止・制限（上記3）。差別化は**資格者・実務者の監修と実体験**のみ。
- **許認可・規制:** 各プラットフォームのAI規約、著作権。
- **初期資金とCEOの作業:** 0円。専門家の確保が必要（外部）。
- **最大の弱点:** AI代替の影響が最も大きい。上位集中。**単独では推奨しない**。
- **検証:** 実行しない。専門家と組む場合のみ、特定資格1つで先行販売の可否を確認。

### 案13. 一次情報型の有料ニュースレター（業界特化）
- **誰が・何に・なぜ:** 業界の実務者・投資家が、公開情報にない一次情報・分析・更新に月額を払う。
- **収益構造:** Substackは手数料10%＋Stripe手数料。平均価格は月$10／年$96（Sacra）。
- **実績の根拠:** Substack有料購読500万超、年$100万超50人超、1,000有料購読超の媒体10,000（海外、二次情報）。**日本の個人運営の業界特化ニュースレターの購読者数・月額の実績は今回の検索で見つからず（不明）**。
- **初回売上までの経路と期間:** 既存オーディエンスがないと難しい（推定）。期間は不明。
- **到達性:** 既存SNS・業界コミュニティ。ゼロからの実績は不明。
- **AI代替:** 汎用情報は高。**独自の取材・非公開データ・専門家の分析は低〜中**。
- **許認可・規制:** 投資助言・医療情報等は規制に注意。
- **初期資金とCEOの作業:** 0円。アカウント・名義（L2）。取材に人が必要。
- **最大の弱点:** オーディエンスと一次情報の入手がなければ成立しない。日本の実績が不明。
- **検証:** 一次情報源（データ・専門家）を持つパートナーがいるか確認。いなければ見送り。

### 案14. Roblox／Steam／itch.ioのゲーム（個人・少人数）
- **誰が・何に・なぜ:** プレイヤーが、ゲーム内アイテム・買い切りに払う。
- **収益構造:** Robloxは開発者の収益化（DevEx）、Steamは非Valve作品の平均取り分が24%との報告（https://gamesmarket.global/average-cut-for-all-non-valve-games-sold-on-steam-in-2025-was-24/ ）。
- **実績の根拠:** 上記2：Steam 66%が$1,000未満、Roblox DevEx参加者の中央値は12か月で$1,440、上位1,000の平均$110万。日本のDevEx対象クリエイターの割合は2022Q4〜2025Q4で415%増（人数は不明）https://about.roblox.com/newsroom/2025/12/how-roblox-impacts-the-global-economy 【事実】。
- **初回売上までの経路と期間:** 不明（長期化の傾向）。
- **到達性:** プラットフォーム内のおすすめ・SNS。ゼロ予算での再現性は低い。
- **AI代替:** 中。AIで制作は速くなるが、供給が増えて競争が激しくなる。
- **許認可・規制:** ストア規約、年齢制限、AI開示（Steam）。
- **初期資金とCEOの作業:** Steamは掲載料がかかる（金額は今回未確認。有料案の扱い）。Robloxは無料。
- **最大の弱点:** 収益が上位に極端に集中。個人の中央値は小さい。
- **検証:** 実行しない（上記データで中央値が小さい）。ゲームは優先度を下げる。

### 案15. note／ブログ等への「AI学習・参照の対価還元」を活用した既存コンテンツの収益化（補助的）
- **誰が・何に:** AI事業者が学習・参照への対価を払う。noteは2025-08開始、2026-11-18に参照実績ベースの還元を発表（2026年4〜7月の参照が対象、支払いは12月中旬予定）。
- **実績の根拠:** 還元額・対象人数は**不明**。独立した事業にはならない。
- **AI代替:** 該当せず。
- **最大の弱点:** 金額が不明。**単独の事業案としては弱い。既存コンテンツがある場合の補助収益のみ**。
- **検証:** 実行しない。参考として記載。

## 5. 実績の根拠が最も強い上位（領域内の比較）
根拠の強さ＝公開された支払額・取扱高の確かさ。個人が稼げるかは別（下の弱点を参照）。
1. **案1 Apify Actor**：月次の支払額と上位水準が公表（自己申告）。個人の分布は不明。
2. **案2 プラットフォーム連携（Shopify等）**：支払総額$13億、100%保持条件が公式。個人の収益は不明。
3. **案4 BOOTH 3D周辺**：取扱高104億円、注文774万件が発表。販売者分布は不明。
4. **案9 ElevenLabs Voice Library**：累計$2,200万・10,400人。声の提供者本人が必要。
5. **案8 専門家のAI学習ワーク**：時給の掲載レートが具体的。資格者本人が必要で、継続性は不明。
（Voicy・FANBOX・Substackも支払実績は強いが、既存オーディエンスと本人の関与が前提。）

## 6. 却下リスト（案にしなかったもの）
| 項目 | 理由 |
|---|---|
| Kindle電子書籍の量産（AI生成） | KDPの1日3冊制限・AI申告、AI由来の増加で点数は19.2倍、売上は8.9倍（英語圏小説）。需要の実績が量産型に不利。日本の実績データは見つからず |
| YouTube量産動画 | 2025-07の「inauthentic content」ポリシーで収益化対象外になりうる |
| Etsy／TPTのAI生成テンプレ・パターン・教材 | 2026年10月に禁止・制限。買い手もAIで代替可能 |
| 汎用AIアプリ・ラッパーアプリの量産 | Apple 4.3(b)強化、TrustMRRで中央値は小さい。代替されやすい |
| MCPサーバーの販売 | 「95%以上が収益ゼロ」は販売業者のブログの主張で監査なし。ChatGPTアプリ内ではデジタル商品の販売が不可（2025-12時点） |
| GPTs（GPT Store）の収益化 | 公式の収益データなし。逸話のみ（$10,000事例は販売者の事例記事） |
| 自動化テンプレ（n8n/Make/Zapier）の単体販売 | コミュニティでは「テンプレ単体はあまり売れず、設定代行付きが売れる」との逸話のみ。数字なし。代行は領域2へ |
| LINEスタンプ | 2014年の上位実績のみ。AI規約・最新の収益分布は確認できず |
| Chrome拡張の有料化（単体） | 70.4%が利用者100人以下、有料転換0.5〜3%は個人ブログの報告のみ、Google側の決済機能は終了と報告。AIで量産でき飽和しやすい。案5（SaaS）に含めて検討 |
| 資格過去問アプリ | 収益の数字が見つからず。需要は季節的との開発者の記述のみ |
| 画像ストック素材（Adobe Stock） | AI供給が約半数。売上減は掲示板の逸話のみで未検証 |
| DLsite等の同人（AI生成） | AI作品は専用フロア・月2作品等の制限。成人向けを含む領域で、規制・倫理の確認が必要 |
| 個人情報を含むデータの販売・名簿売買 | 個人情報保護法・倫理の観点で対象外 |
| 日本の個人SaaS「MRR100万円」事例 | 今回の検索で日本語の実例が見つからず（不明）。案5で扱うが実績としては使わない |

## 7. 領域5の総括（傾向）と不明点
- **AIで大量に作れる成果物は、規制され、上位集中で、個人の中央値は小さい（案7, 12, 14と却下リスト）。**
- **プラットフォームが支払い続けている領域は存在する（案1, 2, 4, 9）が、個人の分布は非公開で、日本向けの需要は未検証。**
- **AIで代替しにくい要素（本人の声・資格・既存オーディエンス・保守の継続）は、「本人（CEO）の関与」を要する案（8, 9, 10, 11, 13）に集中する。AI社員だけで完結する案は、代替されやすい。**
- 不明点：（a）Apify・Shopify・BOOTHの個人別の収益分布と、初回売上までの期間（b）日本語・日本市場でのApify Actor・kintoneプラグインの需要（c）BOOTH手数料率・販売者数・AI生成物規約（d）CEOの保有する専門資格・声・既存オーディエンス（案8〜11, 13の成否を決める）（e）原典ページでの再確認（本書は検索要約経由）。
- CEOへの確認事項：案8〜11・13は、CEO本人の資格・声・オーディエンスの有無で成否が決まる。有無を教えてほしい（有／無／不明）。

## 8. 出典URL一覧（調査日はすべて 2026-11-22）
- https://authorsguild.org/news/amazon-adds-to-kdp-generative-ai-policy-caps-daily-self-publishing-uploads/
- https://technews.tw/2026/09/20/ai-disrupts-publishing-industry/
- https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/
- https://www.revenuecat.com/state-of-subscription-apps-2026/
- https://9to5mac.com/2026/03/04/new-report-looks-into-the-sustainability-of-the-subscription-app-market-for-2026/
- https://adapty.io/ja/state-of-in-app-subscriptions/
- https://macrumors.com/2026/06/09/app-store-guidelines-low-quality-apps/
- https://newly.app/guides/guideline-4-3-spam-rejection
- https://natlawreview.com/press-releases/apify-bets-1m-independent-developers-building-ais-missing-tools
- https://help.apify.com/en/articles/8684010-how-does-actor-monetization-work
- https://shopify.dev/docs/apps/launch/distribution/revenue-share
- https://help.shopify.com/en/partners/how-to-earn
- https://cybozu.dev/ja/kintone/tips/development/plugins/development-plugin/plugin-license-management/
- https://www.xserver.ne.jp/news_detail.php?view_id=10486
- https://www.aspicjapan.org/asu/article/72528
- https://koubo.jp/press-release/prtimes/c35885_r460
- https://www.moguravr.com/booth-3d-2025-white-paper/
- https://bigideasdb.com/state-of-saas-valuations-2026
- https://gigazine.net/news/20210201-bootstrapped-saas/
- https://www.secondtalent.com/resources/domain-expert-ai-trainer-rates/
- https://advisorperspectives.com/articles/2026/02/03/some-ai-gig-workers-1-000-hour-can-last
- https://elevenlabs.io/blog/22-million-earned-by-voice-creators-on-elevenlabs
- https://www.oricon.co.jp/pressrelease/3003513/
- https://koubo.jp/article/74736
- https://hashout.jp/?p=14330
- https://www.advertimes.com/?p=564388
- https://sacra.com/research/substack
- https://www.tubefilter.com/2025/03/12/substack-five-million-paid-subscribers-journalist-reporter-newsletter/amp/
- https://80.lv/articles/steam-earned-usd16b-in-2025-but-nearly-half-of-19-000-games-got-under-10-reviews
- https://about.roblox.com/newsroom/2025/12/how-roblox-impacts-the-global-economy
- https://insightraider.com/en/data/gumroad-statistics-2026
- https://www.chalkbeat.org/2026/10/15/teachers-pay-teachers-to-ban-ai-generated-teaching-resources/
- https://spencergreenhalgh.com/2020-Koehler-et-al-TPT.pdf
- https://www.digitaltrends.com/computing/etsy-sellers-are-quitting-as-ai-slop-floods-the-handmade-marketplace/
- https://valueaddedresource.net/etsy-bans-ai-patterns/
- https://konabayev.com/blog/extension-monetization-statistics-2026/
- https://extensionbooster.net/blog/chrome-extension-first-sale-solo-dev-revenue-guide/
- https://9to5google.com/2025/07/23/google-ai-overview-link-click-study/
- https://community.adobe.com/questions-38/drastic-decrease-in-monthly-earnings-317425
- https://automaton-media.com/en/nongaming-news/20230512-18862/
- https://www.fiverr.com/news/fiverr-q4-earnings-2025 （T-0023経由）
