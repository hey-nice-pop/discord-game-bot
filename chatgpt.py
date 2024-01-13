# chatgpt.py
import openai

def set_openai_key(key):
    openai.api_key = key

character_description = "stoneはペンギンです。脱俗的で掴みどころのない性格を持ちます。サウナに入ることが大好きでカスタードクリームなどの甘い食べ物が好きです。ユーザーからのメッセージにstoneとして、自然な会話のスタイルで応答してください。"

async def generate_response(messages):
    try:
        # messages は [{"role": "user" or "assistant", "content": "message content"}, ...] 形式のリスト
        full_messages = [{"role": "system", "content": character_description}] + messages

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_messages
        )
        if response and hasattr(response, 'choices') and response.choices:
            return response.choices[0].message['content']
        else:
            return "応答を生成できませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {e}"
