from pathlib import Path
import time


class FileHendler:
    def __init__(self, dir: str):
        self.dir = Path(dir)

    def write(self, img_bytes: bytes, image_format: str) -> str:
        ts = str(int(time.time()))
        file_name = f"{ts}.{image_format}"
        file_path = self.dir / file_name
        file_path.write_bytes(img_bytes)
        return file_name

    def mayby_cleanupup(self, max_age_sec=1800):
        now = time.time()
        for file in self.dir.glob("*.*"):
            try:
                ts = int(file.stem)
                if now - ts > max_age_sec:
                    file.unlink()
            except ValueError:
                pass
 