"""
若見え魅力タイプ診断 Webアプリ（Streamlit）v5.2
マルチステップ・フォーム化（離脱率低減・サンクコスト効果でメアド入力率UP）
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
from calculations.jinsei_kaika import QUESTIONS as KAIKA_QUESTIONS
from email_sender import send_pdf_email, send_admin_notification


st.set_page_config(
    page_title="若見え魅力タイプ診断 - サラグラシアアカデミー",
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
    .stButton>button:disabled { background-color: #ccc; color: #888; }
    div[data-testid="stExpander"] { background-color: #F4ECF7; border-radius: 10px; }
    .stProgress > div > div { background-color: #8B4789; }
    .question-card {
        background: #FAF5FB;
        border-left: 4px solid #8B4789;
        padding: 20px 24px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ========== セッション状態の初期化 ==========
def init_session_state():
    defaults = {
        'step': 1,                  # 1=基本情報, 2=24問, 3=自由記述, 4=メアド, 5=診断実行
        'question_index': 0,        # 何問目を表示中か（0〜23）
        'answers': {},              # 24問の回答 {q_id: "A/B/C/D"}
        'narrative_answers': {},    # 自由記述2問の回答
        'last_name': '',
        'first_name': '',
        'name_kana': '',
        'birth_date': date(1970, 1, 1),
        'birth_time': time(12, 0),
        'birth_time_unknown': True,
        'birth_place': '',
        'email': '',
        'diagnosis_completed': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state()


# ========== 共通ヘッダー（全ステップで表示） ==========
def render_header():
    st.markdown('<h1 class="main-header">🌹 若見え魅力タイプ診断</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">老けて見える本当の理由と、あなた本来の輝き方がわかる<br>監修：山岡サラ（サラグラシアアカデミー）</p>',
                unsafe_allow_html=True)


# ========== Step 1: 基本情報 ==========
def render_step_1():
    render_header()

    st.markdown("""
最近、写真や鏡を見て
「私、こんなに疲れて見えていた？」
と思ったことはありませんか？

老け見えの原因は、シワやたるみだけではありません。

自分を後回しにすること。
人の期待に応えすぎること。
心が満たされないまま、頑張り続けること。

そうした内側の状態が、知らないうちに表情や雰囲気に表れることがあります。

この診断では、あなたの**生年月日・お名前・心理傾向**から、
あなたが本来持っている**魅力**と、もう一度**若々しい印象**を取り戻すための整え方を読み解きます。

無理な若作りではなく、
今のあなたのまま、もう一度きれいに咲くための診断です。

**所要時間：約7〜10分**　→ **個人設計図PDF**を最後にメールでお届けします
""")

    st.divider()
    st.subheader("👤 まずは、あなたのことを少しだけ")

    col1, col2 = st.columns(2)
    with col1:
        last_name = st.text_input("姓（漢字）", value=st.session_state.last_name, placeholder="山岡")
    with col2:
        first_name = st.text_input("名（漢字）", value=st.session_state.first_name, placeholder="サラ")

    name_kana = st.text_input("お名前（カタカナ・スペースなしで入力）",
                              value=st.session_state.name_kana,
                              placeholder="ヤマオカサラ",
                              help="姓と名の間にスペースを入れず、続けてご入力ください")

    birth_date_input = st.date_input("生年月日",
                                       value=st.session_state.birth_date,
                                       min_value=date(1900, 1, 1),
                                       max_value=date.today())

    st.markdown("")
    st.markdown("---")
    st.markdown("##### 🌙 ここから先は任意項目です")
    st.caption("分かれば、より精密な**西洋占星術の診断**が追加されます。空欄のままでも診断可能です。")

    col3, col4 = st.columns([1, 2])
    with col3:
        birth_time_unknown = st.checkbox("時間は分からない", value=st.session_state.birth_time_unknown)
    with col4:
        if not birth_time_unknown:
            birth_time_input = st.time_input("出生時間（任意）", value=st.session_state.birth_time)
        else:
            birth_time_input = time(12, 0)
            st.caption("（12:00で計算します）")

    birth_place = st.text_input("出生地（任意・都道府県＋市町村）",
                                 value=st.session_state.birth_place,
                                 placeholder="例：東京都新宿区")

    st.markdown("")

    # 必須項目チェック
    step1_valid = bool(last_name.strip() and first_name.strip() and name_kana.strip())

    if not step1_valid:
        st.caption("⚠️ 姓・名・カタカナ氏名は必須です")

    if st.button("次へ →", disabled=not step1_valid, key="btn_step1_next"):
        # session_state に保存
        st.session_state.last_name = last_name.strip()
        st.session_state.first_name = first_name.strip()
        st.session_state.name_kana = name_kana.strip()
        st.session_state.birth_date = birth_date_input
        st.session_state.birth_time = birth_time_input
        st.session_state.birth_time_unknown = birth_time_unknown
        st.session_state.birth_place = birth_place.strip()
        st.session_state.step = 2
        st.session_state.question_index = 0
        st.rerun()


# ========== Step 2: 24問の質問（1問ずつ） ==========
def render_step_2():
    render_header()

    q_idx = st.session_state.question_index
    total = len(KAIKA_QUESTIONS)
    q = KAIKA_QUESTIONS[q_idx]

    # 進捗バー
    progress_val = (q_idx + 1) / total
    st.progress(progress_val)
    st.caption(f"📊 質問 **{q_idx + 1}** / {total}")

    st.markdown("##### 🌸 若見え魅力タイプ診断")
    st.caption("「最も近いもの」を1つ選んでください")

    st.markdown(f'<div class="question-card"><h4>Q{q_idx + 1}. {q["question"]}</h4></div>',
                unsafe_allow_html=True)

    options = q['options']
    current_ans = st.session_state.answers.get(q['id'])

    options_keys = list(options.keys())
    default_index = options_keys.index(current_ans) if current_ans in options_keys else None

    ans = st.radio(
        label="選択肢",
        options=options_keys,
        format_func=lambda x: f"{x}: {options[x]}",
        key=f"radio_q_{q['id']}",
        index=default_index,
        label_visibility="collapsed",
    )

    st.markdown("")

    # ナビゲーション
    col_back, col_next = st.columns(2)
    with col_back:
        if q_idx > 0:
            if st.button("← 戻る", key=f"btn_back_{q_idx}"):
                if ans is not None:
                    st.session_state.answers[q['id']] = ans
                st.session_state.question_index -= 1
                st.rerun()
        else:
            if st.button("← 基本情報に戻る", key="btn_back_to_step1"):
                if ans is not None:
                    st.session_state.answers[q['id']] = ans
                st.session_state.step = 1
                st.rerun()
    with col_next:
        if q_idx < total - 1:
            if st.button("次へ →", disabled=(ans is None), key=f"btn_next_{q_idx}"):
                st.session_state.answers[q['id']] = ans
                st.session_state.question_index += 1
                st.rerun()
        else:
            if st.button("質問完了 →", disabled=(ans is None), key="btn_to_step3"):
                st.session_state.answers[q['id']] = ans
                st.session_state.step = 3
                st.rerun()


# ========== Step 3: 自由記述（2問・任意） ==========
def render_step_3():
    render_header()

    st.progress(1.0)
    st.caption("📊 質問は完了しました")

    st.subheader("✍️ もう少しだけ、あなたの言葉を聞かせてください")

    st.markdown("""
ここからは **任意** です。
空欄のままでも診断は完成します。

ただ——

占術データだけだと、診断は「**あなたタイプの一般的な傾向**」で止まってしまいます。

ここに**あなた自身の言葉**が加わると、診断は
「**あなただけの個人設計図**」に変わります。

特に、次の3つが鮮明になります：

🌸 **あなたの才能の指紋** — 占術では見えない、あなただけの輝き方
🌸 **あなたの落とし穴** — 同じパターンで繰り返してしまう癖
🌸 **あなたの価値観のコンパス** — 人生で本当に大切にしたいもの

書ける範囲で大丈夫です。
**書いていただくほど、診断は深く、あなただけのものになります。**
""")

    st.caption("⚠️ 入力後、テキストボックスの外を一度クリックすると文字数が反映されます（Streamlitの仕様）")

    st.markdown("")

    filled_count = 0
    for n in NARRATIVE_QUESTIONS:
        st.markdown(f"**{n['question']}** _（任意）_")
        st.caption(f"💡 ヒント：{n['hint']}")
        current_val = st.session_state.narrative_answers.get(n['id'], '')
        ans = st.text_area(
            label=n['question'],
            value=current_val,
            key=f"n_{n['id']}",
            label_visibility="collapsed",
            height=150,
            max_chars=n['max_length'],
            placeholder="（書ける範囲で。50字以上書くと、診断が深くなります）"
        )
        st.session_state.narrative_answers[n['id']] = ans
        char_count = len((ans or '').strip())
        if char_count == 0:
            st.caption("📝 空欄でも次に進めます。書いていただくと診断が深くなります。")
        elif char_count < 50:
            st.caption(f"📝 現在 **{char_count}字** / あと {50 - char_count}字書くと診断が深くなります")
        elif char_count < 200:
            st.caption(f"✅ 現在 **{char_count}字** — 十分です。200字を目安にするとさらに深くなります")
            filled_count += 1
        else:
            st.caption(f"✨ 現在 **{char_count}字** — 深い診断に十分な分量です")
            filled_count += 1
        st.markdown("")

    # 何も書いていない時のさりげない後押し（押し付けすぎない）
    if filled_count == 0:
        st.info("💡 **時間がない方は空欄のままで大丈夫**です。「次へ」を押せば診断結果に進みます。\n\n"
                "ただ、ここを少しでも書いていただけると、診断結果のあなたへのメッセージが、ぐっと立体的になります。")

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("← 質問に戻る", key="btn_back_to_q"):
            st.session_state.question_index = len(KAIKA_QUESTIONS) - 1
            st.session_state.step = 2
            st.rerun()
    with col_next:
        # 任意化：常に次へ進める
        btn_label = "次へ →" if filled_count > 0 else "空欄のまま次へ →"
        if st.button(btn_label, key="btn_to_step4"):
            st.session_state.step = 4
            st.rerun()


# ========== Step 4: メールアドレス入力（最後） ==========
def render_step_4():
    render_header()

    st.progress(1.0)

    st.markdown("""
### 🎉 お疲れさまでした！

あなただけの「**若見え魅力タイプ診断レポート**」が、もうすぐ完成します。

診断結果は約20ページのPDFで、サラさんからの個別メッセージとともに、
あなたのメールアドレスにお届けします。
""")

    st.markdown("")

    email = st.text_input("📧 PDFをお届けするメールアドレス",
                          value=st.session_state.email,
                          placeholder="your@email.com",
                          key="input_email")
    st.session_state.email = email

    email_valid = bool(email and "@" in email and "." in email)
    if email and not email_valid:
        st.caption("⚠️ メールアドレスの形式が正しくないようです")

    st.caption("📌 入力されたアドレスは診断レポート送付以外には使用しません。")

    st.markdown("")

    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("← 戻る", key="btn_back_to_narrative"):
            st.session_state.step = 3
            st.rerun()
    with col_submit:
        if st.button("✨ 診断結果を受け取る ✨", disabled=not email_valid, key="btn_diagnose"):
            st.session_state.step = 5
            st.rerun()


# ========== Step 5: 診断実行＋結果表示 ==========
def render_step_5():
    render_header()

    if st.session_state.diagnosis_completed:
        st.success("✅ 診断は完了しています。メールをご確認ください。")
        if st.button("🔄 もう一度診断する", key="btn_restart"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        return

    user_input = {
        "name": f"{st.session_state.last_name} {st.session_state.first_name}",
        "last_name": st.session_state.last_name,
        "first_name": st.session_state.first_name,
        "name_kana": st.session_state.name_kana,
        "birth_date": st.session_state.birth_date.strftime("%Y-%m-%d"),
        "birth_time": st.session_state.birth_time.strftime("%H:%M"),
        "birth_place": st.session_state.birth_place or "東京都",
        "lat": 35.6762, "lon": 139.6503,
        "answers": {k: v for k, v in st.session_state.answers.items() if v is not None},
        "narrative": st.session_state.narrative_answers,
    }

    with st.spinner("あなたの占術データと性格を計算中... 🔮"):
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
            st.markdown(f"### 📧 PDFレポートを **{st.session_state.email}** にお送りします")

            with st.spinner("メール送信中... 📨"):
                user_input['email_to'] = st.session_state.email
                user_input['narrative'] = st.session_state.narrative_answers
                admin_result = None
                try:
                    admin_result = send_admin_notification(user_input, result, pdf_path)
                except Exception as e:
                    admin_result = {"success": False, "message": f"Exception: {e}"}

                if admin_result and not admin_result.get('success'):
                    st.caption(f"🔧 管理者通知デバッグ: {admin_result.get('message', '不明')}")

                email_result = send_pdf_email(st.session_state.email,
                                               user_input['name'],
                                               pdf_path)
                if email_result['success']:
                    st.success(f"""
✅ **{st.session_state.email} にメールを送信しました！**

📬 メールボックスをご確認ください。

⚠️ **届かない場合**：
- 迷惑メールフォルダもチェックしてください
- 5分待っても届かない場合は、メールアドレスを確認して再度診断してください
                    """)
                    if admin_result and admin_result.get('success'):
                        st.caption(f"📊 管理者通知も送信済み: {admin_result.get('message')}")
                    st.balloons()
                    st.session_state.diagnosis_completed = True
                else:
                    st.error(f"❌ メール送信に失敗しました\n\n{email_result['message']}")
                    st.info("メールアドレスを確認して、もう一度お試しください。")
                    if st.button("← メールアドレスを修正する"):
                        st.session_state.step = 4
                        st.rerun()

            try:
                os.unlink(pdf_path)
            except Exception:
                pass

        except Exception as e:
            st.error(f"診断中にエラーが発生しました：{e}")
            st.exception(e)
            if st.button("← 最初に戻る"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()


# ========== ステップディスパッチャ ==========
step = st.session_state.step

if step == 1:
    render_step_1()
elif step == 2:
    render_step_2()
elif step == 3:
    render_step_3()
elif step == 4:
    render_step_4()
elif step == 5:
    render_step_5()


# ========== フッター ==========
st.divider()
BUILD_VERSION = "v5.2 / 2026-06-22 multi-step-form"
st.markdown(f"""
<div style='text-align:center; color:#888; font-size:0.85em; margin-top:30px;'>
    若見え魅力タイプ診断 v5.2<br>
    監修：山岡サラ（サラグラシアアカデミー）<br>
    『人生は、何度でも再起動できる』<br>
    <span style='color:#bbb; font-size:0.8em;'>Build: {BUILD_VERSION}</span>
</div>
""", unsafe_allow_html=True)
