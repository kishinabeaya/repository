#!/usr/bin/env python3
"""受付票の回答（JSON）の欠けを検出し、追加で聞くべき質問を1通にまとめて出力する。
使い方: python3 check_answers.py answers.json
終了コード: 0=そのまま制作に進める / 1=欠け・個人情報あり / 2=読み込みエラー
回答の作り方: 顧客の返信を読み、answers_template.json の形に、Claude Codeが書き起こす（JSONは標準ライブラリで読める）。"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from common import ORDER_RE, find_pii  # noqa: E402

TYPES = ("homepage", "lp", "automation", "data")

# キー: (追加質問の文面, 種類の一覧 or None=すべて)
REQUIRED = [
    ("business_name", "事業・サービスの名前", None),
    ("one_line", "何をしている事業か（1〜2文）", None),
    ("audience", "主なお客様はどんな方か", None),
    ("goal", "今回の制作で達成したいこと（1つ）", None),
    ("about", "事業の紹介に載せたい内容（事実だけ、数行）", ("homepage",)),
    ("services", "提供しているサービス・商品の名前と説明（1〜2文ずつ）", ("homepage",)),
    ("contact_method", "お問い合わせの受け方の種類（フォーム／メール／電話など。実際の連絡先は不要）", ("homepage", "lp")),
    ("offer", "紹介する商品・サービスの内容（数行）", ("lp",)),
    ("benefits", "特長・メリット（見出しと説明を3つ）", ("lp",)),
    ("cta_label", "ページ最後のボタンの文言", ("lp",)),
    ("current_process", "いま手作業でしている作業の流れ（順番に）", ("automation",)),
    ("input_format", "元になるデータの形式（Excel／CSVなど）", ("automation",)),
    ("desired_output", "仕上がりとして欲しいもの", ("automation",)),
    ("frequency", "作業の頻度と1回あたりの件数の目安", ("automation",)),
    ("environment", "使っている環境（Windows／Mac、Excel、Googleスプレッドシートなど）", ("automation",)),
    ("data_description", "集計するデータの内容と、おおよその件数", ("data",)),
    ("columns", "列（項目）の名前", ("data",)),
    ("questions", "知りたいことの具体的な内容", ("data",)),
    ("output_format", "仕上がりの形式", ("data",)),
]
EMPTY_WORDS = {"", "未定", "不明", "todo", "未記入", "わからない", "わかりません"}
# 「おまかせ」が通る項目（顧客が決められない項目）
OMAKASE_OK = {"contact_method"}
# 個人情報の検査から外す項目（顧客が自分から書いた、公開用の事業の連絡先）
PII_SKIP_KEYS = {"contact_text"}


def _empty(v):
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip().lower() in EMPTY_WORDS
    if isinstance(v, (list, dict)):
        return len(v) == 0
    return False


def _list_problems(key, v):
    """リスト項目の中身の欠けを、質問の補足文で返す。"""
    if key == "services":
        bad = [i + 1 for i, s in enumerate(v) if not isinstance(s, dict) or _empty(s.get("name")) or _empty(s.get("description"))]
        if bad:
            return "サービスの名前と説明（%s番目が空です）" % "・".join(map(str, bad))
    if key == "benefits":
        good = [b for b in v if isinstance(b, dict) and not _empty(b.get("title")) and not _empty(b.get("text"))]
        if len(good) < 3:
            return "特長・メリット（見出しと説明を、あと%d個）" % (3 - len(good))
    return None


def missing_fields(a):
    """[(キー, 質問文), ...]"""
    out = []
    t = a.get("type")
    if t not in TYPES:
        out.append(("type", "依頼の種類（ホームページ／LP／業務自動化／データ集計）"))
        return out
    oid = a.get("order_id")
    if not isinstance(oid, str) or not ORDER_RE.match(oid):
        out.append(("order_id", "（社内用）注文番号。英数字とハイフンのみ。個人名は使わない"))
    for key, q, kinds in REQUIRED:
        if kinds and t not in kinds:
            continue
        v = a.get(key)
        if _empty(v) or (isinstance(v, str) and v.strip() == "おまかせ" and key not in OMAKASE_OK and key in ("business_name", "one_line")):
            out.append((key, q))
            continue
        if isinstance(v, list):
            p = _list_problems(key, v)
            if p:
                out.append((key, p))
    return out


def pii_hits(a):
    """[(キー, 種類, 該当部分), ...]"""
    out = []

    def walk(key, v):
        if key in PII_SKIP_KEYS:
            return
        if isinstance(v, str):
            for kind, s in find_pii(v):
                out.append((key, kind, s))
        elif isinstance(v, list):
            for x in v:
                walk(key, x)
        elif isinstance(v, dict):
            for k2, x in v.items():
                walk("%s.%s" % (key, k2), x)

    for k, v in a.items():
        walk(k, v)
    return out


def ng_hits(a):
    """顧客の希望文に含まれる、そのまま載せられない表現（調整の連絡用）。"""
    from ngwords import find_hits
    out = []
    for k, v in a.items():
        if k in ("must_not_include", "order_id", "type"):
            continue
        texts = []
        if isinstance(v, str):
            texts = [v]
        elif isinstance(v, list):
            for x in v:
                texts.extend(x.values() if isinstance(x, dict) else [x])
        for t in texts:
            if isinstance(t, str):
                for _, cat, w, _ in find_hits(t):
                    out.append((k, cat, w))
    return out


def render(a):
    miss = missing_fields(a)
    pii = pii_hits(a)
    ng = ng_hits(a)
    lines = []
    if miss:
        lines.append("【お客様への追加質問（この1通で、すべて聞けます）】")
        lines.append("制作を進めるために、あと %d 点だけ教えてください。" % len(miss))
        for i, (_, q) in enumerate(miss, 1):
            lines.append("%d. %s" % (i, q))
        lines.append("わからない項目は「おまかせ」とお返事ください。")
    else:
        lines.append("【結果】必須項目はそろっています。制作に進めます。")
    if pii:
        lines.append("")
        lines.append("【社内メモ】個人情報らしき記載があります。制作物に入れず、記録からも除いてください。")
        for k, kind, s in pii:
            lines.append("- %s: %s（%s）" % (k, kind, re.sub(r"\S", "*", s)))
    if ng:
        lines.append("")
        lines.append("【社内メモ】次の表現は、そのまま載せません。事実に基づく言い方に直して制作します（必要なら、根拠をお客様に確認）。")
        for k, cat, w in ng:
            lines.append("- %s: 「%s」（%s）" % (k, w, cat))
    return "\n".join(lines) + "\n", bool(miss or pii)


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            a = json.load(f)
        if not isinstance(a, dict):
            raise ValueError("JSONの最上位はオブジェクトにしてください")
    except (OSError, ValueError) as e:
        print("読み込みエラー: %s" % e, file=sys.stderr)
        return 2
    text, bad = render(a)
    sys.stdout.write(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
