import discord
from discord.ext import commands
import config

from othello import OthelloGame, start_game, place_piece, pass_turn, end_game  # othello.pyからクラスと関数をインポート
import bj # BlackjackBotモジュールをインポート
import minesweeper
import chatgpt

YOUR_BOT_TOKEN = config.BOT_TOKEN

RESPONSE_CHANNEL_ID = config.RESPONSE_CHANNEL_ID

OPENAI_API_KEY = config.OPENAI_API_KEY
chatgpt.set_openai_key(OPENAI_API_KEY)

# インテントを有効化
intents = discord.Intents.all()

# Botオブジェクトの生成
bot = commands.Bot(
    command_prefix='/', 
    intents=intents, 
    sync_commands=True,
    activity=discord.Game("外気浴")
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ログイン完了: {bot.user}')

# コマンドをothello.pyから読み込む
bot.tree.command(name='othello_start', description='新しいオセロを始めます')(start_game)
bot.tree.command(name='othello_place', description='指定した位置にコマを置きます')(place_piece)
bot.tree.command(name='othello_pass', description='手番をパスします')(pass_turn)
bot.tree.command(name='othello_end', description='オセロを強制終了します')(end_game)

# マインスイーパー機能のセットアップ
minesweeper.setup(bot)

# ブラックジャック機能のセットアップ
bj.setup(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name}がログインしました')

# chatGPT機能
@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:
        print("Bot自身のメッセージを無視します。")
        return

    if message.channel.id != RESPONSE_CHANNEL_ID:
        print(f"指定されたチャンネル以外でのメッセージです: {message.channel.id}")
        return

    print(f"メッセージを受信しました: {message.content}")
    response = await chatgpt.generate_response(message.content)
    print(f"生成された応答: {response}")

    await message.channel.send(response)
    await bot.process_commands(message)

# Discordボットを起動
bot.run(YOUR_BOT_TOKEN)