import customtkinter as ctk
import os, json, random, subprocess, sys
from datetime import datetime
from threading import Thread

# --- CORE LOGICS ---

class StealthEngine:
    def __init__(self):
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
    def get_headers(self):
        return {
            "User-Agent": random.choice(self.ua_list),
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "Connection": "keep-alive"
        }

class DependencyManager:
    @staticmethod
    def install_ffmpeg():
        bin_dir = os.path.join(os.getcwd(), "bin")
        if not os.path.exists(bin_dir): os.makedirs(bin_dir)
        ffmpeg_exe = os.path.join(bin_dir, "ffmpeg.exe")
        if not os.path.exists(ffmpeg_exe):
            # Buraya hızlı bir indirme scripti veya kullanıcı uyarısı gelebilir.
            # Şimdilik GitHub Actions'da ffmpeg bağımlılığı aranmaz, exe içine gömülmez, runtime'da çekilir.
            pass

# --- UI LOGIC ---

class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Professional Stealth")
        self.geometry("1100x700")
        
        # Portable Yapı
        self.config_dir = os.path.join(os.getcwd(), "config")
        self.downloads_dir = os.path.join(os.getcwd(), "Downloads")
        for d in [self.config_dir, self.downloads_dir]:
            if not os.path.exists(d): os.makedirs(d)

        self.stealth = StealthEngine()
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        self.btn_queue = ctk.CTkButton(self.sidebar, text="📥 Aktif Kuyruk", command=self.show_queue).pack(pady=10, padx=20)
        self.btn_xtream = ctk.CTkButton(self.sidebar, text="📺 Xtream / XUI", command=self.show_xtream).pack(pady=10, padx=20)
        self.btn_fav = ctk.CTkButton(self.sidebar, text="⭐ Favoriler").pack(pady=10, padx=20)
        
        # Gece Modu Durumu
        self.mode_label = ctk.CTkLabel(self.sidebar, text="Mod: Gündüz (Tam Hız)", text_color="green")
        self.mode_label.pack(side="bottom", pady=20)
        self._check_night_mode()

        # Ana İçerik Alanı
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_queue()

    def _check_night_mode(self):
        hour = datetime.now().hour
        if 0 <= hour <= 7: # Gece 00-07 arası
            self.mode_label.configure(text="Mod: Gece (Hız Sınırlı)", text_color="orange")
        self.after(60000, self._check_night_mode)

    def show_queue(self):
        self._clear_container()
        lbl = ctk.CTkLabel(self.container, text="İndirme Kuyruğu", font=("Arial", 20, "bold"))
        lbl.pack(pady=10)
        
        self.scroll = ctk.CTkScrollableFrame(self.container, label_text="Dosya Adı | Boyut | Hız | Kalan Süre")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Test Verisi (Arayüzün boş kalmaması için)
        self._add_test_row("Örnek_Film_HLS.mp4", "1.2 GB", "5.4 MB/s", "04:20")

    def _add_test_row(self, name, size, speed, eta):
        row = ctk.CTkFrame(self.scroll)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=f"{name} | {size} | {speed} | {eta}").pack(side="left", padx=10)
        ctk.CTkProgressBar(row, width=300).pack(side="right", padx=10)
        ctk.CTkButton(row, text="X", width=30, fg_color="red").pack(side="right", padx=5)

    def show_xtream(self):
        self._clear_container()
        ctk.CTkLabel(self.container, text="Xtream Codes / XUI.ONE Girişi", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.entry_host = ctk.CTkEntry(self.container, placeholder_text="http://url-adresi.com:8080", width=400)
        self.entry_host.pack(pady=5)
        self.entry_user = ctk.CTkEntry(self.container, placeholder_text="Kullanıcı Adı", width=400)
        self.entry_user.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self.container, placeholder_text="Şifre", show="*", width=400)
        self.entry_pass.pack(pady=5)
        
        ctk.CTkButton(self.container, text="Bağlan ve Listele", fg_color="green").pack(pady=20)

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
