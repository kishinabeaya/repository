---
name: reject
description: CEOが承認依頼（A-xxxx）を却下または差し戻す。CEO専用。
argument-hint: <A-xxxx> <理由・修正指示>
disable-model-invocation: true
---

# /reject — 却下・差し戻し

CEOの入力: **$ARGUMENTS**

1. 先頭の承認依頼ID（A-xxxx）を特定し、`company/inbox/ceo/A-xxxx.md` を読む。理由が書かれていない場合は、CEOに理由を1行で聞く。
2. `python3 scripts/next_id.py D` で採番し、`company/decisions/D-xxxx.md` に却下の決定と理由を記録する。
3. 承認依頼ファイルを更新する: `status: rejected`、`decision: D-xxxx`、`applied: true`、`decided: <日付>`。
4. 関連タスクを更新する:
   - 修正すれば通る内容なら → `status: rejected` にし、Feedback欄にCEOの指示を追記する（次の `/daily` で担当者が修正する）。
   - 方針そのものが却下なら → `status: done` にし、Reportに「CEOにより中止（D-xxxx）」と記録する。後続タスクも見直す。
5. 学びがあれば `company/knowledge/lessons.md` に1行追記する。
6. コミットし（`reject: A-xxxx`）、次に何が起きるかをCEOに1〜2行で伝える。
