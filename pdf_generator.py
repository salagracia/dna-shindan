"""
PDF生成（8ページ拡張版）
詳細プロファイル・相性診断・運勢サイクルを含む
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

FONT_REGULAR = None
FONT_BOLD = None


def register_japanese_fonts():
    """日本語フォント登録（環境別自動切替）
    優先順位：
    1. ローカル同梱 IPAex Gothic（fonts/ipaexg.ttf）← Render等のLinuxサーバー
    2. Windows標準フォント
    3. Mac標準フォント
    4. Linuxシステムフォント
    5. ReportLab CID内蔵フォント（最終フォールバック）
    """
    global FONT_REGULAR, FONT_BOLD

    # プロジェクトルートからのパス
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. ローカル同梱 IPAex（最優先・どの環境でも動く）
    local_fonts = [
        ('IPAexGothic', os.path.join(project_dir, 'fonts', 'ipaexg.ttf'),
                         os.path.join(project_dir, 'fonts', 'ipaexg.ttf')),
        ('IPAexMincho', os.path.join(project_dir, 'fonts', 'ipaexm.ttf'),
                         os.path.join(project_dir, 'fonts', 'ipaexm.ttf')),
    ]

    # 2. システム標準フォント候補
    system_fonts = [
        # Windows
        ('YuGothic', r'C:\Windows\Fonts\YuGothM.ttc', r'C:\Windows\Fonts\YuGothB.ttc'),
        ('Meiryo', r'C:\Windows\Fonts\meiryo.ttc', r'C:\Windows\Fonts\meiryob.ttc'),
        ('MSGothic', r'C:\Windows\Fonts\msgothic.ttc', r'C:\Windows\Fonts\msgothic.ttc'),
        # Mac
        ('HiraginoSans', '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                          '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'),
        # Linux (Render/Debian/Ubuntu系)
        ('NotoSansCJK', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                         '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'),
        ('IPAexSys', '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf',
                      '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'),
    ]

    all_candidates = local_fonts + system_fonts

    for name, regular_path, bold_path in all_candidates:
        try:
            if os.path.exists(regular_path):
                # TTC（コレクション）と TTF を区別
                if regular_path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont(name, regular_path, subfontIndex=0))
                else:
                    pdfmetrics.registerFont(TTFont(name, regular_path))
                FONT_REGULAR = name

                if os.path.exists(bold_path) and bold_path != regular_path:
                    try:
                        bold_name = f"{name}-Bold"
                        if bold_path.endswith('.ttc'):
                            pdfmetrics.registerFont(TTFont(bold_name, bold_path, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                        FONT_BOLD = bold_name
                    except Exception:
                        FONT_BOLD = name
                else:
                    FONT_BOLD = name

                print(f"[FONT] Registered: {name} (regular={regular_path})")
                return
        except Exception as e:
            print(f"[FONT] Failed {name}: {e}")
            continue

    # 5. ReportLab CID内蔵フォント（フォールバック・PDF Viewer依存）
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
        FONT_REGULAR = 'HeiseiKakuGo-W5'
        FONT_BOLD = 'HeiseiKakuGo-W5'
        print(f"[FONT] Registered CID fallback: HeiseiKakuGo-W5")
        return
    except Exception as e:
        print(f"[FONT] CID font fallback failed: {e}")

    raise RuntimeError("日本語フォントが見つかりません（IPAex fontsがリポジトリに含まれているか確認してください）")


def make_styles():
    styles = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('TitleJP', parent=styles['Title'], fontName=FONT_BOLD,
                                 fontSize=24, leading=30, alignment=TA_CENTER,
                                 textColor=colors.HexColor('#8B4789'), spaceAfter=15),
        'h1': ParagraphStyle('H1JP', parent=styles['Heading1'], fontName=FONT_BOLD,
                              fontSize=16, leading=22, textColor=colors.HexColor('#8B4789'),
                              spaceBefore=18, spaceAfter=6,
                              borderPadding=4, borderColor=colors.HexColor('#8B4789'),
                              borderWidth=0, leftIndent=0),
        'h2': ParagraphStyle('H2JP', parent=styles['Heading2'], fontName=FONT_BOLD,
                              fontSize=13, leading=18, textColor=colors.HexColor('#C0392B'),
                              spaceBefore=8, spaceAfter=4),
        'h3': ParagraphStyle('H3JP', parent=styles['Heading3'], fontName=FONT_BOLD,
                              fontSize=11, leading=15, textColor=colors.HexColor('#6C3483'),
                              spaceBefore=5, spaceAfter=3),
        'body': ParagraphStyle('BodyJP', parent=styles['Normal'], fontName=FONT_REGULAR,
                                fontSize=9.5, leading=15, textColor=colors.black,
                                alignment=TA_LEFT, spaceAfter=4),
        'small': ParagraphStyle('SmallJP', parent=styles['Normal'], fontName=FONT_REGULAR,
                                 fontSize=8, leading=12, textColor=colors.grey, alignment=TA_CENTER),
        'quote': ParagraphStyle('QuoteJP', parent=styles['Normal'], fontName=FONT_REGULAR,
                                 fontSize=10.5, leading=18, textColor=colors.HexColor('#6C3483'),
                                 leftIndent=15, rightIndent=15, spaceAfter=8,
                                 backColor=colors.HexColor('#F4ECF7')),
        'tip': ParagraphStyle('TipJP', parent=styles['Normal'], fontName=FONT_REGULAR,
                               fontSize=9.5, leading=15, textColor=colors.HexColor('#8B4789'),
                               leftIndent=15, spaceAfter=3),
    }


def bullet_list(items, styles):
    """ブレットリスト生成"""
    return ListFlowable(
        [ListItem(Paragraph(it, styles['body']), leftIndent=12) for it in items],
        bulletType='bullet', start='•', leftIndent=18, spaceBefore=2, spaceAfter=4
    )


def build_prologue(user_data: dict, result: dict, styles) -> list:
    """序章：あなたという奇跡
    山岡サラ監修・希望のトーンで、占術データを「数千〜数万人に1人」の希少性として提示。
    """
    elements = []
    name = user_data.get('first_name') or user_data.get('name', '').split(' ')[-1]
    birth_place = user_data.get('birth_place', '—')
    birth_time = user_data.get('birth_time', '—')
    ws = result.get('western_astrology', {})
    sun_sign = ws.get('sun', {}).get('name', '—')
    moon_sign = ws.get('moon', {}).get('name', '—')
    asc = ws.get('asc', {}).get('name', '—')
    kaika = result.get('personality', {}).get('jinsei_kaika', {})
    main_type = kaika.get('name', '—')
    main_tag = kaika.get('tagline', '')
    second_type = kaika.get('second_name', '—')
    second_tag = kaika.get('second_tagline', '')

    elements.append(Paragraph("序章　あなたという奇跡", styles['h1']))

    # 段落リスト：すべて body スタイル、一行ずつの改行リズムを <br/> で表現
    intro = (
        f"{name}さん。<br/><br/>"
        f"今、あなたはこのレポートをどんな気持ちで開いているでしょうか。<br/>"
        f"自分のことをもっと知りたい。<br/>"
        f"これからの人生をより豊かに生きたい。<br/>"
        f"あるいは、心のどこかで「私は本当は何者なのだろう」と感じているのかもしれません。<br/><br/>"
        f"このレポートは、そんな問いに対して一つの視点を提供するために作られました。<br/><br/>"
        f"まず最初にお伝えしたいことがあります。<br/>"
        f"それは、<b>「あなたは極めて希少な存在である」</b>という事実です。"
    )
    elements.append(Paragraph(intro, styles['body']))
    elements.append(Spacer(1, 4*mm))

    moment = (
        f"{name}さんが生まれたその瞬間。<br/>"
        f"<b>{birth_place}</b>の空の下で、<b>{birth_time}</b>という時刻に一つの命が誕生しました。<br/><br/>"
        f"その時、太陽は<b>{sun_sign}</b>にあり、<br/>"
        f"月は<b>{moon_sign}</b>を巡り、<br/>"
        f"地平線には<b>{asc}</b>が昇っていました。<br/><br/>"
        f"世界では同じ日にも多くの命が生まれていましたが、<br/>"
        f"まったく同じ条件で生まれた人は存在しません。<br/><br/>"
        f"私たちは普段、自分を「普通の一人」と考えがちです。<br/>"
        f"しかし数字で見てみると、まったく違う景色が見えてきます。"
    )
    elements.append(Paragraph(moment, styles['body']))
    elements.append(Spacer(1, 4*mm))

    # 希少性の数字証明（quoteスタイルで強調）
    rarity = (
        "太陽星座は12種類。月星座も12種類。<br/>"
        "数秘ライフパスは9種類。干支の組み合わせは60種類。<br/><br/>"
        "これだけでも、<b>12 × 12 × 9 × 60 ＝ 77,760通り</b>。<br/>"
        "さらに出生時刻と出生地を加味すると、<b>およそ93万通り以上</b>の組み合わせになります。<br/><br/>"
        "地球人口を約80億人とすると、<b>80億 ÷ 93万 ＝ 約8,600人</b>。<br/><br/>"
        f"つまり、{name}さんと同じ組み合わせを持つ人は、<br/>"
        "統計上およそ<b>8,600人に1人</b>程度。<br/><br/>"
        "そして実際には、育った環境、出会った人、経験してきた出来事まで含めれば、<br/>"
        "<b>まったく同じ人生を歩んだ人は一人も存在しません</b>。<br/><br/>"
        "これは占いの話ではありません。<br/>"
        "単純な組み合わせの計算から見ても、あなたが希少な存在であることを示す数字です。"
    )
    elements.append(Paragraph(rarity, styles['quote']))
    elements.append(Spacer(1, 4*mm))

    # 3つの層
    layers = (
        "このレポートでは、そんなあなたを<b>「3つの層」</b>から立体的に見ていきます。<br/><br/>"
        "<b>第一の層</b>は、生まれ持った傾向や資質を読み解く<b>命術の視点</b>。<br/><br/>"
        "<b>第二の層</b>は、今回の診断で導き出された<br/>"
        f"<b>「{main_type}（{main_tag}）」</b>という人生開花タイプの視点。<br/>"
        f"さらに、<b>「{second_type}（{second_tag}）」</b>という隠れた才能の視点。<br/><br/>"
        "<b>第三の層</b>は、あなた自身の言葉や選択から見えてくる<b>現実の視点</b>です。<br/><br/>"
        "人は一つの言葉では説明できません。<br/>"
        "だからこそ、このレポートでは一方向から決めつけるのではなく、<br/>"
        "複数の角度からあなたという存在を描いていきます。"
    )
    elements.append(Paragraph(layers, styles['body']))
    elements.append(Spacer(1, 4*mm))

    # メッセージの核
    core_message = (
        "大切なのは、<b>「何者かになること」</b>ではありません。<br/>"
        "むしろ、<b>「すでに持っているものに気づくこと」</b>です。<br/><br/>"
        "人は欠けているから成長するのではなく、<br/>"
        "持っているものを使い始めることで人生が動き出します。<br/><br/>"
        "このレポートは、未来を予言するためのものではありません。<br/>"
        "<b>あなたの中にすでに存在している可能性を、見つけやすくするための地図</b>です。"
    )
    elements.append(Paragraph(core_message, styles['quote']))
    elements.append(Spacer(1, 4*mm))

    # 読み方ガイド
    elements.append(Paragraph("📖 このレポートの読み方", styles['h2']))
    guide = (
        "もし最初に読むなら、<br/>"
        "・<b>第1章「あなたの本質」</b><br/>"
        "・<b>第2章「人生開花タイプ」</b><br/>"
        "・<b>第4章「人生の追い風とブレーキ」</b><br/>"
        "から読み進めてください。今の自分を理解するヒントが見つかるはずです。<br/><br/>"
        "また、迷った時、自信を失った時、人生の転機を迎えた時には、<br/>"
        "<b>第5章「これからの開花シナリオ」</b>を開いてみてください。<br/>"
        "そこには、今のあなたが忘れかけている大切な視点が記されています。"
    )
    elements.append(Paragraph(guide, styles['body']))
    elements.append(Spacer(1, 4*mm))

    # 結びの一文
    closing = (
        f"{name}さん。<br/><br/>"
        "あなたの人生は、誰かの人生のコピーではありません。<br/>"
        "そしてあなたという存在は、数字で見ても、経験で見ても、<br/>"
        "<b>二度と再現されない唯一の組み合わせ</b>です。<br/><br/>"
        "ここから始まるページは、その事実を思い出すための旅になります。"
    )
    elements.append(Paragraph(closing, styles['quote']))

    return elements


def generate_pdf(user_data: dict, result: dict, output_path: str):
    register_japanese_fonts()
    styles = make_styles()

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=f"人生開花タイプ診断レポート - {user_data['name']}"
    )

    story = []

    # ============== Page 1: 表紙 ==============
    story.append(Spacer(1, 18*mm))
    story.append(Paragraph("人生開花タイプ診断レポート", styles['title']))
    story.append(Paragraph("人生再起動のための、あなた専用の設計図", styles['small']))
    story.append(Spacer(1, 20*mm))

    user_info = [
        ['氏名', user_data['name']],
        ['生年月日', user_data['birth_date']],
        ['出生時間', user_data.get('birth_time', '不明')],
        ['出生地', user_data.get('birth_place', '不明')],
        ['診断日', datetime.now().strftime('%Y-%m-%d')],
    ]
    tbl = Table(user_info, colWidths=[40*mm, 100*mm])
    tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR), ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#8B4789')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F4ECF7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#8B4789')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 14*mm))
    story.append(Paragraph(
        "東洋・西洋の占術と現代心理学を統合し、<br/>"
        "あなたという唯一無二の存在を立体的に描き出した、<br/>"
        "<b>あなただけの個人設計図</b>です。",
        styles['body']
    ))
    story.append(PageBreak())

    # ============== 序章：あなたという奇跡 ==============
    for el in build_prologue(user_data, result, styles):
        story.append(el)
    story.append(PageBreak())

    # ============== 第1章：あなたの本質（占術データ一覧） ==============
    story.append(Paragraph("第1章：あなたの本質", styles['h1']))
    story.append(Paragraph("8つの占術が語る、あなたの生まれ持った設計", styles['body']))
    story.append(Spacer(1, 5*mm))

    n = result['numerology']
    ws = result['western_astrology']
    ky = result['kyusei']
    sp = result['shichuusuimei']

    occult_data = [
        ['占術', 'あなたの結果', '意味'],
        ['数秘・ライフパス', f"{n['life_path']['number']}", n['life_path']['meaning'][:30]],
        ['数秘・誕生数', f"{n['birth_day']['number']}", n['birth_day']['meaning'][:30]],
        ['太陽星座', ws['sun']['name'], ws['sun']['theme']],
        ['月星座', ws['moon']['name'], ws['moon'].get('theme', '感情と本能の核')],
        ['アセンダント', ws['asc']['name'], '外向きの表情'],
        ['本命星（九星）', ky['honmei']['name'], ky['honmei']['meaning'][:30]],
        ['月命星', ky['gekkimei']['name'], ky['gekkimei']['meaning'][:30]],
        ['年柱（四柱）', sp['year']['kanshi'], sp['year']['meaning']],
        ['月柱（四柱）', sp['month']['kanshi'], sp['month']['meaning']],
        ['日柱（四柱）', sp['day']['kanshi'], sp['day']['meaning']],
        ['時柱（四柱）', sp.get('hour', {}).get('kanshi', '-'), sp.get('hour', {}).get('meaning', '-')],
        ['動物キャラ（個性心理学）',
         f"{result['doubutsu'].get('name_60', '')}\n（12種類：{result['doubutsu'].get('name_12', '')}）",
         result['doubutsu']['meaning']],
        ['算命学（主星）', result['shusei']['name'], result['shusei']['meaning'][:30]],
        ['帝王学', result['teiou']['name'], result['teiou']['meaning'][:30]],
        ['人生開花タイプ（メイン）', result['personality']['jinsei_kaika']['type'], result['personality']['jinsei_kaika'].get('name', '')],
        ['隠れ才能タイプ', result['personality']['jinsei_kaika'].get('second_type', ''), result['personality']['jinsei_kaika'].get('second_name', '')],
    ]

    tbl = Table(occult_data, colWidths=[38*mm, 55*mm, 77*mm])
    tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR), ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4789')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#F4ECF7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    story.append(tbl)

    # 第1章 本文（narrative_generatorから取得・サラ専用テスト本文／Phase2でAPI生成）
    from calculations.narrative_generator import get_chapter1_narrative
    ch1 = get_chapter1_narrative(user_data, result)
    if ch1:
        story.append(Spacer(1, 6*mm))
        for key in ['intro', 'theme', 'impression', 'conflict', 'shine']:
            story.append(Paragraph(ch1[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch1[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))
        story.append(Paragraph(
            "<i>このあと続く章では、その資質がどのような才能として現れ、<br/>"
            "どのように人生の追い風へと変わっていくのかを見ていきましょう。</i>",
            styles['quote']
        ))

    # ============== Page 3: 人生開花タイプ詳細（メイン） ==============
    mbti = result['personality']['mbti']
    story.append(Paragraph(f"第2章：あなたの人生開花タイプ", styles['h1']))

    # narrative_generatorから本文取得（サラ専用テスト本文／Phase2でAPI生成）
    from calculations.narrative_generator import get_chapter2_narrative
    ch2 = get_chapter2_narrative(user_data, result)
    if ch2:
        story.append(Paragraph(f"あなたのタイプ：<b>{mbti['type']} — {mbti.get('label', '')}</b>", styles['h2']))
        for key in ['talent', 'scene', 'past', 'bloom', 'future']:
            story.append(Paragraph(ch2[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch2[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))
    else:
        # フォールバック（旧テンプレ）
        story.append(Paragraph(f"あなたのタイプ：<b>{mbti['type']} — {mbti.get('label', '')}</b>", styles['h2']))
        story.append(Paragraph(mbti.get('summary', ''), styles['quote']))

        story.append(Paragraph("💪 あなたの強み", styles['h3']))
        story.append(bullet_list(mbti.get('strengths', []), styles))

        story.append(Paragraph("⚠️ 気をつけたい弱点", styles['h3']))
        story.append(bullet_list(mbti.get('weaknesses', []), styles))

        story.append(Paragraph("💖 人間関係の特徴", styles['h3']))
        story.append(Paragraph(mbti.get('relationships', ''), styles['body']))

        story.append(Paragraph("💼 適職・キャリア", styles['h3']))
        story.append(Paragraph(mbti.get('career', ''), styles['body']))

        story.append(Paragraph("🎯 あなたが取り組むといいチャレンジ", styles['h3']))
        story.append(Paragraph(mbti.get('challenge', ''), styles['tip']))

    # ============== Page 4: 隠れ才能タイプ（第2位） ==============
    wd = result['personality']['wd']
    story.append(Paragraph(f"第3章：あなたの隠れ才能タイプ", styles['h1']))

    from calculations.narrative_generator import get_chapter3_narrative
    ch3 = get_chapter3_narrative(user_data, result)
    if ch3:
        story.append(Paragraph(f"あなたのタイプ：<b>{wd['type']} — {wd.get('label', '')}</b>", styles['h2']))
        for key in ['awakening', 'scene', 'overlap', 'practice', 'future']:
            story.append(Paragraph(ch3[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch3[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))
    else:
        # フォールバック（旧テンプレ）
        story.append(Paragraph(f"あなたのタイプ：<b>{wd['type']} — {wd.get('label', '')}</b>", styles['h2']))
        story.append(Paragraph(f"戦略：{wd.get('subtitle', '')}", styles['h3']))
        story.append(Paragraph(wd.get('summary', ''), styles['quote']))

        story.append(Paragraph("💎 あなたの強み", styles['h3']))
        story.append(bullet_list(wd.get('strengths', []), styles))

        story.append(Paragraph("⚠️ 気をつけたい弱点", styles['h3']))
        story.append(bullet_list(wd.get('weaknesses', []), styles))

        story.append(Paragraph("🌸 運気を上げる戦略", styles['h3']))
        story.append(Paragraph(wd.get('fortune_strategy', ''), styles['quote']))

    # ============== 第4章：人生の追い風とブレーキ ==============
    story.append(Paragraph("第4章：人生の追い風とブレーキ", styles['h1']))

    from calculations.narrative_generator import get_chapter4_narrative
    ch4 = get_chapter4_narrative(user_data, result)
    if ch4:
        for key in ['tailwind', 'overflow', 'brake', 'ally', 'mantra']:
            story.append(Paragraph(ch4[f'{key}_h2'], styles['h2']))
            # 「あなた専用の呪文」セクションだけ quote スタイルで強調
            body_style = styles['quote'] if key == 'mantra' else styles['body']
            story.append(Paragraph(ch4[f'{key}_body'], body_style))
            story.append(Spacer(1, 3*mm))
    else:
        story.append(Paragraph("あなたの中で働く2つの力——あなたを前に進ませるものと、立ち止まらせるもの", styles['body']))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph("📌 占術が示すあなたの才能の核", styles['h2']))
        talent_text = (
            f"{ws['sun']['name']}の太陽が示す「{ws['sun']['theme']}」、"
            f"そして「{n['life_path']['meaning'].split('。')[0]}」というライフパスが、"
            f"あなたの才能の中心軸を形作っています。<br/><br/>"
            f"{result['shusei']['name']}（算命学）と{ky['honmei']['name']}（九星気学）の組み合わせは、"
            f"<b>「{result['shusei']['meaning'].split('。')[0]}」</b>という資質を裏付けています。"
            f"動物キャラ「{result['doubutsu'].get('name_60', '')}」の特徴である"
            f"「{result['doubutsu']['meaning'].split('。')[0]}」も加わり、"
            f"独自の輝きを放つ人物像が浮かび上がります。"
        )
        story.append(Paragraph(talent_text, styles['body']))
        story.append(Spacer(1, 4*mm))

        story.append(Paragraph("🎯 あなたの使命の方向", styles['h2']))
        mission_text = (
            f"{result['teiou']['name']}（帝王学）のあり方が示す通り、"
            f"あなたの使命は<b>「{result['teiou']['meaning']}」</b>という方向にあります。<br/><br/>"
            f"{mbti['type']}としての「{mbti.get('summary', '').split('。')[0]}」を発揮しながら、"
            f"{wd['type']}（{wd.get('label', '')}）として"
            f"「{wd.get('summary', '').split('。')[0]}」を実践することが、"
            f"最も自然な人生の歩み方です。"
        )
        story.append(Paragraph(mission_text, styles['body']))
        story.append(Spacer(1, 4*mm))

        story.append(Paragraph("⚠️ あなたが気をつけるべき落とし穴", styles['h2']))
        pitfall_text = (
            f"あなたの最大の強み「{mbti.get('strengths', [''])[0]}」は、"
            f"そのまま最大の弱点「{mbti.get('weaknesses', [''])[0]}」と裏表です。<br/><br/>"
            f"{wd['type']}タイプの典型的な落とし穴である「{wd.get('weaknesses', [''])[0]}」も意識し、"
            f"<b>自分の強みを過信せず、補完してくれる仲間と組む</b>ことが鍵です。"
        )
        story.append(Paragraph(pitfall_text, styles['body']))

    # ============== 第5章：これからの開花シナリオ ==============
    fortune = result.get('fortune', {})
    fortune_3y = result.get('fortune_3years', [])
    tc_periods = result.get('tenchusatsu_years', {})
    tc = tc_periods.get('tenchusatsu', fortune.get('tenchusatsu_info', {}))
    prev_p = tc_periods.get('previous_period')
    next_p = tc_periods.get('next_period')
    current_p = tc_periods.get('current_period')

    story.append(Paragraph("第5章：これからの開花シナリオ", styles['h1']))

    from calculations.narrative_generator import get_chapter5_narrative
    ch5 = get_chapter5_narrative(user_data, result)
    if ch5:
        for key in ['three_years', 'pause', 'actions', 'release', 'letter']:
            story.append(Paragraph(ch5[f'{key}_h2'], styles['h2']))
            # 「1年後のあなたへ」セクションだけquoteスタイルで温度感UP
            body_style = styles['quote'] if key == 'letter' else styles['body']
            story.append(Paragraph(ch5[f'{key}_body'], body_style))
            story.append(Spacer(1, 3*mm))
        # 補足：天中殺の具体的な年（実用情報）
        story.append(Paragraph("📅 補足：あなたの「立ち止まる時期」の具体的な年", styles['h3']))
        period_lines = []
        if prev_p:
            period_lines.append(f"前回：<b>{prev_p[0]}年〜{prev_p[1]}年</b>")
        if current_p:
            period_lines.append(f"現在：<b>{current_p[0]}年〜{current_p[1]}年</b>（今まさにこの時期）")
        if next_p:
            period_lines.append(f"次回：<b>{next_p[0]}年〜{next_p[1]}年</b>（大きな決断はこの前までに）")
        story.append(Paragraph("<br/>".join(period_lines), styles['body']))
    else:
        # フォールバック（旧テンプレ）
        story.append(Paragraph("運勢サイクルを味方に、1年後のあなたを描く", styles['body']))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph("🌙 あなたの天中殺", styles['h2']))
        tc_text = (
            f"<b>{tc.get('name', '')}</b>（日柱：{tc.get('day_kanshi', '')}）<br/>"
            f"{tc.get('meaning', '')}"
        )
        story.append(Paragraph(tc_text, styles['quote']))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph("📅 あなたの天中殺の年（具体的時期）", styles['h3']))

        if prev_p:
            story.append(Paragraph(
                f"<b>前回の天中殺：{prev_p[0]}年〜{prev_p[1]}年</b>　← この2年に大きな変化があったはず",
                styles['body']
            ))
        if current_p:
            story.append(Paragraph(
                f"<b>現在の天中殺：{current_p[0]}年〜{current_p[1]}年</b>　← 今まさに天中殺中！",
                styles['body']
            ))
        if next_p:
            story.append(Paragraph(
                f"<b>★ 次の天中殺：{next_p[0]}年〜{next_p[1]}年</b>　← 大きな決断はこの前までに完了させる",
                styles['tip']
            ))

        all_periods = tc_periods.get('all_periods', [])
        if all_periods:
            all_str = "、".join([f"{s}-{e}" if s != e else f"{s}" for s, e in all_periods[:6]])
            story.append(Paragraph(f"<i>※ 全期間：{all_str}（12年周期で繰り返す）</i>", styles['small']))

        story.append(Spacer(1, 5*mm))

        story.append(Paragraph("🌸 これから3年のキーワード（毎年の運勢）", styles['h2']))

        year_data = [['年', '十二支', 'キーワード', '解説', '天中殺']]
        for f in fortune_3y:
            is_tc = "⚠️天中殺" if f['is_tenchusatsu_year'] else "—"
            year_data.append([
                f"{f['target_year']}年",
                f"{f['now_shi']}年",
                f['keyword'],
                f['description'],
                is_tc
            ])

        year_tbl = Table(year_data, colWidths=[18*mm, 16*mm, 22*mm, 80*mm, 24*mm])
        year_tbl.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4789')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (2, 1), (2, -1), FONT_BOLD),
            ('TEXTCOLOR', (2, 1), (2, -1), colors.HexColor('#C0392B')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(year_tbl)
        story.append(Spacer(1, 4*mm))

        story.append(Paragraph("💡 戦略的ポイント", styles['h3']))
        next_year_str = f"{next_p[0]}年" if next_p else "?"
        strategy_text = (
            f"あなたの次の天中殺は<b>{next_year_str}からの2年間</b>です。<br/>"
            f"<b>それまでに大きな決断・拡大・新規挑戦を完了させる</b>のが運気活用の鉄則。<br/><br/>"
            f"特に<b>12年サイクルの頂点「結実」の年</b>は最大の収穫期です。"
            f"その年までに種を蒔き、準備を整えておくと、人生最大の実りを得られます。"
        )
        story.append(Paragraph(strategy_text, styles['quote']))
        story.append(Spacer(1, 5*mm))

        # 第5章の最後に「1年の行動指針」をサブセクションとして統合
        story.append(Paragraph("🌸 これから1年であなたが取るべき3つのアクション", styles['h2']))
        actions = [
            f"<b>1. 才能を開く</b>：{ws['sun']['name']}の輝きを活かした「{ws['sun']['theme'].split('・')[0]}」の場を1つ作る。",
            f"<b>2. 仲間を結ぶ</b>：{result['shusei']['name']}の力を活かして、信頼できる仲間との対話を月1回以上持つ。",
            f"<b>3. 強みを投下する</b>：{wd['type']}としての「{wd.get('strengths', [''])[0]}」を、新しい挑戦に投下する。",
        ]
        for a in actions:
            story.append(Paragraph(a, styles['body']))
            story.append(Spacer(1, 2*mm))

        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("⚠️ 今年避けるべきこと", styles['h2']))
        avoid = [
            f"<b>1. </b>{mbti.get('weaknesses', [''])[0]}に陥らないよう、自分のパターンを観察する。",
            f"<b>2. </b>{wd.get('weaknesses', [''])[0]}は{wd['type']}の典型的な失敗パターン。仲間と補完する。",
            f"<b>3. </b>天中殺の年（{'・'.join(tc.get('branches', []))}年）に大きな決断はしない。",
        ]
        for a in avoid:
            story.append(Paragraph(a, styles['body']))
            story.append(Spacer(1, 2*mm))

    # ============== 第6章：大切な人との相性 ==============
    story.append(Paragraph("第6章：大切な人との相性", styles['h1']))

    from calculations.narrative_generator import get_chapter6_narrative
    ch6 = get_chapter6_narrative(user_data, result)
    if ch6:
        for key in ['seeking', 'enabler', 'draining', 'quality', 'nurture']:
            story.append(Paragraph(ch6[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch6[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))
    else:
        # フォールバック（旧テンプレ）
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph("💖 恋愛・パートナーシップ相性", styles['h2']))
        love_text = (
            f"<b>{mbti['type']}としての相性：</b><br/>{mbti.get('love_match', '')}<br/><br/>"
            f"<b>{wd['type']}としての相性：</b><br/>{wd.get('love_match', '')}"
        )
        story.append(Paragraph(love_text, styles['quote']))
        story.append(Spacer(1, 4*mm))

        story.append(Paragraph("✨ 相性まとめ", styles['h2']))
        matching_summary = (
            f"あなたは<b>{mbti['type']}×{wd['type']}</b>の組み合わせ。<br/>"
            f"パートナーには、あなたの<b>「{mbti.get('strengths', [''])[0]}」</b>を理解し、"
            f"あなたが苦手な<b>「{mbti.get('weaknesses', [''])[0]}」</b>を補ってくれる人が最適です。<br/><br/>"
            f"恋愛では深い理解と魂レベルのつながりを大切に。"
        )
        story.append(Paragraph(matching_summary, styles['body']))

    # ============== 第7章：数字に宿る、あなたの人生のテーマ ==============
    from calculations.narrative_generator import get_chapter7_narrative
    ch7 = get_chapter7_narrative(user_data, result)
    lp_deep = result.get('numerology', {}).get('life_path_deep', {})

    if ch7:
        # 本文（サラ専用 or 汎用テンプレ）＋ 数秘の具体解説
        story.append(Paragraph("第7章：数字に宿る、あなたの人生のテーマ", styles['h1']))
        for key in ['intro', 'essence', 'shadow', 'triple', 'mature']:
            story.append(Paragraph(ch7[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch7[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))

        # 数秘ライフパスの具体解説（計算結果由来の固有情報）
        if lp_deep:
            story.append(Paragraph(f"📖 ライフパス{n['life_path']['number']}の詳細：{lp_deep.get('title', '')}", styles['h3']))
            story.append(Paragraph(lp_deep.get('essence', ''), styles['quote']))
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph("💎 あなたの才能", styles['h3']))
            story.append(Paragraph(lp_deep.get('talent', ''), styles['body']))
            story.append(Paragraph("🌱 成長の余白（伸びしろ）", styles['h3']))
            story.append(Paragraph(lp_deep.get('growth', ''), styles['body']))
            story.append(Paragraph("🌟 魂の使命", styles['h3']))
            story.append(Paragraph(lp_deep.get('mission', ''), styles['body']))
            story.append(Paragraph("🌸 50代以上のあなたへ", styles['h3']))
            story.append(Paragraph(lp_deep.get('for_50s', ''), styles['quote']))
    elif lp_deep:
        story.append(Paragraph(f"第7章：数秘ライフパス {n['life_path']['number']} — あなたの数の物語", styles['h1']))
        story.append(Paragraph(f"<b>{lp_deep.get('title', '')}</b>", styles['h2']))
        story.append(Paragraph(lp_deep.get('essence', ''), styles['quote']))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph("💎 あなたの才能", styles['h3']))
        story.append(Paragraph(lp_deep.get('talent', ''), styles['body']))

        story.append(Paragraph("🌱 成長の余白（伸びしろ）", styles['h3']))
        story.append(Paragraph(lp_deep.get('growth', ''), styles['body']))

        story.append(Paragraph("🌟 魂の使命", styles['h3']))
        story.append(Paragraph(lp_deep.get('mission', ''), styles['body']))

        story.append(Paragraph("🌸 50代以上のあなたへ", styles['h3']))
        story.append(Paragraph(lp_deep.get('for_50s', ''), styles['quote']))

    # ============== 第8章：名前に宿る、あなたへの祝福 ==============
    from calculations.narrative_generator import get_chapter8_narrative
    ch8 = get_chapter8_narrative(user_data, result)
    seimei = result.get('seimei', {})

    if ch8:
        # 本文（サラ専用 or 汎用テンプレ）
        story.append(Paragraph("第8章：名前に宿る、あなたへの祝福", styles['h1']))
        # gift → five は本文だけ。その後で実際の五格テーブルを挿入。
        for key in ['gift', 'five']:
            story.append(Paragraph(ch8[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch8[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))

        # 五格テーブル＋具体解説（計算結果は必ず表示する）
        if seimei:
            story.append(Paragraph("📜 あなたの五格（計算結果）", styles['h3']))
            gokaku = seimei.get('gokaku', {})
            gokaku_data = [
                ['格', '画数', '数霊の名', '役割'],
                ['天格', str(gokaku.get('tenkaku', 0)), seimei['tenkaku']['name'], '先祖から受け継ぐ運'],
                ['人格 ★', str(gokaku.get('jinkaku', 0)), seimei['jinkaku']['name'], 'あなたの本質（主運）'],
                ['地格', str(gokaku.get('chikaku', 0)), seimei['chikaku']['name'], '青年期までの基礎'],
                ['外格', str(gokaku.get('gaikaku', 0)), seimei['gaikaku']['name'], '社会での印象'],
                ['総格', str(gokaku.get('soukaku', 0)), seimei['soukaku']['name'], '人生全体の大運'],
            ]
            tbl = Table(gokaku_data, colWidths=[18*mm, 16*mm, 50*mm, 56*mm])
            tbl.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR), ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4789')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#FBE9EC')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 4*mm))

        # essence（主運）→ totality（総格）の本文＋具体解説
        story.append(Paragraph(ch8['essence_h2'], styles['h2']))
        story.append(Paragraph(ch8['essence_body'], styles['body']))
        if seimei:
            story.append(Paragraph(f"⭐ あなたの主運：{seimei['jinkaku']['name']}（{seimei['jinkaku']['number']}画）", styles['h3']))
            story.append(Paragraph(seimei['jinkaku']['description'], styles['body']))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph(ch8['totality_h2'], styles['h2']))
        story.append(Paragraph(ch8['totality_body'], styles['body']))
        if seimei:
            story.append(Paragraph(f"🌸 人生全体の大運：{seimei['soukaku']['name']}（{seimei['soukaku']['number']}画）", styles['h3']))
            story.append(Paragraph(seimei['soukaku']['description'], styles['body']))
            sansai = seimei.get('sansai', {})
            story.append(Paragraph(f"🌳 三才配置：{sansai.get('combo', '')}", styles['h3']))
            story.append(Paragraph(sansai.get('meaning', ''), styles['body']))
        story.append(Spacer(1, 3*mm))

        # calling（締めくくり）
        story.append(Paragraph(ch8['calling_h2'], styles['h2']))
        story.append(Paragraph(ch8['calling_body'], styles['body']))
    elif seimei:
        story.append(Paragraph("第8章：姓名判断 — 名前という、最初の贈り物", styles['h1']))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph(
            seimei.get('intro', '').replace('\n', '<br/>'),
            styles['quote']
        ))
        story.append(Spacer(1, 4*mm))

        # 五格テーブル
        story.append(Paragraph("📜 あなたの五格", styles['h2']))
        gokaku = seimei.get('gokaku', {})
        gokaku_data = [
            ['格', '画数', '数霊の名', '役割'],
            ['天格', str(gokaku.get('tenkaku', 0)), seimei['tenkaku']['name'], '先祖から受け継ぐ運'],
            ['人格 ★', str(gokaku.get('jinkaku', 0)), seimei['jinkaku']['name'], 'あなたの本質（主運）'],
            ['地格', str(gokaku.get('chikaku', 0)), seimei['chikaku']['name'], '青年期までの基礎'],
            ['外格', str(gokaku.get('gaikaku', 0)), seimei['gaikaku']['name'], '社会での印象'],
            ['総格', str(gokaku.get('soukaku', 0)), seimei['soukaku']['name'], '人生全体の大運'],
        ]
        tbl = Table(gokaku_data, colWidths=[18*mm, 16*mm, 50*mm, 56*mm])
        tbl.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4789')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#FBE9EC')),  # 人格行をハイライト
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 4*mm))

        # 主運（人格）の詳細解説
        story.append(Paragraph(f"⭐ あなたの主運：{seimei['jinkaku']['name']}", styles['h3']))
        story.append(Paragraph(seimei['jinkaku']['description'], styles['body']))
        story.append(Spacer(1, 3*mm))

        # 総格（人生全体）
        story.append(Paragraph(f"🌸 人生全体の大運：{seimei['soukaku']['name']}", styles['h3']))
        story.append(Paragraph(seimei['soukaku']['description'], styles['body']))
        story.append(Spacer(1, 3*mm))

        # 三才配置
        sansai = seimei.get('sansai', {})
        story.append(Paragraph(f"🌳 三才配置：{sansai.get('combo', '')}", styles['h3']))
        story.append(Paragraph(sansai.get('meaning', ''), styles['body']))

    # ============== 第9章：あなたの言葉が映す本質 ==============
    from calculations.narrative_generator import get_chapter9_narrative
    ch9 = get_chapter9_narrative(user_data, result)
    narrative = result.get('narrative', {})
    n1 = (narrative.get('N1') or '').strip()
    n2 = (narrative.get('N2') or '').strip()

    if ch9:
        # サラ専用：深掘り版本文
        story.append(Paragraph("第9章：あなたの言葉が映す本質", styles['h1']))
        for key in ['opening', 'talent', 'value', 'future', 'integration']:
            story.append(Paragraph(ch9[f'{key}_h2'], styles['h2']))
            story.append(Paragraph(ch9[f'{key}_body'], styles['body']))
            story.append(Spacer(1, 3*mm))
    elif n1 or n2:
        # フォールバック（旧テンプレ）：簡易版引用＋コメント
        kaika_main = result.get('personality', {}).get('jinsei_kaika', {})
        story.append(Paragraph("✍️ 第9章：あなたの言葉が映す本質", styles['h1']))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(
            "あなたが書いてくれた言葉から、内側の輝きを読み解きます。<br/>"
            "占術データと心理タイプが「設計図」なら、ここに書かれた言葉は「あなたの魂の声」です。",
            styles['quote']
        ))
        story.append(Spacer(1, 4*mm))

        if n1:
            story.append(Paragraph("📝 あなたの夢中体験", styles['h2']))
            story.append(Paragraph(
                f"<i>「{n1}」</i>",
                styles['body']
            ))
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph(
                f"<b>ここに見える「{kaika_main.get('name', 'あなた')}」の才能</b><br/>"
                f"この体験の中で、あなたは時間を忘れて没頭しています。<br/>"
                f"これこそ、あなたが本当の自分でいる瞬間。<br/>"
                f"この時間が増えれば増えるほど、人生の輝きが増します。",
                styles['tip']
            ))
            story.append(Spacer(1, 5*mm))

        if n2:
            story.append(Paragraph("📝 あなたの譲れない信念", styles['h2']))
            story.append(Paragraph(
                f"<i>「{n2}」</i>",
                styles['body']
            ))
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph(
                f"<b>ここに見える「価値観のコンパス」</b><br/>"
                f"この信念は、あなたの人生の北極星です。<br/>"
                f"迷った時、選択に悩んだ時、この言葉に立ち返ると、必ず本当の道が見えます。<br/>"
                f"「{kaika_main.get('name', 'あなた')}」のタイプと組み合わせることで、揺るぎない人生軸ができます。",
                styles['tip']
            ))

        story.append(PageBreak())

    # ============== Page 10: サラからの手紙 ==============
    story.append(Spacer(1, 12*mm))
    story.append(Paragraph("あなたへ — サラからの手紙", styles['title']))
    story.append(Spacer(1, 8*mm))

    letter_paragraphs = [
        "このレポートを読み終えたあなたに、伝えたいことがあります。",
        "",
        "50代を超えた女性は、「もう遅い」と思いがちです。<br/>"
        "でも、それは社会が植え付けた幻想です。",
        "",
        "あなたの星。<br/>"
        "あなたの命。<br/>"
        "あなたの名前。<br/>"
        "すべてが、「<b>これからが本番</b>」と語っています。",
        "",
        "老いることは、衰えることではありません。<br/>"
        "<b>深まること。磨かれること。本物になっていくこと</b>。",
        "",
        "これからのあなたは、20代の自分には決して手に入らなかった<br/>"
        "・<b>ゆるぎない美しさ</b><br/>"
        "・<b>本物の自由</b><br/>"
        "・<b>深い愛</b><br/>"
        "を、一年ごとに重ねていく女性です。",
        "",
        "恐れないでください。<br/>"
        "<b>あなたの最も美しい時間は、これから始まります。</b>",
        "",
        "<br/>でもね。<br/>"
        "<b>人生は、自分を知っただけでは変わりません。</b>",
        "",
        "私もたくさん学びました。<br/>"
        "本も読みました。セミナーにも行きました。<br/>"
        "でも本当に人生が変わり始めたのは、<br/>"
        "<b>「毎日の小さな習慣」が変わった時</b>でした。",
        "",
        "だから私は、私自身が14年間続けてきた<br/>"
        "<b>食・感謝・心・体の整え方</b>を、<br/>"
        "<b>「人生を生き直す28日間」</b>にまとめました。",
        "",
        "もしあなたが、この診断結果を読んで<br/>"
        "「もっと自分らしく生きたい」<br/>"
        "「人生をもう一度輝かせたい」<br/>"
        "そう感じたなら、次の一歩を踏み出してみてください。",
    ]
    for p in letter_paragraphs:
        if p:
            story.append(Paragraph(p, styles['body']))
        else:
            story.append(Spacer(1, 3*mm))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "<b>『人生は、何度でも再起動できる』</b><br/><br/>"
        "その言葉を、今度は知識ではなく、<br/>"
        "あなた自身の人生で体験してほしいのです。",
        styles['quote']
    ))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "サラ 🌹",
        styles['small']
    ))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        f"人生開花タイプ診断 v4.0 / 監修：山岡サラ（サラグラシアアカデミー）<br/>"
        f"発行日：{datetime.now().strftime('%Y年%m月%d日')}",
        styles['small']
    ))

    doc.build(story)
    print(f"PDF saved: {output_path}")
