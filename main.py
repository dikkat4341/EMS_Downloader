import customtkinter as ctk
import os, json, random, subprocess, sys, time
from datetime import datetime
from threading import Thread

# --- [MADDE 7 & 11] GİZLİLİK VE USER-AGENT YÖNETİMİ ---
class StealthEngine:
    def __init__(self):
        self.ua_file = "config/user_agents.json"
        self.default_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 14; BRAVIA 4K) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Version/17.2 Mobile/15E148 Safari/604.1"
        ] # Normalde 20+ adet olacak
        self._load_agents()

    def _load_agents(self):
        if not os.path.exists(self.ua_file):
            with open(self.ua_file, "w") as f: json.dump(self.default_agents, f)
        with open(self.ua_file, "r") as f: self.agents = json.load(f)

    def get_random_headers(self):
        return {
            "User-Agent": random.choice(self.agents),
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "DNT": "1" # Do Not Track
        }

# --- [MADDE 2 & 10] XTREAM VE PLAYLIST MOTORU ---
class XtreamHandler:
    def __init__(self, host, user, password):
        self.base_url = host
        self.params = {"username": user, "password": password}

    def get_data(self, action="get_live_categories"):
        import requests
        url = f"{self.base_url}/player_api.php"
        try:
            resp = requests.get(url, params={**self.params, "action": action}, timeout=7)
            return resp.json()
        except: return []

# --- [MADDE 4 & 9] İNDİRME VE GECE MODU YÖNETİMİ ---
class DownloadManager:
    def __init__(self, settings):
        self.settings = settings
        self.ffmpeg = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")

    def is_night_mode(self):
        now = datetime.now().hour
        s, e = self.settings.get("night_start", 0), self.settings.get("night_end", 7)
        return s <= now < e

    def start_hls(self, url, filename, headers):
        # [MADDE 11] Stealth m3u8 indirme
        h_str = "".join([f"{k}: {v}\r\n" for k, v in headers.items()])
        output = os.path.join(self.settings.get("path", "Downloads"), f"{filename}.mp4")
        
        cmd = [self.ffmpeg, '-headers', h_str, '-i', url, '-c', 'copy', '-y', output]
        if self.is_night_mode():
            cmd.insert(1, "-re") # Gerçek zamanlı hız sınırlama simülasyonu
        
        return subprocess.Popen(cmd, creationflags=0x08000000)

# --- [MADDE 6 & 12] ANA ARAYÜZ (GUI) ---
class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - v1.0 Final")
        self.geometry("1150x750")
        
        self.settings = {"night_start": 0, "night_end": 7, "path": "Downloads"}
        self.stealth = StealthEngine()
        self._init_folders()
        self.setup_ui()

    def _init_folders(self):
        for d in ["Downloads", "config", "bin"]:
            if not os.path.exists(d): os.makedirs(d)

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        # [MADDE 12] Menü Yapısı
        ctk.CTkButton(self.sidebar, text="📥 İndirmeler", command=self.ui_queue).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream/XUI", command=self.ui_xtream).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📡 RSS Takip", command=self.ui_rss).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler").pack(pady=10, padx=20)
        
        # [MADDE 4] Gece Modu Göstergesi
        self.mode_lbl = ctk.CTkLabel(self.sidebar, text="MOD: GÜNDÜZ", text_color="green")
        self.mode_lbl.pack(side="bottom", pady=20)

        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.ui_queue()

    def ui_queue(self):
        self._clear()
        ctk.CTkLabel(self.container, text="Aktif İndirme Kuyruğu", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.container)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        # [MADDE 6] Satır Detayları: Ad, Hız, Progress, Kontroller
        self._add_row(scroll, "Örnek_Yayın_01.ts", "4.2 MB/s", 0.65)

    def _add_row(self, master, name, speed, progress):
        row = ctk.CTkFrame(master)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=name, width=200).pack(side="left", padx=10)
        pb = ctk.CTkProgressBar(row, width=300)
        pb.set(progress)
        pb.pack(side="left", padx=10)
        ctk.CTkLabel(row, text=speed).pack(side="left", padx=10)
        ctk.CTkButton(row, text="Durdur", width=60, fg_color="orange").pack(side="right", padx=5)

    def ui_xtream(self):
        self._clear()
        # [MADDE 2] Xtream/XUI Giriş Formu
        ctk.CTkLabel(self.container, text="Xtream UI / XUI.ONE Paneli", font=("Arial", 22, "bold")).pack(pady=10)
        self.e_url = ctk.CTkEntry(self.container, placeholder_text="Server URL", width=400)
        self.e_url.pack(pady=5)
        self.e_user = ctk.CTkEntry(self.container, placeholder_text="Username", width=400)
        self.e_user.pack(pady=5)
        self.e_pass = ctk.CTkEntry(self.container, placeholder_text="Password", show="*", width=400)
        self.e_pass.pack(pady=5)
        ctk.CTkButton(self.container, text="Bağlan ve Kategorize Et", fg_color="green").pack(pady=15)

    def ui_rss(self):
        self._clear()
        # [MADDE 13] RSS Filtreleme
        ctk.CTkLabel(self.container, text="RSS Otomatik Takip", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkEntry(self.container, placeholder_text="RSS Feed URL", width=400).pack(pady=5)
        ctk.CTkEntry(self.container, placeholder_text="Filtre (örn: 1080p, 4K, Dual)", width=400).pack(pady=5)
        ctk.CTkButton(self.container, text="RSS İzlemeyi Başlat").pack(pady=10)

    def _clear(self):
        for w in self.container.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
