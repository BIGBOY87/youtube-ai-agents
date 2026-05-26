import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

# Mock συνάρτηση για το υπάρχον YouTube Upload (Αντικαταστήστε με τη δική σας βιβλιοθήκη/λογική)
def existing_youtube_upload_function(file_stream, metadata):
    # Προσομοίωση επιτυχούς μεταφόρτωσης και επιστροφή ενός Mock Video ID
    import time
    time.sleep(1) # Τεχνητή καθυστέρηση για το demo
    return "dQw4w9WgXcQ"

@app.route('/dashboard')
def dashboard():
    # Επιστρέφει το νέο, σύγχρονο template
    return render_template('dashboard.html')

@app.route('/api/upload/status')
def upload_status():
    return jsonify({"success": True, "status": "No active batch uploads running."}), 200

@app.route('/api/drive/status')
def drive_status():
    try:
        if not os.environ.get("DRIVE_API_KEY"):
            raise ValueError("Missing DRIVE_API_KEY inside Render Environment Variables.")
        return jsonify({"success": True, "status": "connected"}), 200
    except Exception as e:
        print(f"Drive API Error [/api/drive/status]: {e}")
        return jsonify({"success": False, "error": str(e)}), 200

@app.route('/api/drive/scan')
def drive_scan():
    try:
        if not os.environ.get("DRIVE_FOLDER_ID"):
            raise ValueError("Target drive directory is undefined.")
        return jsonify({"success": True, "files": []}), 200
    except Exception as e:
        print(f"Drive API Error [/api/drive/scan]: {e}")
        return jsonify({"success": False, "error": str(e)}), 200

# Νέα Endpoints που ζητήθηκαν για τα υπάρχοντα κουμπιά (Mock Responses)
@app.route('/api/registry')
def source_registry():
    return jsonify({"success": True, "registry": "Main Production Registry Active"}), 200

@app.route('/api/growth')
def growth_loop():
    return jsonify({"success": True, "growth_loop": "Optimization engine running"}), 200

@app.route('/api/queue')
def queue_status():
    return jsonify({"success": True, "queue": [], "count": 0}), 200


# TASK 3, 4 & 5: Manual Multipart/Form-Data Video Upload Endpoint
@app.route('/api/upload/manual', methods=['POST'])
def upload_manual():
    try:
        # Έλεγχος αν υπάρχει το αρχείο στο request
        if 'video_file' not in request.files:
            return jsonify({"success": False, "error": "No video file provided in the request"}), 400
            
        file = request.files['video_file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Selected file has no filename"}), 400

        if not file.filename.endswith('.mp4'):
            return jsonify({"success": False, "error": "Only .mp4 video files are accepted"}), 400

        # Ανάγνωση των metadata από τη φόρμα
        metadata = {
            "title": request.form.get("title", "Untitled Video"),
            "description": request.form.get("description", ""),
            "tags": request.form.get("tags", ""),
            "privacy": request.form.get("privacy", "private")
        }

        # Κλήση της υπάρχουσας συνάρτησης YouTube Upload περνώντας το file stream
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