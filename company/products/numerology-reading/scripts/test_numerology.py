#!/usr/bin/env python3
"""手計算との照合テスト。実行: python3 test_numerology.py"""
import unittest
from datetime import date
import numerology as n

# (生年月日, LP, LP別流派, 誕生数, 2027個人年)  すべて手計算で確認した値
CASES = [
    # 1990-05-14: 年1990->19->10->1, 月5, 日14->5 => 11(マスター)。誕生数14->5。個人年 5+1+4+2+0+2+7=21->3
    (date(1990, 5, 14), 11, 11, 5, 3),
    # 1985-12-03: 年1985->23->5, 月12->3, 日3 => 11。誕生数3。個人年 1+2+3+11=17->8
    (date(1985, 12, 3), 11, 11, 3, 8),
    # 1992-07-23: 年1992->21->3, 月7, 日23->5 => 15->6。誕生数5。個人年 7+5+11=23->5
    (date(1992, 7, 23), 6, 6, 5, 5),
    # 1978-11-29: A: 7+2+2=11。B: 7+11+11=29->11。誕生数29->11。個人年 2+11+11=24->6
    (date(1978, 11, 29), 11, 11, 11, 6),
    # 1997-11-01: A: 8+2+1=11。B: 8+11+1=20->2（流派で結果が割れる例）。誕生数1。個人年 2+1+11=14->5
    (date(1997, 11, 1), 11, 2, 1, 5),
    # 2000-01-01: 2+1+1=4。誕生数1。個人年 1+1+11=13->4
    (date(2000, 1, 1), 4, 4, 1, 4),
    # 1983-09-22: 年1983->21->3, 月9, 日22->4 => 16->7。誕生数22(残す)。個人年 9+4+11=24->6
    (date(1983, 9, 22), 7, 7, 22, 6),
    # 1989-03-30: 年1989->27->9, 月3, 日30->3 => 15->6。誕生数3。個人年 3+3+11=17->8
    (date(1989, 3, 30), 6, 6, 3, 8),
]


class T(unittest.TestCase):
    def test_cases(self):
        for b, lp, alt, bn, py in CASES:
            with self.subTest(b=b):
                self.assertEqual(n.life_path(b.year, b.month, b.day), lp)
                self.assertEqual(n.life_path_alt(b.year, b.month, b.day), alt)
                self.assertEqual(n.birth_number(b.day), bn)
                self.assertEqual(n.personal_year(b.month, b.day, 2027), py)

    def test_reduce(self):
        self.assertEqual(n.reduce_num(29), 11)
        self.assertEqual(n.reduce_num(29, False), 2)
        self.assertEqual(n.reduce_num(33), 33)
        self.assertEqual(n.reduce_num(38), 11)
        self.assertEqual(n.reduce_num(19, False), 1)

    def test_personal_months(self):
        # 個人年5の1月=6, 4月=9, 5月=10->1
        pm = n.personal_months(5)
        self.assertEqual((pm[1], pm[4], pm[5], pm[12]), (6, 9, 1, 8))

    def test_name(self):
        # JOHN: J1 O6 H8 N5=20->2。母音O=6、子音 1+8+5=14->5
        r = n.name_numbers("John")
        self.assertEqual((r["expression"], r["soul_urge"], r["personality"]), (2, 6, 5))
        # ANNA: 1+5+5+1=12->3、母音 1+1=2、子音 10->1
        r = n.name_numbers("Anna")
        self.assertEqual((r["expression"], r["soul_urge"], r["personality"]), (3, 2, 1))
        self.assertIsNone(n.name_numbers("やまだ"))

    def test_sun_sign(self):
        # 各星座の開始日・終了日と、年またぎ（山羊座）
        exp = [((1, 1), "山羊座"), ((1, 19), "山羊座"), ((1, 20), "水瓶座"), ((2, 18), "水瓶座"),
               ((2, 19), "魚座"), ((3, 20), "魚座"), ((3, 21), "牡羊座"), ((4, 19), "牡羊座"),
               ((4, 20), "牡牛座"), ((5, 20), "牡牛座"), ((5, 21), "双子座"), ((6, 21), "双子座"),
               ((6, 22), "蟹座"), ((7, 22), "蟹座"), ((7, 23), "獅子座"), ((8, 22), "獅子座"),
               ((8, 23), "乙女座"), ((9, 22), "乙女座"), ((9, 23), "天秤座"), ((10, 23), "天秤座"),
               ((10, 24), "蠍座"), ((11, 22), "蠍座"), ((11, 23), "射手座"), ((12, 21), "射手座"),
               ((12, 22), "山羊座"), ((12, 31), "山羊座"), ((2, 29), "魚座"), ((7, 23), "獅子座")]
        for (m, d), name in exp:
            with self.subTest(m=m, d=d):
                self.assertEqual(n.sun_sign(m, d), name)

    def test_sun_sign_boundary(self):
        self.assertEqual(n.sun_sign_boundary(7, 23), ["蟹座", "獅子座"])   # 切り替え当日
        self.assertEqual(n.sun_sign_boundary(7, 22), ["蟹座", "獅子座"])   # 前日
        self.assertEqual(n.sun_sign_boundary(7, 24), ["蟹座", "獅子座"])   # 翌日
        self.assertEqual(n.sun_sign_boundary(1, 1), None)
        self.assertEqual(n.sun_sign_boundary(12, 22), ["射手座", "山羊座"])
        self.assertEqual(n.sun_sign_boundary(1, 19), ["山羊座", "水瓶座"])
        self.assertEqual(n.sun_sign_boundary(5, 5), None)
        self.assertEqual(n.sun_sign_boundary(2, 29), None)
        # 1992-07-23 は星座の境目、かつ calculate に反映される
        r = n.calculate(date(1992, 7, 23))
        self.assertEqual((r["sun_sign"], r["sun_sign_boundary"]), ("獅子座", ["蟹座", "獅子座"]))

    def test_flag_and_cli(self):
        self.assertTrue(n.calculate(date(1997, 11, 1))["life_path_differs_by_school"])
        self.assertFalse(n.calculate(date(1992, 7, 23))["life_path_differs_by_school"])
        self.assertEqual(n.main(["2020-02-30"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
