import sys

from PySide6.QtWidgets import QApplication

from navigation import NAVIGATION_ITEMS
from ui import MainWindow
from utils import get_stylesheet


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(get_stylesheet())

    window = MainWindow(NAVIGATION_ITEMS)
    window.show()

    sys.exit(app.exec())
