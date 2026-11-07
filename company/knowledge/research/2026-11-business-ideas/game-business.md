# ゲーム事業の実態調査（T-0017 / D-0016）

- 作成: strategist / 2026-11-07。依頼: D-0016（ゲームアプリを事業として評価）。
- 性格: **評価材料の整理であり、結論（やる／やらない）は出さない。** 売上見通しは載せない（D-0009）。類似事業の実績の範囲だけを示す。
- 調べ方の制約（重要）: Web検索45回。**一次資料のページ取得（WebFetch）は、この環境のネットワーク制限で全て失敗した**（kokusen.go.jp、pocketgamer.biz、gameworldobserver.com）。よって**本書の数値は、すべて「検索結果の要約経由」**であり、一次資料を直接読んではいない。各行の出典URLは、要約が依拠した記事のURL。数値を意思決定に使う前に、一次資料での確認が要る。
- 凡例: 【調査】調査会社・研究者の数値／【公的】公的機関／【自己申告】会社・開発者の公表値／【推定】第三者サイトの推計（手法不明または粗い）／【要約】検索要約経由。
- 法令・規約の記述は**弁護士の確認ではない**。CEOが公式情報で確認する（service-principles.md の方針）。

---

## 0. 要点（CEOが判断するための事実整理）

1. **市場は大きいが、成長は鈍く、新規参入者の取り分は極端に少ない。** 2025年の世界ゲーム市場は約2,016億ドル（Newzoo、要約）。一方、2025年に公開された約19万本のモバイルゲームのうち、50万DL超は約2,500本（約1.3%、Moloco、要約）。
2. **「衝動型」は収益への寄与が大きいことがデータにある。** 同時に、害（未成年の課金トラブル、問題ギャンブルとの相関、規制当局の制裁）のデータもある。収益の上位集中（ホエール）は複数の調査で確認できる（2.1節）。
3. **「価値型」で成立した実例はある。** ただし、実例の多くは**買い切り（PC）か、大規模なコスメ課金**であり、ヒットした少数の例である（3章）。個人開発の成功率は低い（4章）。
4. **予算ゼロでできるのは、ウェブゲームの制作・公開・検証まで。** アプリストア公開は、Apple年99ドル（有料）、Google 25ドル（有料）が必要で、D-0002とぶつかる（6章）。
5. **AIでの開発は、ウェブゲーム（HTML5）やテキスト・パズル系なら現実的。** アセットは、無料のCC0素材を使えば著作権の論点を小さくできる。AI生成物には、米国・日本とも「プロンプトだけでは著作物になりにくい」という見解がある（5章）。
6. **提供原則（特に3・4・5）との関係:** ガチャ型・損失回避型・連続記録型の設計は、原則に反する（2.3節）。原則を維持する場合、使える収益設計は「価値型」に限られる。

---

## 1. 市場（日本と世界）

### 1.1 市場規模と成長

| 指標 | 数値 | 区分・出典 |
|---|---|---|
| 世界ゲーム市場 2025年 | 約2,016億ドル。モバイル1,133億ドル（+10.7%）、PC 436億ドル（+12%）、コンソール447億ドル（+2.8%）。Newzooの発表は9月予測1,888億→12月予測約1,970億→確定2,016億と改定されている | 【調査】Newzoo。【要約】https://www.pocketgamer.biz/global-games-revenue-surpasses-200bn-for-the-first-time-mobile-generates-113bn/ ／ https://gameworldobserver.com/2025/09/09/newzoo-in-2025-more-than-half-of-the-gaming-markets-revenue-will-come-from-two-countries-china-and-the-united-states |
| モバイルゲームのアプリ内課金（iOS+Google Play） | 2025年 約817.5億ドル（+1.3%）。ダウンロード約504億（-7.2%）。**非ゲームアプリの消費（855億ドル、+21%）が初めてゲームを上回った** | 【調査】Sensor Tower。【要約】https://gameworldobserver.com/2026/01/21/in-2025-the-revenue-of-the-mobile-gaming-market-grew-but-only-slightly-analysis ／ https://www.techspot.com/news/111010-global-app-spending-overtakes-mobile-games-first-time.html |
| 2024年（比較） | モバイルゲームIAP 約809億ドル（+4%）、DL 496億（-6%）。ジャンル別: ストラテジー175億、RPG168億ドル | 【調査】Sensor Tower。【要約】https://gamesbeat.com/?p=241428 |
| 日本のゲームコンテンツ市場 | 2024年 2兆3,961億円（+3.4%）。2025年は約2.5兆円に拡大（「ファミ通ゲーム白書2026」）。世界市場（同白書の換算）は2025年32.1兆円 | 【調査】KADOKAWA Game Linkage（ファミ通）。【要約】https://gamebiz.jp/news/410304 ／ https://gamebiz.jp/news/430671 |
| 世界モバイル市場（同白書） | 2024年12兆4,103億円、2025年12兆6,001億円（+1.4%） | 【調査】【要約】https://gamebiz.jp/news/422906 |

読み取り（事実の範囲）: モバイルのIAP市場は2025年にほぼ横ばい（+1.3%）で、DLは減少。成長はPC・コンソールとハイブリッド型（広告+課金）にある、という報道がある（Sensor Tower 2024年: 広告併用ゲームのIAPが+37%。【要約】https://dailyastorian.com/?p=16122）。国内モバイルだけの金額は、今回の検索では取得できなかった（未取得）。

### 1.2 ジャンル別の収益構造（取得できた範囲）

- 売上の大きいジャンル（世界モバイル、2024年）: ストラテジー175億ドル、RPG168億ドル（上記Sensor Tower）。いずれも**ガチャ・長期課金・ホエール依存度が高い領域**とされるが、ジャンル別の「ホエール比率」の一次データは未取得（未検証）。
- カジュアル・ハイパーカジュアル: 広告収益が中心。IAPの課金率は、全サブジャンルで1%未満、課金者1人あたりの売上は18〜42ドル（GameAnalytics系ベンチマークの要約。年・条件不明）。【要約】https://salestechstar.com/mobile-field-sales-enablement/iap-in-casual-games-declines-by-15-20-with-strategy-and-rpg-games-accounting-for-the-majority-of-non-ad-based-revenue-according-to-the-latest-gameanalytics-benchmark-report/4/ 。純広告型はLTVが低く、広告+課金の「ハイブリッド」が伸びている、という指摘（Mobile Casual Benchmarks Report 2025、Android・米国のみ。【要約】https://files.gameindustrylibrary.com/documents/mobile-casual-benchmarks-report-2025.pdf ）。
- 診断・占い・性格系アプリ: 7章で別に整理。
- ノベル・テキスト系、育成系、放置系、ウェブゲーム: **ジャンル別の収益統計は、今回の検索では取得できなかった（未取得）。** ウェブゲームは、ポータル（Poki、CrazyGames）の広告収益分配が主な収益経路。分配率は、Poki「自分で呼んだ流入は100%、Pokiの流入は50/50」、CrazyGames「成績により50〜70%（資料により55%上限とも）」という低品質ソースの要約のみで、CPMや個別ゲームの収益は取得できなかった（【推定】【要約】https://app.cinevva.com/guides/publish-game-poki ／ https://abratabia.com/publishing-web-games/where-to-publish.php ）。

---

## 2. 課金設計: 効果と害（中立に並べる）

### 2.1 衝動型（ガチャ・ルートボックス・損失回避・連続記録）の収益への寄与

| 項目 | データ | 区分・出典 |
|---|---|---|
| 課金する人の割合 | F2Pゲームで課金するプレイヤーは約1〜2%（Playnomics 2013年Q1 0.77%、Swrve 2013年 月間1.5%）。古いデータ | 【調査】【要約】https://gamesbeat.com/only-0-15-of-mobile-gamers-account-for-50-percent-of-all-in-game-revenue-exclusive/ 他 |
| ホエールの収益比率 | Slice Intelligence（2015年、米国パネル）: 上位1%の課金者がF2Pモバイルゲーム売上の58%。Playnomics: 上位1%が33%。Swrve: プレイヤーの約0.15%がIAP売上の50%。GameAnalytics（2016年）: 32ドル超の課金者が売上の86.6%（広告含む）。**定義・年が異なり、直接比較できない** | 【調査】【要約】https://gameanalytics.com/?p=4410 ／ https://gamesbeat.com/only-0-15-of-mobile-gamers-account-for-50-percent-of-all-in-game-revenue-exclusive/ |
| ホエールの比率は時間とともに上昇 | Moloco（2025年、55本のモバイルゲーム分析）: ローンチ後10か月で、広い層向けゲームのIAP売上に占めるホエールの比率は41.4%→54.4%、ホエール向けゲームでは53.4%→81.2% | 【調査】Moloco。【要約】（同上の検索結果。一次未確認） |
| ルートボックスの収益構造 | Close et al.（2021、6データセット・購入者約7,700人の二次分析）: 課金額の上位5%（月100ドル超）がルートボックス売上の半分。その上位層の約3分の1は問題ギャンブル水準と報道（自己申告のアンケート） | 【調査】https://pubmed.ncbi.nlm.nih.gov/33578105/ ／ https://nichegamer.com/uk-study-concludes-5-of-lootbox-buyers-make-up-50-of-revenue-1-3-of-them-problem-gamblers |
| 規模感 | Genshin Impact（ガチャ型）: 生涯の課金額が2025年末に約100億ドル（第三者サイトがSensor Tower・AppMagicを引用。要確認）。ただしモバイルの2025年売上は約3.2〜3.35億ドルと、資料により差があり、減少傾向 | 【推定】【要約】https://www.shanethegamer.com/research/genshin-impact-revenue-statistics/ ／ https://wnhub.io/news/finance/item-45753 |
| 日本の課金行動（参考） | ゲームテスター1,612名の調査で、スマホゲーム課金経験86.8%、直近3か月64.7%（**対象がデバッガーで一般より課金層に偏る可能性**）。2021年アスマーク調査: 有職者20〜50代の課金経験は約4割、課金者の34.8%は平均500円未満。**日本での「上位◯%が売上の◯%」は取得できず** | 【調査】【要約】https://iphone-mania.jp/news-394718/ ／ https://webtan.impress.co.jp/n/2021/09/17/41626 |

### 2.2 害のデータ

| 項目 | データ | 区分・出典 |
|---|---|---|
| ゲーム障害の有病率 | メタ分析（Stevens et al. 2021、53研究・226,247人・17か国）: 世界で3.05%（訂正後2.96%）。厳格な標本条件では1.96%。測定ツールの影響が大きく、方法論で過大になりうると著者が指摘。男女比約2.5:1。別のメタ分析（Kim et al.）は3.3%（代表標本のみで2.4%）。**課金設計との因果は示していない** | 【調査】https://pubmed.ncbi.nlm.nih.gov/33028074/ ほか【要約】 |
| WHOの定義 | ICD-11 6C51: 制御の障害・ゲームの優先度上昇・悪影響があっても継続、通常12か月以上 | 【公的】（mechanism-structure.md に記載済。転載サイト経由の要約） |
| ルートボックスと問題ギャンブル | Spicer et al.（2022、系統的レビュー）: 13論文中12で正の関連、平均r=.27。**因果の方向は不明**。Zendle & Cairns（2019、7,422人）: 問題ギャンブルが重いほどルートボックス課金が多い。青少年ではその関連が成人の2倍超（同著者の別研究）。相関であり因果ではないと著者が明記 | 【調査】https://pureportal.bcu.ac.uk/en/publications/loot-boxes-problem-gambling-and-problem-video-gaming-a-systematic/ ／ https://eprints.whiterose.ac.uk/143229 |
| 日本の未成年の課金トラブル | 国民生活センター: 小中高生のオンラインゲーム相談は2022年度4,024件、契約購入金額の平均約33万円（2024年3月公表）。2025年3月5日公表の現況調査: インターネットゲームの相談は2018年度以降増加し、**20歳未満が相談者の過半数**。2020年度の子ども関連は3,723件（前年度比+45.6%、小学生約半数）という報道もある。**2024年度の件数は未取得。一次資料は未読（要約経由）** | 【公的】【要約】https://www.kokusen.go.jp/news/data/n-20240313_1.html ／ https://www.kokusen.go.jp/news/data/n-20250305_1.html ／ https://gamebiz.jp/news/331307 |
| 海外の制裁事例 | 米FTC: Genshin Impactの運営Cognosphereが、未成年向けルートボックスの不当なマーケティング（実コストの不明瞭化、確率の誤認）とCOPPA違反の申立てに対し、2,000万ドルで和解（2025年1月発表）。16歳未満は保護者の同意なしに課金できないようにし、ルートボックスを仮想通貨経由だけで売らない措置。会社は「申立ての多くは不正確」と述べ、責任は認めていない | 【公的】https://www.pcgamer.com/games/rpg/ftc-says-genshin-impact-deceived-children-and-orders-its-publisher-to-pay-a-usd20-million-fine-and-stop-selling-loot-boxes-to-kids ／ https://www.videogameschronicle.com/news/genshin-impact-maker-fined-20m-over-deceptive-loot-boxes-and-child-privacy-violation |
| ゲーム時間とウェルビーイング | Vuorre et al.（2022、約3.8〜3.9万人、ゲーム会社のプレイログ+調査）: プレイ時間がウェルビーイングに与える因果的影響は、ほぼない〜非常に小さい。**内発的動機はウェルビーイングと正の関連、外発的動機は負の関連**（7ゲームのみ） | 【調査】https://research.tilburguniversity.edu/en/publications/time-spent-playing-video-games-is-unlikely-to-impact-well-being/ |
| 課金の動機 | Hamari（2015）: ゲームの楽しさは購入意向を下げ、継続意向を上げる（mechanism-structure.md 記載済） | 【調査】https://ideas.repec.org/a/eee/ininma/v35y2015i3p299-308.html |

### 2.3 提供原則（5項目、D-0015）との関係（事実の整理。結論は出さない）

| 設計 | 原則との関係（事実） |
|---|---|
| ガチャ・ルートボックス（ランダム性による課金） | 原則5「ランダム性による課金（くじ・ガチャ型）は行わない」に**明示的に該当**。採用するにはCEOが原則を改める必要がある（D-0016 CoS注記）。 |
| 損失回避の演出（期間限定、残り時間、「今だけ」） | 原則3「『今すぐ』『あなただけ』などの煽りは使わない」に該当しうる。 |
| 終わりのない連続記録（ログインボーナス・ストリーク） | 原則4「続ける理由を価値にする。やめやすくする。不安が戻ることを前提にした設計にはしない」と緊張関係。ストリークが離脱の不安を使う設計かは、個別の設計次第（データでの効果比較は未取得）。 |
| ランキング・比較による競争 | 原則3・顧客像（比較による劣等感を抱えやすい層）との関係は設計次第。比較を使わず、自己ベスト・協力型にする選択肢がある（mechanism-structure.md）。 |
| 上位課金者への依存（ホエール構造） | 原則5「価格を、その人の弱さに連動させない」との関係: 上位5%の約3分の1が問題ギャンブル水準という調査（自己申告アンケート）は、**高額課金層に弱い状態の人が一定数含まれうる**ことを示唆する（因果は未確定）。ホエール依存の収益設計は、確認基準「仕組みを全部知ったうえで、その人は、それでも選ぶか」を満たしにくい、という論点がある。 |
| 事実としての両面 | 衝動型は収益が大きい（2.1）。同時に、規制・制裁・未成年トラブルのリスクが実在する（2.2、8章）。**どちらを取るかはCEOの価値判断**であり、本書は決めない。 |

---

## 3. 価値型（見た目・表現・応援・時短・買い切り・バトルパス）の収益実績

| 事例 | 設計 | 収益・規模のデータ | 開発体制 | 区分・出典 |
|---|---|---|---|---|
| Stardew Valley | 買い切り（価格は今回未確認） | 累計4,100万本超（2024年12月）。PC約2,600万、Switch約790万。2024年だけで約1,000万本 | 当初は1人（Eric Barone）。現在は小規模チーム | 【自己申告】公式プレスサイト。【要約】https://gamedeveloper.com/business/stardew-valley-sales-grew-to-over-41-million-by-2024-s-end ／ https://www.gamesradar.com/games/simulation/cozy-farming-sim-stardew-valley-has-sold-over-41-million-copies-as-of-right-now-with-over-half-on-pc-and-almost-8-million-on-the-switch 。**開発期間（約4.5年とされる）は今回の検索で未確認** |
| Vampire Survivors | 買い切り（Steam定価4.99ドル、推計サイトの表記）+ DLC。モバイルは無料+広告/IAP | プレイヤー2,700万人超（自己申告、無料・モバイル含む）。Steamの販売本数は推計で約500万〜1,360万本、粗収益は約2,000万〜5,000万ドル超と**推計の幅が大きい**（Boxleiter法等） | 2020年に開発開始、失業中の個人（Luca Galante、Phaser使用）。友人が余暇に協力。2022年3月にフリーランスを雇用。現在は複数スタジオ | 【自己申告】+【推定】https://en.wikipedia.org/wiki/Vampire_Survivors ／ https://steampulse.org/game/1794680 ／ https://www.steampageanalyzer.com/games/1794680 。創業者自身が「成功は運」と述べる記事あり https://gamesradar.com/games/roguelike/vampire-survivors-creator-admits-his-success-was-lucky-amid-a-wave-of-cheap-mobile-knock-offs-for-everyone-else-they-have-to-stand-out-among-the-hundreds |
| Wordle | 無料、広告なし、課金なし。NYTが買収 | 2022年1月末〜2月、NYTが「低い7桁（ドル）」で買収（金額は非公表）。2021年10月公開、2か月後で30万人、買収時は数百万人/日 | 個人（Josh Wardle）。パートナーのために作成 | 【調査/報道】https://www.newshub.co.nz/home/technology/2022/02/new-york-times-buys-wordle-for-low-seven-figures.html ／ https://www.trustedreviews.com/news/wordle-sold-to-new-york-times-but-will-stay-free-to-play-4206192 。「数週間で作った」は未確認 |
| Among Us | PC 5ドル買い切り、モバイルは無料+広告+コスメ課金 | 公式の売上は非公表。App Annieの推計: 約3年でモバイル消費8,600万ドル（ピーク月2020年10月2,450万ドル）。SuperData: 2020年9月だけで3,900万ドル。第三者の通年推計は5,000万〜8,600万ドル（信頼度低） | ローンチ時は小規模（3人とする資料と13人超とする資料があり**不一致**） | 【推定】https://expertbeacon.com/how-much-money-has-among-us-made-in-total/ ／ https://www.ggrecon.com/articles/in-depth-with-innersloth-the-developers-behind-among-us 。**公開から約2年後の急成長で、運の要素が大きいことは開発側の記事でも示される（要約）** |
| Fortnite | コスメ（スキン）とバトルパス、ランダム要素なしの限定アイテム | 2018年 約24億ドル（推定）。バトルパスは2019年に収益の少なくとも3分の1（SuperData、二次報道）。Sacraの推計は2022年約52億→2023年約44億ドル（推定） | 大企業（Epic） | 【推定】https://sacra.com/chat/h/8d70a8fc-7248-444d-9c1c-cc3fac8340b8/ 。大企業の例であり、個人開発の参考にはならない |
| バトルパス（追加事例） | シーズンパス | Clash of Clans: 導入月の売上が直前30日比+72%、Lords Mobile: プレイヤー支出が2倍（2021年1月に9,000万ドル）。**市場全体の売上比率は未取得** | 大企業 | 【調査】Sensor Tower。【要約】https://gamesbeat.com/?p=173195 |
| Flappy Bird（広告型） | 無料+広告 | 作者の自己申告: 広告収入が平均1日約5万ドル（2014年）。その後、作者が自らストアから削除。「3日で作った」は資料により異なり未確認 | 個人（Dong Nguyen） | 【自己申告】https://www.huffingtonpost.co.uk/amp/entry/flappy-bird-50k-per-day_n_4735582 |

読み取り（事実の範囲）:
- 上記の「衝動型に頼らず成立した」例は、**買い切り（Stardew、Vampire Survivors）、無料の話題作を売却（Wordle）、コスメ課金（Among Us、Fortnite）**。いずれも**ヒットした少数の例（生存者バイアスあり）**で、ヒット前の失敗数は分からない。
- 価値型の課金率・ARPUを、衝動型と同条件で比べたデータは**取得できなかった（未取得）**。「価値型の売上が衝動型より小さい」とも「大きい」とも、データでは言えない。
- 日本の個人開発のゲームの収益事例は、今回の検索では**具体的な数字が見つからなかった**（副業記事に「半年で月10万円」の例があるが、受託を含みゲーム限定ではない。https://www.alc.co.jp/programming/sidejob/app-development/ ）。

---

## 4. ヒット率の現実

| 指標 | データ | 区分・出典 |
|---|---|---|
| モバイルゲーム（2025年） | 約19万本が公開、うち初年度に50万DL超は約2,500本（約1.3%、計算は当方） | 【調査】Moloco。【要約】https://www.pocketgamer.biz/report-only-2500-of-190000-mobile-games-released-in-2025-surpassed-500000-downloads/ |
| Steam（2025年） | Valveの公表: 粗収益10万ドル超が5,863タイトル（2020年の約3,000の約2倍）。第三者推計（Gamalytic、年途中）: 2025年公開作の約8%が10万ドル超、**40%が公開料100ドルを回収できず**。2023年は約5%が10万ドル超。100万ドル超は約300本（約1.5%） | 【公的/調査】https://www.player.one/nearly-6000-games-steam-earned-100k-2025-valve-reveals-162428 ／ https://opencritic.com/news/22399/only-8-of-steam-games-gross-over-100-thousand-40-make-less-than-steam-listing-fees ／ https://wnhub.io/news/stores-and-publishing/item-51947 。**Steamの中央値収益は12年連続で低下**という報道あり |
| 継続率（GameAnalytics 2025年） | 中央値: D1 約22%、D7 4%未満。上位1%でもD30は約10% | 【調査】【要約】https://investgame.net/news/pdf/2026-01-27-2026-mobile-pc-benchmarks_compressed/ 。古いAppsFlyer（2022〜23年）はパズルでD1 約32%、D7 約12%、D30 約5%で、**サンプルが異なり高い** |
| 獲得単価 | ハイパーカジュアルのCPI中央値: Android 0.20ドル、iOS 0.42ドル（2022年Q4、Tenjin/GameAnalytics）。別資料: 先進国で0.5〜2ドル。**年・地域で不一致** | 【調査】【要約】https://gameindustrylibrary.com/documents/benchmark-2022 ほか |
| 運の要素 | Vampire Survivorsの作者が「成功は運だった」「模倣モバイルゲームが多数ある」と発言 | 【自己申告】上記gamesradar記事 |

個人開発の「成功率」を直接示す公的統計は、今回の検索では見つからなかった。上記のストア全体の分布が最も近い代替データ。

---

## 5. AIでの開発可能性

### 5.1 作れる範囲（Claude Codeを想定）
- **作れると考えられる範囲（推定、本調査では実証していない）:** HTML5/JavaScript（Phaserなどのライブラリ）によるウェブゲーム、テキスト・パズル・カード・放置系。Vampire Survivorsの原型もPhaser（ブラウザ向けフレームワーク）で作られた（https://en.wikipedia.org/wiki/Vampire_Survivors の要約）。
- **難しいと考えられる範囲（推定）:** 大規模な3D、リアルタイム対戦サーバー、高品質な絵・音の大量制作。
- 「Claude Codeでゲームを作って収益が出た」という公開事例は、今回は調べていない（未取得）。**開発の可否は、小さな試作で実証するのが確実**（要提案）。

### 5.2 アセット（絵・音）
- **無料で商用利用できるCC0素材**: Kenneyの全アセットはCC0で、商用利用でき、クレジット表記は不要（Kenney公式サイトの要約。https://kenney.nl/support ）。OpenGameArtはアセットごとにライセンスが違い（CC0、CC-BY、CC-BY-SA、GPLなど）、**個別確認が必要**（CC-BY-SAは表示義務と継承義務あり）。
- 絵・音の自作は、Claude Code単体では画像・音声を生成できない（推定）。コードで描く図形・SVG・CSSアニメ、効果音のコード生成（WebAudio）は可能な範囲。

### 5.3 AI生成物の著作権・ストア規約
| 項目 | 内容 | 出典 |
|---|---|---|
| 米国 | 著作権局（2025年1月29日、AI報告書Part 2）: 現在の技術では、**プロンプトだけでは、利用者が出力の著作者になるのに十分な人間の制御がない**。AIを補助ツールとして使うことは保護を妨げない。人間が作った表現を入力・修正する場合は保護されうる。個別判断 | 【公的】【要約】https://copyrightalliance.org/ai-report-part-2-copyrightability/ ／ https://ipwatchdog.com/2025/01/29/part-two-copyright-office-ai-report-says-creative-prompting-doesnt-constitute-authorship/ |
| 日本 | 文化庁「AIと著作権に関する考え方について」（2024年3月15日、法的拘束力なし）: 指示がアイデアにとどまる場合、AI生成物に著作物性は認められない。指示が具体的なほど創作的寄与が認められやすい。人間の加筆・修正部分は、創作的表現かで判断。2024年7月にチェックリスト＆ガイダンスも公表 | 【公的】【要約】https://www.gamebusiness.jp/article/2024/04/19/22981.html |
| Steam | AI生成コンテンツの開示が必要。**開発の補助ツール（コード補助など）は開示対象外**に絞り込まれたと報道（2026年1月、法律事務所ブログ等。Valve一次資料は未確認）。ライブ生成AIは対策の説明が必要。成人向け性的内容のライブ生成は禁止 | 【自己申告】Valve。【要約】https://www.pcgamer.com/software/ai/steam-updates-ai-disclosure-form-to-specify-that-its-focused-on-ai-generated-content-that-is-consumed-by-players-not-efficiency-tools-used-behind-the-scenes/ |
| Steamの現状 | 2025年公開作の約5本に1本がAI使用を開示（7,818タイトル、全体の7%、2025年7月。Totally Human Media）。その後、新作の約3分の1とする推計や、2026年10月に約50%とする分析あり（手法がそれぞれ異なる）。**AI開示作は新作の約3分の1だが、推定売上では10〜27%にとどまる**という推計（Sulka Haro、要約） | 【調査】https://www.tomshardware.com/video-games/pc-gaming/1-in-5-steam-games-released-in-2025-use-generative-ai-up-nearly-700-percent-year-on-year-7-818-titles-disclose-genai-asset-usage-7-percent-of-entire-steam-library ／ https://app.cinevva.com/news/2026-07-20-steam-ai-disclosure-study |
| Apple/Google | AI生成コンテンツに関する、ゲーム向け個別の規約は今回の検索で取得できなかった（**未取得**）。Appleは「ウェブサイトの再パッケージに近い薄いアプリ」（4.2）と「類似アプリの量産」（4.3）を拒否対象にしている（ベンダーブログ経由。公式ガイドライン原文は未読）。 | 【要約】https://newly.app/guides/minimum-functionality-rejection |

---

## 6. 予算ゼロ（D-0002）の可否

| 段階 | 費用 | ゼロで可能か | 出典 |
|---|---|---|---|
| 開発（Claude Code） | Proプラン利用料のみ（既存） | 可 | D-0002 |
| ウェブゲームの公開（静的HTML） | GitHub Pages: サイト1GB、月100GB帯域（ソフトキャップ）。**ただし「オンラインビジネス・EC・商取引を主目的とするサイトの無料ホスティングには使えない」**と規定。無料ゲームの公開は可能性が高いが、**課金サイトとしての利用は規約に反するおそれ**（弁護士ではなく規約文言に基づく読み） | 【公的】https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits 。Cloudflare Pagesの無料枠は今回未取得 |
| itch.io | 手数料は開発者が0〜100%で設定、デフォルト10%。決済手数料は別（Stripe/PayPal） | 初期費用ゼロ（手数料は売上から。D-0002は手数料を支出とみなさない） | 【自己申告】https://www.summerengine.com/make-great-games/make-money-from-your-indie-game （要約）。itch.ioの一次資料は未読 |
| 決済手段（自社サイト） | Stripe日本: 国内カード3.6%、初期・月額費用なし。個人事業主も利用可と第三者サイトにあるが、**公式での要件（開業届、特定商取引法表記など）は未確認** | 初期費用ゼロの可能性。要確認 | 【要約】https://atsoho.com/apps/p/stripe |
| 広告収益（ウェブ） | ポータル（Poki等）の分配は上記1.2。**CPMなどの実績値は未取得** | 費用なし。収益規模は不明 | 同上 |
| Steam | 1タイトル100ドル（返金不可、粗売上1,000ドル超で回収可能）。**有料** | 不可（支出） | 【公的】https://partner.steamgames.com/doc/gettingstarted/appfee |
| Apple App Store | Developer Program 年99ドル。Small Business Program適用で手数料15%（年間収益100万ドル以下）、通常30% | **不可（支出）** | 【自己申告】【要約】https://splitmetrics.com/blog/google-play-apple-app-store-fees/ ほか。Apple公式は未読 |
| Google Play | 登録料25ドル（1回）。**2023年11月13日以降に作った個人アカウントは、12人以上のテスターが14日連続で参加するクローズドテストを経ないと製品版を公開できない**（組織アカウントは免除）。手数料は最初の100万ドル/年まで15% | **不可（登録料。さらにテスター12人の確保が必要）** | 【公的】https://support.google.com/googleplay/android-developer/answer/14151465 ほか【要約】 |
| 集客 | 広告は使えない（D-0002）。獲得単価はハイパーカジュアルで0.2〜2ドル（4章）。オーガニック（SNS、コミュニティ）のゲーム向け実績データは今回未取得 | 広告は不可。オーガニックの成否は不明 | — |

ゼロでできる範囲（事実）: 制作、ウェブでの公開、無料での検証（プレイ数、反応）。**費用が必要になる地点:** Apple（年99ドル）、Google Play（25ドル+テスター確保）、Steam（100ドル/タイトル）、広告（獲得単価）、法人化が必要になった場合の費用（未調査）。

段階的な進め方（ゼロで検証→売上が出たら再投資）が成立するか: **ウェブゲームの無料公開までは成立する。ただし、ウェブゲームの課金（決済・規約・前払式支払手段）の扱いは、規約・法令の確認が前提**。売上が出る前に、ストア公開で費用が必要になる。

---

## 7. 顧客像（personas.md）との接点と、自己理解型コンテンツの市場

### 7.1 悩みとゲームの接点（データにある範囲）
- 顧客像の悩みは、personas.md では「決める基準がない」（P1、P2）、「他者の基準で確かめる」（共通）、「話せる相手がいない・孤立」（P4）、「自分の軸が弱い」（P2）。
- ゲームの構造が、これらの欲求を満たすという**研究上の説明**は mechanism-structure.md にある（目標の明確さ、即時フィードバック、進歩の可視化、仲間・承認。自己決定理論など）。ただし**「顧客がゲームを求めている」ことを示すデータはない**（同ファイル、未検証）。
- ゲームの時間がウェルビーイングに与える影響は、ほぼない〜非常に小さい（Vuorre 2022）。**内発的動機での遊びは良い関連、外発的動機は悪い関連**。顧客像の悩みへの「効果」を約束できるデータはない（原則2と整合しない主張は避ける）。
- ゲームが孤独・孤立を減らす因果のデータは、今回の検索では取得できなかった（未取得）。

### 7.2 診断・性格系のゲーム的コンテンツの市場（日本）
- Z世代（661名、otalab、2023年10月）: MBTIの認知は約6割、知ったきっかけはSNSが過半数。「自分の性格を理解できた」が6割以上（自己申告）。https://webtan.impress.co.jp/n/2023/10/23/45832
- Z世代女性のMBTI診断経験41.3%（MERY、2024年9月）。30〜40代女性は半分程度（要約）。
- Z世代（15〜29歳）の33.9%が週1回程度以上占いを利用（リスミィ調査、要約）。
- 海外: Co-Starは累計2,000万DL超（2021年の資金調達時、自己申告）。月間売上は第三者推計で幅があり（10K+ドルや10K未満ドル）、**信頼できる収益データは未取得**。The Pattern（占星術）は第三者推計で売上約30万ドル、35K DL（【推定】）。https://www.axios.com/2021/04/14/astrology-app-co-star-raises-15-million-funding ／ https://appgoblin.info/apps/com.costarastrology
- 16Personalitiesの利用者数・収益は取得できなかった（未取得）。
- 読み取り: 自己理解型コンテンツの**関心**はデータにある。**収益性（無料が主流か、課金できるか）のデータは弱い**。これはゲーム事業とは別の、既存の「自己理解」ビジネスの評価に近く、別途の調査が要る。

---

## 8. 規制・規約（弁護士の確認ではない。CEOが公式情報で確認する）

| 論点 | 事実（要約経由） | 出典 |
|---|---|---|
| 景品表示法（コンプガチャ） | 消費者庁が2012年5月に、特定の複数アイテムを揃えた者に別のアイテム等を提供する「コンプガチャ」が告示の「カード合わせ」に当たるとし、運用基準を2012年7月1日に改正。**ガチャ自体が直ちに違法とは限らない**という趣旨の発言あり。ガチャの確率表示そのもの、優良誤認、個別の措置命令は今回取得できなかった（**未取得**） | 【公的】https://www.gamebusiness.jp/article/2012/06/29/6366.html ／ https://www.gamebusiness.jp/article/2012/05/18/6111.html |
| 業界の自主規制 | 日本オンラインゲーム協会（JOGA）のガイドライン: ガチャの確率表記は**強制ではなく**、条件のいずれかを満たす形（個別確率の明記、推定金額が1回の課金額の100倍以内または5万円以内など）。事務局の説明（報道要約）。2013年版は未成年者保護が中心 | 【自己申告】https://japanonlinegame.org/wp-content/uploads/2017/06/JOGA130405-1.pdf ／ https://gamebiz.jp/news/158947 |
| 賭博罪・風営法との線引き | 今回の検索では、有料ガチャ一般の賭博罪該当性の判断、風営法の位置づけを**確認できなかった（未取得）**。コンプガチャの見解は景品表示法に関するもので、賭博罪の判断ではない、という解説あり | 【要約】https://www.amt-law.com/asset/pdf/bulletins17_pdf/241018.pdf など |
| 資金決済法（前払式支払手段） | ゲーム内通貨が「自家型前払式支払手段」に当たる場合: 有効期限が6か月超で、基準日（3月末・9月末）の未使用残高が1,000万円を超えると、届出が必要（基準日から2か月以内）、未使用残高の1/2以上の発行保証金などの資産保全、払戻しは原則禁止。**行政書士系サイトの解説で、該当性は個別判断。条文・財務局の公式は未読** | 【要約】https://www.shigyo.co.jp/search_post/kinyu/prepaid/issuance-notification/ ／ https://www.japaneselawtranslation.go.jp/ja/laws/view/2319/ja |
| 未成年の課金 | 国民生活センターの相談件数（2.2）。未成年者取消権（民法）は今回未調査 | 【公的】2.2参照 |
| アプリストアの確率表示 | Apple: 2017年12月からApp Store審査ガイドライン3.1.1で、ランダムなバーチャルアイテムの販売では、購入前に各アイテムの確率の開示が必須。Google Play: 同様の確率開示を要求（日付は未取得）。**2017〜2019年の報道・法律事務所解説で、現行の規約原文は未読** | 【自己申告】https://www.fenwick.com/insights/publications/apple-now-requires-disclosure-of-loot-box-odds ／ https://www.fenwick.com/insights/publications/google-play-now-requires-disclosure-of-loot-box-odds |
| 海外規制 | 米FTCのGenshin和解（2.2）。EU・英国・ベルギーなどの規制は今回未調査 | — |
| 価値型の場合 | 買い切り・コスメの固定価格販売は、確率表示の論点が生じない（推定）。ただし、特定商取引法（通信販売の表記）、景品表示法（優良誤認）、消費者契約法、個人情報の扱い（未成年を含む場合）の確認は必要（service-principles.md） | — |

---

## 9. 比較の整理（CEOが判断するための表。結論は出さない）

| 観点 | 衝動型（ガチャ等） | 価値型（買い切り・コスメ・バトルパス等） |
|---|---|---|
| 収益実績（データ） | 世界の大型タイトルで巨額。ホエール依存が高い（上位1%が33〜58%、上位5%が50%など） | Stardew（4,100万本）、Vampire Survivors（推計数百〜数千万ドル）、Fortnite（コスメ中心）など。ただし少数のヒット例 |
| 個人・小規模での再現性 | 規模が必要（獲得費用が大きい）。データ未取得 | 個人開発の例があるが、運の要素が大きい。ヒット率は低い（4章） |
| 害・規制リスク | 問題ギャンブルとの相関、未成年トラブル、FTC制裁、確率表示規約 | 小さい（確率・ランダム性を使わない場合。推定） |
| 提供原則との整合 | 原則3・4・5に反する | 原則と整合可能（設計次第） |
| 予算ゼロとの整合 | ストア公開が必要でゼロではない | ウェブ公開はゼロ。課金・ストアは費用または規約確認が必要 |

---

## 10. 不明点・未取得（CEO・次のタスクが埋める候補）

1. 一次資料の未確認: 国民生活センター、Newzoo、Sensor Tower、Moloco、Valve、Apple/Google規約。ネットワーク制限で取得できなかった。
2. 日本の「上位課金者の売上比率」、日本の個人開発ゲームの収益事例、ノベル・放置・育成系の収益統計。
3. 価値型と衝動型を同条件で比べた課金率・ARPUの比較データ。
4. 個人開発の成功率を直接示す統計（ストア全体の分布のみ）。
5. Claude Codeによるゲーム開発の実証事例、AI生成アセットのApple/Google規約。
6. Cloudflare Pagesの無料枠、ウェブゲームの広告CPM、ウェブでの課金（Stripeの要件）。
7. 賭博罪・風営法の整理、EU・英国の規制、未成年者取消権。
8. 顧客像が「ゲーム」を求めるか（インタビュー等、CEO承認が必要）。
9. 診断・自己理解アプリの収益性（信頼できる収益データ）。
