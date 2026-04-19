from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.theme import *


def _make_dialog(parent, title: str) -> QDialog:
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setModal(True)
    dlg.setMinimumWidth(420)
    dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
    dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    return dlg


def _wrap_in_frame(dlg: QDialog) -> tuple:
    """Returns (outer_layout, inner_layout, frame)"""
    outer = QVBoxLayout(dlg)
    outer.setContentsMargins(0, 0, 0, 0)
    frame = QFrame()
    frame.setObjectName("dialogFrame")
    frame.setStyleSheet(f"""
        QFrame#dialogFrame {{
            background: {BG_SURFACE};
            border: 1.5px solid {BORDER_ACCENT};
            border-radius: 14px;
        }}
    """)
    inner = QVBoxLayout(frame)
    inner.setContentsMargins(28, 24, 28, 24)
    inner.setSpacing(14)
    outer.addWidget(frame)
    return outer, inner, frame


def _title_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(15)
    f.setWeight(QFont.Weight.Bold)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; background: transparent;")
    return lbl


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; background: transparent; font-weight: 500; letter-spacing: 0.5px;")
    return lbl


def _divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
    return line


def _button_row(ok_text, ok_id, cancel_cb, ok_cb) -> tuple:
    row = QHBoxLayout()
    row.setSpacing(10)
    cancel_btn = QPushButton("Cancel")
    cancel_btn.setFixedHeight(38)
    cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    ok_btn = QPushButton(ok_text)
    ok_btn.setObjectName(ok_id)
    ok_btn.setFixedHeight(38)
    ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    cancel_btn.clicked.connect(cancel_cb)
    ok_btn.clicked.connect(ok_cb)
    row.addStretch()
    row.addWidget(cancel_btn)
    row.addWidget(ok_btn)
    return row, ok_btn, cancel_btn


class AddCollectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Collection")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.result_name = None
        self._build()

    def _build(self):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("New Collection"))
        inner.addWidget(_divider())
        inner.addWidget(_field_label("COLLECTION NAME"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("e.g. Favorite Worlds")
        self._name_input.setFixedHeight(40)
        inner.addWidget(self._name_input)
        row, ok_btn, _ = _button_row("Create", "accent", self.reject, self._accept)
        inner.addLayout(row)
        self._name_input.returnPressed.connect(self._accept)

    def _accept(self):
        name = self._name_input.text().strip()
        if name:
            self.result_name = name
            self.accept()


class EditCollectionDialog(QDialog):
    def __init__(self, current_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Collection")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.result_name = None
        self._current = current_name
        self._build()

    def _build(self):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Edit Collection"))
        inner.addWidget(_divider())
        inner.addWidget(_field_label("COLLECTION NAME"))
        self._name_input = QLineEdit(self._current)
        self._name_input.setFixedHeight(40)
        inner.addWidget(self._name_input)
        row, _, _ = _button_row("Save", "accent", self.reject, self._accept)
        inner.addLayout(row)
        self._name_input.returnPressed.connect(self._accept)

    def _accept(self):
        name = self._name_input.text().strip()
        if name:
            self.result_name = name
            self.accept()


class DeleteCollectionDialog(QDialog):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Collection")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build(name)

    def _build(self, name: str):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Delete Collection"))
        inner.addWidget(_divider())
        msg = QLabel(f'Are you sure you want to delete\n<b>"{name}"</b> and all its links?')
        msg.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; font-size: 13px;")
        msg.setWordWrap(True)
        inner.addWidget(msg)
        row = QHBoxLayout()
        row.setSpacing(10)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("danger")
        del_btn.setFixedHeight(38)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        del_btn.clicked.connect(self.accept)
        row.addStretch()
        row.addWidget(cancel_btn)
        row.addWidget(del_btn)
        inner.addLayout(row)


class AddLinkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Link")
        self.setModal(True)
        self.setMinimumWidth(440)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.result_name = None
        self.result_url = None
        self._build()

    def _build(self):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Add Link"))
        inner.addWidget(_divider())
        inner.addWidget(_field_label("LINK NAME"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("e.g. Cozy Lounge World")
        self._name_input.setFixedHeight(40)
        inner.addWidget(self._name_input)
        inner.addWidget(_field_label("URL"))
        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText("https://vrchat.com/home/world/...")
        self._url_input.setFixedHeight(40)
        inner.addWidget(self._url_input)
        row, _, _ = _button_row("Add Link", "accent", self.reject, self._accept)
        inner.addLayout(row)
        self._url_input.returnPressed.connect(self._accept)

    def _accept(self):
        name = self._name_input.text().strip()
        url = self._url_input.text().strip()
        if name and url:
            self.result_name = name
            self.result_url = url
            self.accept()


class EditLinkDialog(QDialog):
    def __init__(self, current_name: str, current_url: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Link")
        self.setModal(True)
        self.setMinimumWidth(440)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.result_name = None
        self.result_url = None
        self._cn = current_name
        self._cu = current_url
        self._build()

    def _build(self):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Edit Link"))
        inner.addWidget(_divider())
        inner.addWidget(_field_label("LINK NAME"))
        self._name_input = QLineEdit(self._cn)
        self._name_input.setFixedHeight(40)
        inner.addWidget(self._name_input)
        inner.addWidget(_field_label("URL"))
        self._url_input = QLineEdit(self._cu)
        self._url_input.setFixedHeight(40)
        inner.addWidget(self._url_input)
        row, _, _ = _button_row("Save", "accent", self.reject, self._accept)
        inner.addLayout(row)
        self._url_input.returnPressed.connect(self._accept)

    def _accept(self):
        name = self._name_input.text().strip()
        url = self._url_input.text().strip()
        if name and url:
            self.result_name = name
            self.result_url = url
            self.accept()


class DeleteLinkDialog(QDialog):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Link")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build(name)

    def _build(self, name: str):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Delete Link"))
        inner.addWidget(_divider())
        msg = QLabel(f'Delete <b>"{name}"</b>?')
        msg.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; font-size: 13px;")
        msg.setWordWrap(True)
        inner.addWidget(msg)
        row = QHBoxLayout()
        row.setSpacing(10)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("danger")
        del_btn.setFixedHeight(38)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        del_btn.clicked.connect(self.accept)
        row.addStretch()
        row.addWidget(cancel_btn)
        row.addWidget(del_btn)
        inner.addLayout(row)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(420)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build()

    def _build(self):
        _, inner, _ = _wrap_in_frame(self)
        inner.addWidget(_title_label("Settings"))
        inner.addWidget(_divider())

        info = QLabel("VR Links — Quick link manager for VRChat\nVersion 1.0.0")
        info.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent; font-size: 12px; line-height: 1.6;")
        inner.addWidget(info)

        storage_container = QHBoxLayout()

        storage_lbl = QLabel(f"Data file: %APPDATA%/VRLinks/vr_links_data.json")
        storage_lbl.setStyleSheet(
            f"color: {TEXT_DIM}; background: transparent; font-size: 11px; font-family: monospace;")

        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.setFixedHeight(32)
        open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        import os
        import subprocess

        def open_folder():
            folder = os.path.join(os.environ.get("APPDATA"), "VRLinks")
            os.makedirs(folder, exist_ok=True)
            subprocess.Popen(f'explorer "{folder}"')

        open_folder_btn.clicked.connect(open_folder)

        storage_container.addWidget(storage_lbl)
        storage_container.addStretch()
        storage_container.addWidget(open_folder_btn)

        inner.addLayout(storage_container)

        inner.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        row = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(38)
        close_btn.setObjectName("accent")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        row.addStretch()
        row.addWidget(close_btn)
        inner.addLayout(row)