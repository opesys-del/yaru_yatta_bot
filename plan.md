# Discord Bot 開発計画書（Python / discord.py / Replit）

作成日: 2025年11月14日

---

## 📋 プロジェクト概要

### 目的
- Discord Bot を Python（discord.py）で作成し、Replit で常時稼働させる
- スラッシュコマンド `/yaru` と `/yatta` を実装
- モーダル（ポップアップ入力）で情報を収集し、固定チャンネルに投稿

### 対象ユーザー
- Python 初心者でも読めるコード
- 明確なコメント付き
- シンプルで保守しやすい構成

---

## 🎯 機能要件

### 1. スラッシュコマンド `/yaru`（やるぞ宣言）

**モーダル表示内容**:
- タイトル: 「やるぞ宣言」
- 入力項目:
  - 「やること」（必須、1行テキスト）
  - 「締切（任意）」（任意、1行テキスト）

**投稿フォーマット**:
```
@ユーザー さんが「やるぞ宣言」をしました！
■ やること: {入力値}
■ 締切: {入力値}
```

### 2. スラッシュコマンド `/yatta`（やったよ報告）

**モーダル表示内容**:
- タイトル: 「やったよ報告」
- 入力項目:
  - 「やったこと」（必須、複数行テキスト）
  - 「ひとこと感想（任意）」（任意、複数行テキスト）

**投稿フォーマット**:
```
@ユーザー さんが「やったよ報告」をしました！
■ やったこと: {入力値}
■ ひとこと感想: {入力値}
```

### 3. 共通仕様

- **投稿先**: 固定チャンネル ID `1435802151648497711`
- **モーダル実装**: `discord.ui.Modal` を使用
- **スラッシュコマンド**: `discord.app_commands.command` を使用
- **Intents**: 最小構成（`message_content` なし）
- **エラー処理**: try-except で捕捉し、ログ出力
- **再接続処理**: discord.py のデフォルト機能を利用

---

## 📁 ファイル構成

```
discord_bot_yaru_yatta/
├── plan.md                 # このファイル（実装計画書）
├── main.py                 # Bot 本体
├── keep_alive.py           # Replit 用の簡易 Web サーバー（Flask）
├── requirements.txt        # 依存パッケージ
├── .env                    # Bot トークン（Git 除外）
├── .gitignore              # Git 除外設定
└── README.md               # セットアップ手順
```

---

## 🔧 技術スタック

### 使用ライブラリ
- **discord.py**: v2.3 以降（Discord API クライアント）
- **Flask**: Web サーバー（Replit の keep-alive 用）
- **python-dotenv**: 環境変数読み込み

### Python バージョン
- Python 3.10 以上推奨

---

## 📝 実装詳細

### 1. main.py（Bot 本体）

**構成要素**:

#### 1-1. インポートとセットアップ
```python
import discord
from discord import app_commands
from discord.ui import Modal, TextInput
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
```

#### 1-2. Bot 設定
```python
# 最小限の Intents
intents = discord.Intents.default()
# message_content は不要（スラッシュコマンドのみ）

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
```

#### 1-3. 固定チャンネル ID
```python
TARGET_CHANNEL_ID = 1435802151648497711
```

#### 1-4. モーダルクラス定義

**YaruModal（やるぞ宣言用）**:
- `やること` フィールド（必須、短文）
- `締切` フィールド（任意、短文）
- `on_submit` メソッドで投稿処理

**YattaModal（やったよ報告用）**:
- `やったこと` フィールド（必須、長文）
- `ひとこと感想` フィールド（任意、長文）
- `on_submit` メソッドで投稿処理

#### 1-5. スラッシュコマンド定義

**`/yaru` コマンド**:
- YaruModal を表示
- interaction.response.send_modal() で送信

**`/yatta` コマンド**:
- YattaModal を表示
- interaction.response.send_modal() で送信

#### 1-6. イベントハンドラ

**`on_ready`**:
- Bot 起動時にログ出力
- スラッシュコマンドを同期

**`on_error`**:
- エラー時のログ出力

#### 1-7. Bot 起動
```python
if __name__ == "__main__":
    keep_alive()  # Replit 用 Web サーバー起動
    client.run(os.getenv('BOT_TOKEN'))
```

---

### 2. keep_alive.py（Web サーバー）

**目的**: Replit の無料プランでは一定時間操作がないとスリープする。
UptimeRobot などで定期的にアクセスさせることで稼働を維持。

**実装**:
```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

---

### 3. requirements.txt

```
discord.py>=2.3.0
flask>=3.0.0
python-dotenv>=1.0.0
```

---

### 4. .env（環境変数）

```
BOT_TOKEN=あなたのBotトークンをここに貼り付け
```

**注意**:
- Git にコミットしない（.gitignore に追加）
- Discord Developer Portal から取得したトークンを設定

---

### 5. .gitignore

```
.env
__pycache__/
*.pyc
.replit
replit.nix
```

---

## 🚀 実装手順

### フェーズ 1: ローカル開発（デバッグ用）

1. ✅ ディレクトリ作成
2. ✅ `plan.md` 作成（このファイル）
3. ⏳ `main.py` 実装
4. ⏳ `keep_alive.py` 実装
5. ⏳ `requirements.txt` 作成
6. ⏳ `.env.example` 作成
7. ⏳ `.gitignore` 作成
8. ⏳ `README.md` 作成
9. ⏳ ローカルでテスト実行

### フェーズ 2: Replit デプロイ

1. Replit でプロジェクト作成
2. ファイルをアップロード
3. `.env` に BOT_TOKEN を設定
4. `python main.py` で実行
5. UptimeRobot で ping 設定（任意）

---

## 🔐 Discord Developer Portal 設定

### 必要な設定

#### 1. Bot の作成
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリック
3. アプリ名を入力（例: やる・やったBot）
4. 「Bot」タブに移動
5. 「Add Bot」をクリック
6. Bot トークンをコピーして `.env` に保存

#### 2. Bot の権限設定
- **Privileged Gateway Intents**: 不要（デフォルトのまま）
- **Bot Permissions**:
  - `Send Messages` - メッセージ送信
  - `Use Slash Commands` - スラッシュコマンド使用

#### 3. OAuth2 URL Generator
- **Scopes**:
  - `bot`
  - `applications.commands`
- **Bot Permissions**:
  - `Send Messages`
- 生成された URL で Bot をサーバーに招待

---

## 📊 データフロー

### `/yaru` コマンドの処理フロー

```
ユーザー
  ↓
/yaru コマンド実行
  ↓
Bot: YaruModal を表示
  ↓
ユーザー: フォームに入力して送信
  ↓
Bot: on_submit() が呼ばれる
  ↓
Bot: 固定チャンネル (1435802151648497711) に投稿
  ↓
ユーザー: モーダルに「投稿しました！」と表示
```

### `/yatta` コマンドの処理フロー

```
ユーザー
  ↓
/yatta コマンド実行
  ↓
Bot: YattaModal を表示
  ↓
ユーザー: フォームに入力して送信
  ↓
Bot: on_submit() が呼ばれる
  ↓
Bot: 固定チャンネル (1435802151648497711) に投稿
  ↓
ユーザー: モーダルに「投稿しました！」と表示
```

---

## ⚠️ 注意事項

### 1. スラッシュコマンドの同期
- 初回起動時、スラッシュコマンドが Discord サーバーに反映されるまで数分〜数時間かかる場合があります
- `tree.sync()` を実行することで手動同期できます

### 2. Replit の制限
- 無料プランでは一定時間操作がないとスリープします
- UptimeRobot で定期的に ping することで稼働を維持できます

### 3. Bot トークンの管理
- `.env` ファイルは Git にコミットしないでください
- トークンが漏洩した場合は、Discord Developer Portal で再生成してください

### 4. チャンネル ID の確認
- Discord で開発者モードを有効化
- チャンネルを右クリック → 「ID をコピー」

---

## 🧪 テスト計画

### ローカルテスト

1. `/yaru` コマンドが表示されるか確認
2. モーダルが正しく表示されるか確認
3. フォーム送信後、固定チャンネルに投稿されるか確認
4. `/yatta` コマンドで同様にテスト
5. エラー時のログが正しく出力されるか確認

### Replit デプロイ後のテスト

1. Bot が起動するか確認
2. Web サーバー（:8080）にアクセスできるか確認
3. スラッシュコマンドが Discord で使えるか確認
4. 24時間稼働が維持されるか確認（UptimeRobot 設定後）

---

## 📚 参考リンク

- [discord.py ドキュメント](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Replit ドキュメント](https://docs.replit.com/)
- [UptimeRobot](https://uptimerobot.com/)

---

## 🔄 今後の拡張案（オプション）

### 機能拡張
- データベース連携（やること・やったことを記録）
- 統計情報の表示（やったこと集計）
- リマインダー機能（締切前に通知）
- 複数チャンネル対応

### UI 改善
- Embed メッセージでリッチな表示
- ボタン操作の追加
- コマンドオプションの追加

---

## ✅ 実装チェックリスト

### コードファイル
- [ ] `main.py` - Bot 本体
- [ ] `keep_alive.py` - Web サーバー
- [ ] `requirements.txt` - 依存パッケージ
- [ ] `.env.example` - 環境変数テンプレート
- [ ] `.gitignore` - Git 除外設定
- [ ] `README.md` - セットアップ手順

### 機能実装
- [ ] スラッシュコマンド `/yaru`
- [ ] YaruModal の実装
- [ ] スラッシュコマンド `/yatta`
- [ ] YattaModal の実装
- [ ] 固定チャンネルへの投稿
- [ ] エラーハンドリング
- [ ] 日本語コメント

### テスト
- [ ] ローカルで動作確認
- [ ] Replit で動作確認
- [ ] スラッシュコマンドの同期確認
- [ ] モーダル表示の確認
- [ ] 投稿内容の確認

### ドキュメント
- [ ] `plan.md` の作成（✅ 完了）
- [ ] `README.md` の作成
- [ ] コード内コメントの充実
- [ ] セットアップ手順の説明

---

## 📝 開発メモ

### 実装のポイント

1. **モーダルの実装**
   - `discord.ui.Modal` を継承したクラスを作成
   - `discord.ui.TextInput` でフィールドを定義
   - `on_submit` メソッドで送信処理

2. **スラッシュコマンドの実装**
   - `@tree.command()` デコレータを使用
   - `interaction.response.send_modal()` でモーダルを表示
   - 同期は `tree.sync()` で実行

3. **エラーハンドリング**
   - try-except で例外を捕捉
   - print() でログ出力（Replit のコンソールに表示）
   - ユーザーにもエラーメッセージを返す

4. **初心者向けの工夫**
   - 各行にコメントを記載
   - 変数名は分かりやすく
   - 処理の流れが追いやすい構造

---

**次のステップ**: 各ファイルの実装に進みます。

