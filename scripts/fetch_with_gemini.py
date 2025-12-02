import os
from google import genai

# APIキーを環境変数から取得
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def call_gemini_ai_url(game_name, url):
    prompt = f"""
ゲーム「{game_name}」公式お知らせページのURLです。
このページを解析して、最新アップデート情報のみを以下のJSON形式で出力してください。

JSON形式例:
[
  {{
    "game": "ゲーム名",
    "date": "YYYY-MM-DD",
    "title": "アップデートタイトル",
    "description": "内容要約",
    "link": "公式URL"
  }}
]

URL:
{url}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5",
            contents=[prompt],
            temperature=0.0,
            max_output_tokens=1000
        )

        text = response.text
        return json.loads(text) if text else []

    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
        return []
