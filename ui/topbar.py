from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from ui.theme import *


class TopBar(QWidget):
    add_collection_clicked = Signal()
    add_link_clicked = Signal()
    settings_clicked = Signal()
    search_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setStyleSheet(f"""
            background: {BG_DEEP};
            border-bottom: 1.5px solid {BORDER};
        """)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        # App logo / name
        logo = QLabel("VR Links")
        logo.setStyleSheet(f"""
            color: {ACCENT_BRIGHT};
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: transparent;
        """)
        layout.addWidget(logo)

        layout.addSpacing(16)

        # Search bar
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search links...")
        self._search.setFixedHeight(36)
        self._search.setMinimumWidth(200)
        self._search.setMaximumWidth(340)
        self._search.setStyleSheet(f"""
            QLineEdit {{
                background: {BG_SURFACE};
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding: 0 12px;
                color: {TEXT_PRIMARY};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {ACCENT};
                background: {BG_CARD};
            }}
        """)
        self._search.textChanged.connect(self.search_changed)
        layout.addWidget(self._search)

        layout.addStretch()

        # Settings button
        settings_btn = self._make_btn("⚙  Settings", flat=True)
        settings_btn.clicked.connect(self.settings_clicked)
        layout.addWidget(settings_btn)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"background: {BORDER}; color: {BORDER};")
        sep.setFixedHeight(24)
        layout.addWidget(sep)

        # Add Collection
        add_col_btn = self._make_btn("＋ Collection")
        add_col_btn.clicked.connect(self.add_collection_clicked)
        layout.addWidget(add_col_btn)

        # Add Link
        add_link_btn = self._make_btn("＋ Link", accent=True)
        add_link_btn.clicked.connect(self.add_link_clicked)
        layout.addWidget(add_link_btn)

    def _make_btn(self, text: str, accent=False, flat=False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if accent:
            btn.setObjectName("accent")
        elif flat:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    color: {TEXT_SECONDARY};
                    font-size: 13px;
                    padding: 0 12px;
                }}
                QPushButton:hover {{
                    color: {TEXT_PRIMARY};
                    background: {BG_HOVER};
                    border-radius: 8px;
                }}
            """)
        return btn

    def clear_search(self):
        self._search.clear()
