#!/bin/sh
# T-0013 スピリチュアル商材レビュー分析の再実行（標準ライブラリのみ）
cd "$(dirname "$0")" && python3 -I spiritual_review_analysis.py > spiritual_review_analysis_out.txt
