import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

URLS = {
    "カーセンサー": "https://www.carsensor.net/usedcar/search.php?CARC=SB_S052&GRDKC=SB_S052_F001_K018%2ASB_S052_F001_K022&OPTCD=REP0&YMIN=2017&SMAX=100000&CL=GL&AL=1&SORT=19&STID=SMPH0001",
    "グーネット": "https://www.goo-net.com/php/search/summary.php",
    "スグダス": "https://ucar.subaru.jp/php/search/summary.php?baitai=iphone",
}

def notify(message):
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

def check():
    print("WEBHOOK =", WEBHOOK)
    notify("✅ GitHub Actions テスト通知")

if __name__ == "__main__":
    check()
