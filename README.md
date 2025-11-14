# やる・やったBot

Discord で「やるぞ宣言」と「やったよ報告」ができる Bot です。

## 🎯 機能

### `/yaru` - やるぞ宣言
- やることを宣言できます
- 締切を設定できます（任意）
- 固定チャンネルに投稿されます

### `/yatta` - やったよ報告
- やったことを報告できます
- ひとこと感想を添えられます（任意）
- 固定チャンネルに投稿されます

## 📋 前提条件

- Python 3.10 以上
- Discord Bot のトークン
- Bot が参加している Discord サーバー

## 🚀 セットアップ手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/yaru_yatta_bot.git
cd yaru_yatta_bot
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

`.env` ファイルを作成し、Bot トークンを設定します：

```env
BOT_TOKEN=あなたのBotトークンをここに貼り付け
```

**Bot トークンの取得方法**:
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリック
3. アプリ名を入力（例: やる・やったBot）
4. 「Bot」タブに移動
5. 「Add Bot」をクリック
6. Bot トークンをコピーして `.env` に保存

### 4. Bot を起動

```bash
python main.py
```

起動に成功すると、以下のようなメッセージが表示されます：

```
Keep-alive サーバーを起動しました (ポート: 8080)
Bot を起動中...
=====================================
Bot が起動しました: やる・やったBot
Bot ID: 1234567890123456789
=====================================
スラッシュコマンドを 2 件同期しました
同期されたコマンド:
  - /yaru
  - /yatta
```

## 🔐 Discord Bot の設定

### 必要な権限

Bot に以下の権限を付与してください：

- `Send Messages` - メッセージ送信
- `Use Slash Commands` - スラッシュコマンド使用

### Bot の招待

1. Discord Developer Portal で OAuth2 URL Generator を開く
2. **Scopes** で以下を選択：
   - `bot`
   - `applications.commands`
3. **Bot Permissions** で以下を選択：
   - `Send Messages`
4. 生成された URL で Bot をサーバーに招待

## 📝 使い方

### やるぞ宣言

1. Discord で `/yaru` と入力
2. モーダル（入力フォーム）が表示される
3. 「やること」を入力（必須）
4. 「締切」を入力（任意）
5. 送信ボタンをクリック

投稿例：
```
@ユーザー さんが「やるぞ宣言」をしました！
■ やること: Pythonの勉強を1時間やる
■締切: 明日の18時まで
```

### やったよ報告

1. Discord で `/yatta` と入力
2. モーダルが表示される
3. 「やったこと」を入力（必須）
4. 「ひとこと感想」を入力（任意）
5. 送信ボタンをクリック

投稿例：
```
@ユーザー さんが「やったよ報告」をしました！
■ やったこと: Pythonの勉強を1時間やりました
■ ひとこと感想: 思ったより難しかったけど楽しかった！
```

## 🌐 Replit でのデプロイ

### 1. Replit プロジェクトを作成

1. [Replit](https://replit.com/) にアクセス
2. 「Create Repl」をクリック
3. テンプレートで「Python」を選択
4. プロジェクト名を入力（例: yaru-yatta-bot）

### 2. ファイルをアップロード

以下のファイルを Replit にアップロード：
- `main.py`
- `keep_alive.py`
- `requirements.txt`

### 3. 環境変数を設定

Replit の Secrets タブで以下を設定：
- Key: `BOT_TOKEN`
- Value: あなたの Bot トークン

### 4. 実行

Replit の「Run」ボタンをクリックして Bot を起動。

### 5. 常時稼働（任意）

[UptimeRobot](https://uptimerobot.com/) で定期的に `https://your-repl.replit.app/` にアクセスするように設定すると、Bot が常時稼働します。

## 📂 ファイル構成

```
yaru_yatta_bot/
├── main.py              # Bot 本体
├── keep_alive.py        # Replit 用 Web サーバー
├── requirements.txt     # 依存パッケージ
├── .env                 # 環境変数（Git 除外）
├── .gitignore           # Git 除外設定
├── plan.md              # 実装計画書
└── README.md            # このファイル
```

## 🛠️ 開発

### ローカルでのテスト

```bash
# 仮想環境を作成（任意）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt

# Bot を起動
python main.py
```

### コードの説明

- `main.py`: Bot のメインロジック
  - スラッシュコマンド `/yaru` と `/yatta` の定義
  - モーダル（入力フォーム）の実装
  - 固定チャンネルへの投稿処理
  
- `keep_alive.py`: Replit 用の Web サーバー
  - Flask で簡易的な HTTP サーバーを起動
  - UptimeRobot などで定期的にアクセスさせることで Bot を稼働させ続ける

## ⚠️ 注意事項

### スラッシュコマンドの同期

- 初回起動時、スラッシュコマンドが Discord サーバーに反映されるまで数分〜数時間かかる場合があります
- コマンドが表示されない場合は、Discord を再起動してください

### チャンネル ID の確認

投稿先チャンネル ID は `main.py` の `TARGET_CHANNEL_ID` で設定されています：

```python
TARGET_CHANNEL_ID = 1435802151648497711
```

チャンネル ID を変更する場合：
1. Discord で開発者モードを有効化
2. チャンネルを右クリック → 「ID をコピー」
3. `main.py` の `TARGET_CHANNEL_ID` を更新

### Bot トークンの管理

- `.env` ファイルは Git にコミットしないでください（`.gitignore` で除外済み）
- トークンが漏洩した場合は、Discord Developer Portal で再生成してください

## 📚 参考リンク

- [discord.py ドキュメント](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Replit ドキュメント](https://docs.replit.com/)
- [UptimeRobot](https://uptimerobot.com/)

## 🤝 コントリビューション

プルリクエストや Issue を歓迎します！

## 📄 ライセンス

MIT License

---

**作成日**: 2025年11月14日

