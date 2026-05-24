
import os
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string

from youtube_client import YouTubeClient
from bangitup_agents import (
    GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent,
    InitiativeEngine, ApprovalQueue, ShortWorkflowAgent
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
        "service": "youtube-ai-agents-v14-auto-shorts-workflow",
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
                "auto_shorts_workflow": "active",
                "mode": "shorts-from-original-mp4-url"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/shorts/tasks")
def api_shorts_tasks():
    try:
        max_results = int(request.args.get("max", "10"))
        videos = yt.recent_videos(max_results)
        plan = ShortWorkflowAgent().batch(videos)
        queue.add({
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "auto_shorts_tasks",
            "status": "tasks_ready",
            "plan": plan
        })
        return jsonify(plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/shorts/task/<video_id>")
def api_shorts_task(video_id):
    try:
        rows = yt.videos_by_ids([video_id])
        if not rows:
            return jsonify({"error": "video not found"}), 404
        task = ShortWorkflowAgent().make_short_task(rows[0])
        queue.add({
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "single_short_task",
            "status": "task_ready",
            "task": task
        })
        return jsonify(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/shorts/upload-from-url", methods=["POST"])
def api_shorts_upload_from_url():
    """
    Pass-through convenience endpoint.
    It uploads a ready vertical Short MP4 URL using /api/upload/from-url logic expectations.
    The caller must provide a direct MP4 URL for a legally owned/generated Short.
    """
    from upload_routes import _safe_upload_allowed, _download_mp4
    from youtube_uploader import upload_video

    data = request.get_json(silent=True) or {}
    allowed, reason = _safe_upload_allowed()
    if not allowed:
        return jsonify({"status": "blocked", "reason": reason}), 400

    if data.get("own_content_confirmed") is not True:
        return jsonify({"status": "blocked", "reason": "own_content_confirmed must be true."}), 400

    url = data.get("short_mp4_url") or data.get("video_url")
    if not url:
        return jsonify({"status": "blocked", "reason": "Missing short_mp4_url."}), 400

    path = None
    try:
        path = _download_mp4(url)
        title = data.get("title", "BANG IT UP MUSIC Short #Shorts")
        if "#shorts" not in title.lower():
            title = title[:90] + " #Shorts"
        description = data.get("description", "BANG IT UP MUSIC Short. #Shorts #BANGITUPMUSIC")
        tags = data.get("tags", ["BANGITUPMUSIC", "Shorts", "TechHouse", "EDM"])
        result = upload_video(
            video_file=path,
            title=title,
            description=description,
            tags=tags,
            category_id=data.get("category_id", "10"),
            privacy_status=data.get("privacy_status", os.getenv("DEFAULT_UPLOAD_PRIVACY", "private")),
            publish_at=data.get("publish_at"),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "short_upload_failed", "error": str(e)}), 500
    finally:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

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

@app.route("/api/auto-run")
def api_auto_run():
    try:
        videos = yt.recent_videos(10)
        plan = ShortWorkflowAgent().batch(videos)
        item = {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "auto_run_shorts_workflow",
            "status": "tasks_ready",
            "plan": plan,
            "note": "Tasks are ready. Provide original/cut Short MP4 direct URLs to upload real Shorts."
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
    <h1>BANG IT UP MUSIC AI Agents v14</h1>
    <p>Auto Shorts workflow from existing YouTube videos. Uses original/cut MP4 direct URLs for real uploads.</p>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/shorts/tasks?max=10')">Create Shorts Tasks</button>
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
