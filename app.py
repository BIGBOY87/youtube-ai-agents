import os
import json
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
STARTED_AT = datetime.now(timezone.utc).isoformat()

@app.get('/')
def index():
    return render_template_string('''
    <html><head><title>YouTube AI Agents</title></head>
    <body style="font-family:Arial;background:#111;color:#eee;padding:40px">
      <h1>🚀 YouTube AI Agents System</h1>
      <p>Status: <b style="color:#0f0">Running</b></p>
      <p>Channel ID: {{ channel_id or 'not configured' }}</p>
      <p><a style="color:#6cf" href="/health">Health check</a></p>
    </body></html>
    ''', channel_id=os.getenv('YOUTUBE_CHANNEL_ID'))

@app.get('/health')
def health():
    required = ['YOUTUBE_API_KEY', 'YOUTUBE_CHANNEL_ID']
    missing = [k for k in required if not os.getenv(k)]
    status = 'ok' if not missing else 'missing_config'
    return jsonify({
        'status': status,
        'started_at': STARTED_AT,
        'missing_required_vars': missing,
        'service': 'youtube-ai-agents',
    }), 200 if not missing else 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
