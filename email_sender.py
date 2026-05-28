"""
メール送信機能
SMTPでPDF添付メールを送る（さくらサーバー対応）
環境変数：
  SMTP_HOST     例: salagracia.sakura.ne.jp
  SMTP_PORT     587 (STARTTLS) or 465 (SSL)
  SMTP_USER     monthly@salagracia.com
  SMTP_PASSWORD （Render環境変数で設定）
  FROM_EMAIL    monthly@salagracia.com
  FROM_NAME     サラ・グラシアアカデミー
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.header import Header


def send_pdf_email(to_email: str, user_name: str, pdf_path: str) -> dict:
    """PDF添付メールを送信
    return: {"success": bool, "message": str}
    """
    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('FROM_EMAIL', 'monthly@salagracia.com')
    from_name = os.environ.get('FROM_NAME', 'サラ・グラシアアカデミー')
    use_ssl = os.environ.get('SMTP_USE_SSL', 'false').lower() == 'true'

    if not all([smtp_host, smtp_user, smtp_password]):
        return {
            "success": False,
            "message": "メール送信の設定が不完全です。管理者にお問い合わせください。"
        }

    # メールメッセージ構築
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(from_name, 'utf-8')), from_email))
    msg['To'] = to_email
    msg['Subject'] = str(Header("【DNA診断】あなたのレポートが完成しました 🌹", 'utf-8'))

    body = f"""{user_name} さん

この度はDNA診断を受けてくださり、本当にありがとうございます。

あなたの「人生再起動のための個人設計図」が完成しました。

📎 添付ファイルからPDFをご確認ください。

────────────────

このレポートには：
・東洋・西洋の占術9種類の結果（数秘・西洋占星術・九星気学・四柱推命・動物キャラ等）
・あなたの16パーソナリティ詳細（強み・弱点・キャリア・チャレンジ）
・ウェルスダイナミクスの詳細（運気戦略）
・才能・落とし穴・使命の方向
・恋愛・ビジネスパートナーの相性
・天中殺と3年間の運勢サイクル

…が、8ページにわたって描かれています。

────────────────

『人生は、何度でも再起動できる』

あなたの再起動の旅を、応援しています🌹

山岡サラ
サラ・グラシアアカデミー
https://salagracia.com

────────────────

※ このメールは自動送信です。
※ DNA診断アプリ：https://dna-shindan-sara.onrender.com
"""
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # PDF添付
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        attach = MIMEApplication(pdf_data, _subtype='pdf')
        # 日本語ファイル名対応
        attach_filename = f"DNA診断_{user_name}.pdf"
        attach.add_header(
            'Content-Disposition',
            'attachment',
            filename=('utf-8', '', attach_filename)
        )
        msg.attach(attach)
    except Exception as e:
        return {"success": False, "message": f"PDF添付エラー: {e}"}

    # SMTP送信
    try:
        if use_ssl:
            # SSL/TLS (port 465)
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            # STARTTLS (port 587)
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

        return {"success": True, "message": f"{to_email} にメールを送信しました"}
    except smtplib.SMTPAuthenticationError as e:
        return {"success": False, "message": f"認証エラー: SMTP認証情報を確認してください ({e})"}
    except smtplib.SMTPException as e:
        return {"success": False, "message": f"SMTP送信エラー: {e}"}
    except Exception as e:
        return {"success": False, "message": f"メール送信失敗: {e}"}


if __name__ == "__main__":
    # ローカルテスト用（環境変数を設定して実行）
    import sys
    if len(sys.argv) < 3:
        print("使い方: python email_sender.py <to_email> <pdf_path>")
        sys.exit(1)

    result = send_pdf_email(sys.argv[1], "テストユーザー", sys.argv[2])
    print(result)
