import os, zipfile, requests, sys

class DependencyManager:
    def __init__(self):
        self.bin_path = os.path.join(os.getcwd(), "bin")
        self.ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

    def setup(self):
        if not os.path.exists(self.bin_path): os.makedirs(self.bin_path)
        ffmpeg_exe = os.path.join(self.bin_path, "ffmpeg.exe")
        if not os.path.exists(ffmpeg_exe):
            self._download_and_extract()
        return ffmpeg_exe

    def _download_and_extract(self):
        zip_path = os.path.join(self.bin_path, "ffmpeg.zip")
        r = requests.get(self.ffmpeg_url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(8192): f.write(chunk)
        with zipfile.ZipFile(zip_path, 'r') as z:
            for file in z.namelist():
                if file.endswith("ffmpeg.exe"):
                    data = z.read(file)
                    with open(os.path.join(self.bin_path, "ffmpeg.exe"), "wb") as f: f.write(data)
        os.remove(zip_path)
