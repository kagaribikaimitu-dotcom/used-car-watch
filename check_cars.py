import requests
import os
SEEN_FILE = "seen.txt"

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_seen(urls):
    with open(SEEN_FILE, "w") as f:
        for u in urls:
            f.write(u + "\n")
WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

def notify(message):
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

def check():
    url = URLS["カーセンサー"]

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15
    )

    car_urls = extract_cars_from_carsensor(r.text)

    seen = load_seen()
    new_cars = [u for u in car_urls if u not in seen]

    if new_cars:
        msg = "🚗 新着レヴォーグ出品\n\n" + "\n".join(new_cars[:5])
        notify(msg)

    save_seen(car_urls)
if __name__ == "__main__":
    check()
