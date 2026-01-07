import customtkinter as ctk
import os, json, random, subprocess, sys
from datetime import datetime
from threading import Thread

# --- GİZLİLİK MOTORU (STEALTH) ---
class StealthEngine:
    def __init__(self):
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 14; BRAVIA 4K NextGen) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
    def get_headers(self):
        return {"User-Agent": random.choice(self.ua_list), "Connection": "keep-alive"}

# --- ANA UYGULAMA ARAYÜZÜ ---
class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Professional Stealth")
        self.geometry("1100x700")
        
        # Klasör Hazırlığı
        for d in ["Downloads", "config", "bin"]:
            if not os.path.exists(d): os.makedirs(d)

        self.stealth = StealthEngine()
        self.setup_ui()

    def setup_ui(self):
        # Yan Menü (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 32)).pack(pady=40)
        
        ctk.CTkButton(self.sidebar, text="📥 İndirme Kuyruğu", command=self.show_queue).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream UI / XUI", command=self.show_xtream).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler").pack(pady=10, padx=20)
        
        self.mode_label = ctk.CTkLabel(self.sidebar, text="Mod: Gündüz", text_color="green")
        self.mode_label.pack(side="bottom", pady=20)

        # Ana Gösterge Alanı
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_queue() # Açılışta kuyruğu göster

    def show_queue(self):
        self._clear_container()
        ctk.CTkLabel(self.container, text="Aktif İndirmeler", font=("Arial", 22, "bold")).pack(pady=10)
        self.scroll = ctk.CTkScrollableFrame(self.container, label_text="Dosya Detayları")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Boş kalmaması için örnek satır
        self._add_row("Örnek_Video_Akışı.m3u8", "Hesaplanıyor", "Beklemede")

    def _add_row(self, name, size, status):
        row = ctk.CTkFrame(self.scroll)
        row.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(row, text=f"{name} | {size}").pack(side="left", padx=10)
        ctk.CTkProgressBar(row, width=200).pack(side="right", padx=10)
        ctk.CTkLabel(row, text=status).pack(side="right", padx=10)

    def show_xtream(self):
        self._clear_container()
        ctk.CTkLabel(self.container, text="Xtream Codes Girişi", font=("Arial", 22, "bold")).pack(pady=20)
        self.entry_url = ctk.CTkEntry(self.container, placeholder_text="Sunucu URL (örn: http://iptv.com:8080)", width=450)
        self.entry_url.pack(pady=10)
        self.entry_user = ctk.CTkEntry(self.container, placeholder_text="Kullanıcı Adı", width=450)
        self.entry_user.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self.container, placeholder_text="Şifre", show="*", width=450)
        self.entry_pass.pack(pady=10)
        ctk.CTkButton(self.container, text="Bağlan ve Yayınları Getir", fg_color="green").pack(pady=20)

    def _clear_container(self):
        for widget in self.container.winfo_children(): widget.destroy()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
