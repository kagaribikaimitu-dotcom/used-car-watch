Name: Used Car Watch

on:
  schedule:
    - cron: "0 * * * *" # 1時間ごと (実行頻度を変えたい場合はこの行を変更するのよ)
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 🌟 1. seen.txt のキャッシュを復元するステップ 🌟
      - name: Restore seen URL cache
        uses: actions/cache/restore@v4
        with:
          path: seen.txt
          key: ${{ runner.os }}-seen-urls

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run checker
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python check_cars.py

      # 🌟 2. seen.txt のキャッシュを保存するステップ 🌟
      - name: Save seen URL cache
        uses: actions/cache/save@v4
        with:
          path: seen.txt
          key: ${{ runner.os }}-seen-urls

