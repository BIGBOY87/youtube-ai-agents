\
"""
Paste into app.py, or import/register it manually.

Adds:
GET  /api/upload/status
POST /api/upload/publish
"""

import os
from flask import request, jsonify
from public_publish_agent import PublicPublishAgent

@app.route("/api/upload/status")
def upload_status():
    return jsonify({
        "youtube_upload_enabled": os.getenv("YOUTUBE_UPLOAD_ENABLED", "false").lower() == "true",
        "auto_public_mode": os.getenv("AUTO_PUBLIC_MODE", "false").lower() == "true",
        "auto_approve_uploads": os.getenv("AUTO_APPROVE_UPLOADS", "false").lower() == "true",
        "has_token_env": bool(os.getenv("YOUTUBE_TOKEN_JSON", "").strip()),
        "has_local_token_file": os.path.exists("token.json"),
        "note": "Upload requires MP4 file + OAuth token with youtube.upload scope."
    })

@app.route("/api/upload/publish", methods=["POST"])
def upload_publish():
    project = request.get_json(force=True, silent=True) or {}
    result = PublicPublishAgent().publish(project)
    code = 200 if result.get("status") == "published_or_uploaded" else 400
    return jsonify(result), code
