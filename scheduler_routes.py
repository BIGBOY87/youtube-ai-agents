
import os
import json
import datetime
import requests
from flask import jsonify, request

SCHEDULER_LOG = "scheduler_log.json"

def _load_log():
    if not os.path.exists(SCHEDULER_LOG):
        return []
    try:
        with open(SCHEDULER_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_log(rows):
    with open(SCHEDULER_LOG, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def _log(action, result):
    rows = _load_log()
    rows.insert(0, {
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "action": action,
        "result": result
    })
    rows = rows[:100]
    _save_log(rows)

def register_scheduler_routes(app, yt=None, queue=None):

    @app.route("/api/scheduler/status")
    def scheduler_status():
        return jsonify({
            "scheduler_routes": "active",
            "mode": "external-cron-trigger",
            "scheduler_secret_configured": bool(os.getenv("SCHEDULER_SECRET", "").strip()),
            "auto_scheduler_enabled": os.getenv("AUTO_SCHEDULER_ENABLED", "false").lower() == "true",
            "recommended_cron_url": "/api/scheduler/run?secret=YOUR_SECRET",
            "note": "Use cron-job.org or Render Cron Job to hit this endpoint daily."
        })

    @app.route("/api/scheduler/log")
    def scheduler_log():
        return jsonify(_load_log())

    @app.route("/api/scheduler/run")
    def scheduler_run():
        if os.getenv("AUTO_SCHEDULER_ENABLED", "false").lower() != "true":
            result = {"status": "blocked", "reason": "AUTO_SCHEDULER_ENABLED is false."}
            _log("scheduler_run", result)
            return jsonify(result), 400

        required_secret = os.getenv("SCHEDULER_SECRET", "").strip()
        provided_secret = request.args.get("secret", "").strip()

        if required_secret and provided_secret != required_secret:
            result = {"status": "blocked", "reason": "Invalid scheduler secret."}
            _log("scheduler_run", result)
            return jsonify(result), 403

        base_url = os.getenv("PUBLIC_BASE_URL", "https://youtube-ai-agents.onrender.com").rstrip("/")
        tasks = []

        # 1. Create Shorts tasks from existing YouTube videos.
        try:
            r = requests.get(f"{base_url}/api/shorts/tasks?max=10", timeout=60)
            tasks.append({"endpoint": "/api/shorts/tasks", "status_code": r.status_code, "ok": r.ok})
        except Exception as e:
            tasks.append({"endpoint": "/api/shorts/tasks", "error": str(e)})

        # 2. Run existing auto-run planner.
        try:
            r = requests.get(f"{base_url}/api/auto-run", timeout=60)
            tasks.append({"endpoint": "/api/auto-run", "status_code": r.status_code, "ok": r.ok})
        except Exception as e:
            tasks.append({"endpoint": "/api/auto-run", "error": str(e)})

        result = {
            "status": "scheduler_completed",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "tasks": tasks,
            "note": "Scheduler creates plans/tasks. It will not invent MP4 files from YouTube; ready MP4/direct URLs are still required for real uploads."
        }
        _log("scheduler_run", result)
        return jsonify(result)
