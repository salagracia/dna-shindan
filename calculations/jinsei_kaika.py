"""
人生開花タイプ診断（サラ・グラシア オリジナル・公式版）
20問×5段階リッカート → 8タイプ判定
メインタイプ + 隠れ才能タイプ（第2位）
"""

# 5段階リッカート
LIKERT_OPTIONS = {
    "5": ("はい", 5),
    "4": ("どちらかというとはい", 4),
    "3": ("どちらでもない", 3),
    "2": ("どちらかというといいえ", 2),
    "1": ("いいえ", 1),
}


# 20問
QUESTIONS = [
    {"id": "K1", "num": 1, "question": "人の悩みを聞くことが多い"},
    {"id": "K2", "num": 2, "question": "「もっと自分らしく生きたい」と感じることがある"},
    {"id": "K3", "num": 3, "question": "アイデアが次々浮かぶ方だ"},
    {"id": "K4", "num": 4, "question": "人に気を遣いすぎて疲れることがある"},
    {"id": "K5", "num": 5, "question": "美しいものや空間に強く惹かれる"},
    {"id": "K6", "num": 6, "question": "一人の時間がないと苦しくなる"},
    {"id": "K7", "num": 7, "question": "誰かの人生のきっかけになる話が好き"},
    {"id": "K8", "num": 8, "question": "新しいことを始めるのは好きな方だ"},
    {"id": "K9", "num": 9, "question": "本音を飲み込んでしまうことがある"},
    {"id": "K10", "num": 10, "question": "「このままで終わりたくない」と感じることがある"},
    {"id": "K11", "num": 11, "question": "人から相談されやすい"},
    {"id": "K12", "num": 12, "question": "感覚や直感を大切にしている"},
    {"id": "K13", "num": 13, "question": "ルールや常識に違和感を覚えることがある"},
    {"id": "K14", "num": 14, "question": "頑張っているのに満たされない感覚がある"},
    {"id": "K15", "num": 15, "question": "学ぶことが好き"},
    {"id": "K16", "num": 16, "question": "周りに合わせすぎて、自分が分からなくなることがある"},
    {"id": "K17", "num": 17, "question": "人を励ましたり勇気づけるのが好き"},
    {"id": "K18", "num": 18, "question": "人生を変えたいと思ったことがある"},
    {"id": "K19", "num": 19, "question": "好きなことには夢中になる"},
    {"id": "K20", "num": 20, "question": "「本来の自分」をもっと生きたいと思う"},
]


# 各タイプの該当質問番号（サラ・グラシア公式仕様）
TYPE_QUESTION_MAP = {
    "A": [3, 8, 12, 13, 19],   # 創造タイプ
    "B": [1, 4, 11, 16, 17],   # 癒しタイプ
    "C": [7, 10, 11, 17, 18],  # 導きタイプ
    "D": [5, 12, 14, 19, 20],  # 美意識タイプ
    "E": [6, 13, 15, 18, 19],  # 探究タイプ
    "F": [2, 8, 10, 13, 18],   # 自由タイプ
    "G": [1, 4, 9, 14, 16],    # 調和タイプ
    "H": [2, 10, 14, 18, 20],  # 覚醒タイプ
}


# ============= 8タイプの結果文（サラ・グラシア公式版） =============
TYPE_PROFILES = {
    "A": {
        "code": "A",
        "name": "創造タイプ",
        "tagline": "アイデア・発信・クリエイティブ才能",
        "body": (
            "あなたは「何もないところから新しいものを生み出せる人」です。\n\n"
            "アイデア、言葉、発想、世界観。\n"
            "あなたの中には、人とは違う視点があります。\n\n"
            "ただ、その感性が強い分、「理解されない苦しさ」を感じることもあったかもしれません。\n\n"
            "でも、本来のあなたは、\n"
            "“自分らしさ”を表現した時に輝く人。\n\n"
            "周りに合わせるより、\n"
            "あなたの感性を信じた時、人生が動き始めます。"
        ),
    },
    "B": {
        "code": "B",
        "name": "癒しタイプ",
        "tagline": "共感・安心感・包容力才能",
        "body": (
            "あなたは「人を安心させる力」を持っています。\n\n"
            "一緒にいるだけでホッとする。\n"
            "つい悩みを話したくなる。\n"
            "そんな空気を自然に作れる人です。\n\n"
            "ただ優しい分、人に合わせすぎて疲れてしまうことも。\n\n"
            "でも本来のあなたは、\n"
            "“誰かを癒しながら、自分も満たされる”ことで輝く人です。\n\n"
            "まずは、自分の心を後回しにしないこと。\n"
            "そこから人生が変わり始めます。"
        ),
    },
    "C": {
        "code": "C",
        "name": "導きタイプ",
        "tagline": "教育・リーダー・影響力才能",
        "body": (
            "あなたは「人を前に進ませる力」を持っています。\n\n"
            "言葉に説得力があり、\n"
            "気づけば人を勇気づけているタイプ。\n\n"
            "本当は、あなた自身の経験が、誰かの希望になります。\n\n"
            "ただ責任感が強く、一人で抱え込みやすいところも。\n\n"
            "でも本来のあなたは、\n"
            "“自分らしく輝く姿”そのものが、人を導く人です。\n\n"
            "完璧じゃなくて大丈夫。\n"
            "あなたの歩みが、誰かの光になります。"
        ),
    },
    "D": {
        "code": "D",
        "name": "美意識タイプ",
        "tagline": "感性・魅力・世界観才能",
        "body": (
            "あなたは「美しさで人を魅了する人」です。\n\n"
            "センス、感性、空気感。\n"
            "あなたは“雰囲気”で人を惹きつける才能があります。\n\n"
            "だからこそ、雑な環境や違和感のある人間関係に強く疲れます。\n\n"
            "本来のあなたは、\n"
            "美しさを我慢せずに生きた時、運気が開く人。\n\n"
            "「好き」を大切にするほど、人生は豊かになっていきます。"
        ),
    },
    "E": {
        "code": "E",
        "name": "探究タイプ",
        "tagline": "知性・分析・学び才能",
        "body": (
            "あなたは「深く学び、本質を見抜く人」です。\n\n"
            "表面的な言葉では満足できない。\n"
            "なぜ？\n"
            "本当は？\n"
            "その奥には何がある？\n\n"
            "そんなふうに、物事を深く考える力があります。\n\n"
            "ただ考えすぎて、動けなくなることもあるかもしれません。\n\n"
            "でも本来のあなたは、\n"
            "“知識を知恵に変えた時”に輝く人。\n\n"
            "あなたの学びは、これから誰かの助けになります。"
        ),
    },
    "F": {
        "code": "F",
        "name": "自由タイプ",
        "tagline": "行動力・挑戦・変化才能",
        "body": (
            "あなたは「変化によって輝く人」です。\n\n"
            "新しい場所、\n"
            "新しい挑戦、\n"
            "新しい出会い。\n\n"
            "あなたは“動く”ことでエネルギーが湧くタイプです。\n\n"
            "逆に、我慢・制限・同じ毎日が続くと、心が苦しくなってしまいます。\n\n"
            "本来のあなたは、\n"
            "自由を許可した時に人生が開花する人。\n\n"
            "「こうあるべき」を手放した時、本来の魅力が動き出します。"
        ),
    },
    "G": {
        "code": "G",
        "name": "調和タイプ",
        "tagline": "人間関係・サポート・バランス才能",
        "body": (
            "あなたは「人と人をつなぐ力」を持っています。\n\n"
            "場の空気を読み、自然とバランスを取れる人。\n\n"
            "あなたがいると、人間関係がなめらかになる。\n"
            "そんな才能があります。\n\n"
            "ただ、自分より周りを優先しすぎることも。\n\n"
            "でも本来のあなたは、\n"
            "“自分を大切にしながら、人と繋がる”ことで輝く人。\n\n"
            "無理に頑張らなくても、\n"
            "あなたの存在そのものに価値があります。"
        ),
    },
    "H": {
        "code": "H",
        "name": "覚醒タイプ",
        "tagline": "人生変容・自己実現・影響力才能",
        "body": (
            "あなたは「人生を大きく変えていく力」を持っています。\n\n"
            "これまで、苦しみや葛藤を経験してきたかもしれません。\n\n"
            "でもその経験こそが、あなたを強くしてきました。\n\n"
            "あなたは、\n"
            "“本当の自分”に戻ることで、人生が一気に動き出すタイプ。\n\n"
            "もう我慢して生きなくていい。\n\n"
            "これからは、\n"
            "「誰かの期待」ではなく、\n"
            "あなた自身の人生を生きる番です。"
        ),
    },
}


# 点数強度の判定
def get_strength_level(score: int) -> str:
    if score >= 22:
        return "かなり強いタイプ"
    elif score >= 18:
        return "才能として強く持っている"
    elif score >= 14:
        return "状況によって出やすい"
    else:
        return "現在は抑えている可能性"


def calculate_jinsei_kaika(answers: dict) -> dict:
    """20問の回答から8タイプ判定（メイン+隠れ才能）"""
    # 質問番号から回答スコアを取得
    q_scores = {}
    for q in QUESTIONS:
        ans = answers.get(q["id"])
        if ans is None:
            continue
        try:
            q_scores[q["num"]] = int(ans)
        except (ValueError, TypeError):
            continue

    # 各タイプのスコア算出
    type_scores = {}
    for type_code, q_nums in TYPE_QUESTION_MAP.items():
        total = sum(q_scores.get(n, 0) for n in q_nums)
        type_scores[type_code] = total

    # メインタイプ（最高点）と隠れ才能タイプ（第2位）
    sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
    main_code, main_score = sorted_types[0]
    second_code, second_score = sorted_types[1] if len(sorted_types) > 1 else (None, 0)

    main_profile = TYPE_PROFILES.get(main_code, {})
    second_profile = TYPE_PROFILES.get(second_code, {}) if second_code else {}

    return {
        "type": main_code,
        "name": main_profile.get("name", ""),
        "tagline": main_profile.get("tagline", ""),
        "body": main_profile.get("body", ""),
        "score": main_score,
        "strength_level": get_strength_level(main_score),
        "second_type": second_code,
        "second_name": second_profile.get("name", ""),
        "second_tagline": second_profile.get("tagline", ""),
        "second_body": second_profile.get("body", ""),
        "second_score": second_score,
        "all_scores": type_scores,
    }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # サラさん想定の回答
    sara_answers = {f"K{i}": "5" for i in range(1, 21)}
    result = calculate_jinsei_kaika(sara_answers)
    print(f"メインタイプ: {result['type']} - {result['name']}")
    print(f"  点数: {result['score']}（{result['strength_level']}）")
    print(f"  タグライン: {result['tagline']}")
    print(f"隠れ才能タイプ: {result['second_type']} - {result['second_name']}")
    print(f"  点数: {result['second_score']}")
    print(f"\n全タイプスコア: {result['all_scores']}")
