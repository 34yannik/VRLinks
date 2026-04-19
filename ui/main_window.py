from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QApplication, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication, QPixmap

from data.storage import Storage
from ui.theme import STYLESHEET
from ui.topbar import TopBar
from ui.sidebar import Sidebar
from ui.link_area import LinkArea
from ui.dialogs import (
    AddCollectionDialog, EditCollectionDialog, DeleteCollectionDialog,
    AddLinkDialog, EditLinkDialog, DeleteLinkDialog, SettingsDialog
)
from utils.thumbnail import ThumbnailFetcher


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VR Links")
        self.resize(1100, 700)
        self.setMinimumSize(780, 500)

        self._storage = Storage()
        self._active_col_id = None
        self._thumbnail_cache: dict[str, QPixmap] = {}
        self._fetcher = ThumbnailFetcher(self)
        self._fetcher.thumbnail_ready.connect(self._on_thumbnail)

        self.setStyleSheet(STYLESHEET)
        self._build_ui()
        self._load_collections()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # top bar
        self._topbar = TopBar()
        self._topbar.add_collection_clicked.connect(self._add_collection)
        self._topbar.add_link_clicked.connect(self._add_link)
        self._topbar.settings_clicked.connect(self._open_settings)
        self._topbar.search_changed.connect(self._on_search)
        root.addWidget(self._topbar)

        # main area
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._sidebar.collection_selected.connect(self._select_collection)
        self._sidebar.add_collection_requested.connect(self._add_collection)
        self._sidebar.edit_collection_requested.connect(self._edit_collection)
        self._sidebar.delete_collection_requested.connect(self._delete_collection)
        body_layout.addWidget(self._sidebar)

        self._link_area = LinkArea()
        self._link_area.copy_link.connect(self._copy_link)
        self._link_area.edit_link.connect(self._edit_link)
        self._link_area.delete_link.connect(self._delete_link)
        body_layout.addWidget(self._link_area, 1)

        root.addWidget(body, 1)

    def _load_collections(self):
        self._sidebar.load_collections(self._storage.collections)
        # auto-select first
        if self._storage.collections:
            first = self._storage.collections[0]
            self._sidebar.select(first.id)
            self._select_collection(first.id)

    # -- Collection actions --

    def _add_collection(self):
        dlg = AddCollectionDialog(self)
        dlg.exec()
        if dlg.result_name:
            col = self._storage.add_collection(dlg.result_name)
            self._sidebar.add_collection(col.id, col.name, 0)
            self._sidebar.select(col.id)
            self._select_collection(col.id)

    def _edit_collection(self, col_id: str):
        col = self._storage.get_collection(col_id)
        if not col:
            return
        dlg = EditCollectionDialog(col.name, self)
        dlg.exec()
        if dlg.result_name:
            self._storage.rename_collection(col_id, dlg.result_name)
            self._sidebar.update_collection(col_id, dlg.result_name, len(col.links))
            if self._active_col_id == col_id:
                self._link_area._col_label.setText(dlg.result_name.upper())

    def _delete_collection(self, col_id: str):
        col = self._storage.get_collection(col_id)
        if not col:
            return
        dlg = DeleteCollectionDialog(col.name, self)
        if dlg.exec():
            self._storage.delete_collection(col_id)
            self._sidebar.remove_collection(col_id)
            if self._active_col_id == col_id:
                self._active_col_id = None
                self._link_area._show_no_collection()
                self._link_area._col_label.setText("Select a Collection")
                self._link_area._count_label.setText("")
                # auto select next
                if self._storage.collections:
                    nxt = self._storage.collections[0]
                    self._sidebar.select(nxt.id)
                    self._select_collection(nxt.id)

    def _select_collection(self, col_id: str):
        self._active_col_id = col_id
        col = self._storage.get_collection(col_id)
        if not col:
            return
        self._link_area.set_collection(col.name, col.links, self._thumbnail_cache)
        # kick off thumbnail fetches
        for link in col.links:
            if link.is_youtube():
                vid_id = link.youtube_id()
                if vid_id and vid_id not in self._thumbnail_cache:
                    self._fetcher.fetch(vid_id)

    # -- Link actions --

    def _add_link(self):
        if not self._active_col_id:
            # no collection selected — silently open add collection first
            self._add_collection()
            return
        dlg = AddLinkDialog(self)
        dlg.exec()
        if dlg.result_name and dlg.result_url:
            link = self._storage.add_link(self._active_col_id, dlg.result_name, dlg.result_url)
            if link:
                self._link_area.add_card(link, self._thumbnail_cache)
                self._update_sidebar_count()
                if link.is_youtube():
                    vid_id = link.youtube_id()
                    if vid_id and vid_id not in self._thumbnail_cache:
                        self._fetcher.fetch(vid_id)

    def _edit_link(self, link_id: str):
        col = self._storage.get_collection(self._active_col_id)
        if not col:
            return
        link = next((l for l in col.links if l.id == link_id), None)
        if not link:
            return
        dlg = EditLinkDialog(link.name, link.url, self)
        dlg.exec()
        if dlg.result_name and dlg.result_url:
            self._storage.edit_link(self._active_col_id, link_id, dlg.result_name, dlg.result_url)
            link.name = dlg.result_name
            link.url = dlg.result_url
            self._link_area.update_card(link)

    def _delete_link(self, link_id: str):
        col = self._storage.get_collection(self._active_col_id)
        if not col:
            return
        link = next((l for l in col.links if l.id == link_id), None)
        if not link:
            return
        dlg = DeleteLinkDialog(link.name, self)
        if dlg.exec():
            self._storage.delete_link(self._active_col_id, link_id)
            self._link_area.remove_card(link_id)
            self._update_sidebar_count()

    def _copy_link(self, name: str, url: str):
        QGuiApplication.clipboard().setText(url)

    def _on_search(self, text: str):
        self._link_area.apply_search(text)

    def _open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def _on_thumbnail(self, video_id: str, pixmap: QPixmap):
        self._thumbnail_cache[video_id] = pixmap
        self._link_area.set_thumbnail_for_video(video_id, pixmap)

    def _update_sidebar_count(self):
        if self._active_col_id:
            col = self._storage.get_collection(self._active_col_id)
            if col:
                self._sidebar.update_collection(self._active_col_id, col.name, len(col.links))
