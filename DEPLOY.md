# DNA診断 Webアプリ デプロイガイド

## ローカル実行

```bash
cd D:/CCBooster/dna-shindan-v2
pip install -r requirements.txt
python -m streamlit run app.py
```

→ ブラウザで http://localhost:8501 が開く

---

## Streamlit Community Cloud にデプロイ（無料・推奨）

### 1. GitHubリポジトリ作成

```bash
cd D:/CCBooster/dna-shindan-v2
git init
git add .
git commit -m "DNA診断アプリ v3.1 初版"
gh repo create dna-shindan-sara --public --source=. --push
```

### 2. Streamlit Cloud に接続

1. https://share.streamlit.io/ にアクセス
2. GitHubでサインイン
3. 「New app」→ 上記リポジトリを選択
4. Main file path: `app.py`
5. 「Deploy」をクリック

→ 数分で公開URLが発行されます（例：`https://dna-shindan-sara.streamlit.app`）

### 3. 独自ドメインを設定（任意）

Streamlit Cloud Settings → Custom domain で `dna.sara-grasia.com` 等を設定可能。

---

## サラさんのLINE登録特典として配布する流れ

1. **LINE登録時の自動メッセージ**に診断URLを記載
   ```
   📜 サラからのプレゼント

   あなたの「人生再起動のためのDNA設計図」を、
   無料で受け取れます。

   👉 https://dna.sara-grasia.com
   
   3分の質問に答えるだけで、
   8ページの個人レポートをダウンロードできます。
   ```

2. **診断ページ末尾にサラの輪への誘導**を追加
   - 「より深く知りたい方は、サラの輪へ」リンクを設置

---

## 注意事項

- **無料プランの制限**：Streamlit Cloud無料版は月間アクセス数制限あり（1,000ユーザー/月程度で十分）
- **アクセス過多時**：有料プラン or 自前サーバー（Render.com等）への移行
- **個人情報**：診断データはサーバーに保存しない設計（一時的処理のみ）。GDPR・個人情報保護法に準拠。

---

## トラブルシューティング

### lunar-pythonが動かない
- `pip install lunar-python --upgrade` で最新版に

### skyfieldの天体データ（de421.bsp）がダウンロードできない
- 初回起動時にネット接続必須
- データはホスティング側のディスクにキャッシュされる

### 日本語フォントが見つからない
- Streamlit Cloudは Linux サーバー → Linux用日本語フォント（IPAex等）に変更必要
- `pdf_generator.py` の FONT_REGULAR 設定を環境別に分岐
