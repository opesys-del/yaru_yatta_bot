# やる・やったBot

Discord で「やるぞ宣言」と「やったよ報告」ができる学習サポート Bot です。
ボタンを押すだけでモーダルが開き、入力内容は Discord の固定チャンネルと
Google スプレッドシート（BigQuery 連携前段）に自動保存されます。

## 🎯 主な特徴

- ボタン操作（/コマンド不要）でモーダルが開く
- `/yaru` / `/yatta` でも従来通り操作可能
- 入力内容を固定チャンネルへ投稿
- 同時に Google スプレッドシート `yaru_yatta_log` へ保存
- Replit 稼働を想定した keep-alive サーバー付き

## 🧱 データ連携

保存先スプレッドシート: [SOZOW 1on1 管理シート](https://docs.google.com/spreadsheets/d/157xGD-aGLFL4Iyteyg5i81NJa7hontZyj7fc_wmVJ0M/edit#gid=555110385)

1. スプレッドシートに `yaru_yatta_log` シートを作成し、以下の列を用意してください。
   | A:記録日時(JST) | B:種類 | C:Discord ID | D:Discord名 | E:メイン内容 | F:補足 |
2. Google Cloud Console でサービスアカウントを作成し、JSON キーをダウンロード
3. 対象シートをサービスアカウントのメールアドレスに「閲覧＋編集」権限で共有

## 📁 ファイル構成

```
yaru_yatta_bot/
├── main.py              # Bot 本体（ボタン・モーダル・Sheets 連携）
├── keep_alive.py        # Replit 用 Web サーバー
├── requirements.txt     # 依存パッケージ
├── .env.example         # 環境変数テンプレート
├── .gitignore
├── plan.md              # 実装計画メモ
└── README.md            # このファイル
```

## 🔧 必要な環境変数（.env）

`.env.example` をコピーし、実際の値を設定してください。

```env
BOT_TOKEN=あなたのBotトークン
TARGET_CHANNEL_ID=1435802151648497711
GOOGLE_SERVICE_ACCOUNT_JSON=/absolute/path/to/service-account.json
SPREADSHEET_ID=157xGD-aGLFL4Iyteyg5i81NJa7hontZyj7fc_wmVJ0M
SHEET_NAME=yaru_yatta_log
```

- **BOT_TOKEN**: Discord Developer Portal > Bot > Reset Token
- **TARGET_CHANNEL_ID**: 投稿先チャンネルの ID（Discord > 設定 > 開発者モード ON）
- **GOOGLE_SERVICE_ACCOUNT_JSON**: サービスアカウント JSON への絶対パス
- **SPREADSHEET_ID**: シート URL の `/d/` と `/edit` の間
- **SHEET_NAME**: 追記したいシート名（存在しない場合は作成してください）

## 🛠 セットアップ手順

```bash
git clone https://github.com/opesys-del/yaru_yatta_bot.git
cd yaru_yatta_bot
pip install -r requirements.txt
cp .env.example .env
# .env を編集して各値を設定
python main.py
```

起動成功時ログ例：
```
Keep-alive サーバーを起動しました (ポート: 8080)
Bot を起動中...
=====================================
Bot が起動しました: やる・やったBot
Bot ID: 1234567890123456789
=====================================
スラッシュコマンドを 3 件同期しました
```

## 💡 Discord 側の使い方

### 1. ボタンを設置

管理者（メッセージ管理権限あり）が、ボタンを置きたいチャンネルで以下を実行：

```
/post_buttons
```

Bot が以下のようなメッセージを投稿するので、ピン留め推奨です。

```
[やるぞ宣言] [やったよ報告]
```

### 2. 子どもたちの操作

- ボタンを押すだけでモーダルが開きます
- 入力 → 送信すると固定チャンネルに投稿され、同時にスプレッドシートへ保存されます
- バックアップとして `/yaru` `/yatta` コマンドも利用可能です

### 投稿例

```
@ユーザー さんが「やるぞ宣言」をしました！
■ やること: 国語プリントを1枚やる
■ 締切: 今日の19時まで
```

```
@ユーザー さんが「やったよ報告」をしました！
■ やったこと: 国語プリントを1枚やりました
■ ひとこと感想: 意外と簡単だった！
```

## 🌐 Replit での常時稼働

1. Replit で新規 Python repl を作成
2. このリポジトリのファイルをアップロード
3. Secrets に `.env` の値を登録（特に BOT_TOKEN, TARGET_CHANNEL_ID, ...）
4. `python main.py` を Run コマンドに設定
5. [UptimeRobot](https://uptimerobot.com/) などで `https://your-repl-name.replit.app/` を定期的に ping

## 🧪 データ連携の動作確認

1. `.env` を設定し `python main.py` を起動
2. `/post_buttons` を実行してボタンを設置
3. ボタンから「やるぞ宣言」「やったよ報告」を送信
4. Discord 固定チャンネルに投稿されることを確認
5. Google スプレッドシート `yaru_yatta_log` に1行追加されることを確認

トラブルシューティング：
- スプレッドシート連携に失敗した場合、Bot は Discord 投稿後に警告メッセージを返信します
- サービスアカウントの権限が足りない/シート名のミスが原因のことが多いです

## ⚠️ 注意事項

- スラッシュコマンドが反映されるまで数分かかる場合があります。表示されない場合は Discord を再起動
- `.env` と サービスアカウント JSON は Git にコミットしないでください
- Google 側の API 呼び出しに失敗すると、Discord 投稿は成功してもシート保存が落ちる場合があります

## 📚 参考リンク

- [discord.py ドキュメント](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Google Cloud サービスアカウント](https://cloud.google.com/iam/docs/service-accounts)
- [gspread ドキュメント](https://docs.gspread.org/en/latest/)

## 🤝 コントリビューション

Issue / Pull Request を歓迎します！

## 📄 ライセンス

MIT License
