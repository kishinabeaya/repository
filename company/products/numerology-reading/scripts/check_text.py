#!/usr/bin/env python3
"""鑑定文の禁止表現チェック。実行: python3 check_text.py 下書き.txt
ヒットした語を行番号つきで表示する。ヒットなし=0、あり=1。機械的な検索のみ。最終判断は人が読んで行う。"""
import sys

NG = {
    "不安をあおる": ["このままだと", "不幸になる", "別れないと", "危険", "大殺界", "凶", "厄年", "災い", "最悪", "手遅れ", "運を逃す", "今すぐ行動"],
    "追加購入誘導": ["追加鑑定", "護符", "お守り", "悪化する", "次の鑑定を受け"],
    "断定": ["必ず当たる", "100%", "１００％", "絶対", "確実に", "間違いなく", "必ず"],
    "霊感・霊視": ["霊視", "因縁", "呪い", "憑い", "除霊", "浄化", "霊感", "前世が見え", "先祖", "波動", "守護"],
    "医療・体": ["病気になる", "治る", "妊娠する", "うつが改善", "完治"],
    "重大な意思決定": ["退職すべき", "離婚すべき", "投資すべき", "借金してでも", "別れるべき", "辞めるべき"],
    "不倫・縁切り・恋愛の約束": ["不倫", "縁切り", "復縁", "両想い", "略奪"],
    "最上級・順位": ["No.1", "NO.1", "ナンバーワン", "ナンバー1", "日本一", "最強", "最安", "どこよりも", "唯一", "プラチナ"],
    "偽の限定・煽り": ["限定", "先着", "今だけ", "残りわずか", "ラスト"],
    "星座・天体の断定": ["水星逆行", "新月", "満月"],
    "外部誘導": ["http", "www.", ".com", ".jp", "@", "＠", "QR", "LINE", "ライン", "Instagram", "インスタ",
                 "Twitter", "ツイッター", "Threads", "スレッズ", "note", "Kindle", "DM", "直接", "ココナラ外",
                 "ココナラ以外", "外部", "連絡先", "メールアドレス", "電話番号", "ブログ", "YouTube"],
    "未記入": ["{{", "}}", "【要記入", "TODO"],
}


def find_hits(text):
    """[(行番号, 区分, 語, 行の内容), ...]。ASCIIの語は大文字小文字を区別しない。"""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for cat, words in NG.items():
            for w in words:
                if w in line or (w.isascii() and w.lower() in low):
                    out.append((i, cat, w, line.strip()[:60]))
    return out


def main():
    if len(sys.argv) != 2:
        print("使い方: python3 check_text.py 下書きファイル.txt", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        hits = find_hits(f.read())
    for i, cat, w, line in hits:
        print(f"{i}行目 [{cat}] 「{w}」: {line}")
    n = len(hits)
    print(f"\n要確認 {n} 件（文脈で問題ない語もあります。読んで判断してください）" if n
          else "禁止語のヒットなし（それでも最後は目で読んで確認してください）")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
