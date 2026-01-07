import customtkinter as ctk
import os, sys
from core.dependency_mgr import DependencyManager
from core.stealth_engine import StealthEngine

class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Portable v1.0")
        self.geometry("900x550")
        
        # Portable klasör kontrolü
        if not os.path.exists("Downloads"): os.makedirs("Downloads")
        if not os.path.exists("config"): os.makedirs("config")

        # Bağımlılıkları kontrol et
        self.dep_mgr = DependencyManager()
        self.dep_mgr.check_and_install()

        self.stealth = StealthEngine()
        self.setup_ui()

    def setup_ui(self):
        # Sol Menü
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="EMS DOWNLOADER", font=("Impact", 20))
        self.logo.pack(pady=20)

        self.btn_new = ctk.CTkButton(self.sidebar, text="Yeni İndirme")
        self.btn_new.pack(pady=10, px=10)

        # Sağ Liste
        self.main_list = ctk.CTkScrollableFrame(self, label_text="İndirme Kuyruğu")
        self.main_list.pack(side="right", fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
