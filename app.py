import datetime
from flask import Flask, jsonify, request, redirect, render_template_string
from youtube_client import YouTubeClient
from upload_routes import register_upload_routes
from bangitup_agents import ApprovalQueue
from source_registry import list_sources, find_by_video_id, append_growth_action, add_drive_source_record
from growth_loop import analyze_video_performance
from drive_scanner import list_source_videos

app = Flask(__name__)
yt = YouTubeClient()
queue = ApprovalQueue()
register_upload_routes(app)

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"youtube-ai-agents-v20-clean-fixed-drive-file","started_at":datetime.datetime.utcnow().isoformat()+"Z"})

@app.route("/api/channel")
def api_channel():
    try:
        return jsonify(yt.my_channel())
    except Exception as e:
        return jsonify({"status":"channel_error","error":str(e)}), 500

@app.route("/api/drive/status")
def api_drive_status():
    try:
        items = list_source_videos(max_results=int(request.args.get("max", "50")))
        return jsonify({"status":"ok","drive_scanner":"active","scope":"drive.file","files_found":len(items),"items":items})
    except Exception as e:
        return jsonify({"status":"drive_error","error":str(e),"note":"Check DRIVE_SOURCE_FOLDER_ID and YOUTUBE_TOKEN_JSON. v20 uses drive.file, not drive.readonly."}), 500

@app.route("/api/drive/scan")
def api_drive_scan():
    try:
        items = list_source_videos(max_results=int(request.args.get("max", "100")))
        registered, skipped = [], []
        for item in items:
            rec, created = add_drive_source_record(item)
            (registered if created else skipped).append(rec)
        result = {"status":"drive_scan_completed","files_found":len(items),"new_registered":len(registered),"already_known":len(skipped),"registered":registered,"skipped":skipped}
        queue.add({"created_at":datetime.datetime.utcnow().isoformat()+"Z","type":"drive_scan","result":result})
        return jsonify(result)
    except Exception as e:
        return jsonify({"status":"drive_scan_failed","error":str(e)}), 500

@app.route("/api/source/registry")
def api_source_registry():
    return jsonify(list_sources())

@app.route("/api/source/<video_id>")
def api_source(video_id):
    rec = find_by_video_id(video_id)
    if not rec:
        return jsonify({"error":"source record not found"}), 404
    return jsonify(rec)

@app.route("/api/source/analyze/<video_id>")
def api_source_analyze(video_id):
    rec = find_by_video_id(video_id)
    if not rec:
        return jsonify({"error":"source record not found"}), 404
    rows = yt.videos_by_ids([video_id])
    if not rows:
        return jsonify({"error":"youtube video not found"}), 404
    analysis = analyze_video_performance(rows[0])
    append_growth_action(video_id, {"type":"performance_analysis","analysis":analysis})
    queue.add({"created_at":datetime.datetime.utcnow().isoformat()+"Z","type":"growth_actions","video_id":video_id,"analysis":analysis})
    return jsonify({"source":rec,"analysis":analysis})

@app.route("/api/source/growth-loop")
def api_source_growth_loop():
    records = list_sources()
    results = []
    for rec in records:
        vid = rec.get("youtube_video_id")
        if not vid:
            results.append({"registry_id":rec.get("id"),"title":rec.get("title"),"status":"registered_source_without_youtube_upload","next_action":"upload_private"})
            continue
        try:
            rows = yt.videos_by_ids([vid])
            if not rows:
                results.append({"video_id":vid,"status":"not_found"})
                continue
            analysis = analyze_video_performance(rows[0])
            append_growth_action(vid, {"type":"scheduled_performance_analysis","analysis":analysis})
            results.append({"video_id":vid,"status":"analyzed","analysis":analysis})
        except Exception as e:
            results.append({"video_id":vid,"status":"error","error":str(e)})
    item = {"created_at":datetime.datetime.utcnow().isoformat()+"Z","type":"source_growth_loop","status":"completed","results":results}
    queue.add(item)
    return jsonify(item)

@app.route("/api/approval-queue")
def api_queue():
    return jsonify(queue.list())

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <h1>BANG IT UP MUSIC AI Agents v20 CLEAN FIXED</h1>
    <p>Clean reset: YouTube Upload + Drive File + Source Registry + Growth Loop.</p>
    <button onclick="go('/health')">Health</button>
    <button onclick="go('/api/channel')">Channel</button>
    <button onclick="go('/api/upload/status')">Upload Status</button>
    <button onclick="go('/api/drive/status')">Drive Status</button>
    <button onclick="go('/api/drive/scan')">Drive Scan</button>
    <button onclick="go('/api/source/registry')">Source Registry</button>
    <button onclick="go('/api/source/growth-loop')">Growth Loop</button>
    <button onclick="go('/api/approval-queue')">Queue</button>
    <pre id=o>Ready</pre>
    <script>
    async function go(p){o.textContent='Loading';let r=await fetch(p);o.textContent=JSON.stringify(await r.json(),null,2)}
    </script>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
