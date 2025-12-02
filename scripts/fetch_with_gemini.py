import os
import json
import requests
from bs4 import BeautifulSoup
from google import genai

OUTPUT_FILE = "data/result.json"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def fetch_genshin_updates():
    url = "https://genshin.hoyoverse.com/ja/news"
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        # ニュース記事部分を抽出（原神公式は li.news-item が多い）
        articles = soup.select("li.news-item")
        text_blocks = [a.get_text(" ", strip=True) for a in articles]

        # チャンク処理（長文対策）
        chunk_size = 5000
        updates = []
        for i in range(0, len(text_blocks), chunk_size):
            chunk = "\n".join(text_blocks[i:i+chunk_size])
            prompt = f"""
ゲーム「原神」公式お知らせページのテキストです。
このテキストから最新アップデート情報のみを以下のJSON形式で抽出してください。

JSON形式例:
[
  {{
    "game": "原神",
    "date": "YYYY-MM-DD",
    "title": "アップデートタイトル",
    "description": "内容要約",
    "link": "{url}"
  }}
]

テキスト:
{chunk}
"""
            response = client.models.generate_content(
                model="gemini-2.5",
                contents=[prompt],
                temperature=0.0,
                max_output_tokens=1000
            )
            if response.text:
                try:
                    updates.extend(json.loads(response.text))
                except Exception as e:
                    print(f"JSON parse error: {e}")
        return updates
    except Exception as e:
        print(f"Error fetching Genshin updates: {e}")
        return []

def main():
    updates = fetch_genshin_updates()
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updates, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(updates)} updates.")

if __name__ == "__main__":
    main()
