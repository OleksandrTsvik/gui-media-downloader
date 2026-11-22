from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class BasePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 0, 0, 0)
        self.main_layout.setSpacing(16)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Content widget
        self.content = QWidget()
        self.content.setObjectName("content")
        self.content.setContentsMargins(0, 24, 24, 24)

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)
        self.content_layout.setSizeConstraints(
            QVBoxLayout.SizeConstraint.SetDefaultConstraint, QVBoxLayout.SizeConstraint.SetFixedSize
        )

        self.scroll_area.setWidget(self.content)

        self.main_layout.addWidget(self.scroll_area)
