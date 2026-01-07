import customtkinter as ctk
import os, json, random, subprocess, sys, requests, time
from datetime import datetime
from threading import Thread

# --- [MADDE 10 & 11] GÜVENLİK VE GİZLİLİK (STEALTH) MOTORU ---
class StealthEngine:
    def __init__(self):
        self.ua_path = "config/user_agents.json"
        self.default_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (SMART-TV; Linux; WebOS) AppleWebkit/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) Chrome/110.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Safari/605.1"
            # ... 20+ UA buraya eklenir
        ]
        self.prepare()

    def prepare(self):
        if not os.path.exists("config"): os.makedirs("config")
        if not os.path.exists(self.ua_path):
            with open(self.ua_path, "w") as f: json.dump(self.default_agents, f)
        with open(self.ua_path, "r") as f: self.agents = json.load(f)

    def get_headers(self):
        return {
            "User-Agent": random.choice(self.agents),
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "Connection": "keep-alive",
            "DNT": "1"
        }

# --- [MADDE 2, 3, 4, 8, 9] İNDİRME VE PANEL YÖNETİMİ ---
class CoreEngine:
    def __init__(self):
        self.download_path = "Downloads"
        if not os.path.exists(self.download_path): os.makedirs(self.download_path)

    def check_night_mode(self, start=0, end=7):
        return start <= datetime.now().hour < end

    def download_hls(self, url, name, headers, limit=False):
        # [MADDE 4 & 10] m3u8 segment birleştirme ve Stealth indirme
        ffmpeg = os.path.join("bin", "ffmpeg.exe")
        output = os.path.join(self.download_path, f"{name}.mp4")
        h_str = "".join([f"{k}: {v}\r\n" for k, v in headers.items()])
        
        cmd = [ffmpeg, '-headers', h_str, '-i', url, '-c', 'copy', '-y', output]
        if limit: cmd.insert(1, "-re") # Hız sınırlama simülasyonu
        return subprocess.Popen(cmd, creationflags=0x08000000)

# --- [MADDE 5, 6, 12] ANA ARAYÜZ (GUI) ---
class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - FULL VERSION")
        self.geometry("1150x750")
        
        self.stealth = StealthEngine()
        self.core = CoreEngine()
        self.setup_ui()

    def setup_ui(self):
        # Yan Menü
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        # İş Emri Modülleri
        ctk.CTkButton(self.sidebar, text="📥 İndirmeler", command=self.ui_queue).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream / XUI", command=self.ui_xtream).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="🧲 Torrent / Magnet", command=self.ui_torrent).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📡 RSS Takip", command=self.ui_rss).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler", command=self.ui_fav).pack(pady=10, padx=20)
        
        self.status_lbl = ctk.CTkLabel(self.sidebar, text="MOD: GÜNDÜZ", text_color="green")
        self.status_lbl.pack(side="bottom", pady=20)

        # İçerik Alanı
        self.view = ctk.CTkFrame(self, corner_radius=15)
        self.view.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.ui_queue()

    def ui_queue(self):
        self._clear()
        ctk.CTkLabel(self.view, text="Aktif İndirme Kuyruğu [MADDE 5]", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.view)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        # Örnek Satır
        row = ctk.CTkFrame(scroll)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text="Kanal_Kaydı_1080p.mp4", width=250).pack(side="left", padx=10)
        ctk.CTkProgressBar(row, width=300).pack(side="left", padx=10)
        ctk.CTkLabel(row, text="4.5 MB/s").pack(side="left", padx=10)
        ctk.CTkButton(row, text="DURDUR", width=60, fg_color="red").pack(side="right", padx=10)

    def ui_xtream(self):
        self._clear()
        ctk.CTkLabel(self.view, text="Xtream Codes & XUI.ONE Panel Girişi [MADDE 2]", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkEntry(self.view, placeholder_text="Server URL (http://host:port)", width=450).pack(pady=5)
        ctk.CTkEntry(self.view, placeholder_text="Username", width=450).pack(pady=5)
        ctk.CTkEntry(self.view, placeholder_text="Password", show="*", width=450).pack(pady=5)
        ctk.CTkButton(self.view, text="BAĞLAN VE LİSTELE", fg_color="green").pack(pady=20)

    def ui_rss(self):
        self._clear()
        ctk.CTkLabel(self.view, text="RSS Otomatik İndirme [MADDE 11]", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkEntry(self.view, placeholder_text="RSS Feed URL", width=450).pack(pady=5)
        ctk.CTkEntry(self.view, placeholder_text="Filtre Kelimeleri (örn: 1080p, 4K)", width=450).pack(pady=5)
        ctk.CTkButton(self.view, text="RSS İZLEMEYİ BAŞLAT").pack(pady=10)

    def ui_torrent(self):
        self._clear()
        ctk.CTkLabel(self.view, text="Torrent / Magnet İndirme [MADDE 4 & 10]", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkEntry(self.view, placeholder_text="Magnet Link veya Torrent URL", width=500).pack(pady=10)
        ctk.CTkButton(self.view, text="TORRENT EKLE (Stealth Mode)").pack(pady=10)

    def ui_fav(self):
        self._clear()
        ctk.CTkLabel(self.view, text="Favori Yayınlar ve Kayıtlar [MADDE 9]", font=("Arial", 22, "bold")).pack(pady=10)

    def _clear(self):
        for w in self.view.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
