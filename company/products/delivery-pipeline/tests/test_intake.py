import copy
import io
import json
import os
import unittest
from contextlib import redirect_stdout

import _paths
import check_answers as ca
import make_questionnaire as mq

ROOT = _paths.ROOT


def sample(name):
    with open(os.path.join(ROOT, "samples", name, "answers.json"), encoding="utf-8") as f:
        return json.load(f)


class TestCheckAnswers(unittest.TestCase):
    def test_complete_homepage(self):
        self.assertEqual(ca.missing_fields(sample("bakery")), [])

    def test_complete_lp(self):
        self.assertEqual(ca.missing_fields(sample("spreadsheet-lp")), [])

    def test_missing_detected_and_grouped(self):
        a = sample("bakery")
        del a["about"]
        a["services"] = [{"name": "A", "description": ""}]
        a["contact_method"] = "未定"
        keys = [k for k, _ in ca.missing_fields(a)]
        self.assertEqual(sorted(keys), ["about", "contact_method", "services"])
        text, bad = ca.render(a)
        self.assertTrue(bad)
        self.assertIn("あと 3 点", text)  # 1通にまとめる

    def test_lp_needs_three_benefits(self):
        a = sample("spreadsheet-lp")
        a["benefits"] = a["benefits"][:1]
        self.assertEqual([k for k, _ in ca.missing_fields(a)], ["benefits"])

    def test_automation_and_data_required(self):
        a = {"order_id": "X-1", "type": "automation", "business_name": "a", "one_line": "b", "audience": "c", "goal": "d"}
        keys = [k for k, _ in ca.missing_fields(a)]
        self.assertEqual(sorted(keys), ["current_process", "desired_output", "environment", "frequency", "input_format"])
        a["type"] = "data"
        self.assertEqual(sorted(k for k, _ in ca.missing_fields(a)), ["columns", "data_description", "output_format", "questions"])

    def test_unknown_type(self):
        self.assertEqual(ca.missing_fields({"type": "x"})[0][0], "type")

    def test_pii_detected_but_contact_text_skipped(self):
        a = sample("bakery")
        a["about"] += " 連絡は taro@example.com か 03-1234-5678 へ"
        kinds = {k for _, k, _ in ca.pii_hits(a)}
        self.assertEqual(kinds, {"メールアドレス", "電話番号"})
        b = sample("bakery")
        b["contact_text"] = "info@example.com"
        self.assertEqual(ca.pii_hits(b), [])
        self.assertTrue(ca.render(a)[1])

    def test_ng_words_reported(self):
        a = sample("bakery")
        a["goal"] = "業界最安で、必ず売上を増やしたい"
        words = {w for _, _, w in ca.ng_hits(a)}
        self.assertTrue({"業界最安", "必ず"} <= words)

    def test_bad_order_id(self):
        a = copy.deepcopy(sample("bakery"))
        a["order_id"] = "山田 太郎"
        self.assertEqual(ca.missing_fields(a)[0][0], "order_id")

    def test_cli_exit_codes(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(ca.main(["x", os.path.join(ROOT, "samples", "bakery", "answers.json")]), 0)
            self.assertEqual(ca.main(["x", os.path.join(ROOT, "no-such.json")]), 2)
            self.assertEqual(ca.main(["x"]), 2)


class TestQuestionnaire(unittest.TestCase):
    def test_all_types_build(self):
        for t in mq.TYPES:
            text = mq.build(t)
            self.assertIn("Q1.", text)
            self.assertIn("個人情報は、書かないでください", text)

    def test_does_not_ask_for_personal_info(self):
        for t in mq.TYPES:
            for line in mq.build(t).splitlines():
                if line.startswith("Q"):
                    for w in ("お名前", "氏名", "住所を", "電話番号を", "メールアドレスを", "連絡先を"):
                        self.assertNotIn(w, line.split("。")[0])

    def test_bad_type(self):
        with self.assertRaises(ValueError):
            mq.build("ec")


if __name__ == "__main__":
    unittest.main()
