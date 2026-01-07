import random

class StealthEngine:
    def __init__(self):
        self.agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) Safari/605.1.15",
            "Mozilla/5.0 (SMART-TV; Linux; WebOS) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0"
        ]

    def get_headers(self):
        return {
            "User-Agent": random.choice(self.agents),
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "DNT": "1"
        }
