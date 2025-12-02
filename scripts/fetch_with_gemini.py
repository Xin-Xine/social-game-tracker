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
        # HTML取得
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        print("=== HTML取得成功 ===")
        print(html[:1000])  # 先頭1000文字だけログに出す（長すぎ防止）

        # BeautifulSoupで記事部分を抽出
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("li.news-item")
        if not articles:
            print("記事要素が見つかりませんでした")
        text_blocks = [a.get_text(" ", strip=True) for a in articles]
        print(f"抽出記事数: {len(text_blocks)}")

        # AIに渡すプロンプト
        chunk = "\n".join(text_blocks[:10])  # とりあえず最初の10件だけ
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
        ai_response = client.models.generate_content(
            model="gemini-2.5",
            contents=[prompt],
            temperature=0.0,
            max_output_tokens=1000
        )

        print("=== AI返り値 ===")
        print(ai_response.text)

        updates = []
        if ai_response.text:
            try:
                updates = json.loads(ai_response.text)
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
