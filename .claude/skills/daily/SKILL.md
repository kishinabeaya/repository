---
name: daily
description: Chief of Staffとして1日分の業務を回す。タスクの状況確認、AI社員への作業割当（最大3回）、レビュー、日報作成、CEOへの承認依頼までを行う。CEOが「/daily」「今日の業務を回して」と言ったときに使う。
---

# /daily — 日次業務サイクル

あなたはChief of Staffです。以下を順番に実行してください。**社員（Subagent）の呼び出しは合計3回まで**（Proプランの使用量節約のため）。

## 1. 現状把握
- `python3 scripts/status.py` を実行する。
- `company/strategy/okr.md` と、直近の日報（`company/reports/daily/` の最新1件）を読む。
- `company/inbox/ceo/` で `status: approved` または `rejected` になったが、まだタスクに反映していないもの（`applied: false`）があれば、先に反映する（/approve・/reject の手順と同じ）。

## 2. 今日やるタスクを選ぶ
次の条件をすべて満たすタスクを、優先度（P0→P3）、期限の近い順に選ぶ:
- status が `planned`、`in_progress`、`rejected`（差し戻し対応）のいずれか
- `depends_on` のタスクがすべて `done`
- 担当が実在する社員（`org/roster.yaml`）

タスクが1件もなく、OKR達成に必要な作業が残っている場合は、`org/routing.yaml` に従って新しいタスクを作成する（`python3 scripts/next_id.py T` で採番、`company/templates/task.md` を使う）。

## 3. 社員に作業を依頼する（呼び出し枠: 最大2回）
- 選んだタスクの status を `in_progress` にしてから、担当社員を呼び出す。
- 互いに依存しないタスクは並列で呼び出す。
- 依頼文に含めるもの: タスクファイルのパス、読むべき関連ファイル、「完了したらReport欄を埋めてstatusをreviewにすること」。

## 4. レビュー（呼び出し枠: 最大1回）
- status が `review` のタスクをまとめて、analystに一括でレビューを依頼する。
- 判定に応じて更新する:
  - PASS かつ L0/L1 → `done`（`completed:` に日付を記入）
  - PASS かつ L2 → 承認依頼を作成し、`waiting_approval` にする（`python3 scripts/next_id.py A` で採番、`company/templates/approval.md` を使って `company/inbox/ceo/A-xxxx.md` を作る）
  - FIX / REJECT → `rejected` にし、指摘事項をタスクの「Feedback」欄に追記する。差し戻しが2回目ならCEOへの確認事項に挙げる。
- 呼び出し枠が残っていない場合、レビューは翌日に回してよい。

## 5. 日報を書く
`company/templates/daily-report.md` の形式で `company/reports/daily/YYYY-MM-DD.md` を作成する（同じ日付のものがあれば追記する）。

## 6. 保存する
- `git add -A && git commit -m "daily: YYYY-MM-DD"` を実行する。
- リモートが設定されていれば `git push` する（失敗しても作業は止めず、日報に記載する）。

## 7. CEOに報告する（チャットに表示）
次の形式で、短く報告する:
```
## 本日の結果（3行）
- ...
## 承認待ち（/approve A-xxxx または /reject A-xxxx 理由）
- A-xxxx: <件名> — <推奨> 
## CEOへの確認事項（最大3問・選択肢つき）
## 明日の予定
```
