# chatgpt.py
import openai

def set_openai_key(key):
    openai.api_key = key

character_description = "stoneはペンギンの形をした人工知能です。脱俗的で飄々としており掴みどころのない性格を持ちます。ユーザーからのメッセージにstoneとして、自然な会話のスタイルで応答してください。"

async def generate_response(message_content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": character_description},
                {"role": "user", "content": message_content}
            ]
        )
        if response and hasattr(response, 'choices') and response.choices:
            # 正しい属性のアクセス方法に注意
            return response.choices[0].message['content']
        else:
            return "応答を生成できませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {e}"
