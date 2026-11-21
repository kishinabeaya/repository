#!/usr/bin/env python3
"""生成した静的サイトの検査。標準ライブラリのみ。結果をMarkdownのレポートにする。
使い方: python3 qa_site.py サイトのフォルダ [--report qa-report.md] [--allow 語 ...] [--require-sample-label]
終了コード: 0=合格（エラーなし） / 1=不合格 / 2=使い方の誤り
検査: HTML構文の基本、lang/title/viewport/charset、見出し階層、画像のalt、内部リンク切れ（ファイルと#アンカー）、
      id重複、CSSの色のコントラスト比（WCAG 2.x、4.5:1）、ファイルサイズ、外部読み込み、禁止・誇大表現。
機械的な検査です。人が読んで確認する作業は、納品チェックリストに残ります。"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ngwords import find_hits  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
OPTIONAL_END = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot", "option", "colgroup"}
MAX_HTML = 100_000
MAX_CSS = 60_000
MAX_TOTAL = 300_000
CONTRAST_MIN = 4.5
SAMPLE_LABEL = "サンプル（架空の事業者）"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []      # (行, 文)
        self.stack = []       # (タグ, 行)
        self.headings = []    # (レベル, 行)
        self.imgs = []
        self.links = []       # (属性, 値, 行)
        self.ids = {}
        self.dup_ids = []
        self.texts = []       # (行, 文字列)
        self.lang = None
        self.title = ""
        self.viewport = False
        self.charset = False
        self.skip_text = 0
        self.in_title = False
        self.h1 = 0
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        d = {k: (v if v is not None else "") for k, v in attrs}
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "meta":
            if d.get("name", "").lower() == "viewport" and "width=device-width" in d.get("content", ""):
                self.viewport = True
            if "charset" in d:
                self.charset = True
            if d.get("name", "").lower() == "description":
                self.texts.append((line, d.get("content", "")))
        if tag == "main":
            self.has_main = True
        if tag == "title":
            self.in_title = True
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.headings.append((int(tag[1]), line))
            if tag == "h1":
                self.h1 += 1
        if tag == "img":
            self.imgs.append((d, line))
            if d.get("alt"):
                self.texts.append((line, d["alt"]))
        if "id" in d:
            if d["id"] in self.ids:
                self.dup_ids.append((d["id"], line))
            self.ids[d["id"]] = line
        if tag == "a" and "href" in d:
            self.links.append(("href", d["href"], line))
        if tag == "img" and "src" in d:
            self.links.append(("src", d["src"], line))
        if tag == "script":
            if d.get("src"):
                self.links.append(("src", d["src"], line))
        if tag == "link" and "href" in d:
            self.links.append(("href", d["href"], line))
        if d.get("title"):
            self.texts.append((line, d["title"]))
        if tag in ("script", "style"):
            self.skip_text += 1
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            if tag in ("script", "style"):
                self.skip_text -= 1

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag in VOID:
            return
        if tag == "title":
            self.in_title = False
        names = [t for t, _ in self.stack]
        if tag in names:
            while self.stack:
                t, ln = self.stack.pop()
                if t in ("script", "style"):
                    self.skip_text -= 1
                if t == tag:
                    break
                if t not in OPTIONAL_END:
                    self.errors.append((ln, "<%s>（%d行目）が閉じられていません" % (t, ln)))
        else:
            self.errors.append((line, "対応する開始タグのない </%s>" % tag))

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.skip_text == 0 and data.strip():
            self.texts.append((self.getpos()[0], data))

    def finish(self):
        for t, ln in self.stack:
            if t not in OPTIONAL_END and t not in ("html", "body", "head"):
                self.errors.append((ln, "<%s>（%d行目）が閉じられていません" % (t, ln)))


# ---------- 色のコントラスト ----------
NAMED = {"white": (255, 255, 255), "black": (0, 0, 0)}


def parse_color(s):
    s = s.strip().lower()
    if s in NAMED:
        return NAMED[s]
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", s)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    l1, l2 = luminance(c1), luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def css_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css)]


def css_decls(body):
    d = {}
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            d[k.strip().lower()] = re.sub(r"\s*!important", "", v.strip(), flags=re.I)
    return d


def check_contrast(css):
    """[(selector, fg, bg, ratio, ok)], [解釈できなかった指定]"""
    rules = css_rules(css)
    vars_ = {}
    for sel, body in rules:
        if sel.strip() == ":root":
            for k, v in css_decls(body).items():
                if k.startswith("--"):
                    vars_[k] = v

    def resolve(v):
        for _ in range(5):
            m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*\)", v.strip())
            if not m:
                return v
            v = vars_.get(m.group(1), "")
        return v

    body_decl = {}
    for sel, body in rules:
        if sel.strip() == "body":
            body_decl = css_decls(body)
    base_fg = parse_color(resolve(body_decl.get("color", ""))) if body_decl else None
    base_bg = parse_color(resolve(body_decl.get("background", body_decl.get("background-color", "")))) if body_decl else None
    results, skipped = [], []
    for sel, body in rules:
        if sel.strip() == ":root":
            continue
        d = css_decls(body)
        fg_raw = d.get("color")
        bg_raw = d.get("background-color", d.get("background"))
        if fg_raw is None and bg_raw is None:
            continue
        fg = parse_color(resolve(fg_raw)) if fg_raw else base_fg
        bg = parse_color(resolve(bg_raw.split()[0] if bg_raw and not bg_raw.startswith("var") else bg_raw)) if bg_raw else base_bg
        if fg is None or bg is None:
            skipped.append(sel)
            continue
        r = contrast_ratio(fg, bg)
        results.append((sel, fg, bg, r, r >= CONTRAST_MIN))
    return results, skipped


def hexs(rgb):
    return "#%02x%02x%02x" % rgb


# ---------- 検査本体 ----------
def run_qa(site_dir, allow=(), require_sample_label=False):
    """{'items': [(区分, 重大度, 文)], 'errors': n, 'warnings': n, 'files': [...], 'contrast': [...]}"""
    items = []

    def add(cat, sev, msg):
        items.append((cat, sev, msg))

    files = sorted(os.listdir(site_dir))
    htmls = [f for f in files if f.endswith(".html")]
    csss = [f for f in files if f.endswith(".css")]
    if not htmls:
        add("構成", "error", "HTMLファイルがありません")
    if "index.html" not in files:
        add("構成", "error", "index.html がありません")
    total = 0
    pages = {}
    for f in files:
        size = os.path.getsize(os.path.join(site_dir, f))
        total += size
        if f.endswith(".html") and size > MAX_HTML:
            add("ファイルサイズ", "error", "%s が %d バイト（上限 %d）" % (f, size, MAX_HTML))
        if f.endswith(".css") and size > MAX_CSS:
            add("ファイルサイズ", "error", "%s が %d バイト（上限 %d）" % (f, size, MAX_CSS))
    if total > MAX_TOTAL:
        add("ファイルサイズ", "error", "全体 %d バイト（上限 %d）" % (total, MAX_TOTAL))
    for f in htmls:
        with open(os.path.join(site_dir, f), encoding="utf-8") as fh:
            src = fh.read()
        p = Page()
        p.feed(src)
        p.close()
        p.finish()
        pages[f] = p
    for f, p in pages.items():
        for ln, msg in p.errors:
            add("HTML構文", "error", "%s: %s" % (f, msg))
        if not p.lang:
            add("アクセシビリティ", "error", "%s: <html lang> がありません" % f)
        if not p.title.strip():
            add("アクセシビリティ", "error", "%s: <title> がないか空です" % f)
        if not p.viewport:
            add("スマホ表示", "error", "%s: viewport（width=device-width）がありません" % f)
        if not p.charset:
            add("HTML構文", "error", "%s: 文字コード（meta charset）の指定がありません" % f)
        if not p.has_main:
            add("アクセシビリティ", "warn", "%s: <main> がありません" % f)
        if p.h1 != 1:
            add("見出し", "error", "%s: h1 が %d 個です（1個にします）" % (f, p.h1))
        prev = 0
        for lvl, ln in p.headings:
            if prev and lvl > prev + 1:
                add("見出し", "error", "%s: %d行目の h%d が h%d の次にあり、階層が飛んでいます" % (f, ln, lvl, prev))
            prev = lvl
        for d, ln in p.imgs:
            if "alt" not in d:
                add("画像alt", "error", "%s: %d行目の <img> に alt がありません" % (f, ln))
        for i, ln in p.dup_ids:
            add("HTML構文", "error", "%s: id「%s」が重複しています（%d行目）" % (f, i, ln))
        contact_like = False
        for attr, val, ln in p.links:
            v = val.strip()
            if v.startswith(("mailto:", "tel:")):
                contact_like = True
                continue
            if v.startswith(("javascript:", "data:")):
                add("リンク", "error", "%s: %d行目 %s は使えません" % (f, ln, v[:20]))
                continue
            if re.match(r"^(https?:)?//", v):
                add("外部読み込み", "warn", "%s: %d行目 外部の参照「%s」（表示速度・プライバシーの確認が必要）" % (f, ln, v[:50]))
                if f == "contact.html":
                    contact_like = True
                continue
            if v in ("", "#"):
                add("リンク", "error" if v == "" else "warn", "%s: %d行目 %s が空です" % (f, ln, attr))
                continue
            u = urlparse(v)
            target = unquote(u.path) or f
            tpath = os.path.normpath(os.path.join(site_dir, target))
            if not tpath.startswith(os.path.normpath(site_dir)) or not os.path.isfile(tpath):
                add("リンク", "error", "%s: %d行目 リンク先「%s」が見つかりません" % (f, ln, v))
                continue
            if u.fragment and target.endswith(".html"):
                tp = pages.get(os.path.basename(target))
                if tp is not None and u.fragment not in tp.ids:
                    add("リンク", "error", "%s: %d行目 アンカー「#%s」が %s にありません" % (f, ln, u.fragment, target))
        if f == "contact.html" and not contact_like and SAMPLE_LABEL not in src:
            add("問い合わせ先", "warn", "contact.html に、問い合わせ先の実体（mailto・tel・リンク）がありません。納品前に入れる方法を、お客様に案内してください")
        # 禁止表現
        seen = set()
        for ln, t in p.texts:
            for _, cat, w, _line in find_hits(t, allow):
                if (ln, w) not in seen:
                    seen.add((ln, w))
                    add("禁止・誇大表現", "error", "%s: %d行目 [%s]「%s」: %s" % (f, ln, cat, w, t.strip()[:40]))
        if require_sample_label and SAMPLE_LABEL not in src:
            add("サンプル表示", "error", "%s: 「%s」の表示がありません" % (f, SAMPLE_LABEL))
    # CSS
    contrast = []
    skipped = []
    for f in csss:
        with open(os.path.join(site_dir, f), encoding="utf-8") as fh:
            css = fh.read()
        res, sk = check_contrast(css)
        contrast.extend(res)
        skipped.extend(sk)
        if "@media" not in css:
            add("スマホ表示", "warn", "%s に @media（レスポンシブ）がありません" % f)
        for m in re.finditer(r"url\(\s*['\"]?(https?:)?//[^)]*\)|@import", css):
            add("外部読み込み", "warn", "%s: 外部のCSS参照があります（%s）" % (f, m.group(0)[:40]))
    if htmls and not csss:
        add("構成", "warn", "CSSファイルがありません")
    for sel, fg, bg, r, ok in contrast:
        if not ok:
            add("コントラスト", "error", "%s: 文字 %s / 背景 %s = %.2f:1（%.1f:1 未満）" % (sel, hexs(fg), hexs(bg), r, CONTRAST_MIN))
    for sel in skipped:
        add("コントラスト", "warn", "%s: 色を解釈できず、検査できませんでした" % sel)
    return {
        "items": items,
        "errors": sum(1 for i in items if i[1] == "error"),
        "warnings": sum(1 for i in items if i[1] == "warn"),
        "files": [(f, os.path.getsize(os.path.join(site_dir, f))) for f in files],
        "contrast": contrast,
        "total": total,
        "n_html": len(htmls),
    }


CATEGORIES = ["構成", "HTML構文", "アクセシビリティ", "見出し", "画像alt", "リンク", "スマホ表示",
              "コントラスト", "ファイルサイズ", "外部読み込み", "禁止・誇大表現", "問い合わせ先", "サンプル表示"]


def render_report(result, site_dir):
    ok = result["errors"] == 0
    L = ["# サイト検査レポート", "",
         "- 対象: `%s`" % site_dir,
         "- 結果: **%s**（エラー %d 件、注意 %d 件）" % ("合格" if ok else "不合格", result["errors"], result["warnings"]),
         "- HTML %d ファイル、合計 %d バイト" % (result["n_html"], result["total"]),
         "- この検査は機械的です。文章の内容・事実との一致・見た目は、人が確認します（納品チェックリスト参照）。", "",
         "## 区分ごとの結果", "", "| 区分 | エラー | 注意 |", "|---|---|---|"]
    for c in CATEGORIES:
        e = sum(1 for i in result["items"] if i[0] == c and i[1] == "error")
        w = sum(1 for i in result["items"] if i[0] == c and i[1] == "warn")
        L.append("| %s | %d | %d |" % (c, e, w))
    L += ["", "## 指摘の一覧", ""]
    if not result["items"]:
        L.append("指摘はありません。")
    for cat, sev, msg in result["items"]:
        L.append("- [%s] %s: %s" % ("エラー" if sev == "error" else "注意", cat, msg))
    L += ["", "## 色のコントラスト比（WCAG、基準 %.1f:1）" % CONTRAST_MIN, "",
          "| 指定 | 文字 | 背景 | 比 | 判定 |", "|---|---|---|---|---|"]
    for sel, fg, bg, r, okk in result["contrast"]:
        L.append("| `%s` | %s | %s | %.2f | %s |" % (sel.replace("|", "/")[:50], hexs(fg), hexs(bg), r, "OK" if okk else "NG"))
    L += ["", "## ファイル", ""]
    for f, s in result["files"]:
        L.append("- %s（%d バイト）" % (f, s))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="静的サイトの検査")
    ap.add_argument("site_dir")
    ap.add_argument("--report")
    ap.add_argument("--allow", nargs="*", default=[], help="根拠があり、人が許可する語")
    ap.add_argument("--require-sample-label", action="store_true")
    args = ap.parse_args(argv)
    if not os.path.isdir(args.site_dir):
        print("フォルダがありません: %s" % args.site_dir, file=sys.stderr)
        return 2
    res = run_qa(args.site_dir, tuple(args.allow), args.require_sample_label)
    rep = render_report(res, args.site_dir)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(rep)
    sys.stdout.write(rep)
    return 0 if res["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
