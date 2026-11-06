# AI COMPANY OS 設計書 v1.0（フェーズ0確定版）

v0.1（CEOレビュー用ドラフト）に、2026-11-06のCEO決定（D-0001〜D-0004）を反映した版。

## 1. 基本方針
- 収益を最優先する。組織を作り込む前に、調査→企画→制作→販売→分析を1周させる。
- ファイル（Gitリポジトリ）を唯一の正本にする。AIは会話をまたいで記憶を持たないため。
- 小さく始めて拡張する。社員は定義ファイルの追加だけで増やせる。
- CEOはコードを書かない。コマンドと承認・却下の返答だけで運用する。
- 人間の判断を必須にする箇所を固定する（L2: 公開・支出・価格・新事業・契約・アカウント）。

## 2. 組織構造
```
CEO（人間）── 承認・意思決定
   │
Chief of Staff（メインセッション）── 割当・進捗管理・報告 ※社員を呼び出せる唯一の存在
   │
   ├─ Strategist（市場調査・事業企画）
   ├─ Product Builder（商品開発）
   ├─ Content Creator（制作）
   ├─ Growth Marketer（マーケティング）
   └─ Analyst（分析・品質・改善）
```
Claude CodeのSubagentはSubagentを呼び出せないため、CoSはメインセッション（CLAUDE.md）が担う。

## 3. 権限レベル
| L0 自律 | L1 CoS承認 | L2 CEO承認 | L3 禁止 |
|---|---|---|---|
| 調査・下書き | 完了判定・試作 | 公開・支出・価格・新事業・契約・アカウント | 削除・秘密情報・force push・決定ログ改変 |

## 4. 連携方式（黒板方式）
社員どうしは直接会話せず、`company/` のファイルを介して協働する。
CEOが読むのは日報（`company/reports/daily/`）と承認キュー（`company/inbox/ceo/`）のみ。

## 5. 業務サイクル
| コマンド | 頻度 | 内容 |
|---|---|---|
| `/daily` | 毎日 | 現状把握 → 社員に作業依頼（最大2回）→ Analystが一括レビュー（1回）→ 日報 → 承認依頼 → コミット |
| `/weekly` | 毎週 | CEOから数値を聞く → KPI分析 → 振り返り → 翌週計画 → 週報 |
| `/assign` | 随時 | 目標をタスクに分解（社員は呼ばない） |
| `/approve` `/reject` | 随時 | CEO専用。決定ログに記録し、作業を進める |
| `/status` | 随時 | 社員を呼ばずに現状表示 |

タスクの状態遷移: `planned → in_progress → review → done`（L2は `waiting_approval` を経由。差し戻しは `rejected`、停止中は `blocked`）

## 6. Claude Code機能の使い分け
| 機能 | 実装 |
|---|---|
| CLAUDE.md | 会社憲章・CoSの行動規範 |
| Subagents | `.claude/agents/` に5名。全員 `model: sonnet`（Proプランの使用量節約） |
| Skills | `.claude/skills/` に6コマンド。`/approve` `/reject` は `disable-model-invocation` でCEO専用 |
| Hooks | SessionStart（現状読込）、PreToolUse（L3・未承認公開をブロック）、PostToolUse（活動ログ） |
| MCP | フェーズ0では使わない（Web検索は標準機能）。必要時に無料のものから追加 |
| Agent Teams | 使わない（トークン消費が大きく、Proプランの上限と合わない） |
| 定期実行 | 使わない（API従量課金が必要なため。`/daily` はCEOが手動実行） |

## 7. データ構造
```
CLAUDE.md / README.md / docs/design.md
.claude/{agents,skills,hooks,settings.json}
org/{roster.yaml,routing.yaml}
company/
  strategy/   mission.md, okr.md, constraints.md, 事業企画書
  tasks/      T-xxxx.md
  decisions/  D-xxxx.md（追記のみ）
  inbox/ceo/  A-xxxx.md（承認依頼）
  knowledge/  research/, lessons.md
  products/ content/{drafts,published}/ marketing/
  metrics/    kpi.csv（date,metric,value,source,note）
  reviews/    T-xxxx.md
  reports/    daily/, weekly/
  playbooks/  業務手順書
  templates/  各種テンプレート
  logs/       activity.jsonl
scripts/      status.py, next_id.py
```
将来の移行先: タスク→GitHub Issues/Notion、KPI→Google Sheets（いずれも無料枠・MCP経由）。

## 8. 拡張方法（数十名規模へ）
1. `company/templates/agent.md` から `.claude/agents/<id>.md` を作る
2. `org/roster.yaml` に登録し、`org/routing.yaml` に担当種別を追加する
3. 部門ができたら、部長エージェントは「計画とレビュー」を担当し、作業の起動はCoSが行う（構造は平らに保つ）
4. 増員はKPIのボトルネックが明確なときに限る。予算が増えたら、上位モデル・定期実行・Agent Teamsを検討する

## 9. 制約とリスク
| 制約・リスク | 対策 |
|---|---|
| Proプランの利用上限（5時間ごと） | 社員はsonnet、/dailyで最大3回、`/status` は社員を呼ばない。止まってもファイルから再開できる |
| 定期実行ができない | CEOが1日1回 `/daily` を実行する |
| ハルシネーション | Analystによるレビューと出典の必須化、外部公開はL2 |
| 外部サービスの操作 | アカウント開設・出品はCEOが行う |
| 法令・規約 | レビューチェックリストで景表法・ステマ規制・著作権・特商法を確認 |
| Hookによる強制の限界 | 社員ごとの書き込み範囲はプロンプトで指示（Hookは全社共通のL3・公開ルールのみ強制）。Gitで巻き戻し可能 |
| Hookの前提 | `python3` が必要（Mac/Linuxは標準） |

## 10. 運用コスト
| 項目 | 金額 |
|---|---|
| Claude Proプラン | 既存の契約のみ |
| GitHub・販売プラットフォーム・SNS | 0円（販売手数料は売上から差し引き） |
| CEOの作業時間 | 1日15〜30分 |

## 11. MVP計画
| フェーズ | 期間 | 内容 | 完了条件 |
|---|---|---|---|
| 0 基盤 | 〜11/8 | このリポジトリの構築 | `/daily` が最後まで動く |
| 1 最初の売上ループ | 11/9〜11/30 | 商品選定（T-0001）→ 企画承認（T-0003）→ 制作 → 公開 | 商品1点の公開（KR2） |
| 2 計測と改善 | 12月前半 | KPI定義（T-0002）、週次改善 | 初売上（KR3） |
| 3 拡張準備 | 12月後半〜 | 社員追加テンプレートの実運用 | 7人目を1時間で追加できる |
