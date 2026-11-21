#!/usr/bin/env python3
"""受付票の回答（JSON）から、静的なホームページ・LPを生成する。標準ライブラリのみ。
使い方: python3 build_site.py --answers answers.json --out 出力フォルダ [--theme clean|warm]
  type が homepage → index.html / about.html / contact.html、lp → index.html（1ページ）。style.css も出力。
回答に欠けがあれば生成しない（intake/check_answers.py と同じ判定）。"""
import argparse
import html
import json
import os
import sys
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMPLATES = os.path.join(ROOT, "templates")
sys.path.insert(0, os.path.join(ROOT, "intake"))
from check_answers import missing_fields  # noqa: E402

THEMES = ("clean", "warm")
SAMPLE_LABEL = "サンプル（架空の事業者）"
E = html.escape


def _read(name):
    with open(os.path.join(TEMPLATES, name), encoding="utf-8") as f:
        return f.read()


def _s(a, key, default=""):
    v = a.get(key, default)
    return v.strip() if isinstance(v, str) else default


def _paras(text):
    """改行で段落に分ける。"""
    return "".join("<p>%s</p>\n" % E(p.strip()) for p in text.replace("\r", "").split("\n") if p.strip())


def _deco():
    return ('<svg class="deco" aria-hidden="true" focusable="false" viewBox="0 0 64 64">'
            '<circle cx="32" cy="32" r="26"/></svg>\n')


def _banner(a):
    if a.get("is_sample"):
        return '<div class="sample-banner" role="note">%s ／ 実在の事業者・依頼・実績ではありません</div>\n' % SAMPLE_LABEL
    return ""


def _footer(a):
    name = E(_s(a, "business_name"))
    lines = ["<p>&copy; %s</p>\n" % name]
    if a.get("is_sample"):
        lines.append("<p>このページは制作例です。%s。掲載内容はすべて作例のための創作です。</p>\n" % SAMPLE_LABEL)
    if a.get("show_ai_note"):
        lines.append("<p>このページは、AI（Claude Code）を補助に使い、人が確認して制作しました。</p>\n")
    return "".join(lines)


def _nav(pages, current):
    items = []
    for href, label in pages:
        cur = ' aria-current="page"' if href == current else ""
        items.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, E(label)))
    return '<nav aria-label="メイン"><ul>\n%s\n</ul></nav>\n' % "\n".join(items)


def _render(a, title, description, body, pages, current):
    return Template(_read("page.html")).substitute(
        title=E(title), description=E(description), banner=_banner(a),
        brand=E(_s(a, "business_name")), nav=_nav(pages, current), body=body, footer=_footer(a))


def _cards(items, three=False):
    out = ['<div class="grid%s">\n' % (" three" if three else "")]
    for it in items:
        out.append('<div class="card">\n<h3>%s</h3>\n<p>%s</p>\n' % (E(it[0]), E(it[1])))
        if len(it) > 2 and it[2]:
            out.append('<p class="price">%s</p>\n' % E(it[2]))
        out.append("</div>\n")
    out.append("</div>\n")
    return "".join(out)


def _contact_block(a):
    method = _s(a, "contact_method", "お問い合わせ")
    if a.get("is_sample"):
        return "<p>%s。サンプルのため、実際の問い合わせ先は設けていません。</p>\n" % E(SAMPLE_LABEL)
    text = _s(a, "contact_text")
    body = "<p>お問い合わせは、「%s」で受け付けています。</p>\n" % E(method)
    if text:
        body += _paras(text)
    else:
        body += "<!-- 差し替え箇所: ここに、実際の問い合わせ先（リンクやアドレス）を入れてください -->\n"
    return body


def build_homepage(a):
    pages = [("index.html", "ホーム"), ("about.html", "事業のご紹介"), ("contact.html", "お問い合わせ")]
    name = _s(a, "business_name")
    services = [(s["name"].strip(), s["description"].strip(), (s.get("price") or "").strip())
                for s in a["services"]]
    hero = ('<section class="hero">\n<div class="wrap">\n%s<h1>%s</h1>\n<p>%s</p>\n'
            '<a class="btn" href="contact.html">お問い合わせ方法を見る</a>\n</div>\n</section>\n'
            % (_deco(), E(name), E(_s(a, "one_line"))))
    svc = ('<section id="services">\n<div class="wrap">\n<h2>サービス</h2>\n%s</div>\n</section>\n'
           % _cards(services, three=len(services) % 3 == 0))
    idx_body = hero + svc
    strengths = [x.strip() for x in a.get("strengths", []) if isinstance(x, str) and x.strip()]
    if strengths:
        idx_body += ('<section id="strengths">\n<div class="wrap">\n<h2>大切にしていること</h2>\n<ul>\n%s</ul>\n'
                     '</div>\n</section>\n' % "".join("<li>%s</li>\n" % E(x) for x in strengths))
    about = ('<section>\n<div class="wrap">\n<h1>事業のご紹介</h1>\n<h2>%s について</h2>\n%s</div>\n</section>\n'
             % (E(name), _paras(_s(a, "about"))))
    notes = []
    if _s(a, "hours_note"):
        notes.append(("営業時間・対応エリア", _s(a, "hours_note")))
    if notes:
        about += '<section>\n<div class="wrap">\n<h2>%s</h2>\n%s</div>\n</section>\n' % (E(notes[0][0]), _paras(notes[0][1]))
    contact = ('<section>\n<div class="wrap">\n<h1>お問い合わせ</h1>\n<h2>お問い合わせ方法</h2>\n%s</div>\n</section>\n'
               % _contact_block(a))
    desc = _s(a, "one_line")
    return {
        "index.html": _render(a, name, desc, idx_body, pages, "index.html"),
        "about.html": _render(a, "事業のご紹介｜" + name, desc, about, pages, "about.html"),
        "contact.html": _render(a, "お問い合わせ｜" + name, desc, contact, pages, "contact.html"),
    }


def build_lp(a):
    name = _s(a, "business_name")
    pages = [("#benefits", "特長"), ("#flow", "ご利用の流れ"), ("#faq", "よくある質問"), ("#contact", "お問い合わせ")]
    pages = [p for p in pages if not (p[0] == "#flow" and not a.get("steps")) and not (p[0] == "#faq" and not a.get("faq"))]
    benefits = [(b["title"].strip(), b["text"].strip()) for b in a["benefits"]]
    body = ('<section class="hero">\n<div class="wrap">\n%s<h1>%s</h1>\n<p>%s</p>\n%s'
            '<a class="btn" href="#contact">%s</a>\n</div>\n</section>\n'
            % (_deco(), E(_s(a, "one_line")), E(name), _paras(_s(a, "offer")), E(_s(a, "cta_label"))))
    body += ('<section id="benefits">\n<div class="wrap">\n<h2>特長</h2>\n%s</div>\n</section>\n'
             % _cards(benefits, three=len(benefits) % 3 == 0))
    steps = [x.strip() for x in a.get("steps", []) if isinstance(x, str) and x.strip()]
    if steps:
        body += ('<section id="flow">\n<div class="wrap">\n<h2>ご利用の流れ</h2>\n<ol class="steps">\n%s</ol>\n'
                 '</div>\n</section>\n' % "".join("<li>%s</li>\n" % E(x) for x in steps))
    faq = [f for f in a.get("faq", []) if isinstance(f, dict) and f.get("q") and f.get("a")]
    if faq:
        body += ('<section id="faq">\n<div class="wrap">\n<h2>よくある質問</h2>\n<dl class="faq">\n%s</dl>\n'
                 '</div>\n</section>\n' % "".join("<dt>%s</dt>\n<dd>%s</dd>\n" % (E(f["q"]), E(f["a"])) for f in faq))
    price = _paras(_s(a, "price_note")) if _s(a, "price_note") else ""
    body += ('<section id="contact" class="cta">\n<div class="wrap">\n<h2>お問い合わせ</h2>\n%s%s</div>\n</section>\n'
             % (price, _contact_block(a)))
    return {"index.html": _render(a, name, _s(a, "one_line"), body, pages, "index.html")}


def build(a, out_dir, theme=None):
    """生成して、書き出したファイル名の一覧を返す。欠けがあれば ValueError。"""
    miss = missing_fields(a)
    if miss:
        raise ValueError("回答に欠けがあります: " + "、".join(k for k, _ in miss))
    t = a.get("type")
    if t not in ("homepage", "lp"):
        raise ValueError("build_site.py は homepage / lp 専用です（type=%s）" % t)
    theme = theme or _s(a, "theme", "clean")
    if theme not in THEMES:
        theme = "clean"
    files = build_homepage(a) if t == "homepage" else build_lp(a)
    css = _read("theme-%s.css" % theme) + "\n" + _read("base.css")
    os.makedirs(out_dir, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
    with open(os.path.join(out_dir, "style.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(css)
    return sorted(files) + ["style.css"]


def main(argv=None):
    p = argparse.ArgumentParser(description="受付票の回答から静的サイトを生成")
    p.add_argument("--answers", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--theme", choices=THEMES)
    args = p.parse_args(argv)
    try:
        with open(args.answers, encoding="utf-8") as f:
            a = json.load(f)
        files = build(a, args.out, args.theme)
    except (OSError, ValueError) as e:
        print("生成できませんでした: %s" % e, file=sys.stderr)
        return 1
    print("生成しました: %s（%s）" % (args.out, "、".join(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
