"""
人生開花タイプ診断（サラグラシア オリジナル・高精度版 v2）
24問×4択（A/B/C/D）→ 4タイプ判定
メインタイプ + 隠れ才能タイプ
"""

# 24問×4択
QUESTIONS = [
    {"id": "K1", "num": 1, "question": "新しいことを始める時、ワクワクするのは？",
     "options": {"A": "新しいアイデアを形にできる", "B": "誰かの役に立てる",
                  "C": "人を導ける", "D": "自分らしい世界観を作れる"}},
    {"id": "K2", "num": 2, "question": "疲れた時、欲しくなるのは？",
     "options": {"A": "一人で考える時間", "B": "安心できる会話",
                  "C": "前向きになれる刺激", "D": "美しい空間や癒し"}},
    {"id": "K3", "num": 3, "question": "周りから言われやすいのは?",
     "options": {"A": "発想が面白い", "B": "優しい",
                  "C": "頼れる", "D": "センスがいい"}},
    {"id": "K4", "num": 4, "question": "つい気になってしまうのは？",
     "options": {"A": "「もっと面白くできないか」", "B": "「相手は大丈夫かな」",
                  "C": "「どうすれば前に進めるか」", "D": "「心地よいかどうか」"}},
    {"id": "K5", "num": 5, "question": "あなたが満たされる瞬間は？",
     "options": {"A": "アイデアが浮かんだ時", "B": "感謝された時",
                  "C": "誰かが変化した時", "D": "心がときめいた時"}},
    {"id": "K6", "num": 6, "question": "どちらかというと…",
     "options": {"A": "自由な発想型", "B": "共感型",
                  "C": "行動型", "D": "感性型"}},
    {"id": "K7", "num": 7, "question": "苦手なのは？",
     "options": {"A": "型にはめられること", "B": "冷たい人間関係",
                  "C": "停滞している状態", "D": "雑な空間"}},
    {"id": "K8", "num": 8, "question": "学び方として近いのは？",
     "options": {"A": "自分で試したい", "B": "人の話から学ぶ",
                  "C": "実践しながら覚える", "D": "感覚で掴みたい"}},
    {"id": "K9", "num": 9, "question": "人生で大切なのは？",
     "options": {"A": "自由", "B": "愛", "C": "成長", "D": "美しさ"}},
    {"id": "K10", "num": 10, "question": "もし発信するなら？",
     "options": {"A": "独自視点を伝える", "B": "誰かを癒したい",
                  "C": "勇気を与えたい", "D": "世界観で魅せたい"}},
    {"id": "K11", "num": 11, "question": "心が動くのは？",
     "options": {"A": "新しい発見", "B": "人の優しさ",
                  "C": "挑戦している人", "D": "美しいもの"}},
    {"id": "K12", "num": 12, "question": "あなたが無意識にしていることは？",
     "options": {"A": "常識を疑う", "B": "空気を読む",
                  "C": "周りを引っ張る", "D": "雰囲気を整える"}},
    {"id": "K13", "num": 13, "question": "落ち込みやすいのは？",
     "options": {"A": "理解されない時", "B": "人間関係がギクシャクした時",
                  "C": "成長できていない時", "D": "美意識を無視した時"}},
    {"id": "K14", "num": 14, "question": "好きなのは？",
     "options": {"A": "アイデアを考えること", "B": "誰かを支えること",
                  "C": "人を変化させること", "D": "魅力を磨くこと"}},
    {"id": "K15", "num": 15, "question": "理想の働き方は？",
     "options": {"A": "自由に創る", "B": "誰かに寄り添う",
                  "C": "人を導く", "D": "好きな世界観で働く"}},
    {"id": "K16", "num": 16, "question": "あなたの強みは？",
     "options": {"A": "発想力", "B": "共感力",
                  "C": "推進力", "D": "感性"}},
    {"id": "K17", "num": 17, "question": "無理をすると…",
     "options": {"A": "飽きる", "B": "抱え込みすぎる",
                  "C": "頑張りすぎる", "D": "神経がすり減る"}},
    {"id": "K18", "num": 18, "question": "本当はもっと…",
     "options": {"A": "自分を表現したい", "B": "心を軽くしたい",
                  "C": "大きく成長したい", "D": "自分らしく美しく生きたい"}},
    {"id": "K19", "num": 19, "question": "気づくと考えているのは？",
     "options": {"A": "新しい可能性", "B": "人の気持ち",
                  "C": "未来や目標", "D": "理想のライフスタイル"}},
    {"id": "K20", "num": 20, "question": "惹かれる人は？",
     "options": {"A": "個性的な人", "B": "温かい人",
                  "C": "行動力がある人", "D": "洗練された人"}},
    {"id": "K21", "num": 21, "question": "人生のテーマとして近いのは？",
     "options": {"A": "創造", "B": "癒し", "C": "変化", "D": "魅力"}},
    {"id": "K22", "num": 22, "question": "「このままでは嫌」と感じるのは？",
     "options": {"A": "同じ毎日", "B": "心が疲れている状態",
                  "C": "成長が止まること", "D": "ときめきがないこと"}},
    {"id": "K23", "num": 23, "question": "もし新しい挑戦をするなら？",
     "options": {"A": "自分らしい企画", "B": "誰かを支える活動",
                  "C": "人生を変える活動", "D": "センスを活かす活動"}},
    {"id": "K24", "num": 24, "question": "今一番近い感覚は？",
     "options": {"A": "もっと自由に表現したい", "B": "もっと心を軽くしたい",
                  "C": "もっと人生を変えたい", "D": "もっと自分らしく輝きたい"}},
]


# 4タイプの結果文（サラグラシア公式版・2026-06-22 若見え魅力タイプ版）
# 各タイプ：本来の魅力 / 崩れる条件 / 老け見え現象 の3ブロック構造
TYPE_PROFILES = {
    "A": {
        "code": "A",
        "name": "創造タイプ",
        "aging_name": "艶めき眠りタイプ",
        "tagline": "ひらめき・ときめき・表現力",
        "essence": (
            "本来は、ひらめき・ときめき・表現力で、"
            "まわりを明るくする魅力を持っている人。\n"
            "心が動いている時ほど、目に輝きが戻り、"
            "表情にも華やかさが出るタイプです。"
        ),
        "shadow": (
            "でも、日々の忙しさや役割に追われて、\n"
            "「楽しい」「やってみたい」「表現したい」という気持ちを抑え込んでしまうと、\n"
            "本来の艶や遊び心が眠ってしまいます。"
        ),
        "aging_signs": (
            "すると、目の輝きが弱くなったり、表情が単調になったり、\n"
            "どこか“自分らしさが薄れた印象”として出やすくなります。"
        ),
        # 既存pdf_generator互換用（後方互換）
        "body": (
            "本来は、ひらめき・ときめき・表現力で、まわりを明るくする魅力を持っている人。\n"
            "心が動いている時ほど、目に輝きが戻り、表情にも華やかさが出るタイプです。\n\n"
            "でも、日々の忙しさや役割に追われて、\n"
            "「楽しい」「やってみたい」「表現したい」という気持ちを抑え込んでしまうと、\n"
            "本来の艶や遊び心が眠ってしまいます。\n\n"
            "すると、目の輝きが弱くなったり、表情が単調になったり、\n"
            "どこか“自分らしさが薄れた印象”として出やすくなります。"
        ),
    },
    "B": {
        "code": "B",
        "name": "癒しタイプ",
        "aging_name": "尽くしすぎ疲れ顔タイプ",
        "tagline": "共感・安心感・包容力",
        "essence": (
            "本来は、人を安心させる優しさや、包み込むような温かさが魅力の人。\n"
            "そばにいるだけで、相手の心をゆるめるような柔らかい雰囲気を持っています。"
        ),
        "shadow": (
            "でも、人の気持ちを優先しすぎたり、家族やまわりのために頑張りすぎたりすると、\n"
            "自分の心と体のエネルギーが後回しになりやすいタイプです。"
        ),
        "aging_signs": (
            "すると、笑顔に力がなくなったり、目元に疲れが出たり、\n"
            "「優しいけれど、どこか疲れて見える」という印象になりやすくなります。"
        ),
        "body": (
            "本来は、人を安心させる優しさや、包み込むような温かさが魅力の人。\n"
            "そばにいるだけで、相手の心をゆるめるような柔らかい雰囲気を持っています。\n\n"
            "でも、人の気持ちを優先しすぎたり、家族やまわりのために頑張りすぎたりすると、\n"
            "自分の心と体のエネルギーが後回しになりやすいタイプです。\n\n"
            "すると、笑顔に力がなくなったり、目元に疲れが出たり、\n"
            "「優しいけれど、どこか疲れて見える」という印象になりやすくなります。"
        ),
    },
    "C": {
        "code": "C",
        "name": "導きタイプ",
        "aging_name": "背負い込み緊張タイプ",
        "tagline": "責任感・支える力・存在感",
        "essence": (
            "本来は、人を導き、支え、安心させる存在感が魅力の人。\n"
            "責任感があり、まわりから頼られやすく、"
            "自然と人の中心に立つ力を持っています。"
        ),
        "shadow": (
            "でも、責任感が強くなりすぎると、\n"
            "「私が何とかしなきゃ」\n"
            "「ちゃんとしていなきゃ」\n"
            "と、知らないうちに背負い込みやすくなります。"
        ),
        "aging_signs": (
            "すると、顔・姿勢・声に緊張感が出やすくなり、\n"
            "本当は温かい人なのに、少し近寄りにくい印象や、"
            "疲れている印象に見えやすくなります。"
        ),
        "body": (
            "本来は、人を導き、支え、安心させる存在感が魅力の人。\n"
            "責任感があり、まわりから頼られやすく、自然と人の中心に立つ力を持っています。\n\n"
            "でも、責任感が強くなりすぎると、\n"
            "「私が何とかしなきゃ」「ちゃんとしていなきゃ」と、\n"
            "知らないうちに背負い込みやすくなります。\n\n"
            "すると、顔・姿勢・声に緊張感が出やすくなり、\n"
            "本当は温かい人なのに、少し近寄りにくい印象や、疲れている印象に見えやすくなります。"
        ),
    },
    "D": {
        "code": "D",
        "name": "端正タイプ",
        "aging_name": "整え不足くすみタイプ",
        "tagline": "整える力・準備力・完成度",
        "essence": (
            "本来は、整える力・準備力・完成度の高さで、品よく若々しく見える人。\n"
            "身の回りや装い、言葉づかい、段取りが整っている時ほど、"
            "端正な魅力が引き立つタイプです。"
        ),
        "shadow": (
            "でも、忙しさに追われて、"
            "自分の身支度や暮らし、空間、予定を整える余裕がなくなると、\n"
            "心の中まで少しざわつきやすくなります。"
        ),
        "aging_signs": (
            "すると、本来の品の良さや清潔感が隠れてしまい、\n"
            "くすみや生活感、余裕のなさとして表れやすくなります。"
        ),
        "body": (
            "本来は、整える力・準備力・完成度の高さで、品よく若々しく見える人。\n"
            "身の回りや装い、言葉づかい、段取りが整っている時ほど、端正な魅力が引き立つタイプです。\n\n"
            "でも、忙しさに追われて、自分の身支度や暮らし、空間、予定を整える余裕がなくなると、\n"
            "心の中まで少しざわつきやすくなります。\n\n"
            "すると、本来の品の良さや清潔感が隠れてしまい、\n"
            "くすみや生活感、余裕のなさとして表れやすくなります。"
        ),
    },
}


# 点数強度の判定（24問×4タイプ、各タイプ最大24点）
def get_strength_level(score: int) -> str:
    if score >= 14:
        return "かなり強いタイプ"
    elif score >= 10:
        return "才能として強く持っている"
    elif score >= 6:
        return "状況によって出やすい"
    else:
        return "現在は抑えている可能性"


def calculate_jinsei_kaika(answers: dict) -> dict:
    """24問の回答からタイプ判定（メイン+隠れ才能）
    answers: {"K1": "A", "K2": "B", ...}
    """
    type_scores = {"A": 0, "B": 0, "C": 0, "D": 0}

    for q in QUESTIONS:
        ans = answers.get(q["id"])
        if ans in type_scores:
            type_scores[ans] += 1

    # ソート（同点時の優先順位は A>B>C>D）
    sorted_types = sorted(type_scores.items(), key=lambda x: (-x[1], x[0]))
    main_code, main_score = sorted_types[0]
    second_code, second_score = sorted_types[1] if len(sorted_types) > 1 else (None, 0)

    main_profile = TYPE_PROFILES.get(main_code, {})
    second_profile = TYPE_PROFILES.get(second_code, {}) if second_code else {}

    return {
        "type": main_code,
        "name": main_profile.get("name", ""),
        "aging_name": main_profile.get("aging_name", ""),
        "tagline": main_profile.get("tagline", ""),
        "body": main_profile.get("body", ""),
        "essence": main_profile.get("essence", ""),
        "shadow": main_profile.get("shadow", ""),
        "aging_signs": main_profile.get("aging_signs", ""),
        "score": main_score,
        "strength_level": get_strength_level(main_score),
        "second_type": second_code,
        "second_name": second_profile.get("name", ""),
        "second_aging_name": second_profile.get("aging_name", ""),
        "second_tagline": second_profile.get("tagline", ""),
        "second_body": second_profile.get("body", ""),
        "second_essence": second_profile.get("essence", ""),
        "second_shadow": second_profile.get("shadow", ""),
        "second_aging_signs": second_profile.get("aging_signs", ""),
        "second_score": second_score,
        "all_scores": type_scores,
    }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # サラさん想定（創造×美意識）の回答
    sara_answers = {}
    for i in range(1, 25):
        # 創造タイプ寄り：A中心、Dも多め
        if i % 3 == 0:
            sara_answers[f"K{i}"] = "D"
        elif i % 5 == 0:
            sara_answers[f"K{i}"] = "C"
        else:
            sara_answers[f"K{i}"] = "A"
    result = calculate_jinsei_kaika(sara_answers)
    print(f"メインタイプ: {result['type']} - {result['name']}")
    print(f"  点数: {result['score']}/24（{result['strength_level']}）")
    print(f"  タグライン: {result['tagline']}")
    print(f"隠れ才能タイプ: {result['second_type']} - {result['second_name']}")
    print(f"  点数: {result['second_score']}/24")
    print(f"\n全タイプスコア: {result['all_scores']}")
