# やる・やったBot 引き継ぎメモ

最終更新: 2025-11-14

## 1. プロジェクト概要

- **目的**: 子どもが「今日やること / やったこと」を Discord で簡単に記録できるようにする。
- **実装技術**: Python / discord.py / Flask / gspread / Google Service Account。
- **保存先**:
  - Discord 固定チャンネル: `TARGET_CHANNEL_ID` (デフォルト: `1435802151648497711`)
  - Google スプレッドシート: `SPREADSHEET_ID=157xGD-aGLFL4Iyteyg5i81NJa7hontZyj7fc_wmVJ0M` の `yaru_yatta_log` シート

## 2. 現状の機能

### 2-1. 入力フロー

- チャンネルに投稿された「やる・やったボタン」メッセージから操作。
- ボタンは 2 種類:
  - **やるぞ宣言ボタン** → `YaruModal` モーダル表示
  - **やったよ報告ボタン** → `YattaModal` モーダル表示
- 予備としてスラッシュコマンドも実装済み:
  - `/yaru`
  - `/yatta`

### 2-2. 投稿内容

- **やるぞ宣言**
  - 入力: `やること`（必須） / `締切`（任意）
  - Discord 投稿例:
    ```
    @ユーザー さんが「やるぞ宣言」をしました！
    ■ やること: 国語プリントを1枚やる
    ■ 締切: 今日の19時まで
    ```
- **やったよ報告**
  - 入力: `やったこと`（必須） / `ひとこと感想`（任意）
  - Discord 投稿例:
    ```
    @ユーザー さんが「やったよ報告」をしました！
    ■ やったこと: 国語プリントを1枚やりました
    ■ ひとこと感想: 意外と簡単だった！
    ```

### 2-3. スプレッドシート連携

`yaru_yatta_log` シートに以下の形式で1行追記されます。

| 列 | 内容                   | 例                          |
|----|------------------------|-----------------------------|
| A  | 記録日時 (JST)         | 2025-11-14 15:50:12         |
| B  | 種類                   | やるぞ宣言 / やったよ報告   |
| C  | Discord ID            | 1262728550696615948        |
| D  | Discord名（表示名）    | かずムチー                  |
| E  | メイン内容             | 算数ドリルを1ページやる     |
| F  | 補足（締切/感想など）  | 今日の19時まで / なしなど   |

※ スキーマは `append_entry()` 内で固定されています。

## 3. 環境変数と前提条件

`.env` の主なキー:

```env
BOT_TOKEN=Discord の Bot トークン
TARGET_CHANNEL_ID=投稿先チャンネルID
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/service-account.json
SPREADSHEET_ID=157xGD-aGLFL4Iyteyg5i81NJa7hontZyj7fc_wmVJ0M
SHEET_NAME=yaru_yatta_log
```

### Service Account 周り

- `GOOGLE_SERVICE_ACCOUNT_JSON` の JSON には以下権限が必要:
  - 対象スプレッドシートに対する「編集者」権限
- 共有設定: スプレッドシート側で、サービスアカウントのメールアドレスを「編集者」として追加。

## 4. Bot の操作方法（管理者視点）

1. `.env` を設定し、`python main.py` で Bot を起動。
2. Discord で、ボタンを設置したいチャンネルへ移動。
3. そのチャンネルで `/post_buttons` を実行（メッセージ管理権限のあるユーザー）。
4. Bot が投稿した「やる・やったボタン」メッセージをピン留め。
5. 子どもたちはそのメッセージのボタンを押すだけで利用可能。

※ Bot 再起動後も、既存のボタンは `client.add_view(ActionButtons())` により有効のままです。

## 5. Next Step / 今後の拡張候補

### 5-1. BigQuery 連携

- 現在はスプレッドシートまでで止めているが、既存の「スプレッドシート → BQ」基盤がある場合は、そのパイプラインに `yaru_yatta_log` を追加するだけでよい。
- 推奨フロー:
  1. GAS または Python バッチで定期的に `yaru_yatta_log` を読み取り
  2. BQ テーブル（例: `yaru_yatta_logs`）へ upsert/append
  3. Looker Studio 等で学習ログダッシュボードを作る

### 5-2. UX 改善

- 曜日・時間帯でボタン付きメッセージをリマインド送信
- 子どもごとに集計して「1週間のやる・やったレポート」を DM 送信
- メンター向けに「今週やるぞ宣言が少ない子」を一覧化

### 5-3. 権限・安全性

- Bot の権限は最小限（`Send Messages`, `Use Slash Commands`）に抑える方針で OK。
- Service Account JSON はローカル / Replit の Secrets にのみ置く（GitHub には絶対にコミットしない）。

## 6. よくあるハマりポイント

- `/post_buttons` を打っても何も起きない:
  - Bot がオンラインか
  - そのサーバーに Bot が招待されているか
  - スラッシュコマンドが同期されるまで数分かかることがある
- シートにデータが入らない:
  - `GOOGLE_SERVICE_ACCOUNT_JSON` のパスが正しいか
  - サービスアカウントにシート編集権限が付いているか
  - `SHEET_NAME` が実在するか（スペルミスを要確認）

## 7. 参考

- GitHub: https://github.com/opesys-del/yaru_yatta_bot
- 利用ライブラリ:
  - discord.py
  - Flask
  - gspread
  - google-auth

