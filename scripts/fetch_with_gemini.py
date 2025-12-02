import os
import json
import requests
from google import genai

OUTPUT_FILE = "data/result.json"
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def fetch_genshin_updates():
    # 公式APIを直接叩く（例: noticeカテゴリ）
    url = "https://genshin.hoyoverse.com/content/yuanshen/getNewsList?game=genshin&category=notice&page=1"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        print("=== API取得成功 ===")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])  # 先頭だけログ

        # 記事リストをAIに渡す
        articles = data.get("data", {}).get("list", [])
        text_blocks = [a.get("title", "") + " " + a.get("content", "") for a in articles]

        prompt = f"""
以下はゲーム「原神」公式サイトの最新お知らせです。
このテキストから最新アップデート情報のみを以下のJSON形式で抽出してください。

JSON形式例:
[
  {{
    "game": "原神",
    "date": "YYYY-MM-DD",
    "title": "アップデートタイトル",
    "description": "内容要約",
    "link": "公式URL"
  }}
]

テキスト:
{text_blocks}
"""
        response = client.models.generate_content(
            model="gemini-2.5",
            contents=[prompt]
        )
        print("=== AI返り値 ===")
        print(response.text)

        updates = []
        if response.text:
            try:
                updates = json.loads(response.text)
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
