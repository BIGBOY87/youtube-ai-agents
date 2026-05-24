from flask import jsonify

def register_upload_routes(app):

    @app.route("/api/upload/status")
    def upload_status():
        return jsonify({
            "upload_engine": "active",
            "oauth": "enabled",
            "autonomous_mode": True,
            "public_actions": False,
            "message": "Upload routes registered successfully"
        })
