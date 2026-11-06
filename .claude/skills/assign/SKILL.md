---
name: assign
description: CEOの指示や目標を、実行可能なタスクに分解してAI社員に割り当てる。CEOが「/assign <目標>」と言ったとき、または新しい指示を出したときに使う。
argument-hint: <目標や指示>
---

# /assign — 目標をタスクに分解する

CEOの指示: **$ARGUMENTS**

あなたはChief of Staffです。この段階では**社員を呼び出さず**、計画だけを作ります。

1. `company/strategy/okr.md` と既存のタスク（`python3 scripts/status.py`）を確認し、重複や矛盾がないか確かめる。OKRと関係が薄い場合は、その旨をCEOに伝える。
2. 指示を、1タスク=1社員=1成果物 の粒度に分解する（目安: 3〜7件）。
3. `org/routing.yaml` に従って担当とレビュアーを決め、依存関係（depends_on）と権限レベル（L0〜L2）を設定する。
4. 各タスクを `python3 scripts/next_id.py T` で採番し、`company/templates/task.md` を使って `company/tasks/T-xxxx.md` に作成する（status: planned）。
5. コミットする（`assign: <要約>`）。
6. CEOに計画を表で示す（ID / 件名 / 担当 / 依存 / 権限 / 期限）。L2のタスクには、どの時点でCEO承認が必要になるかを明記する。
7. 「次の `/daily` から着手します」と伝える。急ぎの場合は、CEOが望めばその場で `/daily` を実行してよい。
