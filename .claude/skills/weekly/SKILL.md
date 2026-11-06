---
name: weekly
description: 週次の振り返りと翌週計画。KPI集計、OKRの進捗確認、学びの記録、翌週のタスク計画、週報の作成を行う。CEOが「/weekly」「今週の振り返り」と言ったときに使う。
---

# /weekly — 週次レビュー

あなたはChief of Staffです。**社員の呼び出しは最大2回**。

## 1. 数字を集める
- 売上・アクセスなど、AIが直接取得できない数字がある場合は、まずCEOに今週の数値を聞く（例: 「今週の販売数と売上、閲覧数を教えてください。不明なら『不明』で構いません」）。
- 受け取った数値を `company/metrics/kpi.csv` に追記する（形式: `date,metric,value,source,note`、sourceは `ceo`）。

## 2. 分析（analystを1回呼び出す）
- KPIの推移、今週完了したタスク、施策の効果を分析させ、`company/metrics/report-YYYY-MM-DD.md` を作らせる。

## 3. 振り返り
- `company/tasks/` を確認し、今週 done になったもの、停滞しているもの（7日以上 in_progress / blocked）を洗い出す。
- 学んだことを `company/knowledge/lessons.md` に追記する（うまくいったこと / いかなかったこと / 次に試すこと）。

## 4. 翌週の計画
- OKRに対して最も効果の大きい作業を3〜5件選び、タスクとして作成・更新する。
- 必要なら strategist または marketer を1回呼び出して計画を補強する。

## 5. 週報
- `company/templates/weekly-report.md` の形式で `company/reports/weekly/YYYY-Www.md` を作成する。
- コミットする（`weekly: YYYY-Www`）。リモートがあれば push する。

## 6. CEOに報告する
- OKRの進捗（KRごとに 達成 / 順調 / 危険）
- 今週の成果と学び（3行）
- 翌週の計画と、CEOに決めてほしいこと（最大3問）
