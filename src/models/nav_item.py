from dataclasses import dataclass

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget


@dataclass(frozen=True)
class NavItem:
    qicon: QIcon
    title: str
    page: QWidget
