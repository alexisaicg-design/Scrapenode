import httpx

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_alert(self, message: str) -> bool:
        if not self.token or not self.chat_id:
            print("[WARN] Token o Chat ID de Telegram no configurados.")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = httpx.post(self.api_url, json=payload, timeout=5.0)
            return res.status_code == 200
        except Exception as e:
            print(f"[ERROR] Fallo al enviar notificación: {e}")
            return False
