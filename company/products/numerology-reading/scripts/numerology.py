#!/usr/bin/env python3
"""数秘術の計算スクリプト（Python標準ライブラリのみ。外部通信なし）。

使い方:
  python3 numerology.py 1992-07-23
  python3 numerology.py 1992-07-23 --name "Hanako Yamada" --year 2027
  python3 numerology.py 1992-07-23 --json

採用方式（詳細は ../spec.md）:
  - ピタゴラス式（A=1..I=9, J=1..R=9, S=1..Z=8 の循環）
  - ライフパス: 年・月・日をそれぞれ1桁に還元して足し、最後だけ 11/22/33 を残す
    （別流派: 月日年の途中のマスターナンバーも残す方式 -> life_path_alt として併記）
  - 誕生数: 日 (1-31) を還元。11, 22 は残す
  - パーソナルイヤー: 月+日+対象年の全桁を足して 1-9 に還元（マスターは残さない）
  - 太陽星座: 一般的な西洋占星術の日付表（年によらず固定）。切り替え日の前後1日は
    「境目」として注記し、依頼者に星座を確認する（spec.md 参照）
"""
import argparse
import json
import sys
from datetime import date

MASTERS = (11, 22, 33)
VOWELS = set("AEIOU")


def digit_sum(n):
    return sum(int(c) for c in str(abs(n)))


def reduce_num(n, keep_master=True):
    """各桁を足して1桁になるまで繰り返す。keep_master=True なら 11/22/33 で止める。"""
    while n > 9:
        if keep_master and n in MASTERS:
            return n
        n = digit_sum(n)
    return n


def life_path(y, m, d):
    """方式A（採用）: 年月日を各々1桁にし、合計を還元（最後だけマスターを残す）。"""
    total = reduce_num(y, False) + reduce_num(m, False) + reduce_num(d, False)
    return reduce_num(total, True)


def life_path_alt(y, m, d):
    """方式B（別流派）: 年月日の各還元でもマスターナンバーを残してから合計。"""
    total = reduce_num(y, True) + reduce_num(m, True) + reduce_num(d, True)
    return reduce_num(total, True)


def birth_number(d):
    return reduce_num(d, True)


def personal_year(m, d, target_year):
    return reduce_num(digit_sum(m) + digit_sum(d) + digit_sum(target_year), False)


def personal_months(py):
    """その年の月ごとのパーソナルマンス（個人年+月、1-9に還元）。"""
    return {mo: reduce_num(py + mo, False) for mo in range(1, 13)}


# 太陽星座: (開始月, 開始日, 名前)。開始日からつぎの開始日の前日まで。
ZODIAC_STARTS = [
    (1, 20, "水瓶座"), (2, 19, "魚座"), (3, 21, "牡羊座"), (4, 20, "牡牛座"),
    (5, 21, "双子座"), (6, 22, "蟹座"), (7, 23, "獅子座"), (8, 23, "乙女座"),
    (9, 23, "天秤座"), (10, 24, "蠍座"), (11, 23, "射手座"), (12, 22, "山羊座"),
]


def _ordinal(m, d):
    """うるう年の2/29は2/28として扱う（基準年2001の通し日）。"""
    if (m, d) == (2, 29):
        d = 28
    return date(2001, m, d).toordinal()


def sun_sign(month, day):
    """太陽星座の名前を返す。1/1-1/19 は山羊座（前年12/22から続く）。"""
    cur = "山羊座"
    for m, d, name in ZODIAC_STARTS:
        if (month, day) >= (m, d):
            cur = name
    return cur


def sun_sign_boundary(month, day):
    """切り替え日の前後1日（計3日）なら [前の星座, 次の星座] を返し、そうでなければ None。
    占星術では切り替えの時刻が年によって前後するため、この3日は本人に確認する。"""
    o = _ordinal(month, day)
    for m, d, name in ZODIAC_STARTS:
        if abs(o - _ordinal(m, d)) <= 1:
            return [sun_sign(*_prev_day(m, d)), name]
    return None


def _prev_day(m, d):
    o = date(2001, m, d).toordinal() - 1
    p = date.fromordinal(o)
    return p.month, p.day


def letter_value(ch):
    return (ord(ch) - ord("A")) % 9 + 1


def name_numbers(name):
    """ローマ字名から (表現数, ソウル数, 外見数)。A-Zのみ対象。Yは常に子音として扱う。"""
    letters = [c for c in name.upper() if "A" <= c <= "Z"]
    if not letters:
        return None
    allv = sum(letter_value(c) for c in letters)
    vow = sum(letter_value(c) for c in letters if c in VOWELS)
    con = sum(letter_value(c) for c in letters if c not in VOWELS)
    return {
        "expression": reduce_num(allv, True),
        "soul_urge": reduce_num(vow, True),
        "personality": reduce_num(con, True),
    }


def calculate(birth, name=None, target_year=2027):
    y, m, d = birth.year, birth.month, birth.day
    py = personal_year(m, d, target_year)
    res = {
        "birth_date": birth.isoformat(),
        "life_path": life_path(y, m, d),
        "life_path_alt": life_path_alt(y, m, d),
        "birth_number": birth_number(d),
        "target_year": target_year,
        "universal_year": reduce_num(digit_sum(target_year), False),
        "personal_year": py,
        "personal_months": personal_months(py),
    }
    res["sun_sign"] = sun_sign(m, d)
    res["sun_sign_boundary"] = sun_sign_boundary(m, d)
    res["life_path_differs_by_school"] = res["life_path"] != res["life_path_alt"]
    if name:
        res["name"] = name
        res["name_numbers"] = name_numbers(name)
    return res


def format_text(r):
    lines = [
        f"生年月日: {r['birth_date']}",
        f"ライフパスナンバー: {r['life_path']}"
        + (f"  ※別流派では {r['life_path_alt']}（鑑定文で流派差に触れるか確認）"
           if r["life_path_differs_by_school"] else ""),
        f"誕生数: {r['birth_number']}",
        f"{r['target_year']}年の個人年数(パーソナルイヤー): {r['personal_year']}"
        f"（その年の全体の数: {r['universal_year']}）",
        f"太陽星座: {r['sun_sign']}"
        + (f"  ※境目の日です。{'か'.join(r['sun_sign_boundary'])}のどちらか、依頼者に確認してから書く"
           if r["sun_sign_boundary"] else ""),
        "月ごとの数: " + " ".join(f"{k}月={v}" for k, v in r["personal_months"].items()),
    ]
    nn = r.get("name_numbers")
    if r.get("name"):
        if nn:
            lines.append(f"名前(ローマ字 {r['name']}): 表現数={nn['expression']} "
                         f"ソウル数={nn['soul_urge']} 外見数={nn['personality']}")
        else:
            lines.append("名前: A-Zの文字がないため計算しませんでした")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="数秘術の計算")
    p.add_argument("birth", help="生年月日 YYYY-MM-DD")
    p.add_argument("--name", help="ローマ字の名前（任意。例: Hanako Yamada）")
    p.add_argument("--year", type=int, default=2027, help="個人年数を出す年（既定2027）")
    p.add_argument("--json", action="store_true", help="JSONで出力")
    a = p.parse_args(argv)
    try:
        birth = date.fromisoformat(a.birth)
    except ValueError:
        print("生年月日は YYYY-MM-DD の形式で、実在する日付を入力してください（例: 1992-07-23）", file=sys.stderr)
        return 2
    r = calculate(birth, a.name, a.year)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else format_text(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
