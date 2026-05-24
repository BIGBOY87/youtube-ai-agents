
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string
from youtube_client import YouTubeClient
from upload_routes import register_upload_routes
from bangitup_agents import ApprovalQueue
from source_registry import list_sources, find_by_video_id, append_growth_action
from growth_loop import analyze_video_performance

app = Flask(__name__)
yt = YouTubeClient()
queue = ApprovalQueue()
register_upload_routes(app)

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "youtube-ai-agents-v18-source-registry-growth-loop", "started_at": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/api/source/registry")
def api_source_registry():
    return jsonify(list_sources())

@app.route("/api/source/<video_id>")
def api_source(video_id):
    rec = find_by_video_id(video_id)
    if not rec:
        return jsonify({"error": "source record not found"}), 404
    return jsonify(rec)

@app.route("/api/source/analyze/<video_id>")
def api_source_analyze(video_id):
    rec = find_by_video_id(video_id)
    if not rec:
        return jsonify({"error": "source record not found"}), 404
    rows = yt.videos_by_ids([video_id])
    if not rows:
        return jsonify({"error": "youtube video not found"}), 404
    analysis = analyze_video_performance(rows[0])
    append_growth_action(video_id, {"type": "performance_analysis", "analysis": analysis})
    queue.add({"created_at": datetime.datetime.utcnow().isoformat() + "Z", "type": "growth_actions", "video_id": video_id, "analysis": analysis})
    return jsonify({"source": rec, "analysis": analysis})

@app.route("/api/source/growth-loop")
def api_source_growth_loop():
    records = list_sources()
    results = []
    for rec in records:
        video_id = rec.get("youtube_video_id")
        try:
            rows = yt.videos_by_ids([video_id])
            if not rows:
                results.append({"video_id": video_id, "status": "not_found"})
                continue
            analysis = analyze_video_performance(rows[0])
            append_growth_action(video_id, {"type": "scheduled_performance_analysis", "analysis": analysis})
            results.append({"video_id": video_id, "status": "analyzed", "analysis": analysis})
        except Exception as e:
            results.append({"video_id": video_id, "status": "error", "error": str(e)})
    item = {"created_at": datetime.datetime.utcnow().isoformat() + "Z", "type": "source_growth_loop", "status": "completed", "results": results}
    queue.add(item)
    return jsonify(item)

@app.route("/api/approval-queue")
def api_queue():
    return jsonify(queue.list())

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <h1>BANG IT UP MUSIC AI Agents v18</h1>
    <p>Source Registry + Growth Loop.</p>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/source/registry')">Source Registry</button>
    <button onclick="go('/api/source/growth-loop')">Run Growth Loop</button>
    <button onclick="go('/api/approval-queue')">Queue</button>
    <pre id=o>Ready</pre>
    <script>
    async function go(p){o.textContent='Loading';let r=await fetch(p);o.textContent=JSON.stringify(await r.json(),null,2)}
    </script>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
