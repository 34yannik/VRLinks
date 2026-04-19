from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtGui import QPixmap


class ThumbnailFetcher(QObject):
    """Async thumbnail loader for YouTube videos."""
    thumbnail_ready = Signal(str, QPixmap)  # video_id, pixmap

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._pending = {}

    def fetch(self, video_id: str):
        if video_id in self._pending:
            return
        url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        req = QNetworkRequest(QUrl(url))
        reply = self._manager.get(req)
        self._pending[video_id] = reply
        reply.finished.connect(lambda r=reply, vid=video_id: self._on_done(vid, r))

    def _on_done(self, video_id: str, reply: QNetworkReply):
        self._pending.pop(video_id, None)
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            px = QPixmap()
            px.loadFromData(data)
            if not px.isNull():
                self.thumbnail_ready.emit(video_id, px)
        reply.deleteLater()
