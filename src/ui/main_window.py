from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractButton, QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from models import NavItem

from .widgets import Sidebar


class MainWindow(QMainWindow):
    def __init__(self, navigation_items: list[NavItem]):
        super().__init__()

        self.navigation_items = navigation_items

        self._init_window()
        self._init_ui()

    def _init_window(self):
        self.setWindowIcon(QIcon("src/ui/resources/icons/app.ico"))
        self.setWindowTitle("Media Downloader")
        self.setMinimumSize(800, 670)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = Sidebar(self.navigation_items)
        layout.addWidget(sidebar)

        # Pages
        pages = QStackedWidget()

        for nav_item in self.navigation_items:
            pages.addWidget(nav_item.page())

        layout.addWidget(pages)

        # Navigation
        sidebar.page_changed.connect(pages.setCurrentIndex)

        # Cursor pointer
        for button in self.findChildren(QAbstractButton):
            button.setCursor(Qt.CursorShape.PointingHandCursor)
