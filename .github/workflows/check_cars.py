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
    notify("【DEBUG】ここまで実行されてます")
# ---------------------------------
if __name__ == "__main__":
    check()
