# 個人的なdiscordサーバー用のbot
## 必要
- discord.py
- openai(0.28)
```bash
pip install openai==0.28
```
- python-dotenv
- .env
```.env
BOT_TOKEN = 'YOURTOKEN'
RESPONSE_CHANNEL_ID = 123456789 # YOURCHANNEL
OPENAI_API_KEY = 'YOURKEY'
```
## 機能
- マインスイーパー
  /minesweeper
- オセロ
  /othello_start,/othello_place ...
- ブラックジャック
  /bj_start,/bj_hit ...
- chatGPT