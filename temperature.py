import json
import datetime
from discord import Message
from filelock import FileLock

# JSONファイルのパス
JSON_FILE_PATH = 'temperature.json'
LOCK_PATH = 'temperature.json.lock'

async def process_message(message: Message):
    with FileLock(LOCK_PATH, timeout=5):
        data = load_json()

        # 現在の日付を取得
        today = str(datetime.date.today())

        # 日付が変わった場合の処理
        if data['last_date'] != today:
            data['yesterday_message_count'] = data['message_count']
            data['message_count'] = 0
            data['temperature'] = 60
            data['last_date'] = today
            for threshold in [60, 70, 80, 90]:
                data[f'notified_{threshold}'] = False

        # メッセージ数の更新
        data['message_count'] += 1

        # 前日のメッセージ数を基に温度の上昇量を計算
        temperature_increase = 30 / (max(data['yesterday_message_count'], 1) * 0.8)
        data['temperature'] += temperature_increase

        # 特定の温度を超えた場合のメッセージ送信
        await check_temperature_thresholds(message, data)

        # JSONファイルにデータを保存
        save_json(data)

async def check_temperature_thresholds(message: Message, data: dict):
    thresholds = [60, 70, 80, 90]
    for threshold in thresholds:
        if data['temperature'] >= threshold and not data.get(f'notified_{threshold}', False):
            await message.channel.send(f'{threshold}度を超えました')
            data[f'notified_{threshold}'] = True

    # 90度に達した場合の特別なメッセージの処理
    if data['temperature'] >= 90:
        if 'last_reward_date' not in data or data['last_reward_date'] != str(datetime.date.today()):
            await message.channel.send('90度に達しました！特別なメッセージです！')
            data['last_reward_date'] = str(datetime.date.today())
            data['temperature'] = 60  # 温度をリセット
        else:
            await message.channel.send('90度を超えましたが、本日のリワードは受取済みです。')

def load_json():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # ファイルが存在しない場合は初期データを作成
        return {'temperature': 60, 'message_count': 0, 'yesterday_message_count': 0, 'last_date': str(datetime.date.today()), 'last_reward_date': ''}

def save_json(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
