# AI COMPANY OS

CEO（あなた）が経営目標と重要な意思決定を行い、市場調査・企画・制作・マーケティング・分析をAI社員が分担して実行する仕組みです。
プログラミングは不要です。Claude Codeでこのフォルダを開き、コマンドを入力して、承認・却下を返答するだけで運用できます。

---

## はじめ方（初回のみ）

1. Claude Code をインストールし、Claude Pro アカウントでログインする
2. このリポジトリを手元にクローンする（またはclaude.ai/codeでこのリポジトリを開く）
3. フォルダ内で Claude Code を起動する
   ```bash
   claude
   ```
4. `/daily` と入力する

> フック（安全装置）は `python3` を使います。Mac/Linuxには通常入っています。

---

## CEOの1日（15〜30分）

| やること | コマンド |
|---|---|
| 朝、1日分の業務を回す | `/daily` |
| 日報と承認依頼を読む | `company/reports/daily/` / `company/inbox/ceo/` |
| 承認する | `/approve A-0001` （コメントを付けてもよい） |
| 却下・差し戻す | `/reject A-0001 価格をもう少し下げて` |
| 新しい指示を出す | `/assign 来週までにSNSのフォロワーを増やす施策を考えて` |
| 現状だけ確認する（使用量ほぼゼロ） | `/status` |
| 週に1回、振り返りと計画 | `/weekly` |

**承認が必要なもの（すべてあなたが判断）:** 外部への公開・投稿・出品、お金の支出、価格、新しい事業、契約、アカウント作成。
AI社員は下書きと準備まで行い、実際のボタン操作（出品・投稿）は当面あなたが行います。

---

## AI社員（6名）

| 役職 | 担当 |
|---|---|
| Chief of Staff | 業務割当・進捗管理・報告（Claude Code本体が担当） |
| Strategist | 市場調査・事業企画・価格案 |
| Product Builder | 商品の制作・実装 |
| Content Creator | 記事・SNS・商品説明の下書き |
| Growth Marketer | 集客戦略・ローンチ計画 |
| Analyst | KPI集計・効果検証・ファクトチェック・品質レビュー |

---

## Proプランで運用するコツ

- 予算はProプランの利用料のみ。**追加費用がかかる施策はAIが提案するだけで、実行しません。**
- Proプランには5時間ごとの利用上限があります。`/daily` は1日1回が目安です。
- 上限に達したら時間をおいて再開してください。作業状態はすべてファイルに保存されているため、途中で止まっても続きから再開できます。
- 状況確認だけなら `/daily` ではなく `/status` を使ってください。

---

## フォルダの見方

```
CLAUDE.md                会社憲章（AIが毎回読む行動規範）
.claude/agents/          AI社員の定義
.claude/skills/          コマンド（/daily など）
.claude/hooks/           安全装置（危険な操作をブロック）
org/                     社員名簿・割当ルール
company/
  strategy/              ミッション・OKR・制約
  tasks/                 タスク
  decisions/             あなたの決定の記録（改変不可）
  inbox/ceo/             あなたの承認待ち
  knowledge/             調査結果・学び
  products/              商品
  content/               下書き（drafts）と公開済み（published）
  marketing/             マーケティング計画
  metrics/kpi.csv        KPIの記録
  reports/               日報・週報
  playbooks/             業務手順書
  templates/             各種テンプレート
scripts/                 補助スクリプト
```

設計の全体像は `docs/design.md` を参照してください。
