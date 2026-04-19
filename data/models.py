from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class Link:
    name: str
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "url": self.url}

    @staticmethod
    def from_dict(d):
        return Link(id=d.get("id", str(uuid.uuid4())), name=d["name"], url=d["url"])

    def is_youtube(self) -> bool:
        return "youtube.com/watch" in self.url or "youtu.be/" in self.url or "youtube.com/shorts" in self.url

    def youtube_id(self) -> Optional[str]:
        import re
        patterns = [
            r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
            r"youtu\.be/([a-zA-Z0-9_-]{11})",
        ]
        for p in patterns:
            m = re.search(p, self.url)
            if m:
                return m.group(1)
        return None


@dataclass
class Collection:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    links: list = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "links": [l.to_dict() for l in self.links],
        }

    @staticmethod
    def from_dict(d):
        links = [Link.from_dict(l) for l in d.get("links", [])]
        return Collection(id=d.get("id", str(uuid.uuid4())), name=d["name"], links=links)
