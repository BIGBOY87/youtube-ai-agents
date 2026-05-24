
import os
from flask import jsonify, request
from youtube_uploader import upload_video

def register_upload_routes(app):
    @app.route("/api/upload/status")
    def upload_status():
        return jsonify({
            "upload_routes":"active",
            "youtube_upload_enabled":os.getenv("YOUTUBE_UPLOAD_ENABLED","false").lower()=="true",
            "auto_public_mode":os.getenv("AUTO_PUBLIC_MODE","false").lower()=="true",
            "auto_approve_uploads":os.getenv("AUTO_APPROVE_UPLOADS","false").lower()=="true",
            "auto_generate_mp4":os.getenv("AUTO_GENERATE_MP4","false").lower()=="true",
            "has_token_env":bool(os.getenv("YOUTUBE_TOKEN_JSON","").strip()),
            "has_local_token_file":os.path.exists("token.json"),
            "message":"Real upload available when MP4 and OAuth token exist."
        })
    @app.route("/api/upload/publish", methods=["POST"])
    def upload_publish():
        data=request.get_json(silent=True) or {}
        if os.getenv("YOUTUBE_UPLOAD_ENABLED","false").lower()!="true": return jsonify({"status":"blocked","reason":"YOUTUBE_UPLOAD_ENABLED false"}),400
        if os.getenv("AUTO_PUBLIC_MODE","false").lower()!="true": return jsonify({"status":"blocked","reason":"AUTO_PUBLIC_MODE false"}),400
        if os.getenv("AUTO_APPROVE_UPLOADS","false").lower()!="true": return jsonify({"status":"needs_approval","reason":"AUTO_APPROVE_UPLOADS false"}),400
        if data.get("own_content_confirmed") is not True: return jsonify({"status":"blocked","reason":"own_content_confirmed required"}),400
        try:
            return jsonify(upload_video(data["video_file"],data.get("title","BANG IT UP MUSIC Upload"),data.get("description",""),data.get("tags",[]),str(data.get("category_id","10")),data.get("privacy_status",os.getenv("DEFAULT_UPLOAD_PRIVACY","private")),data.get("publish_at")))
        except Exception as e:
            return jsonify({"status":"upload_failed","error":str(e)}),500
