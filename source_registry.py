
import os, json, uuid, datetime

REGISTRY_FILE = "source_registry.json"

def _load():
    if not os.path.exists(REGISTRY_FILE):
        return []
    try:
        return json.load(open(REGISTRY_FILE, "r", encoding="utf-8"))
    except Exception:
        return []

def _save(rows):
    json.dump(rows, open(REGISTRY_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def add_source_record(source_mp4_url, youtube_video_id, youtube_url, title, privacy_status="private", extra=None):
    rows = _load()
    record = {
        "id": str(uuid.uuid4())[:8],
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "source_mp4_url": source_mp4_url,
        "youtube_video_id": youtube_video_id,
        "youtube_url": youtube_url,
        "title": title,
        "privacy_status": privacy_status,
        "status": "source_registered",
        "shorts_created": [],
        "growth_actions": [],
        "extra": extra or {}
    }
    rows.insert(0, record)
    _save(rows)
    return record

def list_sources():
    return _load()

def find_by_video_id(video_id):
    for row in _load():
        if row.get("youtube_video_id") == video_id:
            return row
    return None

def update_record(video_id, updates):
    rows = _load()
    for row in rows:
        if row.get("youtube_video_id") == video_id:
            row.update(updates)
            row["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            _save(rows)
            return row
    return None

def append_growth_action(video_id, action):
    rows = _load()
    for row in rows:
        if row.get("youtube_video_id") == video_id:
            row.setdefault("growth_actions", []).insert(0, {
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                **action
            })
            row["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            _save(rows)
            return row
    return None

def append_short(video_id, short_info):
    rows = _load()
    for row in rows:
        if row.get("youtube_video_id") == video_id:
            row.setdefault("shorts_created", []).insert(0, {
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                **short_info
            })
            row["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            _save(rows)
            return row
    return None
