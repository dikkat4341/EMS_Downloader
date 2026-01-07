import customtkinter as ctk
import os, json, random, subprocess, sys
from datetime import datetime

# --- KRİTİK DOSYA SİSTEMİ YÖNETİCİSİ ---
class FileSystem:
    @staticmethod
    def ensure_structure():
        # Gerekli klasörleri oluştur
        for folder in ["config", "bin", "Downloads"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        # User Agents dosyasını kontrol et ve yoksa oluştur
        ua_path = os.path.join("config", "user_agents.json")
        if not os.path.exists(ua_path):
            default_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (SMART-TV; Linux; WebOS) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0"
            ]
            with open(ua_path, "w", encoding="utf-8") as f:
                json.dump(default_agents, f)
        return ua_path

# --- GİZLİLİK MOTORU ---
class StealthEngine:
    def __init__(self, ua_path):
        with open(ua_path, "r", encoding="utf-8") as f:
            self.agents = json.load(f)
    
    def get_headers(self):
        return {
            "User-Agent": random.choice(self.agents),
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "Connection": "keep-alive"
        }

# --- ANA UYGULAMA ---
class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Professional Stealth")
        self.geometry("1100x700")
        
        # 1. Önce dosya sistemini hazırla (Hata almamak için)
        ua_path = FileSystem.ensure_structure()
        
        # 2. Motorları başlat
        self.stealth = StealthEngine(ua_path)
        
        # 3. Arayüzü kur
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        ctk.CTkButton(self.sidebar, text="📥 İndirme Kuyruğu", command=self.show_queue).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream / XUI", command=self.show_xtream).pack(pady=10, padx=20)
        
        self.mode_lbl = ctk.CTkLabel(self.sidebar, text="MOD: GÜNDÜZ", text_color="green")
        self.mode_lbl.pack(side="bottom", pady=20)

        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_queue()

    def show_queue(self):
        self._clear()
        ctk.CTkLabel(self.container, text="Aktif Kuyruk", font=("Arial", 22, "bold")).pack(pady=10)
        self.scroll = ctk.CTkScrollableFrame(self.container, label_text="Dosya Durumu")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Örnek satır (Arayüz testi için)
        row = ctk.CTkFrame(self.scroll)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text="Kanal_Kaydi_Test.mp4").pack(side="left", padx=10)
        ctk.CTkProgressBar(row, width=200).pack(side="right", padx=10)

    def show_xtream(self):
        self._clear()
        ctk.CTkLabel(self.container, text="Xtream Codes Girişi", font=("Arial", 22, "bold")).pack(pady=20)
        self.e_url = ctk.CTkEntry(self.container, placeholder_text="Server URL", width=400)
        self.e_url.pack(pady=10)
        self.e_user = ctk.CTkEntry(self.container, placeholder_text="User", width=400)
        self.e_user.pack(pady=5)
        self.e_pass = ctk.CTkEntry(self.container, placeholder_text="Pass", show="*", width=400)
        self.e_pass.pack(pady=5)
        ctk.CTkButton(self.container, text="Bağlan", fg_color="green").pack(pady=20)

    def _clear(self):
        for w in self.container.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
