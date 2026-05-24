
import os
import json
import datetime
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

def register_scheduler_routes(app, yt=None, queue=None, short_agent_cls=None):
    @app.route("/api/scheduler/status")
    def scheduler_status():
        return jsonify({
            "scheduler_routes": "active",
            "version": "v16.1-direct-internal-run",
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

        try:
            if yt is None or queue is None or short_agent_cls is None:
                raise RuntimeError("Scheduler dependencies not registered.")

            videos = yt.recent_videos(10)
            plan = short_agent_cls().batch(videos)

            item = {
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                "type": "scheduled_short_tasks",
                "status": "tasks_ready",
                "plan": plan,
                "note": "Scheduler ran internally without HTTP self-call."
            }
            queue.add(item)

            result = {
                "status": "scheduler_completed",
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                "tasks": [
                    {
                        "name": "create_short_tasks",
                        "ok": True,
                        "count": plan.get("count", 0)
                    }
                ],
                "queue_item_id": item.get("id"),
                "note": "Short tasks created. Real uploads still require direct MP4 URLs."
            }
            _log("scheduler_run", result)
            return jsonify(result)
        except Exception as e:
            result = {
                "status": "scheduler_failed",
                "error": str(e),
                "created_at": datetime.datetime.utcnow().isoformat() + "Z"
            }
            _log("scheduler_run", result)
            return jsonify(result), 500
