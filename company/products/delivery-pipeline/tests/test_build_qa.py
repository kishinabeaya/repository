import json
import os
import shutil
import tempfile
import unittest

import _paths
import build_site
import ngwords
import qa_site

ROOT = _paths.ROOT
SAMPLES = ("bakery", "spreadsheet-lp", "garden")


def answers(name):
    with open(os.path.join(ROOT, "samples", name, "answers.json"), encoding="utf-8") as f:
        return json.load(f)


class Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def build(self, name, theme=None, mutate=None):
        a = answers(name)
        if mutate:
            mutate(a)
        out = os.path.join(self.tmp, name)
        build_site.build(a, out, theme)
        return out

    def rewrite(self, path, fn):
        with open(path, encoding="utf-8") as f:
            s = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn(s))

    def msgs(self, res, cat):
        return [m for c, s, m in res["items"] if c == cat and s == "error"]


class TestBuild(Tmp):
    def test_homepage_files(self):
        out = self.build("bakery")
        self.assertEqual(sorted(os.listdir(out)), ["about.html", "contact.html", "index.html", "style.css"])

    def test_lp_single_page(self):
        out = self.build("spreadsheet-lp")
        self.assertEqual(sorted(os.listdir(out)), ["index.html", "style.css"])

    def test_html_basics(self):
        out = self.build("bakery")
        s = _paths.read(os.path.join(out, "index.html"))
        self.assertIn('<html lang="ja">', s)
        self.assertIn('name="viewport"', s)
        self.assertIn("サンプル（架空の事業者）", s)

    def test_escaping(self):
        out = self.build("bakery", mutate=lambda a: a.update(about="<script>alert(1)</script>"))
        s = _paths.read(os.path.join(out, "about.html"))
        self.assertNotIn("<script>", s)
        self.assertIn("&lt;script&gt;", s)

    def test_both_themes_pass_contrast(self):
        for theme in ("clean", "warm"):
            out = self.build("garden", theme)
            res = qa_site.run_qa(out)
            self.assertEqual(self.msgs(res, "コントラスト"), [], theme)
            self.assertGreater(len(res["contrast"]), 5)

    def test_refuses_incomplete(self):
        with self.assertRaises(ValueError):
            build_site.build({"type": "lp", "order_id": "A"}, os.path.join(self.tmp, "x"))

    def test_refuses_other_types(self):
        a = answers("bakery")
        a["type"] = "automation"
        with self.assertRaises(ValueError):
            build_site.build(a, os.path.join(self.tmp, "y"))

    def test_no_sample_banner_when_not_sample(self):
        out = self.build("bakery", mutate=lambda a: a.update(is_sample=False))
        s = _paths.read(os.path.join(out, "index.html"))
        self.assertNotIn("サンプル（架空", s)

    def test_contact_marker_when_not_sample(self):
        out = self.build("bakery", mutate=lambda a: a.update(is_sample=False))
        s = _paths.read(os.path.join(out, "contact.html"))
        self.assertIn("差し替え箇所", s)
        res = qa_site.run_qa(out)
        self.assertTrue([m for c, sv, m in res["items"] if c == "問い合わせ先"])


class TestQA(Tmp):
    def test_samples_pass(self):
        for name in SAMPLES:
            res = qa_site.run_qa(os.path.join(ROOT, "samples", name, "site"), require_sample_label=True)
            self.assertEqual(res["errors"], 0, (name, res["items"]))

    def test_samples_regenerate_pass(self):
        for name in SAMPLES:
            out = self.build(name)
            res = qa_site.run_qa(out, require_sample_label=True)
            self.assertEqual(res["errors"], 0, (name, res["items"]))

    def test_committed_samples_are_up_to_date(self):
        for name in SAMPLES:
            out = self.build(name)
            for f in os.listdir(out):
                self.assertEqual(_paths.read(os.path.join(out, f)),
                                 _paths.read(os.path.join(ROOT, "samples", name, "site", f)), (name, f))

    def test_broken_html_fails(self):
        out = self.build("bakery")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace("</div>\n</section>\n<section id=\"services\">", "</section>\n<section id=\"services\">", 1))
        res = qa_site.run_qa(out)
        self.assertTrue(self.msgs(res, "HTML構文"))

    def test_missing_alt(self):
        out = self.build("garden")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace("<main id=\"main\">", '<main id="main"><img src="style.css">', 1))
        self.assertTrue(self.msgs(qa_site.run_qa(out), "画像alt"))

    def test_broken_link_and_anchor(self):
        out = self.build("bakery")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace('href="about.html"', 'href="gone.html"', 1).replace('href="contact.html"', 'href="about.html#nothing"', 1))
        m = self.msgs(qa_site.run_qa(out), "リンク")
        self.assertTrue(any("gone.html" in x for x in m))
        self.assertTrue(any("#nothing" in x for x in m))

    def test_heading_skip_and_two_h1(self):
        out = self.build("garden")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace("<h2>サービス</h2>", "<h4>サービス</h4><h1>二つ目</h1>", 1))
        m = self.msgs(qa_site.run_qa(out), "見出し")
        self.assertGreaterEqual(len(m), 2)
        self.assertTrue(any("h1 が 2 個" in x for x in m))

    def test_no_viewport_no_lang(self):
        out = self.build("garden")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', "").replace(' lang="ja"', ""))
        res = qa_site.run_qa(out)
        self.assertTrue(self.msgs(res, "スマホ表示"))
        self.assertTrue(self.msgs(res, "アクセシビリティ"))

    def test_low_contrast_fails(self):
        out = self.build("garden")
        self.rewrite(os.path.join(out, "style.css"), lambda s: s.replace("--muted: #4b5563", "--muted: #cccccc") + "\n.note { color: #cccccc; }\n")
        m = self.msgs(qa_site.run_qa(out), "コントラスト")
        self.assertTrue(m)

    def test_ng_words_fail(self):
        for word in ("必ず", "絶対", "No.1", "業界最安", "今すぐ", "限定"):
            out = self.build("garden", mutate=lambda a, w=word: a.update(about="当店は%sお得です" % w))
            res = qa_site.run_qa(out)
            self.assertTrue(self.msgs(res, "禁止・誇大表現"), word)
            self.assertGreater(res["errors"], 0)

    def test_allow_option(self):
        out = self.build("garden", mutate=lambda a: a.update(about="全国の賞を受賞しました（根拠あり）"))
        self.assertTrue(self.msgs(qa_site.run_qa(out), "禁止・誇大表現"))
        self.assertEqual(self.msgs(qa_site.run_qa(out, allow=("受賞",)), "禁止・誇大表現"), [])

    def test_oversize(self):
        out = self.build("garden")
        with open(os.path.join(out, "style.css"), "a", encoding="utf-8") as f:
            f.write("/* " + "x" * 70000 + " */")
        self.assertTrue(self.msgs(qa_site.run_qa(out), "ファイルサイズ"))

    def test_missing_sample_label(self):
        out = self.build("garden", mutate=lambda a: a.update(is_sample=False))
        self.assertTrue(self.msgs(qa_site.run_qa(out, require_sample_label=True), "サンプル表示"))

    def test_external_resource_warns(self):
        out = self.build("garden")
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace("</head>", '<link rel="stylesheet" href="https://cdn.example/x.css"></head>', 1))
        res = qa_site.run_qa(out)
        self.assertGreater(res["warnings"], 0)

    def test_report_markdown_and_cli(self):
        out = self.build("garden")
        rep = os.path.join(self.tmp, "r.md")
        self.assertEqual(qa_site.main([out, "--report", rep]), 0)
        self.assertIn("合格", _paths.read(rep))
        self.rewrite(os.path.join(out, "index.html"), lambda s: s.replace("<main id=\"main\">", "<main id=\"main\"><p>絶対</p>", 1))
        self.assertEqual(qa_site.main([out, "--report", rep]), 1)
        self.assertIn("不合格", _paths.read(rep))
        self.assertEqual(qa_site.main([os.path.join(self.tmp, "none")]), 2)


class TestContrastMath(unittest.TestCase):
    def test_known_values(self):
        self.assertAlmostEqual(qa_site.contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0, places=1)
        self.assertAlmostEqual(qa_site.contrast_ratio((255, 255, 255), (255, 255, 255)), 1.0, places=2)
        # #777777 と白は 4.48:1（WCAGの代表例。4.5未満）
        self.assertAlmostEqual(qa_site.contrast_ratio((0x77, 0x77, 0x77), (255, 255, 255)), 4.48, places=2)

    def test_var_resolution(self):
        res, skipped = qa_site.check_contrast(":root{--a:#fff;--b:#000}body{color:var(--b);background:var(--a)}.x{color:var(--a);background:var(--b)}")
        self.assertEqual(skipped, [])
        self.assertTrue(all(r[4] for r in res))

    def test_ngwords_allow(self):
        self.assertTrue(ngwords.find_hits("絶対です"))
        self.assertFalse(ngwords.find_hits("絶対です", allow=("絶対",)))


if __name__ == "__main__":
    unittest.main()
