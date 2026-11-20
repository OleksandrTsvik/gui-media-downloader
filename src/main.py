import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    base_dir = Path(__file__).resolve().parent
    qss_path = base_dir / "ui" / "style.qss"
    qss = qss_path.read_text(encoding="utf-8")

    app.setStyleSheet(qss)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
