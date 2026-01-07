import subprocess
import os
import time
from datetime import datetime

class DownloadManager:
    def __init__(self, settings):
        self.settings = settings
        self.ffmpeg = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")

    def is_night_mode(self):
        now = datetime.now().hour
        start = self.settings.get("night_start", 0)
        end = self.settings.get("night_end", 7)
        return start <= now < end

    def download_hls(self, url, name, headers):
        output = os.path.join(self.settings.get("download_path", "Downloads"), f"{name}.mp4")
        h_str = "".join([f"{k}: {v}\r\n" for k, v in headers.items()])
        
        # Gece modu hız sınırlama simülasyonu (FFmpeg buffer)
        cmd = [self.ffmpeg, '-headers', h_str, '-i', url, '-c', 'copy', '-y', output]
        
        if self.is_night_mode():
            # Hız sınırı koy (örnek: 500k)
            cmd.insert(1, "-re") 
            
        return subprocess.Popen(cmd, creationflags=0x08000000)
