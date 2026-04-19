from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMenu, QSizePolicy
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSize, QRect, QPoint
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QPixmap,
    QLinearGradient, QPainterPath, QFontMetrics
)
from ui.theme import *


class LinkCard(QWidget):
    copy_requested = Signal(str, str)     # name, url
    edit_requested = Signal(str)          # link_id
    delete_requested = Signal(str)        # link_id

    def __init__(self, link_id: str, name: str, url: str, parent=None):
        super().__init__(parent)
        self.link_id = link_id
        self.link_name = name
        self.link_url = url
        self._hovered = False
        self._pressed = False
        self._thumbnail: QPixmap | None = None
        self._copy_flash = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(80)
        self.setMinimumWidth(200)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)
        self._flash_timer = None

    def set_thumbnail(self, pixmap: QPixmap):
        self._thumbnail = pixmap.scaled(
            120, 68, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.update()

    def set_flash(self):
        """Briefly show copied state."""
        self._copy_flash = True
        self.update()
        from PySide6.QtCore import QTimer
        if self._flash_timer:
            self._flash_timer.stop()
        self._flash_timer = __import__("PySide6.QtCore", fromlist=["QTimer"]).QTimer()
        self._flash_timer.setSingleShot(True)
        self._flash_timer.timeout.connect(self._end_flash)
        self._flash_timer.start(600)

    def _end_flash(self):
        self._copy_flash = False
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self._pressed = False
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self._pressed:
            self._pressed = False
            self.copy_requested.emit(self.link_name, self.link_url)
            self.set_flash()
        self._pressed = False
        self.update()

    def _show_menu(self, pos):
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        menu.addSeparator()
        del_action = menu.addAction("Delete")
        action = menu.exec(self.mapToGlobal(pos))
        if action == edit_action:
            self.edit_requested.emit(self.link_id)
        elif action == del_action:
            self.delete_requested.emit(self.link_id)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(2, 3, -2, -3)

        # background
        if self._copy_flash:
            bg = QColor(ACCENT_DIM)
            border_c = QColor(ACCENT_BRIGHT)
        elif self._pressed:
            bg = QColor(BG_SELECTED)
            border_c = QColor(ACCENT)
        elif self._hovered:
            bg = QColor(BG_HOVER)
            border_c = QColor(BORDER_ACCENT)
        else:
            bg = QColor(BG_CARD)
            border_c = QColor(BORDER)

        path = QPainterPath()
        path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), 10, 10)
        painter.fillPath(path, QBrush(bg))
        painter.setPen(QPen(border_c, 1.5))
        painter.drawPath(path)

        # thumbnail area
        thumb_w = 0
        if self._thumbnail:
            thumb_w = 116
            thumb_rect = QRect(rect.left() + 1, rect.top() + 1, thumb_w, rect.height() - 2)
            thumb_path = QPainterPath()
            thumb_path.addRoundedRect(thumb_rect.x(), thumb_rect.y(), thumb_rect.width(), thumb_rect.height(), 9, 9)
            # clip and draw
            painter.save()
            painter.setClipPath(thumb_path)
            scaled = self._thumbnail
            offset_x = thumb_rect.left() + (thumb_rect.width() - scaled.width()) // 2
            offset_y = thumb_rect.top() + (thumb_rect.height() - scaled.height()) // 2
            painter.drawPixmap(offset_x, offset_y, scaled)
            # right gradient fade
            grad = QLinearGradient(thumb_rect.right() - 20, 0, thumb_rect.right(), 0)
            grad.setColorAt(0, QColor(bg.red(), bg.green(), bg.blue(), 0))
            grad.setColorAt(1, bg)
            painter.fillRect(thumb_rect.right() - 20, thumb_rect.top(), 20, thumb_rect.height(), QBrush(grad))
            painter.restore()

        # text area
        text_x = rect.left() + thumb_w + (16 if thumb_w else 16)
        text_w = rect.width() - thumb_w - 32

        # copy icon top-right
        icon_color = QColor(ACCENT_BRIGHT) if self._hovered or self._copy_flash else QColor(TEXT_DIM)
        painter.setPen(QPen(icon_color, 1.3))
        icon_x = rect.right() - 24
        icon_y = rect.top() + 12
        # draw small copy icon (two overlapping squares)
        painter.drawRoundedRect(icon_x + 3, icon_y, 11, 11, 2, 2)
        painter.drawRoundedRect(icon_x, icon_y + 3, 11, 11, 2, 2)

        if self._copy_flash:
            # "Copied!" overlay
            painter.setPen(QPen(QColor(ACCENT_BRIGHT)))
            f = QFont("Segoe UI", 9)
            f.setWeight(QFont.Weight.Bold)
            painter.setFont(f)
            painter.drawText(rect.adjusted(thumb_w + 16, 0, -30, 0),
                             Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Copied!")
        else:
            # name
            name_font = QFont("Segoe UI", 12)
            name_font.setWeight(QFont.Weight.DemiBold)
            painter.setFont(name_font)
            painter.setPen(QPen(QColor(TEXT_PRIMARY)))
            fm = QFontMetrics(name_font)
            name_text = fm.elidedText(self.link_name, Qt.TextElideMode.ElideRight, text_w - 30)
            name_rect = QRect(text_x, rect.top() + 14, text_w - 28, 22)
            painter.drawText(name_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name_text)

            # url
            url_font = QFont("Segoe UI", 10)
            painter.setFont(url_font)
            painter.setPen(QPen(QColor(TEXT_DIM)))
            fm2 = QFontMetrics(url_font)
            url_text = fm2.elidedText(self.link_url, Qt.TextElideMode.ElideRight, text_w - 30)
            url_rect = QRect(text_x, rect.top() + 38, text_w - 28, 18)
            painter.drawText(url_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, url_text)

        painter.end()
