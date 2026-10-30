import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    FETCH_RETRIES = int(os.getenv("FETCH_RETRIES", "3"))
    FETCH_DELAY = float(os.getenv("FETCH_DELAY", "2.0"))
    