"""
人生開花タイプ診断 Webアプリ（Streamlit）v3.2
18問拡張版・7軸総合判定
"""
import streamlit as st
from datetime import date, datetime, time
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import run_diagnosis
from pdf_generator import generate_pdf
from calculations.personality_quiz import NARRATIVE_QUESTIONS
from calculations.jinsei_kaika import QUESTIONS as KAIKA_QUESTIONS, LIKERT_OPTIONS
from email_sender import send_pdf_email


st.set_page_config(
    page_title="人生開花タイプ診断 - サラグラシアアカデミー",
    page_icon="🌹",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header { text-align: center; color: #8B4789; font-size: 2.5em; margin-bottom: 0; }
    .sub-header { text-align: center; color: #C0392B; font-style: italic; margin-bottom: 30px; }
    .stButton>button { background-color: #8B4789; color: white; border-radius: 25px;
                       padding: 12px 40px; font-size: 1.1em; border: none; width: 100%; }
    .stButton>button:hover { background-color: #6C3483; }
    div[data-testid="stExpander"] { background-color: #F4ECF7; border-radius: 10px; }
    .stProgress > div > div { background-color: #8B4789; }
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">🌹 人生開花タイプ診断</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">人生再起動のための、あなた専用の設計図<br>監修：山岡サラ（サラグラシアアカデミー）</p>',
            unsafe_allow_html=True)

st.markdown("""
この**人生開花タイプ診断**は、東洋・西洋の占術と現代心理学を統合して、
**あなたという唯一無二の存在**を立体的に描き出します。

🔮 **占術**：数秘・西洋占星術・九星気学・四柱推命・動物キャラ・算命学・帝王学・姓名判断
🧠 **心理診断**：**サラグラシア独自の人生開花タイプ診断**（ウェルスダイナミクスを元に50代女性向けに発展・8タイプ）
🌙 **運勢**：天中殺・3年間のキーワード
✍️ **自由記述**：夢中体験・譲れない信念（あなたの言葉が、診断の深さを決めます）

**所要時間：約8〜10分**　→ **11ページの個人設計図PDF**をメールでお届け
""")

st.divider()


# ========== Step 1: 基本情報 ==========
st.subheader("👤 Step 1：基本情報")

col1, col2 = st.columns(2)
with col1:
    last_name = st.text_input("姓（漢字）", placeholder="山岡")
    first_name = st.text_input("名（漢字）", placeholder="サラ")
with col2:
    name_kana = st.text_input("お名前（カタカナ）", placeholder="ヤマオカサラ")
    email = st.text_input("📧 メールアドレス（必須・診断結果のPDFをお送りします）", placeholder="your@email.com")

col3, col4, col5 = st.columns([2, 1, 2])
with col3:
    birth_date_input = st.date_input("生年月日", min_value=date(1900, 1, 1),
                                       max_value=date.today(), value=date(1980, 1, 1))
with col4:
    birth_time_unknown = st.checkbox("時間不明", value=False)
with col5:
    if not birth_time_unknown:
        birth_time_input = st.time_input("出生時間", value=time(12, 0))
    else:
        birth_time_input = time(12, 0)
        st.caption("12:00で計算します")

birth_place = st.text_input("出生地（都道府県＋市町村）",
                              placeholder="例：東京都新宿区 / 大阪府大阪市")


# ========== Step 2: 人生開花タイプ診断（20問） ==========
st.divider()
st.subheader("🌸 Step 2：人生開花タイプ診断（20問）")
st.caption("直感で、最も近いものを選んでください。所要時間 約5分。")
st.info("💡 この20問の回答から、あなたの **人生開花タイプ（8タイプ）** が判定されます。")

all_answers = {}
likert_keys = list(LIKERT_OPTIONS.keys())  # "5","4","3","2","1"
likert_labels = {k: v[0] for k, v in LIKERT_OPTIONS.items()}

with st.expander("質問を開始する（20問）", expanded=True):
    for i, q in enumerate(KAIKA_QUESTIONS, 1):
        st.markdown(f"**Q{i}. {q['question']}**")
        ans = st.radio(
            label=q['question'],
            options=likert_keys,
            format_func=lambda x, labels=likert_labels: labels[x],
            key=f"q_{q['id']}",
            label_visibility="collapsed",
            index=None,
            horizontal=True
        )
        all_answers[q['id']] = ans
        st.markdown("")

# プログレス計算
answered = sum(1 for v in all_answers.values() if v is not None)
progress = st.progress(answered / len(KAIKA_QUESTIONS))
st.caption(f"📊 進捗：{answered} / {len(KAIKA_QUESTIONS)} 問")


# ========== Step 3: 自由記述（必須・2問） ==========
st.divider()
st.subheader("✍️ Step 3：自由記述（必須・2問）")
st.caption("あなたの言葉が、診断の深さを決めます。200字以上、書ける範囲で具体的にお願いします。")
st.info("💡 この2問の回答から、あなたの **才能の指紋・落とし穴・価値観のコンパス** が浮かび上がります。")

narrative_answers = {}
for n in NARRATIVE_QUESTIONS:
    st.markdown(f"**{n['question']}**")
    st.caption(f"💡 ヒント：{n['hint']}")
    ans = st.text_area(
        label=n['question'], key=f"n_{n['id']}",
        label_visibility="collapsed", height=150,
        max_chars=n['max_length'],
        placeholder="（200字以上を目安に、できるだけ具体的に）"
    )
    narrative_answers[n['id']] = ans
    st.markdown("")


# ========== 診断ボタン ==========
st.divider()

narrative_filled = all(len(narrative_answers.get(n['id'], '').strip()) >= 50
                        for n in NARRATIVE_QUESTIONS)

input_valid = bool(last_name and first_name and name_kana and birth_place
                   and email and "@" in email and answered >= 15
                   and narrative_filled)

if not input_valid:
    if not (last_name and first_name and name_kana and birth_place):
        st.warning("⚠️ 基本情報（姓・名・カタカナ氏名・出生地）をすべて入力してください。")
    elif not email or "@" not in email:
        st.warning("⚠️ メールアドレスを入力してください（診断結果のPDFをメールでお送りします）。")
    elif answered < 15:
        st.warning(f"⚠️ 質問にあと {15 - answered} 問は回答してください（精度向上のため・最低15問必須）。")
    elif not narrative_filled:
        st.warning("⚠️ 自由記述2問にそれぞれ50字以上ご記入ください（あなたの言葉が診断の深さを決めます）。")

if st.button("✨ あなたの人生開花タイプを診断する ✨", disabled=not input_valid):
    with st.spinner("あなたの占術データと性格を計算中... 🔮"):
        user_input = {
            "name": f"{last_name} {first_name}",
            "last_name": last_name,
            "first_name": first_name,
            "name_kana": name_kana,
            "birth_date": birth_date_input.strftime("%Y-%m-%d"),
            "birth_time": birth_time_input.strftime("%H:%M"),
            "birth_place": birth_place,
            "lat": 35.6762, "lon": 139.6503,
            "answers": {k: v for k, v in all_answers.items() if v is not None},
            "narrative": narrative_answers,
        }

        try:
            result = run_diagnosis(user_input)

            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                pdf_path = tmp.name
            generate_pdf(user_input, result, pdf_path)

            st.success("✅ 診断完了！レポートPDFをメールでお送りします。")
            st.markdown("---")
            st.markdown("### 🔮 あなたの主要結果")

            mbti = result['personality']['mbti']
            wd = result['personality']['wd']

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**🧠 16パーソナリティ：{mbti['type']}**")
                st.markdown(f"_{mbti.get('label', '')}_")
                st.markdown(f"**💎 ウェルスダイナミクス：{wd['type']}**")
                st.markdown(f"_{wd.get('label', '')}_")
                st.markdown(f"**🦁 太陽星座：{result['western_astrology']['sun']['name']}**")
                st.markdown(f"**🌙 月星座：{result['western_astrology']['moon']['name']}**")
            with col_b:
                st.markdown(f"**🐘 動物キャラ：{result['doubutsu']['name_60']}**")
                st.markdown(f"（12種：{result['doubutsu']['name_12']}）")
                st.markdown(f"**⭐ 算命学・主星：{result['shusei']['name']}**")
                st.markdown(f"**👑 帝王学：{result['teiou']['name']}**")
                tc_periods = result.get('tenchusatsu_years', {})
                next_p = tc_periods.get('next_period')
                if next_p:
                    st.markdown(f"**🌙 次の天中殺：{next_p[0]}年〜{next_p[1]}年**")

            st.markdown("---")
            st.markdown(f"### 📧 PDFレポートを **{email}** にお送りします")
            st.caption("8ページの完全版PDFが添付ファイルで届きます。")

            with st.spinner("メール送信中... 📨"):
                result = send_pdf_email(email, user_input['name'], pdf_path)
                if result['success']:
                    st.success(f"""
✅ **{email} にメールを送信しました！**

📬 メールボックスをご確認ください。

⚠️ **届かない場合**：
- 迷惑メールフォルダもチェックしてください
- 5分待っても届かない場合は、メールアドレスを確認して再度診断してください
                    """)
                    st.balloons()
                else:
                    st.error(f"❌ メール送信に失敗しました\n\n{result['message']}")
                    st.info("メールアドレスを確認して、もう一度診断してください。")

            # 一時ファイルを削除
            try:
                os.unlink(pdf_path)
            except Exception:
                pass

        except Exception as e:
            st.error(f"診断中にエラーが発生しました：{e}")
            st.exception(e)


st.divider()
st.markdown("""
<div style='text-align:center; color:#888; font-size:0.85em; margin-top:30px;'>
    人生開花タイプ診断 v4.0<br>
    監修：山岡サラ（サラグラシアアカデミー）<br>
    『人生は、何度でも再起動できる』
</div>
""", unsafe_allow_html=True)
