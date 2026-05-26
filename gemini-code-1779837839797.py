import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    return "Dashboard OK", 200

@app.route('/api/upload/status')
def upload_status():
    return jsonify({"success": True}), 200

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

# TASK 3 & 4: Ο ΜΟΝΑΔΙΚΟΣ ενεργός μηχανισμός startup - Χωρίς background threads ή υποδιεργασίες
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False  # Κρίσιμο: Το debug=False εμποδίζει το Flask από το να σπawnάρει δεύτερο κρυφό process
    )