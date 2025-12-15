import requests
import os
from bs4 import BeautifulSoup

# ==============================
# 設定
# ==============================

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")
SEEN_FILE = "seen.txt"

URLS = {
    "カーセンサー": "https://www.carsensor.net/usedcar/search.php?CARC=SB_S052&GRDKC=SB_S052_F001_K018%2ASB_S052_F001_K022&OPTCD=REP0&YMIN=2017&SMAX=100000&CL=GL&AL=1&SORT=19&STID=SMPH0001",
    "グーネット": "https://www.goo-net.com/php/search/summary.php",
    "スグダス": "https://ucar.subaru.jp/php/search/summary.php?baitai=iphone"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==============================
# Discord通知
# ==============================

def notify(message):
    if not WEBHOOK:
        return
    requests.post(WEBHOOK, json={"content": message})

# ==============================
# 既出URLの管理
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
# 各サイトのURL抽出
# ==============================

def extract_carsensor(html):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "https://www.carsensor.net" + a["href"]
        for a in soup.select("a[href^='/usedcar/detail/']")
    }

def extract_goonet(html):
    soup = BeautifulSoup(html, "html.parser")
    return {
        a["href"]
        for a in soup.select("a[href*='/usedcar/detail/']")
        if a["href"].startswith("https://")
    }

def extract_sugudas(html):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "https://ucar.subaru.jp" + a["href"]
        for a in soup.select("a[href^='/vehicle/']")
    }

EXTRACTORS = {
    "カーセンサー": extract_carsensor,
    "グーネット": extract_goonet,
    "スグダス": extract_sugudas,
}

# ==============================
# メイン処理
# ==============================

def check():
    seen = load_seen()
    found_all = set()
    new_all = []

    for name, url in URLS.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue

            urls = EXTRACTORS[name](r.text)
            found_all |= urls

            for u in urls:
                if u not in seen:
                    new_all.append(f"{name} | {u}")

        except Exception:
            continue

    if new_all:
        msg = "🚗 **新着 レヴォーグ 2.0 STI**\n\n" + "\n".join(new_all[:10])
        notify(msg)

    save_seen(found_all)

# ==============================
# 実行
# ==============================

if __name__ == "__main__":
    check()
