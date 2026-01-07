import requests

class XtreamHandler:
    def __init__(self, host, user, password):
        self.base_url = host
        self.creds = {"username": user, "password": password}

    def get_categories(self, type="live"):
        # type: live, vids, series
        url = f"{self.base_url}/player_api.php"
        params = {**self.creds, "action": f"get_{type}_categories"}
        try:
            return requests.get(url, params=params, timeout=10).json()
        except: return []

    def get_streams(self, cat_id, type="live"):
        url = f"{self.base_url}/player_api.php"
        params = {**self.creds, "action": f"get_{type}_streams", "category_id": cat_id}
        try:
            return requests.get(url, params=params, timeout=10).json()
        except: return []
