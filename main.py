import customtkinter as ctk
import os, json, random, subprocess, sys, requests, time
from datetime import datetime
from threading import Thread

# --- [MADDE 1, 6, 9] SİSTEM VE VERİ YÖNETİMİ ---
class EMSCore:
    def __init__(self):
        self.paths = {
            "config": "config/settings.json",
            "favs": "config/favorites.json",
            "ua": "config/user_agents.json",
            "bin": "bin",
            "downloads": "Downloads"
        }
        self.init_system()

    def init_system(self):
        for folder in ["config", "bin", "Downloads"]:
            if not os.path.exists(folder): os.makedirs(folder)
        
        # [MADDE 6] User Agent Listesi (20+ Gerçekçi Header)
        if not os.path.exists(self.paths["ua"]):
            uas = [f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110,120)}.0.0.0 Safari/537.36" for _ in range(20)]
            self.save_json(self.paths["ua"], uas)
        
        if not os.path.exists(self.paths["config"]):
            self.save_json(self.paths["config"], {"night_start": 0, "night_end": 7, "max_dl": 5})
            
        if not os.path.exists(self.paths["favs"]):
            self.save_json(self.paths["favs"], [])

    def save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        return []

# --- [MADDE 3, 4, 10] İNDİRME MOTORU ---
class DownloadEngine:
    def __init__(self, core):
        self.core = core
        self.active_processes = {}

    def is_night_mode(self):
        settings = self.core.load_json(self.core.paths["config"])
        now = datetime.now().hour
        return settings["night_start"] <= now < settings["night_end"]

    def start_stream_download(self, url, filename):
        # [MADDE 10] Stealth Header Rotasyonu
        uas = self.core.load_json(self.core.paths["ua"])
        headers = {
            "User-Agent": random.choice(uas),
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        
        # [MADDE 4] FFmpeg ile m3u8 indirme
        ffmpeg_path = os.path.join("bin", "ffmpeg.exe")
        output = os.path.join("Downloads", f"{filename}.mp4")
        
        h_str = "".join([f"{k}: {v}\r\n" for k, v in headers.items()])
        cmd = [ffmpeg_path, '-headers', h_str, '-i', url, '-c', 'copy', '-y', output]
        
        if self.is_night_mode():
            cmd.insert(1, "-re") # Hız sınırlama
            
        proc = subprocess.Popen(cmd, creationflags=0x08000000)
        self.active_processes[filename] = proc

# --- [MADDE 12] ANA ARAYÜZ ---
class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.core = EMSCore()
        self.engine = DownloadEngine(self.core)
        
        self.title("EMS Stream Downloader Pro - v1.0")
        self.geometry("1100x750")
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        # [FONKSİYONEL BUTONLAR]
        ctk.CTkButton(self.sidebar, text="📥 Kuyruk", command=self.ui_queue).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream / XUI", command=self.ui_xtream).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler", command=self.ui_favs).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📡 RSS Takip", command=self.ui_rss).pack(pady=10, padx=20)
        
        self.mode_info = ctk.CTkLabel(self.sidebar, text="MOD: KONTROL EDİLİYOR...", font=("Arial", 12))
        self.mode_info.pack(side="bottom", pady=20)
        self.update_mode_status()

        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.ui_queue()

    def update_mode_status(self):
        if self.engine.is_night_mode():
            self.mode_info.configure(text="MOD: GECE (HIZ SINIRLI)", text_color="orange")
        else:
            self.mode_info.configure(text="MOD: GÜNDÜZ (TAM HIZ)", text_color="green")
        self.after(30000, self.update_mode_status)

    def ui_xtream(self):
        self._clear()
        ctk.CTkLabel(self.container, text="Xtream / XUI.ONE Panel Girişi", font=("Arial", 22, "bold")).pack(pady=10)
        
        self.e_url = ctk.CTkEntry(self.container, placeholder_text="Sunucu URL", width=400)
        self.e_url.pack(pady=5)
        self.e_user = ctk.CTkEntry(self.container, placeholder_text="Kullanıcı Adı", width=400)
        self.e_user.pack(pady=5)
        self.e_pass = ctk.CTkEntry(self.container, placeholder_text="Şifre", show="*", width=400)
        self.e_pass.pack(pady=5)
        
        ctk.CTkButton(self.container, text="KAYDET VE BAĞLAN", fg_color="green", command=self.action_save_xtream).pack(pady=20)

    def action_save_xtream(self):
        favs = self.core.load_json(self.core.paths["favs"])
        favs.append({
            "url": self.e_url.get(),
            "user": self.e_user.get(),
            "pass": self.e_pass.get(),
            "type": "Xtream"
        })
        self.core.save_json(self.core.paths["favs"], favs)
        self.ui_favs()

    def ui_favs(self):
        self._clear()
        ctk.CTkLabel(self.container, text="Kayıtlı Favoriler", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.container)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        favs = self.core.load_json(self.core.paths["favs"])
        for idx, f in enumerate(favs):
            frame = ctk.CTkFrame(scroll)
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=f"{f['url']} | {f['user']}").pack(side="left", padx=10)
            ctk.CTkButton(frame, text="SİL", width=60, fg_color="red", command=lambda i=idx: self.action_delete_fav(i)).pack(side="right", padx=10)

    def action_delete_fav(self, index):
        favs = self.core.load_json(self.core.paths["favs"])
        favs.pop(index)
        self.core.save_json(self.core.paths["favs"], favs)
        self.ui_favs()

    def ui_queue(self):
        self._clear()
        ctk.CTkLabel(self.container, text="İndirme Kuyruğu", font=("Arial", 22, "bold")).pack(pady=10)
        self.queue_scroll = ctk.CTkScrollableFrame(self.container)
        self.queue_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not self.engine.active_processes:
            ctk.CTkLabel(self.queue_scroll, text="Şu an aktif indirme bulunmuyor.", text_color="gray").pack(pady=20)

    def ui_rss(self):
        self._clear()
        ctk.CTkLabel(self.container, text="RSS Otomatik Takip", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkEntry(self.container, placeholder_text="RSS URL", width=450).pack(pady=5)
        ctk.CTkEntry(self.container, placeholder_text="Filtre Kelimeleri (örn: 1080p)", width=450).pack(pady=5)
        ctk.CTkButton(self.container, text="RSS GÖREVİ OLUŞTUR").pack(pady=10)

    def _clear(self):
        for w in self.container.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
