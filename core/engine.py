import subprocess, os, libtorrent as lt
from datetime import datetime

class DownloadEngine:
    def __init__(self, settings):
        self.settings = settings
        self.ffmpeg = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")

    def is_night_mode(self):
        now = datetime.now().hour
        start, end = self.settings['night_start'], self.settings['night_end']
        return start <= now < end

    def download_hls(self, url, name, headers):
        h_str = "".join([f"{k}: {v}\r\n" for k, v in headers.items()])
        output = os.path.join(self.settings['download_path'], f"{name}.mp4")
        
        limit = self.settings['night_limit'] if self.is_night_mode() else ""
        
        cmd = [self.ffmpeg, '-headers', h_str, '-i', url, '-c', 'copy', '-y', output]
        return subprocess.Popen(cmd, creationflags=0x08000000)

    def download_torrent(self, magnet):
        ses = lt.session({'listen_interfaces': '0.0.0.0:6881', 'enable_dht': False}) # Gizli mod
        params = {'save_path': self.settings['download_path'], 'url': magnet}
        handle = ses.add_torrent(params)
        return handle
