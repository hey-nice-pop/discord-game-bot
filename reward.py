import datetime
import discord
import requests
import random

# YouTube Data APIのエンドポイントとAPIキー
YOUTUBE_SEARCH_API_URL = "https://www.googleapis.com/youtube/v3/search"
API_KEY = "AIzaSyBJyTHzc0HHXKx3AOqqT0XaAWojHraPliA"  # APIキーを設定

async def search_youtube_videos(query, max_results=50):
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(YOUTUBE_SEARCH_API_URL, params=params)
    response.raise_for_status()
    return response.json()

async def get_random_youtube_video_url():
    keywords = ["DSC", "IMG"]
    query = random.choice(keywords)
    videos_data = await search_youtube_videos(query)

    # 再生回数が0の動画を抽出 (APIから直接取得する方法はないため、再生回数は別途確認が必要)
    # この部分はAPIの制限により実際には実行できないかもしれません
    zero_view_videos = [video for video in videos_data['items'] if video['snippet']['liveBroadcastContent'] == 'none']

    if zero_view_videos:
        selected_video = random.choice(zero_view_videos)
        video_id = selected_video['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"

    return None


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

    youtube_video_url = await get_random_youtube_video_url()

    most_reacted_post = await get_most_reacted_post(guild, date)
    if most_reacted_post:
        post_url = most_reacted_post.jump_url
        await channel.send(f'90度に達しました！特別なリワードです！ 前日の最もリアクションが多かった投稿: {post_url}\n{youtube_video_url}')
    else:
        await channel.send('90度に達しましたが、前日の投稿は見つかりませんでした。')