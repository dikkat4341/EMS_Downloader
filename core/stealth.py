import random, json, os

class StealthEngine:
    def __init__(self):
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) Chrome/110.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        ] # Burası 20+ gerçekçi UA ile doldurulacak.

    def get_headers(self):
        return {
            "User-Agent": random.choice(self.ua_list),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Origin": "null"
        }
