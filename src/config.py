from dataclasses import dataclass
from pathlib import Path

from PySide6.QtGui import QIcon


SRC_DIR = Path(__file__).resolve().parent

RESOURCES_DIR = SRC_DIR / "ui" / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
STYLES_DIR = RESOURCES_DIR / "styles"


@dataclass(frozen=True)
class QIcons:
    SIDEBAR_EXPAND = QIcon(str(ICONS_DIR / "arrow-left-to-line.svg"))
    SIDEBAR_COLLAPSE = QIcon(str(ICONS_DIR / "arrow-right-to-line.svg"))

    YOUTUBE = QIcon(str(ICONS_DIR / "youtube.svg"))
    INSTAGRAM = QIcon(str(ICONS_DIR / "instagram.svg"))
