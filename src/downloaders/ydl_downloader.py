import os
import threading
from typing import Literal

import yt_dlp
from PySide6.QtCore import QThread, Signal


class YdlDownloader(QThread):
    qualities_ready = Signal(object, str)
    progress_changed = Signal(float, str, str)
    status_changed = Signal(str)
    download_complete = Signal(str)
    error_occurred = Signal(str)
    cancelled = Signal()

    def __init__(
        self,
        url: str,
        mode: Literal["info", "download"],
        output_dir: str = "",
        quality: str = "best",
    ):
        super().__init__()

        self.url = url
        self.mode = mode
        self.output_dir = output_dir
        self.quality = quality
        self.cancel_event = threading.Event()

    def run(self) -> None:
        try:
            match self.mode:
                case "info":
                    self.get_video_info()
                case "download":
                    self.download_video()
        except yt_dlp.utils.DownloadCancelled:
            self.cancelled.emit()
        except Exception as e:
            if self.cancel_event.is_set():
                self.cancelled.emit()
            else:
                self.error_occurred.emit(str(e))

    def cancel(self) -> None:
        self.cancel_event.set()

    def get_video_info(self) -> None:
        self.status_changed.emit("Отримання інформації про відео...")

        options = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(self.url, download=False)

        if self.cancel_event.is_set():
            self.cancelled.emit()
            return

        title = info.get("title") or info.get("fulltitle") or "Unknown video"

        heights = {
            format.get("height")
            for format in info.get("formats", [])
            if format.get("height") and format.get("vcodec") != "none"
        }

        qualities = ["best"] + [str(height) for height in sorted(heights, reverse=True)]

        self.qualities_ready.emit(qualities, title)
        self.status_changed.emit("Інформацію про відео отримано.")

    def download_video(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

        format_selector = self.get_format_selector()

        options = {
            "format": format_selector,
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self.progress_hook],
        }

        self.status_changed.emit("Початок завантаження...")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([self.url])

        if self.cancel_event.is_set():
            self.cancelled.emit()
            return

        self.download_complete.emit(self.output_dir)

    def get_format_selector(self) -> str:
        if self.quality == "best":
            return "bestvideo+bestaudio/best"

        height = int(self.quality)

        return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

    def progress_hook(self, data: dict) -> None:
        if self.cancel_event.is_set():
            raise yt_dlp.utils.DownloadCancelled("Download cancelled by user.")

        status = data.get("status")

        match status:
            case "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate")
                downloaded = data.get("downloaded_bytes", 0)

                speed = data.get("speed")
                eta = data.get("eta")

                percent = downloaded / total * 100 if total else 0
                speed_text = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "Calculating..."
                eta_text = f"{eta} сек." if eta is not None else "Calculating..."

                self.progress_changed.emit(percent, speed_text, eta_text)
            case "finished":
                self.status_changed.emit("Обробка відео та об'єднання аудіо...")
