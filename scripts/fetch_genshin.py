# scripts/fetch_genshin.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 取得対象 URL（原神公式アップデートページ例）
URL = "https://genshin.hoyoverse.com/ja/news"

# データを書き込むファイル
OUTPUT_FILE = "data/result.json"

def fetch_updates():
    updates = []

    try:
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # ニュース記事のセレクタ例（2025/12 現行構造に対応）
        # 適宜クラス名を公式サイトに合わせて変更してください
        articles = soup.select("ul.news-list li.news-item")
        for art in articles:
            date_tag = art.select_one(".date")
            title_tag = art.select_one(".title")
            link_tag = art.select_one("a")
            desc_tag = art.select_one(".summary")  # 要約があれば

            if not date_tag or not title_tag or not link_tag:
                continue

            date_text = date_tag.text.strip()
            try:
                # 日付形式を YYYY-MM-DD に統一
                date_obj = datetime.strptime(date_text, "%Y.%m.%d")
                date_str = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                date_str = date_text

            updates.append({
                "date": date_str,
                "game": "原神",
                "title": title_tag.text.strip(),
                "description": desc_tag.text.strip() if desc_tag else "",
                "link": link_tag["href"]
            })

    except Exception as e:
        print("Error fetching updates:", e)

    return updates

def save_json(updates):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updates, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    data = fetch_updates()
    save_json(data)
    print(f"Fetched {len(data)} updates.")
