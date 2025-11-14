"""
Replit で Bot を常時稼働させるための Web サーバー

Replit の無料プランでは一定時間操作がないとスリープします。
UptimeRobot などで定期的にこのサーバーにアクセスすることで、
Bot を起動し続けることができます。
"""

from flask import Flask
from threading import Thread

# Flask アプリを作成
app = Flask('')


@app.route('/')
def home():
    """
    ルートパス（/）にアクセスがあった時の処理
    Bot が起動していることを示すメッセージを返す
    """
    return "Bot is alive!"


@app.route('/status')
def status():
    """
    ステータス確認用エンドポイント
    UptimeRobot などでこのURLを監視する
    """
    return {
        'status': 'ok',
        'message': 'やる・やったBot is running'
    }


def run():
    """
    Flask サーバーを起動する関数
    0.0.0.0 ですべてのネットワークインターフェースでリッスン
    ポート 8080 で起動
    """
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    """
    Flask サーバーを別スレッドで起動する関数
    main.py から呼び出される
    """
    # 別スレッドでサーバーを起動
    t = Thread(target=run)
    t.daemon = True  # メインスレッド終了時に自動的に終了
    t.start()
    print('Keep-alive サーバーを起動しました (ポート: 8080)')


if __name__ == '__main__':
    # このファイルを直接実行した場合はサーバーを起動
    print('Keep-alive サーバーを起動します...')
    run()

