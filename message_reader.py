from telethon.sync import TelegramClient
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import csv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Channel details
channel_username = "@neuesausrussland"  # Use @channelname or ID (-100...)
start_date = datetime(2022, 2, 24, tzinfo=timezone.utc)
end_date = datetime(2023, 2, 24, tzinfo=timezone.utc)

# CSV file path
csv_file = "messages_full.csv"

with TelegramClient("anon", api_id, api_hash) as client:
    messages = client.iter_messages(channel_username, offset_date=start_date, reverse=True)

    # Open CSV file and write messages
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "sender", "is_reply", "forward", "bot", "message"])  # Header

        for msg in messages:
            if msg.date > end_date:
                break
            sender = msg.sender_id if msg.sender_id else "Unknown"
            writer.writerow([msg.date, sender, msg.is_reply, msg.forward, msg.via_bot, msg.text])

print(f"Messages saved to {csv_file}")