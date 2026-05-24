import os
import datetime
from flask import Flask, jsonify, request, redirect, render_template_string

from youtube_client import YouTubeClient
from bangitup_agents import (
    GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent,
    InitiativeEngine, VideoCreatorAgent, ApprovalQueue, ThumbnailAgent, SchedulerAgent
)
from upload_routes import register_upload_routes

app = Flask(__name__)
yt = YouTubeClient()
queue = ApprovalQueue()
register_upload_routes(app)

def missing_vars():
    return [k for k in ["YOUTUBE_API_KEY", "YOUTUBE_CHANNEL_ID"] if not os.getenv(k)]

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "youtube-ai-agents-clean-reset",
        "missing_required_vars": missing_vars(),
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
        return jsonify(yt.recent_videos(max_results=int(request.args.get("max", "12"))))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/report")
def api_report():
    try:
        channel = yt.channel()
        videos = yt.recent_videos(max_results=12)
        return jsonify({
            "channel": {
                "title": channel.get("snippet", {}).get("title"),
                "subscribers": channel.get("statistics", {}).get("subscriberCount"),
                "views": channel.get("statistics", {}).get("viewCount"),
                "videos": channel.get("statistics", {}).get("videoCount")
            },
            "growth_report": GrowthAgent().report(channel, videos),
            "initiatives": InitiativeEngine().decide(channel, videos),
            "agent_status": {
                "growth": "active",
                "seo": "active",
                "shorts": "active",
                "initiative": "active",
                "upload": "status-only until OAuth token and MP4 are configured"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/seo")
def api_seo():
    return jsonify(SEOAgent().generate(
        request.args.get("title", "New BANG IT UP MUSIC Track"),
        request.args.get("genre", "Tech House"),
        request.args.get("mood", "high energy")
    ))

@app.route("/api/shorts")
def api_shorts():
    return jsonify(ShortsAgent().generate(
        request.args.get("title", "New BANG IT UP MUSIC Track"),
        request.args.get("genre", "Tech House")
    ))

@app.route("/api/distribution")
def api_distribution():
    return jsonify(DistributionAgent().posts(
        request.args.get("title", "New BANG IT UP MUSIC Track"),
        request.args.get("genre", "Tech House")
    ))

@app.route("/api/calendar")
def api_calendar():
    return jsonify(CalendarAgent().weekly())

@app.route("/api/create-video-project")
def api_create_video_project():
    try:
        title = request.args.get("title", "Autonomous Dark Tech House Night Drive Concept")
        genre = request.args.get("genre", "Tech House")
        project = VideoCreatorAgent().create_project(title, genre)
        queue.add({"type": "video_project", "status": "needs_approval", "project": project})
        return jsonify(project)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auto-run")
def api_auto_run():
    try:
        videos = yt.recent_videos(max_results=5)
        source = videos[0] if videos else {}
        source_title = source.get("snippet", {}).get("title", "Autonomous Dark Tech House Night Drive Concept")
        project = VideoCreatorAgent().create_project(source_title, "Tech House")
        shorts = ShortsAgent().generate(source_title, "Tech House")
        item = {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "video_project",
            "status": "needs_approval",
            "source_title": source_title,
            "project": project,
            "assets": {"shorts_package": shorts},
            "note": "Public actions remain blocked until upload OAuth token, MP4 file, and safety settings are configured."
        }
        queue.add(item)
        return jsonify({"status": "completed", "created_items": [item]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/approval-queue")
def api_approval_queue():
    return jsonify(queue.list())

@app.route("/api/approve")
def api_approve():
    return jsonify(queue.approve(request.args.get("id")))

@app.route("/api/scheduler")
def api_scheduler():
    return jsonify(SchedulerAgent().daily_plan())

@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_HTML)

DASHBOARD_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>BANG IT UP MUSIC AI Agents</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;background:#080812;color:#f5f7ff;font-family:Arial,Helvetica,sans-serif}
header{padding:28px} h1{margin:0;font-size:32px}.sub{color:#a8aac0}
.wrap{padding:0 28px 40px}.card{background:#161625;border:1px solid #303047;border-radius:18px;padding:18px;margin-bottom:16px}
button{background:#7c3aed;border:0;color:white;padding:11px 14px;border-radius:12px;font-weight:700;cursor:pointer;margin:4px}
input{background:#0c0c12;color:white;border:1px solid #333;border-radius:10px;padding:11px;margin:4px;min-width:240px}
pre{white-space:pre-wrap;background:#07070d;border:1px solid #222;border-radius:14px;padding:16px;max-height:520px;overflow:auto}
.video{display:flex;gap:14px;margin:12px 0;padding:12px;border:1px solid #2b2b42;border-radius:14px;background:#10101c}
.video img{width:180px;border-radius:10px;object-fit:cover}.pill{display:inline-block;padding:5px 9px;border-radius:999px;background:#20203a;color:#bfc1ff;margin:2px;font-size:12px}
.danger{color:#ff4d6d}
</style>
</head>
<body>
<header><h1>BANG IT UP MUSIC AI Agents Dashboard</h1><div class="sub">Growth · SEO · Shorts · Initiative · Upload status</div></header>
<div class="wrap">
<div class="card">
<button onclick="loadChannel()">Channel</button>
<button onclick="loadVideos()">Recent Videos</button>
<button onclick="load('/api/report')">Full Growth Report</button>
<button onclick="load('/api/calendar')">Calendar</button>
<button onclick="load('/api/auto-run')">Auto Run</button>
<button onclick="load('/api/approval-queue')">Approval Queue</button>
<button onclick="load('/api/upload/status')">Upload Status</button>
</div>
<div class="card">
<h3>Generate Campaign Assets</h3>
<input id="title" value="New BANG IT UP MUSIC Track">
<input id="genre" value="Tech House">
<button onclick="asset('seo')">SEO</button>
<button onclick="asset('shorts')">Shorts</button>
<button onclick="asset('distribution')">Distribution</button>
<button onclick="createProject()">Create Video Project</button>
</div>
<div id="out" class="card"><pre>Click a button.</pre></div>
</div>
<script>
const out=document.getElementById("out");
function safe(v){return String(v??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","'":"&#039;"}[m]));}
async function getJson(path){const r=await fetch(path);if(!r.ok)throw new Error(path+" returned HTTP "+r.status);return await r.json();}
async function load(path){out.innerHTML="<pre>Loading...</pre>";try{const data=await getJson(path);out.innerHTML="<pre>"+safe(JSON.stringify(data,null,2))+"</pre>";}catch(e){out.innerHTML="<pre class='danger'>"+safe(e.toString())+"</pre>";}}
async function loadChannel(){out.innerHTML="<pre>Loading channel...</pre>";try{const data=await getJson("/api/channel");const s=data.snippet||{};const st=data.statistics||{};const thumb=s.thumbnails?.medium?.url||s.thumbnails?.default?.url||"";out.innerHTML=`<h2>${safe(s.title||"Channel")}</h2>${thumb?`<img src="${thumb}" style="width:140px;border-radius:16px">`:""}<p>${safe(s.description||"")}</p><span class="pill">Subscribers: ${safe(st.subscriberCount||"0")}</span><span class="pill">Views: ${safe(st.viewCount||"0")}</span><span class="pill">Videos: ${safe(st.videoCount||"0")}</span>`;}catch(e){out.innerHTML="<pre class='danger'>"+safe(e.toString())+"</pre>";}}
async function loadVideos(){out.innerHTML="<pre>Loading videos...</pre>";try{const data=await getJson("/api/videos");let html="<h2>Recent Videos</h2>";data.forEach(v=>{const s=v.snippet||{};const st=v.statistics||{};const thumb=s.thumbnails?.medium?.url||s.thumbnails?.default?.url||"";html+=`<div class="video">${thumb?`<img src="${thumb}">`:""}<div><h3>${safe(s.title||"Untitled")}</h3><p>${safe((s.description||"").slice(0,220))}</p><span class="pill">Views: ${safe(st.viewCount||"0")}</span><span class="pill">Likes: ${safe(st.likeCount||"0")}</span><span class="pill">Comments: ${safe(st.commentCount||"0")}</span></div></div>`;});out.innerHTML=html;}catch(e){out.innerHTML="<pre class='danger'>"+safe(e.toString())+"</pre>";}}
function asset(kind){const t=encodeURIComponent(document.getElementById("title").value);const g=encodeURIComponent(document.getElementById("genre").value);load(`/api/${kind}?title=${t}&genre=${g}`);}
function createProject(){const t=encodeURIComponent(document.getElementById("title").value);const g=encodeURIComponent(document.getElementById("genre").value);load(`/api/create-video-project?title=${t}&genre=${g}`);}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
