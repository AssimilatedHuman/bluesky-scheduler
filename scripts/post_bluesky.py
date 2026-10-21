import os
import csv
from datetime import datetime, timedelta
from atproto import Client

CSV_PATH = "content/bluesky.csv"

def load_posts():
    posts = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append(row)
    return posts

def save_posts(posts):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "text", "posted"])
        writer.writeheader()
        writer.writerows(posts)

def should_post(timestamp_str):
    ts = datetime.fromisoformat(timestamp_str)
    now = datetime.utcnow()
    window_start = now - timedelta(hours=3)
    window_end = now + timedelta(hours=3)
    return window_start <= ts <= window_end

def post_to_bluesky(text):
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")

    client = Client()
    client.login(handle, password)
    client.send_post(text)

def main():
    posts = load_posts()
    changed = False

    for post in posts:
        if post["posted"].strip().lower() == "yes":
            continue
        if should_post(post["timestamp"]):
            print(f"Posting: {post['text']}")
            post_to_bluesky(post["text"])
            post["posted"] = "yes"
            changed = True

    if changed:
        save_posts(posts)

if __name__ == "__main__":
    main()

