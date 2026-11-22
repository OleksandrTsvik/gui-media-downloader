from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from config import QIcons
from models import NavItem


class Sidebar(QFrame):
    page_changed = Signal(int)
    buttons: list[QPushButton]

    EXPANDED_WIDTH = 220
    COLLAPSED_WIDTH = 48

    def __init__(self, navigation_items: list[NavItem], is_collapsed: bool = False, parent=None):
        super().__init__(parent)

        self.navigation_items = navigation_items
        self.is_collapsed = is_collapsed

        self.buttons = []

        self._init_widget()
        self._init_animation()
        self._init_ui()

    def _init_widget(self):
        self.setObjectName("sidebar")

        self.setMinimumWidth(0)
        self.setMaximumWidth(self.EXPANDED_WIDTH)

    def _init_animation(self):
        self.animation = QPropertyAnimation(self, b"maximumWidth", self)
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = self.create_header()
        layout.addWidget(header)

        for index, nav_item in enumerate(self.navigation_items):
            button = self.create_navigation_button(nav_item, index)

            layout.addWidget(button)
            self.buttons.append(button)

        layout.addStretch()

        self.set_active_page(0)

    def create_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("sidebar__header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

        # Toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName("sidebar__toggle-button")
        self.toggle_button.setIconSize(QSize(18, 18))
        self.toggle_button.setFixedSize(32, 32)

        self.update_toggle_icon()

        self.toggle_button.clicked.connect(self.toggle_sidebar)

        layout.addWidget(self.toggle_button)

        # Title
        title = QLabel("Media Downloader")
        title.setObjectName("sidebar__title")

        layout.addWidget(title)

        return header

    def create_navigation_button(self, nav_item: NavItem, index: int) -> QPushButton:
        button = QPushButton(nav_item.title)
        button.setObjectName("sidebar__nav-button")

        button.setIcon(nav_item.qicon)
        button.setIconSize(QSize(20, 20))

        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        button.clicked.connect(lambda checked=False, i=index: self._on_click(i))

        return button

    def _on_click(self, index: int):
        self.set_active_page(index)
        self.page_changed.emit(index)

    def set_active_page(self, index: int):
        for i, button in enumerate(self.buttons):
            button.setChecked(i == index)

    def toggle_sidebar(self):
        self.is_collapsed = not self.is_collapsed

        start_width = self.width()
        end_width = self.COLLAPSED_WIDTH if self.is_collapsed else self.EXPANDED_WIDTH

        self.animation.stop()

        # Animate sidebar width
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.start()

        # Update toggle icon
        self.update_toggle_icon()

    def update_toggle_icon(self):
        self.toggle_button.setIcon(QIcons.SIDEBAR_COLLAPSE if self.is_collapsed else QIcons.SIDEBAR_EXPAND)
