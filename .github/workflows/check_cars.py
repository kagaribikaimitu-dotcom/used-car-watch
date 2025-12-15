import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

# ■ 今回のカーセンサー検索URL
URLS = {
    "カーセンサー": "https://www.carsensor.net/usedcar/search.php?CARC=SB_S052&GRDKC=SB_S052_F001_K018%2ASB_S052_F001_K022&OPTCD=REP0&YMIN=2017&SMAX=100000&CL=GL&AL=1&SORT=19&STID=SMPH0001"
}

# ---------------------------------
def notify(message):
    """Discordに通知"""
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

# ---------------------------------
def extract_cars_from_carsensor(html_text):
    """
    CarSensorの検索結果から
    詳細ページURLを抽出して返す
    """
    soup = BeautifulSoup(html_text, "html.parser")
    results = set()

    # CarSensor の詳細リンクは /usedcar/detail/ で始まることが多い
    # <a href="/usedcar/detail/...">
    for a in soup.select("a[href*='/usedcar/detail/']"):
        href = a.get("href")
        if href and href.startswith("/usedcar/detail/"):
            full_url = "https://www.carsensor.net" + href
            results.add(full_url)

    return sorted(results)

# ---------------------------------
def check():
    notify("【テスト】check() 実行確認")
    # まずカーセンサーだけ
    name = "カーセンサー"
    url = URLS[name]
    print(f"[INFO] Fetching {name} ... {url}")

    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        print("HTTP取得失敗:", e)
        return

    if r.status_code != 200:
        print("ステータスコード:", r.status_code)
        return

    # HTML取得OK
    print("HTML length:", len(r.text))

    # 詳細URL一覧を抽出
    car_urls = extract_cars_from_carsensor(r.text)
    print(f"Found {len(car_urls)} car links")

    # ここでは「全部リストアップ」だけ
    for cu in car_urls:
        new_listings.append(f"{name} | {cu}")

    # 通知する（今回は全部）
    if new_listings:
        body = "🚗 **カーセンサー検索結果（仮）**\n\n"
        body += "\n".join(new_listings[:10])  # 最初の10件だけ
        notify(body)
    else:
        print("No car URLs found")

# ---------------------------------
if __name__ == "__main__":
    check()
