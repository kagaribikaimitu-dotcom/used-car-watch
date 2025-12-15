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
    notify("✅ GitHub Actions からのテスト通知です")

if __name__ == "__main__":
    check()
