import discord
from discord.ext import commands
import config

import othello
import bj # BlackjackBotモジュールをインポート
import minesweeper
import chatgpt

from temperature import process_message

YOUR_BOT_TOKEN = config.BOT_TOKEN

RESPONSE_CHANNEL_ID = config.RESPONSE_CHANNEL_ID #chatGPTを動作させるチャンネルID
IGNORED_CATEGORY_ID = 123456789012345678  # 温度上昇を無視するカテゴリのID

OPENAI_API_KEY = config.OPENAI_API_KEY
chatgpt.set_openai_key(OPENAI_API_KEY)

# インテントを有効化
intents = discord.Intents.all()

# Botオブジェクトの生成
bot = commands.Bot(
    command_prefix='/', 
    intents=intents, 
    sync_commands=True,
    activity=discord.Game("水風呂")
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ログイン完了: {bot.user}')

# コマンドをothello.pyから読み込む
#othello.setup(bot)

# マインスイーパー機能のセットアップ
#minesweeper.setup(bot)

# ブラックジャック機能のセットアップ
#bj.setup(bot)

#chatGPT
async def handle_chatgpt_response(message):
    if message.channel.id == RESPONSE_CHANNEL_ID:
        # チャンネルの履歴を取得(10件)
        history = [msg async for msg in message.channel.history(limit=10)]
        # 履歴をAPIに渡す形式に変換
        history_messages = [{"role": "user" if msg.author != bot.user else "assistant", "content": msg.content} for msg in history[::-1]]
        # 応答の生成
        response = await chatgpt.generate_response(history_messages)
        await message.channel.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # ChatGPT応答処理を実行
    #await handle_chatgpt_response(message)

    # 温度更新処理を実行
    if message.channel.category_id != IGNORED_CATEGORY_ID:  # YOUR_CATEGORY_IDには特定のカテゴリIDを設定
        await process_message(message)

    # 他のコマンドも処理
    await bot.process_commands(message)

# Discordボットを起動
bot.run(YOUR_BOT_TOKEN)
