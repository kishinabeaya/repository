import io
import json
import os
import shutil
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout

import _paths
import build_site
import log_step
import package_delivery
import report_share

ROOT = _paths.ROOT


def answers(name):
    with open(os.path.join(ROOT, "samples", name, "answers.json"), encoding="utf-8") as f:
        return json.load(f)


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_package_contents(self):
        a = answers("garden")
        dest = package_delivery.package(os.path.join(ROOT, "samples", "garden", "site"), a, self.tmp)
        names = sorted(os.listdir(dest))
        self.assertEqual(names, ["CHECKLIST.md", "DELIVERY_MESSAGE.md", "REVISION_REQUEST.md", "SAMPLE-003-site.zip", "qa-report.md"])
        with zipfile.ZipFile(os.path.join(dest, "SAMPLE-003-site.zip")) as z:
            self.assertIsNone(z.testzip())
            zn = sorted(z.namelist())
        self.assertEqual(zn, ["README.md", "site/about.html", "site/contact.html", "site/index.html", "site/style.css"])
        chk = _paths.read(os.path.join(dest, "CHECKLIST.md"))
        self.assertIn("CEOの作業", chk)
        self.assertIn("入金", chk)
        rev = _paths.read(os.path.join(dest, "REVISION_REQUEST.md"))
        self.assertIn("まとめて", rev)

    def test_deterministic_zip(self):
        a = answers("garden")
        site = os.path.join(ROOT, "samples", "garden", "site")
        d1 = package_delivery.package(site, a, os.path.join(self.tmp, "1"))
        d2 = package_delivery.package(site, a, os.path.join(self.tmp, "2"))
        z = "SAMPLE-003-site.zip"
        self.assertEqual(_paths.read(os.path.join(d1, z), "rb"), _paths.read(os.path.join(d2, z), "rb"))

    def test_refuses_failing_site(self):
        a = answers("garden")
        a["about"] = "絶対に満足できます"
        site = os.path.join(self.tmp, "site")
        build_site.build(a, site)
        with self.assertRaises(ValueError):
            package_delivery.package(site, a, os.path.join(self.tmp, "out"))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "out", "SAMPLE-003")))
        dest = package_delivery.package(site, a, os.path.join(self.tmp, "out"), force=True)
        self.assertIn("警告", _paths.read(os.path.join(dest, "CHECKLIST.md")))

    def test_bad_order_id(self):
        a = answers("garden")
        a["order_id"] = "../x"
        with self.assertRaises(ValueError):
            package_delivery.package(os.path.join(ROOT, "samples", "garden", "site"), a, self.tmp)

    def test_cli(self):
        with redirect_stdout(io.StringIO()):
            rc = package_delivery.main(["--site", os.path.join(ROOT, "samples", "bakery", "site"),
                                        "--answers", os.path.join(ROOT, "samples", "bakery", "answers.json"),
                                        "--out", self.tmp])
        self.assertEqual(rc, 0)


class TestTracking(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.f = os.path.join(self.tmp, "steps.jsonl")

    def log(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return log_step.main(list(args) + ["--file", self.f])

    def test_record_format(self):
        self.assertEqual(self.log("--order", "A-1", "--step", "build", "--actor", "claude", "--minutes", "30", "--note", "LP作成"), 0)
        rec = json.loads(_paths.read(self.f))
        self.assertEqual(sorted(rec), ["actor", "minutes", "note", "order_id", "step"])
        self.assertEqual(rec["minutes"], 30)

    def test_japanese_step_name(self):
        self.assertEqual(self.log("--order", "A-1", "--step", "修正対応", "--actor", "claude", "--minutes", "5"), 0)
        self.assertEqual(json.loads(_paths.read(self.f))["step"], "revision")

    def test_rejects_bad_input(self):
        base = ["--order", "A-1", "--step", "build", "--actor", "claude", "--minutes", "5"]
        for repl in ({"--step": "x"}, {"--actor": "bob"}, {"--minutes": "-1"}, {"--minutes": "abc"}, {"--order": "山田太郎"},
                     {"--note": "連絡先 a@b.com"}, {"--note": "03-1234-5678"}):
            args = list(base)
            for k, v in repl.items():
                if k in args:
                    args[args.index(k) + 1] = v
                else:
                    args += [k, v]
            self.assertEqual(self.log(*args), 1, repl)
        self.assertFalse(os.path.exists(self.f))

    def test_share(self):
        rows = [("A", "intake", "ceo", 5), ("A", "requirements", "claude", 20), ("A", "build", "claude", 60),
                ("A", "qa", "claude", 10), ("A", "delivery", "ceo", 5), ("A", "payment", "ceo", 2), ("A", "revision", "claude", 5)]
        for o, s, a, m in rows:
            self.log("--order", o, "--step", s, "--actor", a, "--minutes", str(m))
        recs, bad = report_share.load(self.f)
        s = report_share.summarize(recs)
        self.assertEqual(bad, [])
        self.assertEqual(s["units"], 7)
        self.assertAlmostEqual(s["step_share"], 3 / 7)
        self.assertAlmostEqual(s["time_share"], 12 / 107)
        text = report_share.render(s)
        self.assertIn("目標超過", text)  # 11.2% > 10%
        self.assertIn("時間ベース", text)

    def test_share_within_target(self):
        for s, a, m in (("build", "claude", 90), ("payment", "ceo", 5)):
            self.log("--order", "A", "--step", s, "--actor", a, "--minutes", str(m))
        recs, _ = report_share.load(self.f)
        self.assertIn("目標内", report_share.render(report_share.summarize(recs)))

    def test_bad_lines_and_empty(self):
        with open(self.f, "w", encoding="utf-8") as fh:
            fh.write('{"order_id":"A","step":"build","actor":"claude","minutes":10,"note":""}\nnot json\n{"order_id":"A","step":"zzz","actor":"ceo","minutes":1}\n')
        recs, bad = report_share.load(self.f)
        self.assertEqual(len(recs), 1)
        self.assertEqual(len(bad), 2)
        empty = report_share.summarize([])
        self.assertIsNone(empty["time_share"])
        self.assertIn("データなし", report_share.render(empty))

    def test_cli_missing_file(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(report_share.main(["--file", os.path.join(self.tmp, "none")]), 1)


if __name__ == "__main__":
    unittest.main()
