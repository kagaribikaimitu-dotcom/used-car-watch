import requests
import os

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

def notify(message):
    if not WEBHOOK:
        print("Webhook未設定のため通知スキップ")
        return
    requests.post(WEBHOOK, json={"content": message})

def check():
    print("スクリプト実行テストOK")

if __name__ == "__main__":
    check()
