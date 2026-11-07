#!/usr/bin/env python3
"""check_text.py のテスト。実行: python3 test_check_text.py"""
import os
import unittest
import check_text as c


def cats(text):
    return {h[1] for h in c.find_hits(text)}


class T(unittest.TestCase):
    def test_new_categories(self):
        cases = {
            "不倫・縁切り・恋愛の約束": ["不倫を成就", "縁切りします", "復縁できる", "必ず両想い"],
            "最上級・順位": ["No.1の的中率", "日本一", "最強の鑑定", "どこよりも", "最安です", "no.1"],
            "偽の限定・煽り": ["今月限定", "先着10名", "今だけ", "残りわずか"],
            "外部誘導": ["https://example.com", "詳しくは@abc", "QRコード", "LINEで", "noteに書きました",
                         "DMください", "ココナラ外で", "外部の連絡先", "line", "Kindle版"],
            "星座・天体の断定": ["水星逆行の影響", "新月に", "満月の夜"],
            "霊感・霊視": ["先祖の", "波動が", "守護"],
        }
        for cat, texts in cases.items():
            for t in texts:
                with self.subTest(t=t):
                    self.assertIn(cat, cats(t))

    def test_old_categories_still_work(self):
        self.assertIn("断定", cats("必ず当たる"))
        self.assertIn("不安をあおる", cats("大殺界です"))
        self.assertIn("医療・体", cats("うつが改善します"))

    def test_clean_text_and_narrowed_word(self):
        self.assertEqual(c.find_hits("2027年は整える時間を持つと過ごしやすいと言われます。気が向いたら試してみてください。"), [])
        self.assertEqual(c.find_hits("暮らしが改善すると感じる人もいます"), [])  # 「改善する」単体は対象外

    def test_disclaimer_templates_clean(self):
        # 免責・開示文そのものが誤検出されないこと（「制作について」以降の本文のみ検査）
        base = os.path.join(os.path.dirname(__file__), "..", "templates", "disclaimer.md")
        txt = open(base, encoding="utf-8").read()
        body = txt.split("## 鑑定文の末尾に入れる文")[1].split("## 重い悩み")[0]
        self.assertEqual(c.find_hits(body), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
