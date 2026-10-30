import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get_secret(key: str, default: str = None) -> str:
        # 1. Intenta leer desde st.secrets (Streamlit Cloud)
        try:
            import streamlit as st
            if key in st.secrets:
                return str(st.secrets[key])
        except Exception:
            pass
        
        # 2. Si falla o es entorno local, lee desde os.getenv / .env
        return os.getenv(key, default)

    TELEGRAM_BOT_TOKEN = get_secret("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = get_secret("TELEGRAM_CHAT_ID")