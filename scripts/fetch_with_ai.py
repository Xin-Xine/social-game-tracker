import requests
import json
import os

# Google Gemini / Copilot API を呼ぶライブラリは仮置きです
# 実際には公式SDKに置き換えてください
# 例: pip install openai for GPT-4o-mini
# ここでは fetch_genshin.py を土台にAI呼び出し部分を組み込み

GAMES = [
    {"name": "原神", "url": "https://genshin.hoyoverse.com/ja/news"},
    {"name": "GameB", "url": "https://example.com/gameb/news"}
]

OUTPUT_FILE = "data/result.json"

def fetch_html(url):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

def call_ai(html, game_name):
    """
    仮のAI呼び出し関数。
    実際は Gemini または Copilot API を呼び出し、
    プロンプトとHTMLを渡してJSONを返す
    """
    # ここではサンプルJSONを返す
    return [
        {
            "game": game_name,
            "date": "2025-12-02",
            "title": "Ver1.2.0 アップデート",
            "description": "新イベント開始、バランス調整など",
            "link": "https://example.com/news/12345"
        }
    ]

def main():
    all_updates = []
    for g in GAMES:
        try:
            html = fetch_html(g["url"])
            updates = call_ai(html, g["name"])
            all_updates.extend(updates)
        except Exception as e:
            print(f"Error fetching {g['name']}: {e}")

    # ディレクトリがなければ作る
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_updates, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_updates)} updates.")

if __name__ == "__main__":
    main()
