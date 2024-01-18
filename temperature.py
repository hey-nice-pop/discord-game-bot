import json
import datetime
from discord import Message
from filelock import FileLock, Timeout

# 温度を送信するチャンネル
TARGET_THREAD_CHANNEL_ID = 1184679498222932049

# JSONファイルのパス
JSON_FILE_PATH = 'temperature.json'
LOCK_PATH = 'temperature.json.lock'

async def process_message(message: Message):
    # 対象のスレッドを取得
    target_thread = message.guild.get_channel(TARGET_THREAD_CHANNEL_ID)

    try:
        with FileLock(LOCK_PATH, timeout=5):
            data, new_file_created = load_json()
            
            # JSONファイルが新しく作成された場合に60度の通知を送信
            if new_file_created:
                await target_thread.send('60度に達しました')

            # 現在の日付を取得
            today = str(datetime.date.today())

            # 日付が変わった場合の処理
            if data['last_date'] != today:
                data['yesterday_message_count'] = data['message_count']
                data['message_count'] = 0
                reset_temperature(data)
                data['last_date'] = today
                await target_thread.send('60度に達しました')

            previous_temperature = data['temperature']

            # メッセージ数の更新
            data['message_count'] += 1

            # 前日のメッセージ数を基に温度の上昇量を計算
            temperature_increase = 30 / (max(data['yesterday_message_count'], 1) * 0.8)
            data['temperature'] += temperature_increase

            # 特定の温度を超えた場合のメッセージ送信
            await check_temperature_thresholds(message, data, previous_temperature)

            # JSONファイルにデータを保存
            save_json(data)
    except Timeout as e:
        print(f"ロックの獲得に失敗しました: {e}")
        # 必要に応じて、ここで再試行のロジックを追加する

async def check_temperature_thresholds(message: Message, data: dict, previous_temperature: float):
    # 対象のスレッドを取得
    target_thread = message.guild.get_channel(TARGET_THREAD_CHANNEL_ID)

    thresholds = [70, 80, 90]
    for threshold in thresholds:
        if previous_temperature < threshold <= data['temperature']:
            if threshold == 90:
                # 90度に達した場合、特別な処理を行う
                await handle_90_degree_threshold(data, message)
            else:
                # それ以外の閾値を超えた場合、通知メッセージを送信
                await target_thread.send(f'{threshold}度を超えました')

async def handle_90_degree_threshold(data: dict, message: Message):
    # 対象のスレッドを取得
    target_thread = message.guild.get_channel(TARGET_THREAD_CHANNEL_ID)

    # 90度に達した場合の特別なメッセージの処理
    if 'last_reward_date' not in data or data['last_reward_date'] != str(datetime.date.today()):
        await target_thread.send('90度に達しました！特別なメッセージです！')
        data['last_reward_date'] = str(datetime.date.today())
    else:
        await target_thread.send('90度を超えましたが、本日のリワードは受取済みです。')
    
    reset_temperature(data)
    await target_thread.send('60度にリセットされました')

def reset_temperature(data: dict):
    data['temperature'] = 60
    for threshold in [70, 80, 90]:
        data[f'notified_{threshold}'] = False

def load_json():
    new_file_created = False
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file), new_file_created
    except FileNotFoundError:
        # ファイルが存在しない場合は初期データを作成し、新ファイル作成フラグをTrueに設定
        new_file_created = True
        initial_data = {'temperature': 60, 'message_count': 0, 'yesterday_message_count': 20, 'last_date': str(datetime.date.today()), 'last_reward_date': ''}
        save_json(initial_data)
        return initial_data, new_file_created

def save_json(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
