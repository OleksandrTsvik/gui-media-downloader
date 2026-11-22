from PySide6.QtWidgets import QLabel

from .base_page import BasePage


class InstagramPage(BasePage):
    def __init__(self):
        super().__init__()

        self.content_layout.addWidget(QLabel("InstagramPage"))
