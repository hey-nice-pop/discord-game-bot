import datetime
import discord

async def get_most_reacted_post(guild: discord.Guild, date):
    most_reacted_post = None
    max_reactions = 0

    start_of_day = datetime.datetime.combine(date, datetime.time.min)
    end_of_day = datetime.datetime.combine(date, datetime.time.max)

    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=100, after=start_of_day, before=end_of_day):
                total_reactions = sum(reaction.count for reaction in message.reactions)
                if total_reactions > max_reactions:
                    most_reacted_post = message
                    max_reactions = total_reactions
        except Exception as e:
            print(f"チャンネル {channel.name} の履歴取得中にエラー: {e}")

    return most_reacted_post

async def send_90_degree_reward(channel_id: int, guild: discord.Guild, date):
    channel = guild.get_channel(channel_id)
    if not channel:
        print(f"チャンネルID {channel_id} が見つかりません。")
        return

    most_reacted_post = await get_most_reacted_post(guild, date)
    if most_reacted_post:
        post_url = most_reacted_post.jump_url
        await channel.send(f'90度に達しました！特別なリワードです！ 前日の最もリアクションが多かった投稿: {post_url}')
    else:
        await channel.send('90度に達しましたが、前日の投稿は見つかりませんでした。')