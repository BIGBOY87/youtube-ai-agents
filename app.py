
import os
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string

from youtube_client import YouTubeClient
from bangitup_agents import GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent, InitiativeEngine, VideoCreatorAgent, ApprovalQueue
from upload_routes import register_upload_routes

app = Flask(__name__)
yt = YouTubeClient()
queue = ApprovalQueue()
register_upload_routes(app)

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "youtube-ai-agents-v12-upload-ready-mp4-only", "started_at": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/api/channel")
def api_channel():
    try:
        return jsonify(yt.channel())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/videos")
def api_videos():
    try:
        return jsonify(yt.recent_videos(int(request.args.get("max", "12"))))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/report")
def api_report():
    try:
        c = yt.channel()
        v = yt.recent_videos(12)
        return jsonify({
            "growth_report": GrowthAgent().report(c, v),
            "initiatives": InitiativeEngine().decide(c, v),
            "agent_status": {"upload": "active", "mode": "ready-mp4-url-only"}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/seo")
def api_seo():
    return jsonify(SEOAgent().generate(request.args.get("title", "New Track"), request.args.get("genre", "Tech House")))

@app.route("/api/shorts")
def api_shorts():
    return jsonify(ShortsAgent().generate(request.args.get("title", "New Track"), request.args.get("genre", "Tech House")))

@app.route("/api/distribution")
def api_distribution():
    return jsonify(DistributionAgent().posts(request.args.get("title", "New Track"), request.args.get("genre", "Tech House")))

@app.route("/api/calendar")
def api_calendar():
    return jsonify(CalendarAgent().weekly())

@app.route("/api/create-video-project")
def api_create_video_project():
    title = request.args.get("title", "BANG IT UP MUSIC Upload")
    genre = request.args.get("genre", "Tech House")
    project = VideoCreatorAgent().create_project(title, genre)
    queue.add({"type": "ready_mp4_project", "status": "needs_mp4_url", "project": project})
    return jsonify(project)

@app.route("/api/auto-run")
def api_auto_run():
    title = request.args.get("title", "Autonomous BANG IT UP MUSIC Upload")
    genre = request.args.get("genre", "Tech House")
    project = VideoCreatorAgent().create_project(title, genre)
    item = {
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "type": "auto_run",
        "status": "needs_mp4_url",
        "project": project,
        "note": "Render is configured to upload ready MP4 URLs only. Generate MP4 externally, then POST it to /api/upload/from-url."
    }
    queue.add(item)
    return jsonify({"status": "completed", "created_items": [item]})

@app.route("/api/approval-queue")
def api_queue():
    return jsonify(queue.list())

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <h1>BANG IT UP MUSIC AI Agents v12</h1>
    <p>Upload-ready MP4 URL mode. Render does not render videos.</p>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/auto-run')">Auto Run</button>
    <button onclick="go('/api/report')">Report</button>
    <pre id="o">Ready</pre>
    <script>
    async function go(p){
      o.textContent='Loading';
      let r=await fetch(p);
      o.textContent=JSON.stringify(await r.json(),null,2);
    }
    </script>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
