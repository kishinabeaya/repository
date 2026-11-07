#!/usr/bin/env python3
"""鑑定文の禁止表現チェック。実行: python3 check_text.py 下書き.txt
ヒットした語を行番号つきで表示する。ヒットなし=0、あり=1。機械的な検索のみ。最終判断は人が読んで行う。"""
import sys

NG = {
    "不安をあおる": ["このままだと", "不幸になる", "別れないと", "危険", "大殺界", "凶", "厄年", "災い", "最悪", "手遅れ", "運を逃す", "今すぐ行動"],
    "追加購入誘導": ["追加鑑定", "護符", "お守り", "悪化する", "次の鑑定を受け"],
    "断定": ["必ず当たる", "100%", "１００％", "絶対", "確実に", "間違いなく", "必ず"],
    "霊感・霊視": ["霊視", "因縁", "呪い", "憑い", "除霊", "浄化", "霊感", "前世が見え"],
    "医療・体": ["病気になる", "治る", "妊娠する", "うつが改善", "完治", "改善する"],
    "重大な意思決定": ["退職すべき", "離婚すべき", "投資すべき", "借金してでも", "別れるべき", "辞めるべき"],
    "未記入": ["{{", "}}", "【要記入", "TODO"],
}


def main():
    if len(sys.argv) != 2:
        print("使い方: python3 check_text.py 下書きファイル.txt", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        lines = f.read().splitlines()
    hits = 0
    for i, line in enumerate(lines, 1):
        for cat, words in NG.items():
            for w in words:
                if w in line:
                    hits += 1
                    print(f"{i}行目 [{cat}] 「{w}」: {line.strip()[:60]}")
    print(f"\n要確認 {hits} 件" if hits else "禁止語のヒットなし（それでも最後は声に出さず目で読んで確認してください）")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
