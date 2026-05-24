
import os, json, uuid

class ApprovalQueue:
    def __init__(self, path="approval_queue.json"):
        self.path = path
    def _load(self):
        if not os.path.exists(self.path):
            return []
        try:
            return json.load(open(self.path, "r", encoding="utf-8"))
        except Exception:
            return []
    def _save(self, rows):
        json.dump(rows, open(self.path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    def add(self, item):
        rows = self._load()
        item.setdefault("id", str(uuid.uuid4())[:8])
        rows.insert(0, item)
        self._save(rows)
        return item
    def list(self):
        return self._load()
