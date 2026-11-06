---
name: approve
description: CEOが承認依頼（A-xxxx）を承認する。CEO専用。
argument-hint: <A-xxxx> [コメント]
disable-model-invocation: true
---

# /approve — 承認

CEOの入力: **$ARGUMENTS**

1. 先頭の承認依頼ID（A-xxxx）を特定し、`company/inbox/ceo/A-xxxx.md` を読む。見つからなければ、`status: pending` の承認依頼一覧を示してCEOに確認する。
2. `python3 scripts/next_id.py D` で決定IDを採番し、`company/templates/decision.md` を使って `company/decisions/D-xxxx.md` を作成する（決定: 承認、CEOのコメントがあれば記録）。
3. 承認依頼ファイルを更新する: `status: approved`、`decision: D-xxxx`、`applied: true`、`decided: <日付>`。
4. 関連タスクを更新する: `status: done`、`completed: <日付>`、`decision: D-xxxx`。
5. 承認内容が「外部への公開」の場合:
   - 公開する最終版を `company/content/published/` にコピーし、frontmatterに `decision: D-xxxx` と公開先を記録する。
   - 実際の公開作業（出品・投稿）はCEOが行う。CEOがやることを、手順として番号つきで具体的に示す（所要時間の目安つき）。
6. 承認によって着手可能になったタスクがあれば、それを伝える。
7. コミットする（`approve: A-xxxx`）。
