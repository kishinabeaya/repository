#!/usr/bin/env python3 -I
"""CSVから追加集計（評価件数順カテゴリ、添削・書類系キーワード）。python3 -I extra.py <csv>"""
import sys, csv, re, collections
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
for r in rows: r['c'] = int(r['service_rating_count']); r['p'] = int(r['proxy_lower_bound_yen']) if r['proxy_lower_bound_yen'] else 0
print('## カテゴリ別（評価件数合計の降順、分単価含む）\n| 順 | カテゴリ | 親 | 評価件数合計 | 円建てのみの代理指標合計 | 分単価サービス数 |\n|---|---|---|---|---|---|')
g = collections.defaultdict(lambda: [0, 0, 0, '']);
for r in rows:
    a = g[r['category']]; a[0] += r['c']; a[1] += r['p']; a[2] += (r['price_unit'] == '円/分'); a[3] = r['parent_category']
for i, (k, a) in enumerate(sorted(g.items(), key=lambda x: -x[1][0]), 1): print(f'| {i} | {k} | {a[3]} | {a[0]:,} | {a[1]:,} | {a[2]} |')
KW = {'履歴書・職務経歴書・ES・自己PR・志望動機の作成/添削': r'履歴書|職務経歴書|エントリーシート|\bES\b|自己PR|志望動機|経歴書',
      '婚活・恋愛プロフィール/メッセージ添削': r'婚活|プロフィール|マッチングアプリ|メッセージ',
      '面接対策': r'面接', 'LP・ホームページ制作': r'LP|ランディング|ホームページ|HP|サイト制作', '資料・スライド・企画書': r'資料|スライド|パワポ|PowerPoint|企画書|提案書',
      'ロゴ': r'ロゴ', '動画編集': r'動画編集|カット編集', '文章添削・校正': r'添削|校正', '電話・通話相談': r'電話|通話'}
print('\n## 用途キーワード別（タイトルに含む。重複除去、複数キーワード該当あり）\n| 区分 | サービス数 | 評価件数合計 | 代理指標合計(円建てのみ) | 評価件数100以上のサービス数 |\n|---|---|---|---|---|')
for k, p in KW.items():
    s = [r for r in rows if re.search(p, r['title'])]
    print(f"| {k} | {len(s)} | {sum(r['c'] for r in s):,} | {sum(r['p'] for r in s):,} | {sum(1 for r in s if r['c']>=100)} |")
