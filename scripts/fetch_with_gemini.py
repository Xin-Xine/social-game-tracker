import os
import json
import google.generativeai as genai
from google.generativeai import ToolInput  # 必要なら

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません。")

# 最新 SDK では Client は不要、直接 genai.configure() を使用
genai.configure(api_key=GEMINI_API_KEY)

# 対象ゲームと公式お知らせURL
GAMES = [
    {"name": "原神", "url": "https://genshin.hoyoverse.com/ja/news"},
    # 他ゲームも追加可能
]

OUTPUT_FILE = "data/result.json"

def call_gemini_ai_url(game_name, url):
    """
    URLだけ渡してAIにページを解析させ、JSONを返す
    """
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
        # 最新 Gemini API 仕様に沿った呼び出し
        response = genai.models.generate_content(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_output_tokens=1000,
            # URL context は tools ではなく input_context を利用する場合もある
            # tools=[ToolInput(name="url_context", input=url)]  # 必要に応じて有効化
        )

        # 最新 SDK では response.output_text が返る
        text = getattr(response, "output_text", None)
        if not text:
            print(f"No output from AI for {game_name}")
            return []

        # JSON化
        try:
            return json.loads(text)
        except Exception as e:
            print(f"JSON parse error for {game_name}: {e}")
            return []

    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
        return []

def main():
    all_updates = []
    for g in GAMES:
        updates = call_gemini_ai_url(g["name"], g["url"])
        all_updates.extend(updates)

    # JSON保存
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_updates, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_updates)} updates.")

if __name__ == "__main__":
    main()
