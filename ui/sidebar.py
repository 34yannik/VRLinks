from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient
from ui.theme import *


class CollectionItem(QWidget):
    clicked = Signal(str)      # collection id
    edit_requested = Signal(str)
    delete_requested = Signal(str)

    def __init__(self, col_id: str, name: str, count: int, parent=None):
        super().__init__(parent)
        self.col_id = col_id
        self.name = name
        self.count = count
        self._selected = False
        self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(48)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)

    def set_selected(self, val: bool):
        self._selected = val
        self.update()

    def set_count(self, count: int):
        self.count = count
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.col_id)

    def _show_menu(self, pos):
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        menu.addSeparator()
        del_action = menu.addAction("Delete")
        del_action.setObjectName("deleteAction")
        action = menu.exec(self.mapToGlobal(pos))
        if action == edit_action:
            self.edit_requested.emit(self.col_id)
        elif action == del_action:
            self.delete_requested.emit(self.col_id)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(4, 3, -4, -3)

        if self._selected:
            painter.setBrush(QBrush(QColor(ACCENT_DIM)))
            painter.setPen(QPen(QColor(ACCENT), 1.5))
            painter.drawRoundedRect(rect, 8, 8)
            # left accent bar
            bar = QRect(rect.left(), rect.top() + 8, 3, rect.height() - 16)
            painter.setBrush(QBrush(QColor(ACCENT_BRIGHT)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(bar, 2, 2)
        elif self._hovered:
            painter.setBrush(QBrush(QColor(BG_HOVER)))
            painter.setPen(QPen(QColor(BORDER), 1))
            painter.drawRoundedRect(rect, 8, 8)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

        # name text
        text_color = QColor(TEXT_PRIMARY) if self._selected else (QColor(TEXT_PRIMARY) if self._hovered else QColor(TEXT_SECONDARY))
        painter.setPen(QPen(text_color))
        font = QFont("Segoe UI", 11)
        font.setWeight(QFont.Weight.Medium if self._selected else QFont.Weight.Normal)
        painter.setFont(font)
        text_rect = rect.adjusted(14, 0, -40, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.name)

        # count badge
        if self.count > 0:
            count_str = str(self.count)
            badge_font = QFont("Segoe UI", 9)
            badge_font.setWeight(QFont.Weight.Bold)
            painter.setFont(badge_font)
            fm = painter.fontMetrics()
            badge_w = max(22, fm.horizontalAdvance(count_str) + 12)
            badge_rect = QRect(rect.right() - badge_w - 6, rect.center().y() - 10, badge_w, 20)
            badge_bg = QColor(ACCENT) if self._selected else QColor(BORDER_ACCENT)
            painter.setBrush(QBrush(badge_bg))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(badge_rect, 10, 10)
            painter.setPen(QPen(QColor("white")))
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, count_str)

        painter.end()


class Sidebar(QWidget):
    collection_selected = Signal(str)
    add_collection_requested = Signal()
    edit_collection_requested = Signal(str)
    delete_collection_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self._items: dict[str, CollectionItem] = {}
        self._active_id = None
        self._build()

    def _build(self):
        self.setStyleSheet(f"background: {BG_DEEP}; border-right: 1.5px solid {BORDER};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(56)
        header.setStyleSheet(f"background: {BG_DEEP}; border-bottom: 1.5px solid {BORDER};")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(14, 0, 14, 0)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title = QLabel("COLLECTIONS")
        title.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; background: transparent;")
        h_layout.addWidget(title)
        layout.addWidget(header)

        # scroll area for items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        self._list_widget = QWidget()
        self._list_widget.setStyleSheet("background: transparent;")
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setContentsMargins(8, 8, 8, 8)
        self._list_layout.setSpacing(2)
        self._list_layout.addStretch()
        scroll.setWidget(self._list_widget)
        layout.addWidget(scroll, 1)

        # Empty state
        self._empty_label = QLabel("No collections yet.\nClick + to create one.")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px; background: transparent; padding: 20px;")
        self._list_layout.insertWidget(0, self._empty_label)

    def load_collections(self, collections):
        # clear
        for item in list(self._items.values()):
            item.setParent(None)
        self._items.clear()
        self._list_layout.itemAt(0)  # keep empty label at idx 0

        for col in collections:
            self._add_item(col.id, col.name, len(col.links))

        self._empty_label.setVisible(len(collections) == 0)

    def _add_item(self, col_id, name, count):
        item = CollectionItem(col_id, name, count)
        item.clicked.connect(self._on_item_click)
        item.edit_requested.connect(self.edit_collection_requested)
        item.delete_requested.connect(self.delete_collection_requested)
        # insert before stretch
        idx = self._list_layout.count() - 1
        self._list_layout.insertWidget(idx, item)
        self._items[col_id] = item
        if self._empty_label:
            self._empty_label.setVisible(False)

    def add_collection(self, col_id, name, count=0):
        self._add_item(col_id, name, count)

    def update_collection(self, col_id, name, count):
        if col_id in self._items:
            self._items[col_id].name = name
            self._items[col_id].set_count(count)

    def remove_collection(self, col_id):
        if col_id in self._items:
            self._items[col_id].setParent(None)
            del self._items[col_id]
        self._empty_label.setVisible(len(self._items) == 0)

    def select(self, col_id):
        if self._active_id and self._active_id in self._items:
            self._items[self._active_id].set_selected(False)
        self._active_id = col_id
        if col_id in self._items:
            self._items[col_id].set_selected(True)

    def _on_item_click(self, col_id):
        self.select(col_id)
        self.collection_selected.emit(col_id)
