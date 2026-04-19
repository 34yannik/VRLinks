from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel,
    QGridLayout, QFrame, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from ui.link_card import LinkCard
from ui.theme import *


class EmptyState(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel("🔗")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px; background: transparent;")
        layout.addWidget(icon)

        title = QLabel("No links here yet")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 15px; font-weight: 600; background: transparent;")
        layout.addWidget(title)

        sub = QLabel("Click '+ Link' to add your first link to this collection.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px; background: transparent;")
        layout.addWidget(sub)


class NoCollectionState(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel("⬡")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(f"font-size: 52px; color: {ACCENT_DIM}; background: transparent;")
        layout.addWidget(icon)

        title = QLabel("VR Links")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont("Segoe UI", 20)
        f.setWeight(QFont.Weight.Bold)
        title.setFont(f)
        title.setStyleSheet(f"color: {TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(title)

        sub = QLabel("Select a collection on the left,\nor create a new one to get started.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color: {TEXT_DIM}; font-size: 13px; background: transparent;")
        sub.setWordWrap(True)
        layout.addWidget(sub)


class LinkArea(QWidget):
    copy_link = Signal(str, str)
    edit_link = Signal(str)
    delete_link = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards: dict[str, LinkCard] = {}
        self._search_text = ""
        self._build()

    def _build(self):
        self.setStyleSheet(f"background: {BG_BASE};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header bar
        self._header = QWidget()
        self._header.setFixedHeight(52)
        self._header.setStyleSheet(f"background: {BG_DEEP}; border-bottom: 1.5px solid {BORDER};")
        h_layout = QHBoxLayout(self._header)
        h_layout.setContentsMargins(24, 0, 24, 0)
        self._col_label = QLabel("Select a Collection")
        self._col_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px; font-weight: 600; background: transparent; letter-spacing: 0.5px;")
        self._count_label = QLabel("")
        self._count_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; background: transparent;")
        h_layout.addWidget(self._col_label)
        h_layout.addSpacing(12)
        h_layout.addWidget(self._count_label)
        h_layout.addStretch()
        layout.addWidget(self._header)

        # stacked area
        self._stack = QWidget()
        self._stack.setStyleSheet("background: transparent;")
        stack_layout = QVBoxLayout(self._stack)
        stack_layout.setContentsMargins(0, 0, 0, 0)

        # No collection state
        self._no_col = NoCollectionState()
        stack_layout.addWidget(self._no_col)

        # Scroll area for cards
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("background: transparent; border: none;")

        self._cards_container = QWidget()
        self._cards_container.setStyleSheet("background: transparent;")
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(24, 20, 24, 20)
        self._cards_layout.setSpacing(8)
        self._cards_layout.addStretch()

        self._empty_state = EmptyState()
        self._scroll.setWidget(self._cards_container)
        self._scroll.setVisible(False)

        stack_layout.addWidget(self._scroll)
        layout.addWidget(self._stack, 1)

        self._show_no_collection()

    def _show_no_collection(self):
        self._no_col.setVisible(True)
        self._scroll.setVisible(False)

    def _show_collection(self):
        self._no_col.setVisible(False)
        self._scroll.setVisible(True)

    def set_collection(self, col_name: str, links: list, thumbnail_cache: dict):
        self._show_collection()
        self._col_label.setText(col_name.upper())

        # clear cards
        for card in list(self._cards.values()):
            card.setParent(None)
        self._cards.clear()

        # remove empty state if present
        idx = self._cards_layout.indexOf(self._empty_state)
        if idx >= 0:
            self._cards_layout.removeWidget(self._empty_state)
            self._empty_state.setParent(None)

        for link in links:
            self._insert_card(link, thumbnail_cache)

        self._update_empty_state()
        self._update_count()
        self.apply_search(self._search_text)

    def _insert_card(self, link, thumbnail_cache):
        card = LinkCard(link.id, link.name, link.url)
        card.copy_requested.connect(self.copy_link)
        card.edit_requested.connect(self.edit_link)
        card.delete_requested.connect(self.delete_link)
        # insert before stretch
        idx = self._cards_layout.count() - 1
        self._cards_layout.insertWidget(idx, card)
        self._cards[link.id] = card

        # apply cached thumbnail
        if link.is_youtube():
            vid_id = link.youtube_id()
            if vid_id and vid_id in thumbnail_cache:
                card.set_thumbnail(thumbnail_cache[vid_id])

    def add_card(self, link, thumbnail_cache):
        self._insert_card(link, thumbnail_cache)
        self._update_empty_state()
        self._update_count()
        self.apply_search(self._search_text)

    def remove_card(self, link_id: str):
        if link_id in self._cards:
            self._cards[link_id].setParent(None)
            del self._cards[link_id]
        self._update_empty_state()
        self._update_count()

    def update_card(self, link):
        if link.id in self._cards:
            card = self._cards[link.id]
            card.link_name = link.name
            card.link_url = link.url
            card.update()

    def set_thumbnail_for_video(self, video_id: str, pixmap):
        for card in self._cards.values():
            from data.models import Link as L
            l = L(name=card.link_name, url=card.link_url, id=card.link_id)
            if l.youtube_id() == video_id:
                card.set_thumbnail(pixmap)

    def _update_empty_state(self):
        if len(self._cards) == 0:
            idx = self._cards_layout.indexOf(self._empty_state)
            if idx < 0:
                self._cards_layout.insertWidget(0, self._empty_state)
                self._empty_state.setParent(self._cards_container)
            self._empty_state.setVisible(True)
        else:
            self._empty_state.setVisible(False)

    def _update_count(self):
        n = len(self._cards)
        self._count_label.setText(f"{n} link{'s' if n != 1 else ''}")

    def apply_search(self, text: str):
        self._search_text = text.lower()
        for card in self._cards.values():
            match = (
                self._search_text in card.link_name.lower() or
                self._search_text in card.link_url.lower()
            )
            card.setVisible(match)
