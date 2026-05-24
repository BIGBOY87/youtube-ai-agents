
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string
from youtube_client import YouTubeClient
from bangitup_agents import GrowthAgent, InitiativeEngine, ApprovalQueue, ShortWorkflowAgent
from upload_routes import register_upload_routes
from scheduler_routes import register_scheduler_routes

app = Flask(__name__)
yt = YouTubeClient()
queue = ApprovalQueue()

register_upload_routes(app)
register_scheduler_routes(app, yt, queue)

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "youtube-ai-agents-v16-scheduler",
        "started_at": datetime.datetime.utcnow().isoformat() + "Z"
    })

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
            "agent_status": {
                "mode": "local-short-factory-render-upload-scheduler",
                "upload": "active",
                "scheduler": "active"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/shorts/tasks")
def api_shorts_tasks():
    try:
        plan = ShortWorkflowAgent().batch(yt.recent_videos(int(request.args.get("max", "10"))))
        queue.add({
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "v16_scheduled_short_tasks",
            "status": "tasks_ready",
            "plan": plan
        })
        return jsonify(plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auto-run")
def api_auto_run():
    try:
        plan = ShortWorkflowAgent().batch(yt.recent_videos(10))
        item = {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "auto_run_scheduler",
            "status": "tasks_ready",
            "plan": plan
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
    <h1>BANG IT UP MUSIC AI Agents v16</h1>
    <p>Scheduler + Shorts task automation.</p>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/shorts/tasks?max=10')">Short Tasks</button>
    <button onclick="go('/api/scheduler/status')">Scheduler Status</button>
    <button onclick="go('/api/scheduler/log')">Scheduler Log</button>
    <pre id=o>Ready</pre>
    <script>
    async function go(p){
      o.textContent='Loading';
      let r=await fetch(p);
      o.textContent=JSON.stringify(await r.json(),null,2)
    }
    </script>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
