import os
import json
from google import genai  # 公式 SDK

# APIキーは環境変数から取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません。")

# SDK クライアント生成
client = genai.Client(api_key=GEMINI_API_KEY)

# 対象ゲームリスト
GAMES = [
    {"name": "原神", "url": "https://genshin.hoyoverse.com/ja/news"},
    # 他ゲーム追加可能
]

OUTPUT_FILE = "data/result.json"

def fetch_html(url):
    import requests
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

def call_gemini_ai(html, game_name):
    """
    HTMLを解析してアップデート情報のみを抽出し、JSON形式で返す
    """
    prompt = f"""
    以下はゲーム {game_name} の公式お知らせページHTMLです。
    このHTMLからアップデート情報のみ抽出し、JSONで出力してください。
    JSONフォーマット: 
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
        prompt=prompt,
        temperature=0,
        max_output_tokens=1000
    )

    # Gemini SDK の返り値からテキストを取得
    result_text = response.text

    # JSON化
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        print(f"AI parse failed for {game_name}, raw output:\n{result_text}")
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

    # ディレクトリ作成
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_updates, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_updates)} updates.")

if __name__ == "__main__":
    main()
