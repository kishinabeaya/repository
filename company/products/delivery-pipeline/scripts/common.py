"""共通の定数と関数（標準ライブラリのみ）。"""
import re

STEPS = {
    "intake": "受付",
    "requirements": "要件確認",
    "build": "制作",
    "qa": "検証",
    "delivery": "納品",
    "revision": "修正対応",
    "payment": "入金確認",
}
JA2ID = {v: k for k, v in STEPS.items()}
ACTORS = ("claude", "ceo")
# 工程ごとの担当の初期値（READMEと同じ。実績は log_step.py で記録した値を使う）
DEFAULT_ACTOR = {
    "intake": "ceo",         # ログイン・本人確認・規約確認・メッセージの転記
    "requirements": "claude",
    "build": "claude",
    "qa": "claude",
    "delivery": "ceo",       # 納品メッセージ・ファイルの転記（ZIP作成はclaude）
    "revision": "claude",
    "payment": "ceo",
}
ORDER_RE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")

PII_PATTERNS = [
    ("メールアドレス", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("電話番号", re.compile(r"(?<!\d)0\d{1,3}-\d{2,4}-\d{3,4}(?!\d)")),
    ("電話番号", re.compile(r"(?<!\d)0[5789]0\d{8}(?!\d)")),
    ("郵便番号", re.compile(r"〒\s*\d{3}-?\d{4}")),
    ("郵便番号", re.compile(r"(?<!\d)\d{3}-\d{4}(?!\d)")),
    ("LINE ID等", re.compile(r"(?i)line\s*id")),
]


def find_pii(text):
    """[(種類, 該当部分), ...]。機械的な検出のみ（氏名は検出できない）。"""
    out = []
    for kind, pat in PII_PATTERNS:
        for m in pat.finditer(text or ""):
            out.append((kind, m.group(0)))
    return out
