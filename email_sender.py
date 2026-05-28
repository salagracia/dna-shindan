"""
メール送信機能（Resend API版・HTTPS経由なのでRender制限を回避）
環境変数：
  RESEND_API_KEY    Resend ダッシュボードで発行したAPIキー
  FROM_EMAIL        送信元（独自ドメイン認証前は onboarding@resend.dev）
  FROM_NAME         サラグラシアアカデミー
"""
import os
import base64


def send_pdf_email(to_email: str, user_name: str, pdf_path: str) -> dict:
    """PDF添付メールを Resend API 経由で送信"""
    api_key = os.environ.get('RESEND_API_KEY', '')
    from_email = os.environ.get('FROM_EMAIL', 'onboarding@resend.dev')
    from_name = os.environ.get('FROM_NAME', 'サラグラシアアカデミー')

    if not api_key:
        return {
            "success": False,
            "message": "メール送信の設定が不完全です（API Key未登録）"
        }

    try:
        import resend
    except ImportError:
        return {
            "success": False,
            "message": "Resendパッケージが見つかりません"
        }

    resend.api_key = api_key

    # PDF をbase64エンコード
    try:
        with open(pdf_path, 'rb') as f:
            pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        return {"success": False, "message": f"PDF読み込みエラー: {e}"}

    # メール本文
    html_body = f"""
<div style="font-family: 'Hiragino Sans', 'Yu Gothic', sans-serif; max-width: 600px; margin: auto;">
  <h2 style="color: #8B4789;">🌹 DNA診断レポートが完成しました</h2>
  <p>{user_name} さん</p>
  <p>この度はDNA診断を受けてくださり、本当にありがとうございます。</p>
  <p>あなたの「<strong>人生再起動のための個人設計図</strong>」が完成しました。</p>
  <p>📎 添付ファイルからPDFをご確認ください。</p>

  <hr style="border: 1px solid #F4ECF7;">

  <p><strong>このレポートには：</strong></p>
  <ul>
    <li>東洋・西洋の占術9種類の結果</li>
    <li>16パーソナリティ詳細（強み・弱点・キャリア・チャレンジ）</li>
    <li>ウェルスダイナミクスの詳細（運気戦略）</li>
    <li>才能・落とし穴・使命の方向</li>
    <li>恋愛・ビジネスパートナーの相性</li>
    <li>天中殺と3年間の運勢サイクル</li>
  </ul>
  <p>…が、8ページにわたって描かれています。</p>

  <hr style="border: 1px solid #F4ECF7;">

  <p style="color: #8B4789; font-weight: bold; font-size: 1.1em;">
    『人生は、何度でも再起動できる』
  </p>
  <p>あなたの再起動の旅を、応援しています🌹</p>

  <p>
    山岡サラ<br>
    サラグラシアアカデミー<br>
    <a href="https://salagracia.com" style="color: #8B4789;">https://salagracia.com</a>
  </p>

  <hr style="border: 1px solid #ccc;">
  <p style="color: #888; font-size: 0.85em;">
    ※ このメールは自動送信です<br>
    ※ DNA診断アプリ：<a href="https://dna-shindan-sara.onrender.com">https://dna-shindan-sara.onrender.com</a>
  </p>
</div>
"""

    text_body = f"""{user_name} さん

この度はDNA診断を受けてくださり、本当にありがとうございます。

あなたの「人生再起動のための個人設計図」が完成しました。
📎 添付ファイルからPDFをご確認ください。

────────────────

このレポートには：
・東洋・西洋の占術9種類の結果
・あなたの16パーソナリティ詳細
・ウェルスダイナミクスの詳細
・才能・落とし穴・使命の方向
・恋愛・ビジネスパートナーの相性
・天中殺と3年間の運勢サイクル

…が、8ページにわたって描かれています。

────────────────

『人生は、何度でも再起動できる』

あなたの再起動の旅を、応援しています🌹

山岡サラ
サラグラシアアカデミー
https://salagracia.com
"""

    try:
        params = {
            "from": f"{from_name} <{from_email}>",
            "to": [to_email],
            "subject": "【人生開花タイプ診断】あなたのレポートが完成しました 🌹",
            "html": html_body,
            "text": text_body,
            "attachments": [
                {
                    "filename": f"DNA診断_{user_name}.pdf",
                    "content": pdf_b64,
                }
            ]
        }
        result = resend.Emails.send(params)
        return {
            "success": True,
            "message": f"{to_email} にメールを送信しました",
            "id": result.get('id', '')
        }
    except Exception as e:
        return {"success": False, "message": f"メール送信失敗: {e}"}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("使い方: python email_sender.py <to_email> <pdf_path>")
        sys.exit(1)
    result = send_pdf_email(sys.argv[1], "テストユーザー", sys.argv[2])
    print(result)
