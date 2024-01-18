# コミュニティサーバー向け discord bot
## 必要
- discord.py
- openai(0.28)
```bash
pip install openai==0.28
```
- python-dotenv
```bash
pip install python-dotenv
```
- filelock
```bash
pip install filelock
```
- .env
```.env
BOT_TOKEN = 'YOURTOKEN' #bottoken
OPENAI_API_KEY = 'YOURKEY' #openaikey
RESPONSE_CHANNEL_ID = 123456789 # chatgptを応答させるチャンネル
IGNORED_CATEGORY_ID = 123456789 # 温度上昇を無視するチャンネル
TARGET_THREAD_CHANNEL_ID = 123456789 # 温度上昇を通知するチャンネル
```
## 機能
### スラッシュコマンド( / )に対応
- マインスイーパー
- オセロ
- ブラックジャック
### 指定したチャンネルで応答
- chatGPT
- コミュニティメッセージで上昇する温度計とリワード🌡️
