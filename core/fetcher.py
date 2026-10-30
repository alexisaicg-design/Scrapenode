import httpx
import time
import random
from typing import Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class BaseFetcher:
    def __init__(self, retries: int = 3, delay: float = 2.0, timeout: float = 10.0):
        self.retries = retries
        self.delay = delay
        self.timeout = timeout

    def fetch(self, url: str) -> Optional[str]:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        for attempt in range(1, self.retries + 1):
            try:
                with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                    response = client.get(url, headers=headers)
                    response.raise_for_status()
                    return response.text
            except httpx.HTTPError as e:
                if attempt == self.retries:
                    print(f"[ERROR] Fallo definitivo en {url}: {e}")
                    return None
                time.sleep(self.delay * attempt)
        return None
        