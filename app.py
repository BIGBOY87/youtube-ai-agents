
import os
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string

from youtube_client import YouTubeClient
from bangitup_agents import (
    GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent,
    InitiativeEngine, VideoCreatorAgent, ApprovalQueue, RepurposeAgent
)
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
    return jsonify({
        "status": "ok",
        "service": "youtube-ai-agents-v13-repurpose-existing-videos",
        "started_at": datetime.datetime.utcnow().isoformat() + "Z"
    })

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

@app.route("/api/video/<video_id>")
def api_video(video_id):
    try:
        rows = yt.videos_by_ids([video_id])
        if not rows:
            return jsonify({"error": "video not found"}), 404
        return jsonify(rows[0])
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
            "agent_status": {
                "upload": "active",
                "repurpose_existing_videos": "active",
                "mode": "ready-mp4-url-only"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/repurpose-existing")
def api_repurpose_existing():
    try:
        max_results = int(request.args.get("max", "10"))
        videos = yt.recent_videos(max_results)
        plan = RepurposeAgent().repurpose_batch(videos)
        queue.add({
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "repurpose_existing_videos",
            "status": "plan_ready",
            "plan": plan
        })
        return jsonify(plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/repurpose-video/<video_id>")
def api_repurpose_video(video_id):
    try:
        rows = yt.videos_by_ids([video_id])
        if not rows:
            return jsonify({"error": "video not found"}), 404
        plan = RepurposeAgent().repurpose_video(rows[0])
        queue.add({
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "repurpose_single_video",
            "status": "plan_ready",
            "plan": plan
        })
        return jsonify(plan)
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
    try:
        videos = yt.recent_videos(10)
        repurpose_plan = RepurposeAgent().repurpose_batch(videos)
        item = {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "auto_run_repurpose",
            "status": "plan_ready",
            "plan": repurpose_plan,
            "note": "Repurpose plans are ready. To produce actual Shorts videos, provide original MP4/direct URLs."
        }
        queue.add(item)
        return jsonify({"status": "completed", "created_items": [item]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/approval-queue")
def api_queue():
    return jsonify(queue.list())

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <h1>BANG IT UP MUSIC AI Agents v13</h1>
    <p>Repurpose existing YouTube videos into Shorts plans, captions, SEO refreshes and upload tasks.</p>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/repurpose-existing?max=10')">Repurpose Existing Videos</button>
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
