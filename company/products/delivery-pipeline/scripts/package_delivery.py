#!/usr/bin/env python3
"""納品物のパッケージ化。標準ライブラリのみ。
使い方: python3 package_delivery.py --site サイトのフォルダ --answers answers.json --out 出力フォルダ [--force]
出力（出力フォルダ/<order_id>/）:
  <order_id>-site.zip   納品用ZIP（サイト一式 + README.md）
  DELIVERY_MESSAGE.md   納品メッセージの下書き（お客様宛。CEOが転記）
  REVISION_REQUEST.md   修正依頼の受け方の文面（お客様宛。1回で必要な情報を聞く）
  CHECKLIST.md          納品チェックリスト（社内用。担当 claude / ceo つき）
  qa-report.md          検査レポート（社内用）
検査に不合格ならZIPを作らない（--force で上書き。強制した事実はチェックリストに残る）。"""
import argparse
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import ORDER_RE  # noqa: E402
from qa_site import render_report, run_qa  # noqa: E402

FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # 同じ入力から同じZIPを作る


def readme_text(a, qa):
    ext = [i for i in qa["items"] if i[0] == "外部読み込み"]
    ext_line = ("外部のフォント・画像・スクリプトは使っていません（検査で確認）。" if not ext
                else "外部の参照が含まれています。検査レポートを確認してください。")
    name = a.get("business_name", "")
    return "\n".join([
        "# %s ホームページ 納品物の使い方" % name, "",
        "## 中身",
        "- `site/` フォルダ: ホームページ本体（HTMLとCSS）。",
        "- このファイル（README.md）: 使い方。", "",
        "## 見てみる",
        "1. ZIPを展開します。",
        "2. `site/index.html` をダブルクリックすると、ブラウザで表示されます。",
        "3. スマホでの見え方は、パソコンのブラウザの幅を狭めても確認できます。", "",
        "## 公開する",
        "- 公開（ホスティング）は、お客様ご自身で、お使いのサーバーやサービスにファイルを置いて行います。",
        "- 公開作業を依頼に含むかどうかは、出品ページの記載に従います。",
        "- `site/` の中のファイルを、すべて同じフォルダに置いてください。", "",
        "## 文章・問い合わせ先の差し替え",
        "- HTMLファイルをテキストエディタ（メモ帳など）で開き、文章を直接書き換えられます。",
        "- 問い合わせ先は、`<!-- 差し替え箇所 -->` と書いたコメントの場所に、お客様ご自身のリンクやアドレスを入れてください。",
        "- 書き換えたあとは、ブラウザで表示して確認してください。", "",
        "## 作り方について",
        "- 制作には、AI（Claude Code）を補助として使い、人が内容を確認しています。",
        "- %s" % ext_line,
        "- 使用した素材は、文章と図形（CSSと簡単な図）のみです。写真・イラスト・フォントの追加はありません。", "",
        "## 修正のご依頼",
        "- 同梱の方針に沿って、修正したい箇所を、まとめてお知らせください（メッセージの文面は別紙）。", "",
        "## 注意",
        "- 掲載内容（価格・営業時間・実績など）が事実と合っているかは、公開前にお客様ご自身でご確認ください。",
        "- 法令（景品表示法、特定商取引法など）への適合の判断は、制作の範囲に含まれません。",
    ]) + "\n"


def delivery_message(a):
    return "\n".join([
        "ご依頼ありがとうございました。ご依頼の内容にそって制作したものを、お届けします。", "",
        "【お渡しするもの】",
        "・%s-site.zip（ホームページ一式と、使い方の説明 README.md）" % a["order_id"], "",
        "【ご確認のお願い】",
        "1. ZIPを展開し、site/index.html をブラウザで開いてください。",
        "2. 文章・価格・営業時間などが、事実と合っているか、ご確認ください。",
        "3. 問い合わせ先は、README.md の手順で、ご自身の情報を入れてください。", "",
        "【修正をご希望の場合】",
        "別紙の「修正のご依頼」の項目に、まとめてお答えください。1回のお返事で、修正に必要な情報がそろうようにしています。", "",
        "制作には、AI（Claude Code）を補助として使い、人が内容を確認しています。",
    ]) + "\n"


def revision_request():
    return "\n".join([
        "【修正のご依頼】次の項目を、まとめてお知らせください。（1回のお返事で、修正に必要な情報がそろいます）", "",
        "1. 直したいページと場所: （例: contact.html の「お問い合わせ方法」の2行目）",
        "2. 直したあとの内容: （文章は、載せたい形のまま書いてください）",
        "3. 追加したい項目があれば、その内容と、置きたい場所:",
        "4. 見た目の変更があれば、具体的に: （例: 見出しの色をもう少し濃く、サービスの並びを入れ替え）",
        "5. 優先順位: 公開までに必ず直したいものに、○をつけてください。",
        "6. 確認した環境: （パソコン／スマホ、ブラウザの名前。表示の不具合の場合は、どう見えたか）", "",
        "【お願い】",
        "・お名前、ご住所、電話番号、メールアドレスなどの個人情報は、書かないでください。",
        "・修正の回数や範囲は、出品ページの記載に従います。",
        "・内容を確認したうえで、修正版をお届けします。事実と異なる表現や、誇大な表現になる修正は、言い方を相談させてください。",
    ]) + "\n"


def checklist(a, qa, forced):
    oid = a["order_id"]
    status = "合格" if qa["errors"] == 0 else "不合格（--force で強制作成）"
    L = ["# 納品チェックリスト（%s）" % oid, "",
         "- 自動検査: %s（エラー %d 件、注意 %d 件。詳細は qa-report.md）" % (status, qa["errors"], qa["warnings"]), ""]
    if forced and qa["errors"]:
        L += ["**警告: 検査が不合格のまま作成しています。エラーを解消してから納品してください。**", ""]
    L += ["## Claude Codeの作業（完了したら [x]）",
          "- [ ] 受付票の回答に欠けがない（intake/check_answers.py）",
          "- [ ] サイトを生成した（scripts/build_site.py）",
          "- [ ] 検査に合格した（scripts/qa_site.py）",
          "- [ ] 掲載内容が、受付票の回答と一致している（回答にない実績・口コミ・肩書き・数字を足していない）",
          "- [ ] 禁止・誇大表現が残っていない（検査 + 目で読む）",
          "- [ ] 医療・法律・投資の効果の主張がない",
          "- [ ] ZIPを展開して、index.html が開くことを確認した",
          "- [ ] 工程の記録を残した（scripts/log_step.py）", "",
          "## CEOの作業（完了したら [x]）",
          "- [ ] プラットフォームの規約に照らして、納品の方法（ファイルの納品、AI利用の記載）を確認した",
          "- [ ] 納品メッセージ（DELIVERY_MESSAGE.md）と修正依頼の文面（REVISION_REQUEST.md）を、お客様に転記した",
          "- [ ] ZIPを、プラットフォームの納品機能で送った",
          "- [ ] 入金（売上の確定）を確認した",
          "- [ ] お客様の返信があれば、Claude Codeに転記した", "",
          "## 納品後",
          "- [ ] 修正の依頼が来たら REVISION_REQUEST.md の項目で整理し、1回の修正で対応する",
          "- [ ] 数字（所要時間・担当）を report_share.py で集計し、CEOの割合を確認する"]
    return "\n".join(L) + "\n"


def package(site_dir, answers, out_dir, force=False):
    """作成したフォルダのパスを返す。検査不合格で force なしなら ValueError。"""
    oid = answers.get("order_id", "")
    if not ORDER_RE.match(str(oid)):
        raise ValueError("order_id が不正です（英数字・ハイフン・下線のみ、40字まで）")
    qa = run_qa(site_dir, require_sample_label=bool(answers.get("is_sample")))
    if qa["errors"] and not force:
        raise ValueError("検査が不合格です（エラー %d 件）。直してから再実行してください" % qa["errors"])
    dest = os.path.join(out_dir, oid)
    os.makedirs(dest, exist_ok=True)

    def w(name, text):
        with open(os.path.join(dest, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    w("qa-report.md", render_report(qa, site_dir))
    w("DELIVERY_MESSAGE.md", delivery_message(answers))
    w("REVISION_REQUEST.md", revision_request())
    w("CHECKLIST.md", checklist(answers, qa, force))
    zpath = os.path.join(dest, "%s-site.zip" % oid)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        def put(arc, data):
            zi = zipfile.ZipInfo(arc, FIXED_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        put("README.md", readme_text(answers, qa).encode("utf-8"))
        for f in sorted(os.listdir(site_dir)):
            p = os.path.join(site_dir, f)
            if os.path.isfile(p):
                with open(p, "rb") as fh:
                    put("site/" + f, fh.read())
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(description="納品物のパッケージ化")
    ap.add_argument("--site", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.answers, encoding="utf-8") as f:
            a = json.load(f)
        dest = package(args.site, a, args.out, args.force)
    except (OSError, ValueError) as e:
        print("作成できませんでした: %s" % e, file=sys.stderr)
        return 1
    print("作成しました: %s" % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
