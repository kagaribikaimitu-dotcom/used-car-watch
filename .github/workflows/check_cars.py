import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

URLS = {
    "カーセンサー": "（https://www.carsensor.net/usedcar/search.php?CARC=SB_S052&GRDKC=SB_S052_F001_K018%2ASB_S052_F001_K022&OPTCD=REP0&YMIN=2017&SMAX=100000&CL=GL&AL=1&SORT=19&STID=SMPH0001）",
    "グーネット": "（https://www.goo-net.com/php/search/summary.php）",
    "スグダス": "（https://ucar.subaru.jp/php/search/summary.php?baitai=iphone）",
}

def notify(message):
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

def check():
    hits = []
    for name, url in URLS.items():
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # 仮：VMレヴォーグ文字列チェック（あとで調整）
        if "レヴォーグ" in soup.text:
            hits.append(f"{name} に該当あり\n{url}")

    if hits:
        notify("🚗 **VMレヴォーグ新着候補**\n\n" + "\n\n".join(hits))
    else:
        print("No hits")

if __name__ == "__main__":
    check()
