import customtkinter as ctk
from core.dep_manager import DependencyManager
from core.stealth import StealthEngine
from core.engine import DownloadEngine
from utils.config import ConfigManager

class EMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EMS Stream Downloader - Stealth Portable")
        self.geometry("1000x600")
        
        # Init Managers
        self.config = ConfigManager().load()
        DependencyManager().setup()
        self.stealth = StealthEngine()
        self.engine = DownloadEngine(self.config)

        self._build_ui()

    def _build_ui(self):
        # Sidebar - Menü
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkButton(self.sidebar, text="Yeni İndirme").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Xtream UI / M3U").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Geçmiş").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Ayarlar").pack(side="bottom", pady=10)

        # Ana Liste Alanı
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Aktif İndirmeler")
        self.scroll_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # İndirme başlatma, Xtream login vb. fonksiyonlar buraya eklenecek.

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()
