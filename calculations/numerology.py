"""
数秘術（Numerology）
生年月日からライフパス・誕生数・運命数を算出
"""

def reduce_to_single_digit(n: int, keep_masters: bool = True) -> int:
    """数を1桁に縮約。マスターナンバー（11, 22, 33）は保持。"""
    while n > 9:
        if keep_masters and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n


def life_path_number(year: int, month: int, day: int) -> dict:
    """ライフパスナンバー：生年月日の全桁を合計"""
    total = sum(int(d) for d in f"{year}{month:02d}{day:02d}")
    reduced = reduce_to_single_digit(total)
    return {
        "raw_sum": total,
        "number": reduced,
        "meaning": LIFE_PATH_MEANINGS.get(reduced, "")
    }


def birth_day_number(day: int) -> dict:
    """誕生数：生まれた日のみから"""
    reduced = reduce_to_single_digit(day, keep_masters=True)
    return {
        "raw_day": day,
        "number": reduced,
        "meaning": BIRTH_DAY_MEANINGS.get(reduced, "")
    }


def destiny_number_from_name(name_kana: str) -> dict:
    """運命数（フルネームから・簡易版）
    日本語の母音カタカナを数字にマッピングして合計。
    """
    kana_to_number = {
        'ア': 1, 'イ': 2, 'ウ': 3, 'エ': 4, 'オ': 5,
        'カ': 6, 'キ': 7, 'ク': 8, 'ケ': 9, 'コ': 1,
        'サ': 2, 'シ': 3, 'ス': 4, 'セ': 5, 'ソ': 6,
        'タ': 7, 'チ': 8, 'ツ': 9, 'テ': 1, 'ト': 2,
        'ナ': 3, 'ニ': 4, 'ヌ': 5, 'ネ': 6, 'ノ': 7,
        'ハ': 8, 'ヒ': 9, 'フ': 1, 'ヘ': 2, 'ホ': 3,
        'マ': 4, 'ミ': 5, 'ム': 6, 'メ': 7, 'モ': 8,
        'ヤ': 9, 'ユ': 1, 'ヨ': 2,
        'ラ': 3, 'リ': 4, 'ル': 5, 'レ': 6, 'ロ': 7,
        'ワ': 8, 'ヲ': 9, 'ン': 1,
        'ガ': 6, 'ギ': 7, 'グ': 8, 'ゲ': 9, 'ゴ': 1,
        'ザ': 2, 'ジ': 3, 'ズ': 4, 'ゼ': 5, 'ゾ': 6,
        'ダ': 7, 'ヂ': 8, 'ヅ': 9, 'デ': 1, 'ド': 2,
        'バ': 8, 'ビ': 9, 'ブ': 1, 'ベ': 2, 'ボ': 3,
        'パ': 8, 'ピ': 9, 'プ': 1, 'ペ': 2, 'ポ': 3,
    }
    total = sum(kana_to_number.get(ch, 0) for ch in name_kana)
    reduced = reduce_to_single_digit(total)
    return {
        "raw_sum": total,
        "number": reduced,
        "meaning": DESTINY_MEANINGS.get(reduced, "")
    }


LIFE_PATH_MEANINGS = {
    1: "リーダー型・開拓者。新しいことを始める才能。独立心と先導力。",
    2: "調和・協調・サポート役。人と人をつなぐ繊細さと共感力。",
    3: "創造性・表現・喜びの伝達者。芸術的感性と楽天さで人を魅了する。",
    4: "堅実・組織化・基盤づくり。地に足のついた努力で信頼を築く。",
    5: "自由・変化・冒険。柔軟性と好奇心で世界を広げる。",
    6: "愛・調和・世話役。家族や仲間に深い愛情を注ぐ温かさ。",
    7: "探求・分析・精神性。内省と知性で本質を見抜く哲学者。",
    8: "達成・権威・物質的成功。組織を動かす力と現実化の才能。",
    9: "博愛・完成・奉仕。全体を見渡し人類に貢献する高い視点。",
    11: "直感・霊性・啓発者（マスターナンバー）。スピリチュアルな使命を持つ。",
    22: "マスタービルダー（マスターナンバー）。壮大な夢を現実化する力。",
    33: "愛のマスター（マスターナンバー）。無条件の愛と奉仕で世界を変える。",
}

BIRTH_DAY_MEANINGS = {
    1: "独立・先駆け・主導力。",
    2: "受容・協調・パートナーシップ。",
    3: "創造・表現・喜び。",
    4: "実務・基盤・忍耐。",
    5: "変化・自由・冒険。",
    6: "養育・調和・責任。",
    7: "探究・神秘・深さ。",
    8: "野心・力・達成。",
    9: "理想・奉仕・完成。",
    11: "高い直感・霊感（マスター）。",
    22: "実現力（マスタービルダー）。",
}

DESTINY_MEANINGS = {
    1: "リーダーとして生きる運命。",
    2: "つなぐ役・支える役の運命。",
    3: "表現者・伝え手の運命。",
    4: "築き上げる人の運命。",
    5: "自由な旅人の運命。",
    6: "愛と調和の運命。",
    7: "真理探究者の運命。",
    8: "達成と影響の運命。",
    9: "奉仕と完成の運命。",
    11: "啓発者の運命。",
    22: "建設者の運命。",
    33: "愛の伝道者の運命。",
}


if __name__ == "__main__":
    # サラさんのデータでテスト
    result = life_path_number(1963, 7, 31)
    print(f"ライフパス: {result}")
    bd = birth_day_number(31)
    print(f"誕生数: {bd}")
    dst = destiny_number_from_name("ヤマオカサラ")
    print(f"運命数: {dst}")
