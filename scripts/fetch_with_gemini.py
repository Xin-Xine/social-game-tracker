import os
import json
import requests
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません。")

client = genai.Client(api_key=GEMINI_API_KEY)

GAMES = [
    {"name": "原神", "url": "https://genshin.hoyoverse.com/ja/news"},
    # 他ゲームもここに追加可能
]

OUTPUT_FILE = "data/result.json"

def fetch_html(url):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

def call_gemini_ai(html, game_name):
    prompt = f"""
ゲーム「{game_name}」公式お知らせページHTMLです。
HTMLからアップデート情報のみを抽出し、以下のJSON形式で出力してください。

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

HTML:
{html}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=1000
        )
    )

    text = response.text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"AI parse failed for {game_name}, raw output:\n{text}")
        return []

def main():
    all_updates = []
    for g in GAMES:
        try:
            html = fetch_html(g["url"])
            updates = call_gemini_ai(html, g["name"])
            all_updates.extend(updates)
        except Exception as e:
            print(f"Error fetching {g['name']}: {e}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_updates, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_updates)} updates.")

if __name__ == "__main__":
    main()
