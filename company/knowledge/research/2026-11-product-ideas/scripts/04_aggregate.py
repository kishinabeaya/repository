"""raw/ の4つのCSVを集計して、Markdownの表を標準出力に出す。標準ライブラリのみ。
使い方: python3 -I 04_aggregate.py <rawディレクトリ> [日本の既存rawディレクトリ]
重み付き統計: trustmrr.csv の weight(層の重み)を使う。重みなし(取得行そのまま)も併記する。
"""
import csv, os, statistics, sys, collections
raw = sys.argv[1]
def rd(n): return list(csv.DictReader(open(os.path.join(raw, n), encoding='utf-8')))
def fl(x):
    try: return float(x)
    except: return None
def wq(vals, wts, q):
    p = sorted(zip(vals, wts)); T = sum(w for _, w in p); c = 0
    for v, w in p:
        c += w
        if c >= q * T: return v
    return p[-1][0]
def money(x): return f'${x:,.0f}'
tm = rd('trustmrr.csv')
# 重複(複数カテゴリ)を除く: slug単位で、最初のカテゴリ行を使う。
seen = {}; 
for r in tm: seen.setdefault(r['slug'], r)
uniq = list(seen.values())
print(f'## TrustMRR 取得行 {len(tm)} / slug重複除去後 {len(uniq)}\n')
def stats(rows, label, weighted=True, key='last30d_revenue_usd'):
    v = [fl(r[key]) or 0 for r in rows]; w = [fl(r['weight']) if weighted else 1 for r in rows]
    tw = sum(w)
    return [label, len(rows), money(wq(v, w, .5)), money(wq(v, w, .9)), money(wq(v, w, .99)),
            f'{sum(wi for vi, wi in zip(v, w) if vi == 0) / tw:.1%}', f'{sum(wi for vi, wi in zip(v, w) if 0 < vi < 1000) / tw:.1%}',
            f'{sum(wi for vi, wi in zip(v, w) if vi >= 10000) / tw:.1%}']
hdr = '| 区分 | 取得件数 | 直近30日収益 中央値 | 上位10%の水準(P90) | P99 | 収益0の割合 | 0超〜$1,000未満の割合 | $10,000以上の割合 |\n|---|---|---|---|---|---|---|---|'
def table(rows):
    print('\n'.join('| ' + ' | '.join(map(str, r)) + ' |' for r in rows))
print('### 全体 (直近30日の検証済み収益, USD)\n'); print(hdr)
table([stats(tm, '全取得行・重み付き(層の重みで母集団に拡大)'), stats(tm, '全取得行・重みなし(取得標本そのまま)', False),
       stats([r for r in tm if r['list_page'] == '1'], '各カテゴリ1ページ目(上位30件)のみ・重みなし', False),
       stats([r for r in tm if r['list_page'] != '1'], '2ページ目以降(層抽出)・重み付き')])
print('\n### 累計収益 / MRR (全取得行・重み付き)\n'); print(hdr)
table([stats(tm, '累計収益 total_revenue', True, 'total_revenue_usd'), stats(tm, '現在MRR current_mrr', True, 'mrr_usd')])
print('\n### カテゴリ別 (直近30日収益。重み付き。カテゴリ総数=サイト表示の総数。複数カテゴリに載る事業は、各カテゴリで数える)\n')
print('| カテゴリ | 総数(サイト表示) | 取得件数 | 中央値 | P90 | P99 | 収益0 | 0超〜$1,000未満 | $10,000以上 |\n|---|---|---|---|---|---|---|---|---|')
bycat = collections.defaultdict(list)
for r in tm: bycat[r['category']].append(r)
catrows = []
for c, rs in bycat.items():
    s = stats(rs, c); catrows.append((int(rs[0]['category_total']), [c, rs[0]['category_total']] + s[1:]))
table([x[1] for x in sorted(catrows, key=lambda x: -x[0])])
print('\n### 検証済み収益が正の事業だけの分布 (重み付き。直近30日>0)\n'); print(hdr)
pos = [r for r in tm if (fl(r['last30d_revenue_usd']) or 0) > 0]
table([stats(pos, '直近30日>0')])
print('\n### 価格モデル・開始時期(詳細ページ標本。取得できた件のみ。母集団の代表ではない)\n')
det = [r for r in tm if r['founded'] or r['pricing_model']]
dd = {r['slug']: r for r in det}
print('標本数', len(dd))
print('| 事業 | カテゴリ | 直近30日収益 | 累計 | 開始 | タイムライン最初の収益月(月数) | 価格モデル | 対象 | 設計分類(A/B/U) |\n|---|---|---|---|---|---|---|---|---|')
for r in sorted(dd.values(), key=lambda r: -(fl(r['last30d_revenue_usd']) or 0)):
    print(f"| {r['name']} | {r['category']} | {money(fl(r['last30d_revenue_usd']))} | {money(fl(r['total_revenue_usd']))} | {r['founded'] or '-'} | {r['first_revenue_month_in_timeline'] or '-'}({r['months_in_timeline']}) | {(r['pricing_model'] or '-')[:70]} | {r['audience'] or '-'} | {r['design_cc_class']} |")
print('\n### 【設計】Claude Code分類(説明文キーワード。収益の実績ではない)\n')
print('| 分類 | 件数(取得行,重み付き母集団換算) | 直近30日収益 中央値(重み付き) | 同 P90 |\n|---|---|---|---|')
for k, lab in (('A', 'A ソフト/デジタル型と設計上みなす'), ('B', 'B 物理・人手・サービス型の語あり'), ('U', 'U 説明文なし')):
    rs = [r for r in tm if r['design_cc_class'] == k]
    if rs:
        s = stats(rs, lab); print(f"| {lab} | {len(rs)} ({sum(fl(r['weight']) for r in rs):,.0f}) | {s[2]} | {s[3]} |")
# ---- Chrome ----
ch = rd('chrome-extensions.csv')
print(f'\n## Chrome拡張 {len(ch)}件 (13カテゴリ x 上位32件)\n')
print('| カテゴリ | 件数 | 利用者数(バケット) 中央値 | 評価件数 中央値 | 評価点 中央値 | 利用者100万以上 | 利用者1万未満 |\n|---|---|---|---|---|---|---|')
bc = collections.defaultdict(list)
for r in ch: bc[r['category']].append(r)
for c, rs in sorted(bc.items()):
    u = [fl(r['users_bucket']) or 0 for r in rs]
    print(f"| {c} | {len(rs)} | {statistics.median(u):,.0f} | {statistics.median(int(r['rating_count']) for r in rs):,.0f} | {statistics.median(float(r['rating']) for r in rs):.2f} | {sum(1 for x in u if x >= 1e6)} | {sum(1 for x in u if x < 1e4)} |")
# ---- Gumroad ----
gm = rd('gumroad-top.csv')
print(f'\n## Gumroad {len(gm)}件 (7ビュー x 上位36件, sort=best_sellers)\n')
print('| ビュー | 全商品数(サイト表示) | 件数 | 価格 中央値 | 価格 P90 | 評価件数 中央値 | 評価件数 0 | サブスク(recurrence有) | 評価件数100以上 |\n|---|---|---|---|---|---|---|---|---|')
bg = collections.defaultdict(list)
for r in gm: bg[r['taxonomy']].append(r)
for c, rs in bg.items():
    pr = sorted(fl(r['price_usd']) for r in rs); rc = [int(r['rating_count'] or 0) for r in rs]
    print(f"| {c} | {int(rs[0]['taxonomy_total_products']):,} | {len(rs)} | ${statistics.median(pr):,.2f} | ${pr[int(len(pr)*.9)]:,.2f} | {statistics.median(rc):,.0f} | {sum(1 for x in rc if x == 0)} | {sum(1 for r in rs if r['recurrence'])} | {sum(1 for x in rc if x >= 100)} |")
print('\nGumroad native_type 内訳: ', dict(collections.Counter(r['native_type'] for r in gm).most_common()))
# ---- itch ----
it = rd('itch-top.csv')
print(f'\n## itch.io {len(it)}件 (top-sellers p1-3 と ジャンル2種 x 36件)\n')
import re
def pv(x):
    m = re.search(r'[\d.]+', x.replace(',', '')); return float(m.group()) if m and '$' in x else None
print('| ビュー | 件数 | 価格表示あり | 価格 中央値 | 価格表示なし(無料/PWYW等) |\n|---|---|---|---|---|')
bi = collections.defaultdict(list)
for r in it: bi[r['source_page']].append(r)
for c, rs in bi.items():
    p = [pv(r['price_listed']) for r in rs if pv(r['price_listed']) is not None]
    print(f"| {c} | {len(rs)} | {len(p)} | ${statistics.median(p):.2f} | {len(rs) - len(p)} |" if p else f"| {c} | {len(rs)} | 0 | - | {len(rs)} |")
g = collections.Counter(r['genre'] for r in it if r['source_page'] in ('top', 'p2', 'p3'))
print('\ntop-sellers 3ページのジャンル(一覧表示): ', dict(g.most_common(10)))
# ---- Japan ----
if len(sys.argv) > 2:
    jd = sys.argv[2]
    print('\n## 日本の既存データ(再利用。company/knowledge/research/2026-11-proven-sellers/raw/)\n')
    for fn, pk, ck in (('kindle-bestsellers.csv', 'price_jpy', 'rating_count'), ('booth-top.csv', 'price_jpy', 'wish_lists_count'), ('note-paid.csv', 'price_jpy', 'like_count')):
        rs = list(csv.DictReader(open(os.path.join(jd, fn), encoding='utf-8')))
        pr = sorted(fl(r[pk]) for r in rs if fl(r[pk]) is not None); cn = sorted(fl(r[ck]) or 0 for r in rs)
        print(f"- {fn}: {len(rs)}件 / 価格中央値 {statistics.median(pr):,.0f}円 / {ck}中央値 {statistics.median(cn):,.0f} / 最大 {max(cn):,.0f}")
