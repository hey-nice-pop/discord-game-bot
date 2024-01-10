from dotenv import load_dotenv
load_dotenv()

import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
RESPONSE_CHANNEL_ID = int(os.getenv('RESPONSE_CHANNEL_ID'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')