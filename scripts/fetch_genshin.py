import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 原神公式お知らせページURL
URL = "https://genshin.mihoyo.com/ja/news"

try:
    res = requests.get(URL)
    res.raise_for_status()  # 取得失敗時に例外
except Exception as e:
    print(f"ページ取得エラー: {e}")
    exit(1)

soup = BeautifulSoup(res.text, "html.parser")
updates = []

# HTML構造に合わせてセレクタを調整
# 現状の例は仮のセレクタです。実際はブラウザで要素を確認してください
for item in soup.select(".news-card")[:5]:  # 最新5件だけ
    title_el = item.select_one(".title")
    date_el = item.select_one(".date")
    link_el = item.select_one("a")
    summary_el = item.select_one(".summary")

    # 要素が取得できない場合はスキップ
    if not (title_el and date_el and link_el and summary_el):
        continue

    updates.append({
        "game": "原神",
        "title": title_el.text.strip(),
        "date": date_el.text.strip(),
        "description": summary_el.text.strip(),
        "link": link_el["href"]
    })

# JSONに書き出し
with open("data/result.json", "w", encoding="utf-8") as f:
    json.dump(updates, f, ensure_ascii=False, indent=2)

print(f"{len(updates)}件の更新を取得しました")
