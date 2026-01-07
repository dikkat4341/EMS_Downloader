import os, zipfile, requests

class DependencyManager:
    def __init__(self):
        self.bin_dir = os.path.join(os.getcwd(), "bin")
        self.ffmpeg_path = os.path.join(self.bin_dir, "ffmpeg.exe")
        # Statik ve güvenilir FFmpeg linki
        self.url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

    def check_and_install(self):
        if not os.path.exists(self.bin_dir):
            os.makedirs(self.bin_dir)
        
        if not os.path.exists(self.ffmpeg_path):
            print("FFmpeg indiriliyor, lütfen bekleyin...")
            r = requests.get(self.url, stream=True)
            zip_tmp = os.path.join(self.bin_dir, "temp.zip")
            with open(zip_tmp, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            
            with zipfile.ZipFile(zip_tmp, 'r') as z:
                for file in z.namelist():
                    if file.endswith("ffmpeg.exe"):
                        with open(self.ffmpeg_path, "wb") as f:
                            f.write(z.read(file))
            os.remove(zip_tmp)
            return True
        return True
