# Telegram Keyword Finder

## Task
- Find all messages in selected channels
- Filter messages with keywords list
- Analyse filter effectiveness
- Mark self-posted messages and forwarded messages

## Installation
1. Create a conda environment: `conda env create -f environment.yml`
2. Create a .env file with the following credentials:
```
    API_ID=<your_api_id>
    API_HASH=<your_api_hash>
```

## Usage
- auth_test.py: Authentication test with Telegram API
- message_reader.py: Extract messages from Telegram API into CSV file
- message_filter.py: Filter messages from keywords.txt file
