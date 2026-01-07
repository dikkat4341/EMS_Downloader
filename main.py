import customtkinter as ctk
import os
from core.dependency_mgr import DependencyManager
from core.stealth_engine import StealthEngine

class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Professional Stealth")
        self.geometry("1100x650")
        
        # Klasör yapılandırması (Portable)
        for folder in ["Downloads", "config", "bin"]:
            if not os.path.exists(folder): os.makedirs(folder)

        # Başlatıcılar
        DependencyManager().check_and_install()
        self.stealth = StealthEngine()
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="EMS STREAM", font=("Impact", 24)).pack(pady=30)
        
        # Menü Butonları
        ctk.CTkButton(self.sidebar, text="📥 Aktif Kuyruk").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📺 Xtream UI / XUI").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⭐ Favoriler").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="⚙️ Ayarlar (Gece Modu)").pack(side="bottom", pady=20, padx=20)

        # İndirme Listesi (Ana Ekran)
        self.main_view = ctk.CTkScrollableFrame(self, label_text="İndirme Detayları (Dosya Adı | Boyut | Hız | ETA)")
        self.main_view.pack(side="right", fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
