# temperature.py
import json
import datetime
import math

TEMPERATURE_FILE = 'temperature.json'

async def update_temperature(channel, amount):
    with open(TEMPERATURE_FILE, 'r') as file:
        data = json.load(file)

    data['currentTemperature'] += amount

    thresholds = [60, 70, 80, 90]
    for threshold in thresholds:
        if data['currentTemperature'] >= threshold and data['currentTemperature'] - amount < threshold:
            print ('test')
            await channel.send(f'🌡️ 温度が{math.floor(threshold)}度を超えました！')

    with open(TEMPERATURE_FILE, 'w') as file:
        json.dump(data, file)

async def reset_daily_message_count():
    with open(TEMPERATURE_FILE, 'r') as file:
        data = json.load(file)

    data['previousDayMessageCount'] = data['currentDayMessageCount']
    data['currentDayMessageCount'] = 0
    data['lastResetDate'] = str(datetime.date.today())

    with open(TEMPERATURE_FILE, 'w') as file:
        json.dump(data, file)

def calculate_temperature_increase(data):
    if data['previousDayMessageCount'] == 0:
        return 0

    target_message_count = data['previousDayMessageCount'] * 0.8
    return 30.0 / target_message_count

async def check_and_reward_temperature(channel, data):
    current_date = str(datetime.date.today())
    
    if data['currentTemperature'] >= 90 and (data['lastRewardDate'] != current_date):
        await channel.send('🎉 おめでとうございます！今日のリワードを獲得しました！')
        data['lastRewardDate'] = current_date
        data['currentTemperature'] = 60
    elif data['currentTemperature'] >= 90:
        await channel.send('🌡️ 温度が90度に達しましたが、今日のリワードは既に受け取っています。温度をリセットします。')
        data['currentTemperature'] = 60
