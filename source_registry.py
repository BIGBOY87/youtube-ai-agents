
import os, json, uuid, datetime
REGISTRY_FILE="source_registry.json"

def _load():
    if not os.path.exists(REGISTRY_FILE): return []
    try: return json.load(open(REGISTRY_FILE,"r",encoding="utf-8"))
    except Exception: return []

def _save(rows):
    json.dump(rows,open(REGISTRY_FILE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

def list_sources():
    return _load()

def find_by_drive_file_id(fid):
    for r in _load():
        if r.get("drive_file_id")==fid: return r
    return None

def find_by_video_id(video_id):
    for r in _load():
        if r.get("youtube_video_id")==video_id: return r
    return None

def find_by_source_url(url):
    for r in _load():
        if r.get("source_mp4_url")==url: return r
    return None

def add_drive_source_record(item):
    existing=find_by_drive_file_id(item.get("drive_file_id"))
    if existing: return existing, False
    rows=_load()
    rec={
        "id":str(uuid.uuid4())[:8],
        "created_at":datetime.datetime.utcnow().isoformat()+"Z",
        "status":"drive_source_registered",
        "source_type":"google_drive",
        "drive_file_id":item.get("drive_file_id"),
        "source_mp4_url":item.get("source_mp4_url"),
        "title":item.get("title_guess") or item.get("name"),
        "drive_name":item.get("name"),
        "youtube_video_id":None,
        "youtube_url":None,
        "privacy_status":None,
        "shorts_created":[],
        "growth_actions":[],
        "extra":{"drive_item":item}
    }
    rows.insert(0,rec); _save(rows); return rec, True

def add_source_record(source_mp4_url,youtube_video_id,youtube_url,title,privacy_status="private",extra=None):
    rows=_load()
    existing=find_by_source_url(source_mp4_url)
    if existing:
        existing.update({"youtube_video_id":youtube_video_id,"youtube_url":youtube_url,"privacy_status":privacy_status,"status":"source_uploaded_registered","updated_at":datetime.datetime.utcnow().isoformat()+"Z"})
        _save(rows); return existing
    rec={"id":str(uuid.uuid4())[:8],"created_at":datetime.datetime.utcnow().isoformat()+"Z","source_mp4_url":source_mp4_url,"youtube_video_id":youtube_video_id,"youtube_url":youtube_url,"title":title,"privacy_status":privacy_status,"status":"source_uploaded_registered","shorts_created":[],"growth_actions":[],"extra":extra or {}}
    rows.insert(0,rec); _save(rows); return rec

def append_growth_action(video_id, action):
    rows=_load()
    for r in rows:
        if r.get("youtube_video_id")==video_id:
            r.setdefault("growth_actions",[]).insert(0,{"created_at":datetime.datetime.utcnow().isoformat()+"Z",**action})
            r["updated_at"]=datetime.datetime.utcnow().isoformat()+"Z"
            _save(rows); return r
    return None
