"""
Discord Bot - やる・やったBot
スラッシュコマンド /yaru と /yatta を実装
"""

import discord
from discord import app_commands
from discord.ui import Modal, TextInput
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# .env ファイルから環境変数を読み込む
load_dotenv()

# Bot の設定
# Intents は最小限（message_content は不要）
intents = discord.Intents.default()

# Discord クライアントを作成
client = discord.Client(intents=intents)

# スラッシュコマンド用のツリーを作成
tree = app_commands.CommandTree(client)

# 固定の投稿先チャンネル ID
TARGET_CHANNEL_ID = 1435802151648497711


# ==============================================
# モーダル（入力フォーム）の定義
# ==============================================

class YaruModal(Modal, title='やるぞ宣言'):
    """
    /yaru コマンドで表示されるモーダル
    やることと締切を入力してもらう
    """
    
    # 入力フィールド1: やること（必須）
    yaru_koto = TextInput(
        label='やること',
        placeholder='例: Pythonの勉強を1時間やる',
        required=True,
        max_length=200,
        style=discord.TextStyle.short  # 1行入力
    )
    
    # 入力フィールド2: 締切（任意）
    shime_kiri = TextInput(
        label='締切（任意）',
        placeholder='例: 明日の18時まで',
        required=False,
        max_length=100,
        style=discord.TextStyle.short  # 1行入力
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """
        フォーム送信時の処理
        固定チャンネルに投稿する
        """
        try:
            # 投稿先のチャンネルを取得
            channel = client.get_channel(TARGET_CHANNEL_ID)
            
            if channel is None:
                # チャンネルが見つからない場合
                await interaction.response.send_message(
                    'エラー: 投稿先のチャンネルが見つかりませんでした。',
                    ephemeral=True  # 本人にだけ見えるメッセージ
                )
                return
            
            # 投稿内容を作成
            # ユーザーをメンション形式で表示
            message = f"{interaction.user.mention} さんが「やるぞ宣言」をしました！\n"
            message += f"■ やること: {self.yaru_koto.value}\n"
            
            # 締切が入力されている場合のみ追加
            if self.shime_kiri.value:
                message += f"■ 締切: {self.shime_kiri.value}"
            else:
                message += f"■ 締切: なし"
            
            # チャンネルに投稿
            await channel.send(message)
            
            # ユーザーに完了メッセージを返す（本人にだけ見える）
            await interaction.response.send_message(
                '✅ やるぞ宣言を投稿しました！',
                ephemeral=True
            )
            
            print(f'[やるぞ宣言] {interaction.user.name}: {self.yaru_koto.value}')
            
        except Exception as e:
            # エラーが発生した場合
            print(f'エラーが発生しました: {e}')
            await interaction.response.send_message(
                f'エラーが発生しました: {e}',
                ephemeral=True
            )


class YattaModal(Modal, title='やったよ報告'):
    """
    /yatta コマンドで表示されるモーダル
    やったことと感想を入力してもらう
    """
    
    # 入力フィールド1: やったこと（必須）
    yatta_koto = TextInput(
        label='やったこと',
        placeholder='例: Pythonの勉強を1時間やりました',
        required=True,
        max_length=500,
        style=discord.TextStyle.paragraph  # 複数行入力
    )
    
    # 入力フィールド2: ひとこと感想（任意）
    kanso = TextInput(
        label='ひとこと感想（任意）',
        placeholder='例: 思ったより難しかったけど楽しかった！',
        required=False,
        max_length=500,
        style=discord.TextStyle.paragraph  # 複数行入力
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """
        フォーム送信時の処理
        固定チャンネルに投稿する
        """
        try:
            # 投稿先のチャンネルを取得
            channel = client.get_channel(TARGET_CHANNEL_ID)
            
            if channel is None:
                # チャンネルが見つからない場合
                await interaction.response.send_message(
                    'エラー: 投稿先のチャンネルが見つかりませんでした。',
                    ephemeral=True
                )
                return
            
            # 投稿内容を作成
            message = f"{interaction.user.mention} さんが「やったよ報告」をしました！\n"
            message += f"■ やったこと: {self.yatta_koto.value}\n"
            
            # 感想が入力されている場合のみ追加
            if self.kanso.value:
                message += f"■ ひとこと感想: {self.kanso.value}"
            else:
                message += f"■ ひとこと感想: なし"
            
            # チャンネルに投稿
            await channel.send(message)
            
            # ユーザーに完了メッセージを返す
            await interaction.response.send_message(
                '✅ やったよ報告を投稿しました！',
                ephemeral=True
            )
            
            print(f'[やったよ報告] {interaction.user.name}: {self.yatta_koto.value}')
            
        except Exception as e:
            # エラーが発生した場合
            print(f'エラーが発生しました: {e}')
            await interaction.response.send_message(
                f'エラーが発生しました: {e}',
                ephemeral=True
            )


# ==============================================
# スラッシュコマンドの定義
# ==============================================

@tree.command(name='yaru', description='やるぞ宣言をします')
async def yaru_command(interaction: discord.Interaction):
    """
    /yaru コマンド
    YaruModal（やるぞ宣言フォーム）を表示する
    """
    try:
        # モーダルを表示
        await interaction.response.send_modal(YaruModal())
        print(f'[コマンド実行] /yaru by {interaction.user.name}')
        
    except Exception as e:
        print(f'エラー: {e}')


@tree.command(name='yatta', description='やったよ報告をします')
async def yatta_command(interaction: discord.Interaction):
    """
    /yatta コマンド
    YattaModal（やったよ報告フォーム）を表示する
    """
    try:
        # モーダルを表示
        await interaction.response.send_modal(YattaModal())
        print(f'[コマンド実行] /yatta by {interaction.user.name}')
        
    except Exception as e:
        print(f'エラー: {e}')


# ==============================================
# イベントハンドラ
# ==============================================

@client.event
async def on_ready():
    """
    Bot が起動した時の処理
    """
    print('=====================================')
    print(f'Bot が起動しました: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print('=====================================')
    
    # スラッシュコマンドを Discord に同期
    try:
        synced = await tree.sync()
        print(f'スラッシュコマンドを {len(synced)} 件同期しました')
        print('同期されたコマンド:')
        for cmd in synced:
            print(f'  - /{cmd.name}')
    except Exception as e:
        print(f'コマンドの同期に失敗しました: {e}')


@client.event
async def on_error(event, *args, **kwargs):
    """
    エラーが発生した時の処理
    """
    print(f'エラーが発生しました: {event}')
    import traceback
    traceback.print_exc()


# ==============================================
# Bot の起動
# ==============================================

if __name__ == '__main__':
    # Bot トークンを環境変数から取得
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print('エラー: BOT_TOKEN が設定されていません')
        print('.env ファイルに BOT_TOKEN を設定してください')
        exit(1)
    
    # Replit 用の Web サーバーを起動（keep-alive 用）
    keep_alive()
    
    # Bot を起動
    try:
        print('Bot を起動中...')
        client.run(bot_token)
    except Exception as e:
        print(f'Bot の起動に失敗しました: {e}')
        exit(1)

