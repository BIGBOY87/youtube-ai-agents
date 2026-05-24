
import os, tempfile, requests
from flask import jsonify, request
from youtube_uploader import upload_video

MAX_MB = int(os.getenv("MAX_UPLOAD_SOURCE_MB", "250"))

def _safe_upload_allowed():
    if os.getenv("YOUTUBE_UPLOAD_ENABLED", "false").lower() != "true": return False, "YOUTUBE_UPLOAD_ENABLED is false."
    if os.getenv("AUTO_PUBLIC_MODE", "false").lower() != "true": return False, "AUTO_PUBLIC_MODE is false."
    if os.getenv("AUTO_APPROVE_UPLOADS", "false").lower() != "true": return False, "AUTO_APPROVE_UPLOADS is false."
    if not os.getenv("YOUTUBE_TOKEN_JSON", "").strip() and not os.path.exists("token.json"): return False, "Missing OAuth token."
    return True, "ok"

def _download_mp4(url):
    fd, path = tempfile.mkstemp(suffix=".mp4"); os.close(fd); size = 0
    with requests.get(url, stream=True, timeout=90) as r:
        r.raise_for_status()
        if "text/html" in r.headers.get("content-type", "").lower():
            raise ValueError("URL returned HTML, not MP4.")
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if not chunk: continue
                size += len(chunk)
                if size > MAX_MB*1024*1024: raise ValueError(f"File too large. Limit {MAX_MB} MB.")
                f.write(chunk)
    return path

def register_upload_routes(app):
    @app.route("/api/upload/status")
    def upload_status():
        return jsonify({"upload_routes": "active", "mode": "v16-scheduler", "youtube_upload_enabled": os.getenv("YOUTUBE_UPLOAD_ENABLED","false").lower()=="true", "auto_public_mode": os.getenv("AUTO_PUBLIC_MODE","false").lower()=="true", "auto_approve_uploads": os.getenv("AUTO_APPROVE_UPLOADS","false").lower()=="true", "has_token_env": bool(os.getenv("YOUTUBE_TOKEN_JSON","").strip())})

    @app.route("/api/shorts/upload-from-url", methods=["POST"])
    @app.route("/api/upload/from-url", methods=["POST"])
    def upload_from_url():
        data = request.get_json(silent=True) or {}
        allowed, reason = _safe_upload_allowed()
        if not allowed: return jsonify({"status": "blocked", "reason": reason}), 400
        if data.get("own_content_confirmed") is not True: return jsonify({"status": "blocked", "reason": "own_content_confirmed must be true."}), 400
        url = data.get("short_mp4_url") or data.get("video_url")
        if not url: return jsonify({"status": "blocked", "reason": "Missing short_mp4_url or video_url."}), 400
        path = None
        try:
            path = _download_mp4(url)
            result = upload_video(path, data.get("title","BANG IT UP MUSIC Short #Shorts"), data.get("description","BANG IT UP MUSIC"), data.get("tags",["BANGITUPMUSIC","Shorts"]), data.get("category_id","10"), data.get("privacy_status", os.getenv("DEFAULT_UPLOAD_PRIVACY","private")), data.get("publish_at"))
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "upload_failed", "error": str(e)}), 500
        finally:
            if path and os.path.exists(path):
                try: os.remove(path)
                except Exception: pass
