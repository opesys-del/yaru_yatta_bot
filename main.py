"""
Discord Bot - やる・やったBot
スラッシュコマンド /yaru, /yatta に加えて、ボタンからモーダルを開けるようにする。
送信内容は Discord 固定チャンネルと Google スプレッドシートの両方に保存します。
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Optional

import discord
import gspread
from discord import app_commands
from discord.ui import Modal, TextInput, View
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

from keep_alive import keep_alive

# ==============================================
# 設定読み込み
# ==============================================

load_dotenv()

TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '1435802151648497711'))
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '157xGD-aGLFL4Iyteyg5i81NJa7hontZyj7fc_wmVJ0M')
SHEET_NAME = os.getenv('SHEET_NAME', 'yaru_yatta_log')
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')

# ==============================================
# Discord クライアント設定
# ==============================================

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ==============================================
# Google Sheets クライアント
# ==============================================

_gspread_client: Optional[gspread.Client] = None


def get_worksheet() -> gspread.Worksheet:
    """Google スプレッドシートのワークシートを取得する"""
    global _gspread_client

    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        raise ValueError('GOOGLE_SERVICE_ACCOUNT_JSON が設定されていません')

    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    if _gspread_client is None:
        credentials = Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_JSON,
            scopes=scopes,
        )
        _gspread_client = gspread.authorize(credentials)

    spreadsheet = _gspread_client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet(SHEET_NAME)
    return worksheet


def append_entry(entry_type: str, user: discord.User | discord.Member, primary_text: str, secondary_text: str) -> None:
    """スプレッドシートに1行追加する"""
    worksheet = get_worksheet()
    now_jst = datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')
    row = [
        now_jst,
        entry_type,
        str(user.id),
        user.display_name if hasattr(user, 'display_name') else user.name,
        primary_text,
        secondary_text or '-'
    ]
    worksheet.append_row(row, value_input_option='USER_ENTERED')


async def log_to_sheet(entry_type: str, user: discord.User | discord.Member, main_text: str, optional_text: str) -> None:
    """非同期でスプレッドシートに書き込む"""
    try:
        await asyncio.to_thread(append_entry, entry_type, user, main_text, optional_text)
    except Exception as error:
        print(f'[Spreadsheet Error] {error}')
        raise


# ==============================================
# ユーティリティ
# ==============================================

async def get_target_channel() -> discord.TextChannel:
    """投稿先のチャンネルを取得する"""
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(TARGET_CHANNEL_ID)
    if not isinstance(channel, discord.TextChannel):
        raise TypeError('投稿先のチャンネルがテキストチャンネルではありません')
    return channel


async def post_announcement(
    interaction: discord.Interaction,
    entry_type: str,
    field_title: str,
    field_value: str,
    optional_title: str,
    optional_value: Optional[str],
):
    """Discord チャンネルへの投稿とスプレッドシート保存をまとめて行う"""
    try:
        channel = await get_target_channel()
        optional_text = optional_value.strip() if optional_value else ''
        optional_display = optional_text or 'なし'

        content = (
            f"{interaction.user.mention} さんが「{entry_type}」をしました！\n"
            f"■ {field_title}: {field_value}\n"
            f"■ {optional_title}: {optional_display}"
        )

        await channel.send(content)
        await interaction.response.send_message(f'✅ {entry_type}を投稿しました！', ephemeral=True)

        try:
            await log_to_sheet(entry_type, interaction.user, field_value, optional_text)
        except Exception:
            # スプレッドシート保存に失敗してもユーザーには簡潔に知らせる
            await interaction.followup.send(
                '⚠️ Discord への投稿は成功しましたが、シート保存に失敗しました。',
                ephemeral=True,
            )
    except Exception as error:
        print(f'[投稿エラー] {error}')
        if not interaction.response.is_done():
            await interaction.response.send_message('エラーが発生しました。時間をおいて再度お試しください。', ephemeral=True)


# ==============================================
# モーダル定義
# ==============================================

class YaruModal(Modal, title='やるぞ宣言'):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.yaru_koto = TextInput(
            label='やること',
            placeholder='例: 算数ドリルを1ページやる',
            required=True,
            max_length=200,
            style=discord.TextStyle.short,
        )
        self.shime_kiri = TextInput(
            label='締切（任意）',
            placeholder='例: 今日の19時まで',
            required=False,
            max_length=100,
            style=discord.TextStyle.short,
        )
        self.add_item(self.yaru_koto)
        self.add_item(self.shime_kiri)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await post_announcement(
            interaction,
            entry_type='やるぞ宣言',
            field_title='やること',
            field_value=self.yaru_koto.value,
            optional_title='締切',
            optional_value=self.shime_kiri.value,
        )


class YattaModal(Modal, title='やったよ報告'):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.yatta_koto = TextInput(
            label='やったこと',
            placeholder='例: 算数ドリルを1ページやりました',
            required=True,
            max_length=500,
            style=discord.TextStyle.paragraph,
        )
        self.kanso = TextInput(
            label='ひとこと感想（任意）',
            placeholder='例: 思ったより簡単だった！',
            required=False,
            max_length=500,
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.yatta_koto)
        self.add_item(self.kanso)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await post_announcement(
            interaction,
            entry_type='やったよ報告',
            field_title='やったこと',
            field_value=self.yatta_koto.value,
            optional_title='ひとこと感想',
            optional_value=self.kanso.value,
        )


# ==============================================
# ボタン付きビュー
# ==============================================

class ActionButtons(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label='やるぞ宣言', style=discord.ButtonStyle.primary, custom_id='yaru_button')
    async def yaru_button(self, interaction: discord.Interaction, _: discord.ui.Button):  # type: ignore[override]
        await interaction.response.send_modal(YaruModal())

    @discord.ui.button(label='やったよ報告', style=discord.ButtonStyle.success, custom_id='yatta_button')
    async def yatta_button(self, interaction: discord.Interaction, _: discord.ui.Button):  # type: ignore[override]
        await interaction.response.send_modal(YattaModal())


# ==============================================
# スラッシュコマンド定義
# ==============================================

@tree.command(name='yaru', description='やるぞ宣言（旧: ボタンが使えない場合の予備）')
async def yaru_command(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(YaruModal())


@tree.command(name='yatta', description='やったよ報告（旧: ボタンが使えない場合の予備）')
async def yatta_command(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(YattaModal())


@tree.command(name='post_buttons', description='やる・やったボタンをこのチャンネルに投稿します（管理者向け）')
async def post_buttons(interaction: discord.Interaction) -> None:
    if not interaction.user.guild_permissions.manage_messages:  # type: ignore[attr-defined]
        await interaction.response.send_message('このコマンドは管理者のみ使用できます。', ephemeral=True)
        return

    view = ActionButtons()
    embed = discord.Embed(
        title='やる・やったボタン',
        description='ボタンを押すだけで「やるぞ宣言」と「やったよ報告」ができます。',
        color=0x4caf50,
    )
    await interaction.channel.send(embed=embed, view=view)  # type: ignore[arg-type]
    await interaction.response.send_message('ボタンを投稿しました。必要に応じてピン留めしてください。', ephemeral=True)


# ==============================================
# Discord イベントハンドラ
# ==============================================

@client.event
async def on_ready() -> None:
    print('=====================================')
    print(f'Bot が起動しました: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print('=====================================')

    # 再起動後もボタンが機能するよう persistent view を登録
    client.add_view(ActionButtons())

    try:
        synced = await tree.sync()
        print(f'スラッシュコマンドを {len(synced)} 件同期しました')
    except Exception as error:
        print(f'コマンド同期に失敗しました: {error}')


@client.event
async def on_error(event_method: str, *args, **kwargs) -> None:
    print(f'[Discord Error] {event_method}')
    import traceback
    traceback.print_exc()


# ==============================================
# Bot の起動
# ==============================================

if __name__ == '__main__':
    bot_token = os.getenv('BOT_TOKEN')

    if not bot_token:
        print('エラー: BOT_TOKEN が設定されていません (.env を確認してください)')
        raise SystemExit(1)

    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        print('エラー: GOOGLE_SERVICE_ACCOUNT_JSON が設定されていません')
        raise SystemExit(1)

    keep_alive()

    try:
        print('Bot を起動中...')
        client.run(bot_token)
    except Exception as error:
        print(f'Bot の起動に失敗しました: {error}')
        raise SystemExit(1)
