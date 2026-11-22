from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from downloaders.ydl_downloader import YdlDownloader


class YouTubePage(QWidget):
    def __init__(self):
        super().__init__()

        self._init_state()
        self._init_ui()
        self._init_events()

    def _init_state(self):
        self.downloader = None
        self.video_title = ""
        self.download_dir = str(Path.home() / "Downloads")

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # Application title

        title_label = QLabel("YouTube Downloader")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(title_label)

        # URL section

        url_group = QGroupBox("Відео")
        url_layout = QVBoxLayout(url_group)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Вставте посилання на YouTube...")

        url_layout.addWidget(QLabel("URL відео:"))
        url_layout.addWidget(self.url_input)

        self.video_info_label = QLabel("Інформація про відео відсутня.")
        self.video_info_label.setWordWrap(True)

        url_layout.addWidget(self.video_info_label)

        self.load_button = QPushButton("Отримати інформацію")

        url_layout.addWidget(self.load_button)

        layout.addWidget(url_group)

        # Quality section

        quality_group = QGroupBox("Налаштування завантаження")
        quality_layout = QVBoxLayout(quality_group)

        quality_layout.addWidget(QLabel("Якість відео:"))

        self.quality_combobox = QComboBox()
        self.quality_combobox.addItem("Best quality", "best")
        self.quality_combobox.setEnabled(False)

        quality_layout.addWidget(self.quality_combobox)

        quality_layout.addWidget(QLabel("Папка збереження:"))

        folder_layout = QHBoxLayout()

        self.folder_input = QLineEdit(self.download_dir)
        self.folder_input.setReadOnly(True)

        self.folder_button = QPushButton("Огляд")

        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.folder_button)

        quality_layout.addLayout(folder_layout)

        layout.addWidget(quality_group)

        # Progress section

        progress_group = QGroupBox("Прогрес завантаження")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")

        progress_layout.addWidget(self.progress_bar)

        self.speed_label = QLabel("Швидкість: -")
        self.eta_label = QLabel("Залишилося: -")
        self.status_label = QLabel("Очікування...")

        progress_layout.addWidget(self.speed_label)
        progress_layout.addWidget(self.eta_label)
        progress_layout.addWidget(self.status_label)

        layout.addWidget(progress_group)

        # Action buttons

        buttons_layout = QHBoxLayout()

        self.download_button = QPushButton("Завантажити")
        self.download_button.setEnabled(False)

        self.cancel_button = QPushButton("Скасувати")
        self.cancel_button.setEnabled(False)

        buttons_layout.addWidget(self.download_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

    def _init_events(self):
        self.load_button.clicked.connect(self.load_video_info)
        self.folder_button.clicked.connect(self.select_folder)
        self.download_button.clicked.connect(self.start_download)
        self.cancel_button.clicked.connect(self.cancel_download)

    def load_video_info(self) -> None:
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Помилка", "Введіть посилання на відео.")
            return

        self.set_busy(True)
        self.quality_combobox.clear()
        self.quality_combobox.setEnabled(False)
        self.download_button.setEnabled(False)

        self.progress_bar.setValue(0)
        self.status_label.setText("Отримання інформації...")

        self.downloader = YdlDownloader(url=url, mode="info")

        self.downloader.qualities_ready.connect(self.on_qualities_ready)
        self.downloader.status_changed.connect(self.status_label.setText)
        self.downloader.cancelled.connect(self.on_cancelled)
        self.downloader.error_occurred.connect(self.on_error)
        self.downloader.finished.connect(self.on_worker_finished)

        self.downloader.start()

    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Виберіть папку для збереження", self.download_dir)

        if folder:
            self.download_dir = folder
            self.folder_input.setText(folder)

    def start_download(self) -> None:
        url = self.url_input.text().strip()
        quality = self.quality_combobox.currentData()

        if not url or quality is None:
            return

        self.set_busy(True)

        self.progress_bar.setValue(0)
        self.speed_label.setText("Швидкість: -")
        self.eta_label.setText("Залишилося: -")

        self.status_label.setText("Підготовка до завантаження...")

        self.downloader = YdlDownloader(
            url=url,
            mode="download",
            output_dir=self.download_dir,
            quality=quality,
        )

        self.downloader.progress_changed.connect(self.update_progress)
        self.downloader.status_changed.connect(self.status_label.setText)
        self.downloader.download_complete.connect(self.on_download_complete)
        self.downloader.error_occurred.connect(self.on_error)
        self.downloader.cancelled.connect(self.on_cancelled)
        self.downloader.finished.connect(self.on_worker_finished)

        self.downloader.start()

    def update_progress(self, percent: float, speed: str, eta: str) -> None:
        self.progress_bar.setValue(int(percent))
        self.speed_label.setText(f"Швидкість: {speed}")
        self.eta_label.setText(f"Залишилося: {eta}")

    def cancel_download(self) -> None:
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel()
            self.cancel_button.setEnabled(False)
            self.status_label.setText("Скасування...")

    def set_busy(self, busy: bool) -> None:
        self.load_button.setEnabled(not busy)
        self.download_button.setEnabled(not busy and self.quality_combobox.count() > 0)
        self.cancel_button.setEnabled(busy)

        self.url_input.setEnabled(not busy)
        self.folder_button.setEnabled(not busy)
        self.quality_combobox.setEnabled(not busy and self.quality_combobox.count() > 0)

    def on_qualities_ready(self, qualities: list[str], title: str) -> None:
        self.video_title = title

        self.video_info_label.setText(f"Назва: {title}")
        self.quality_combobox.clear()

        for quality in qualities:
            if quality == "best":
                self.quality_combobox.addItem("Best quality", "best")
            else:
                self.quality_combobox.addItem(f"{quality}p", quality)

        self.quality_combobox.setEnabled(True)
        self.download_button.setEnabled(True)

    def on_download_complete(self, folder: str) -> None:
        self.progress_bar.setValue(100)
        self.status_label.setText("Завантаження успішно завершено!")

        QMessageBox.information(
            self,
            "Готово",
            f"Відео збережено у папці:\n{folder}",
        )

    def on_cancelled(self) -> None:
        self.status_label.setText("Завантаження скасовано.")

    def on_error(self, message: str) -> None:
        self.status_label.setText("Виникла помилка.")
        QMessageBox.critical(self, "Помилка", message)

    def on_worker_finished(self) -> None:
        self.set_busy(False)
        self.downloader = None

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel()
            self.downloader.wait()

        event.accept()
