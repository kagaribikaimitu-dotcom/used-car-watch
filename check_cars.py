import requests
import os
from bs4 import BeautifulSoup

# ==============================
# 設定
# ==============================

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")
SEEN_FILE = "seen.txt"

URLS = {
    "カーセンサー": "https://www.carsensor.net/usedcar/search.php?CARC=SB_S052&GRDKC=SB_S052_F001_K018%2ASB_S052_F001_K022&OPTCD=REP0&YMIN=2017&SMAX=100000&CL=GL&AL=1&SORT=19&STID=SMPH0001"
}

# ==============================
# Discord通知
# ==============================

def notify(message):
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

# ==============================
# 既出URLの読み書き
# ==============================

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_seen(urls):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        for u in sorted(urls):
            f.write(u + "\n")

# ==============================
# カーセンサーHTML解析
# ==============================

def extract_cars_from_carsensor(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    results = set()

    for a in soup.select("a[href*='/usedcar/detail/']"):
        href = a.get("href")
        if href and href.startswith("/usedcar/detail/"):
            results.add("https://www.carsensor.net" + href)

    return list(results)

# ==============================
# メイン処理
# ==============================

def check():
    name = "カーセンサー"
    url = URLS[name]

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15
    )

    if r.status_code != 200:
        notify(f"⚠️ {name} 取得失敗 status={r.status_code}")
        return

    car_urls = extract_cars_from_carsensor(r.text)

    seen = load_seen()
    new_cars = [u for u in car_urls if u not in seen]

    if new_cars:
        msg = "🚗 **新着 レヴォーグ 2.0 STI**\n\n" + "\n".join(new_cars[:5])
        notify(msg)

    save_seen(car_urls)

# ==============================
# 実行
# ==============================

if __name__ == "__main__":
    check()
