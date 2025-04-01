from telethon.sync import TelegramClient
from datetime import datetime, timezone
from dotenv import load_dotenv
import pandas as pd
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

    # Create a list to store message data
    message_data = []

    for msg in messages:
        if msg.date > end_date:
            break
        sender = msg.sender_id if msg.sender_id else "Unknown"
        message_data.append([msg.date, sender, msg.is_reply, msg.forward != None, msg.text])

    # Create a DataFrame from the message data
    df = pd.DataFrame(message_data, columns=["date", "sender", "is_reply", "forward", "message"])

    # Replace \n
    df['message'] = df['message'].str.replace('\n', '|', regex=False)
    print(df)

    # Export to CSV
    df.to_csv(csv_file, index=False)