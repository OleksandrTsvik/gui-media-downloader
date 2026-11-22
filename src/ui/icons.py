from dataclasses import dataclass

from PySide6.QtGui import QIcon

from config import ICONS_DIR


def load_icon(filename: str) -> QIcon:
    path = ICONS_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Icon not found: {path}")

    return QIcon(str(path))


@dataclass(frozen=True)
class QIcons:
    SIDEBAR_EXPAND = load_icon("arrow-left-to-line.svg")
    SIDEBAR_COLLAPSE = load_icon("arrow-right-to-line.svg")

    VIDEO = load_icon("video.svg")
    MUSIC = load_icon("music.svg")

    YOUTUBE = load_icon("youtube.svg")
    INSTAGRAM = load_icon("instagram.svg")
    TIKTOK = load_icon("tiktok.svg")
