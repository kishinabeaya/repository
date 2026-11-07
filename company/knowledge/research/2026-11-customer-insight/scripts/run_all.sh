#!/bin/sh
# 再実行: sh run_all.sh （標準ライブラリのみ。出力は *_out.md。quant-analysis.md はこれらを結合）
cd "$(dirname "$0")"
python3 -I coconala_analysis.py > coconala_out.md
python3 -I qa_analysis.py > qa_out.md
{ cat quant-header.md; sed 's/^# /## /;s/^## \([0-9]\)\./### \1./' coconala_out.md; echo; sed 's/^# /## /' qa_out.md; cat quant-footer.md; } > ../quant-analysis.md
