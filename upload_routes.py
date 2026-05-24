import os
from flask import jsonify, request

def register_upload_routes(app):

    @app.route("/api/upload/status")
    def upload_status():
        return jsonify({
            "upload_routes": "active",
            "youtube_upload_enabled": os.getenv("YOUTUBE_UPLOAD_ENABLED", "false").lower() == "true",
            "auto_public_mode": os.getenv("AUTO_PUBLIC_MODE", "false").lower() == "true",
            "auto_approve_uploads": os.getenv("AUTO_APPROVE_UPLOADS", "false").lower() == "true",
            "has_token_env": bool(os.getenv("YOUTUBE_TOKEN_JSON", "").strip()),
            "has_local_token_file": os.path.exists("token.json"),
            "public_actions": "blocked until MP4 + OAuth token + explicit auto approval are configured",
            "message": "Upload routes registered successfully. This status endpoint is safe."
        })

    @app.route("/api/upload/publish", methods=["POST"])
    def upload_publish():
        data = request.get_json(silent=True) or {}
        if os.getenv("AUTO_APPROVE_UPLOADS", "false").lower() != "true":
            return jsonify({"status":"needs_approval","reason":"AUTO_APPROVE_UPLOADS is false. Keeping upload blocked for safety.","received_project":data}), 400
        if not os.getenv("YOUTUBE_TOKEN_JSON", "").strip() and not os.path.exists("token.json"):
            return jsonify({"status":"blocked","reason":"Missing OAuth token. Set YOUTUBE_TOKEN_JSON or token.json."}), 400
        if not data.get("video_file"):
            return jsonify({"status":"needs_video_file","reason":"No MP4 video_file provided."}), 400
        return jsonify({"status":"ready_for_real_upload_layer","note":"Safety checks passed at route level. Actual videos.insert implementation should be enabled only after private test upload."})
