import customtkinter as ctk
import os, json
from core.dependency_mgr import DependencyManager
from core.stealth_engine import StealthEngine
from core.download_manager import DownloadManager

class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Professional Stealth")
        self.geometry("1100x650")
        
        # Klasörleri hazırla
        for d in ["Downloads", "config", "bin"]:
            if not os.path.exists(d): os.makedirs(d)

        # Servisleri Başlat
        DependencyManager().check_and_install()
        self.stealth = StealthEngine()
        self.settings = self.load_settings()
        
        self.setup_ui()

    def load_settings(self):
        path = "config/settings.json"
        if os.path.exists(path):
            return json.load(open(path))
        return {"night_start": 0, "night_end": 7, "download_path": "Downloads"}

    def setup_ui(self):
        # Sidebar (Görseldeki gibi)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 28)).pack(pady=30)
        
        ctk.CTkButton(self.sidebar, text="📥 Aktif Kuyruk", fg_color="#3498db").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream UI / XUI").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler").pack(pady=10, padx=20)
        
        self.night_label = ctk.CTkLabel(self.sidebar, text="Gece Modu: AKTİF" if DownloadManager(self.settings).is_night_mode() else "Gündüz Modu")
        self.night_label.pack(side="bottom", pady=10)
        
        ctk.CTkButton(self.sidebar, text="⚙️ Ayarlar", fg_color="transparent", border_width=1).pack(side="bottom", pady=20, padx=20)

        # Ana Liste Konteynırı
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="İndirme Detayları (Dosya Adı | Boyut | Hız | ETA)")
        self.scroll_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def add_download_row(self, filename, size):
        # Dinamik satır ekleme fonksiyonu
        row = ctk.CTkFrame(self.scroll_frame)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=f"{filename} | {size} | Bekliyor...").pack(side="left", padx=10)
        ctk.CTkProgressBar(row).pack(side="right", padx=10, fill="x", expand=True)

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
