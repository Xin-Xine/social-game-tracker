import requests
import json
import os

# Gemini APIキーは環境変数から取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません。GitHub Secrets に登録してください。")

# 対象ゲームリスト
GAMES = [
    {"name": "原神", "url": "https://genshin.hoyoverse.com/ja/news"},
    {"name": "GameB", "url": "https://example.com/gameb/news"}
]

OUTPUT_FILE = "data/result.json"

# HTML取得
def fetch_html(url):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

# Gemini API呼び出し（サンプル形式）
def call_gemini_ai(html, game_name):
    """
    HTMLを解析してアップデート情報のみを抽出し、JSON形式で返す
    """
    # APIエンドポイント（仮）
    url = "https://api.generativeai.google/v1beta2/models/gemini-code-assist-1:generateText"
    
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
    
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "temperature": 0,
        "maxOutputTokens": 1000
    }
    
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    # Gemini の応答を解析してJSONを返す（ここはAPI仕様に合わせて調整）
    result_text = resp.json().get("candidates", [{}])[0].get("output", "{}")
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        print(f"AI parse failed for {game_name}, raw output:\n{result_text}")
        return []

# メイン処理
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
