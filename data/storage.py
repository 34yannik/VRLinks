import json
import os
from typing import List, Optional
from data.models import Collection, Link


DATA_FILE = os.path.join(os.environ.get("APPDATA"), "VRLinks", "data.json")


class Storage:
    def __init__(self):
        self.collections: List[Collection] = []
        self.load()

    def load(self):
        if not os.path.exists(DATA_FILE):
            self.collections = []
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.collections = [Collection.from_dict(c) for c in data.get("collections", [])]
        except Exception:
            self.collections = []

    def save(self):
        data = {"collections": [c.to_dict() for c in self.collections]}
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_collection(self, name: str) -> Collection:
        c = Collection(name=name)
        self.collections.append(c)
        self.save()
        return c

    def delete_collection(self, col_id: str):
        self.collections = [c for c in self.collections if c.id != col_id]
        self.save()

    def rename_collection(self, col_id: str, new_name: str):
        for c in self.collections:
            if c.id == col_id:
                c.name = new_name
        self.save()

    def get_collection(self, col_id: str) -> Optional[Collection]:
        for c in self.collections:
            if c.id == col_id:
                return c
        return None

    def add_link(self, col_id: str, name: str, url: str) -> Optional[Link]:
        col = self.get_collection(col_id)
        if col is None:
            return None
        link = Link(name=name, url=url)
        col.links.append(link)
        self.save()
        return link

    def delete_link(self, col_id: str, link_id: str):
        col = self.get_collection(col_id)
        if col:
            col.links = [l for l in col.links if l.id != link_id]
            self.save()

    def edit_link(self, col_id: str, link_id: str, name: str, url: str):
        col = self.get_collection(col_id)
        if col:
            for l in col.links:
                if l.id == link_id:
                    l.name = name
                    l.url = url
            self.save()