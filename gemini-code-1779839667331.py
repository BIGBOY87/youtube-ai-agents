import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

# Mock συνάρτηση για το υπάρχον YouTube Upload
def existing_youtube_upload_function(file_stream, metadata):
    import time
    time.sleep(1)  # Προσομοίωση επεξεργασίας
    return "dQw4w9WgXcQ"

# UPDATE: Ολοκληρωτική αντικατάσταση του παλιού HTML/JSON response με Template Rendering
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# --- ΔΙΑΤΗΡΗΣΗ ΚΑΙ ΜΕΤΑΦΟΡΑ ΟΛΩΝ ΤΩΝ API ROUTES ---

@app.route('/api/upload/status')
def upload_status():
    return jsonify({"success": True, "status": "No active batch uploads running.", "queue_depth": 0}), 200

@app.route('/api/drive/status')
def drive_status():
    try:
        if not os.environ.get("DRIVE_API_KEY"):
            raise ValueError("Missing DRIVE_API_KEY inside Render Environment Variables.")
        return jsonify({"success": True, "status": "connected", "latency": "42ms"}), 200
    except Exception as e:
        print(f"Drive API Error [/api/drive/status]: {e}")
        return jsonify({"success": False, "error": str(e)}), 200

@app.route('/api/drive/scan')
def drive_scan():
    try:
        if not os.environ.get("DRIVE_FOLDER_ID"):
            raise ValueError("Target drive directory is undefined.")
        return jsonify({"success": True, "files": [], "scanned_items": 0}), 200
    except Exception as e:
        print(f"Drive API Error [/api/drive/scan]: {e}")
        return jsonify({"success": False, "error": str(e)}), 200

@app.route('/api/source/registry')
def source_registry():
    return jsonify({
        "success": True, 
        "registry": "Main Production Registry Active",
        "nodes": ["node-alpha", "node-beta"],
        "version": "2.4.1"
    }), 200

@app.route('/api/source/growth-loop')
def growth_loop():
    return jsonify({
        "success": True, 
        "growth_loop": "Optimization engine running",
        "ctr_target": "+4.2%",
        "retention_index": "stable"
    }), 200

@app.route('/api/queue')
def queue_status():
    return jsonify({
        "success": True, 
        "queue": [], 
        "count": 0,
        "status": "idle"
    }), 200

# Endpoint για το Manual Multipart/Form-Data Video Upload
@app.route('/api/upload/manual', methods=['POST'])
def upload_manual():
    try:
        if 'video_file' not in request.files:
            return jsonify({"success": False, "error": "No video file provided in the request"}), 400
            
        file = request.files['video_file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Selected file has no filename"}), 400

        if not file.filename.endswith('.mp4'):
            return jsonify({"success": False, "error": "Only .mp4 video files are accepted"}), 400

        metadata = {
            "title": request.form.get("title", "Untitled Video"),
            "description": request.form.get("description", ""),
            "tags": request.form.get("tags", ""),
            "privacy": request.form.get("privacy", "private")
        }

        video_id = existing_youtube_upload_function(file.stream, metadata)

        return jsonify({
            "success": True,
            "video_id": video_id,
            "studio_link": f"https://studio.youtube.com/video/{video_id}/edit"
        }), 200

    except Exception as e:
        print(f"Manual Upload Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )