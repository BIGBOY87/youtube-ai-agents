
import os
import json
import datetime
import random
from flask import Flask, jsonify, request, redirect, render_template_string
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
APP_NAME = "BANG IT UP MUSIC AI Agents v6"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
APPROVAL_FILE = os.path.join(DATA_DIR, "approval_queue.json")
HISTORY_FILE = os.path.join(DATA_DIR, "initiative_history.json")

REQUIRED_VARS = ["YOUTUBE_API_KEY", "YOUTUBE_CHANNEL_ID"]

SAFETY_POLICY = {
    "auto_allowed": [
        "analyze_channel",
        "create_video_concepts",
        "create_scripts",
        "create_seo_metadata",
        "create_thumbnail_prompts",
        "create_shorts_packages",
        "create_social_captions",
        "create_daily_growth_tasks",
        "add_items_to_approval_queue"
    ],
    "approval_required": [
        "upload_video",
        "schedule_video",
        "change_existing_title",
        "change_existing_description",
        "reply_to_comments",
        "post_to_social_platforms"
    ],
    "blocked": [
        "fake_views",
        "fake_subscribers",
        "bot_engagement",
        "spam_comments",
        "mass_dm",
        "copyright_infringing_assets"
    ]
}

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def yt_get(endpoint, params):
    if not YOUTUBE_API_KEY:
        raise RuntimeError("Missing YOUTUBE_API_KEY")
    params = dict(params)
    params["key"] = YOUTUBE_API_KEY
    url = "https://www.googleapis.com/youtube/v3/" + endpoint
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def get_channel():
    if not YOUTUBE_CHANNEL_ID:
        raise RuntimeError("Missing YOUTUBE_CHANNEL_ID")
    data = yt_get("channels", {
        "part": "snippet,statistics,brandingSettings",
        "id": YOUTUBE_CHANNEL_ID
    })
    items = data.get("items", [])
    return items[0] if items else {}

def get_videos(max_results=8):
    data = yt_get("search", {
        "part": "snippet",
        "channelId": YOUTUBE_CHANNEL_ID,
        "order": "date",
        "maxResults": max_results,
        "type": "video"
    })
    ids = [i["id"]["videoId"] for i in data.get("items", []) if i.get("id", {}).get("videoId")]
    stats = {}
    if ids:
        details = yt_get("videos", {
            "part": "statistics,snippet,contentDetails",
            "id": ",".join(ids)
        })
        for item in details.get("items", []):
            stats[item["id"]] = item
    out = []
    for item in data.get("items", []):
        vid = item.get("id", {}).get("videoId")
        merged = stats.get(vid, item)
        if "snippet" not in merged:
            merged["snippet"] = item.get("snippet", {})
        out.append(merged)
    return out

def infer_genre_from_titles(videos):
    titles = " ".join([v.get("snippet", {}).get("title", "") for v in videos]).lower()
    checks = ["tech house", "industrial", "edm", "trap", "phonk", "bass", "melodic", "dark", "club", "house"]
    found = [c for c in checks if c in titles]
    return found[:3] or ["EDM", "Tech House", "Dark Bass"]

def create_video_concept(seed_title=None, genre="EDM", mood="dark energetic"):
    hooks = [
        "first 3 seconds with a heavy drop preview",
        "neon city night-drive visual",
        "club-ready bass intro",
        "industrial warehouse performance vibe",
        "fast-cut kinetic lyric/visualizer hook"
    ]
    title_core = seed_title or random.choice([
        "STATIC WAVE", "NEON IMPACT", "MIDNIGHT VOLTAGE", "BLACKOUT DRIVE", "BASS SIGNAL"
    ])
    concept = {
        "id": "concept_" + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "type": "video_project",
        "status": "pending_approval",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "risk_level": "low",
        "requires_approval_before_public_action": True,
        "title": f"{title_core} | {genre} Music Visualizer",
        "concept": f"A high-energy {genre} music visualizer for BANG IT UP MUSIC with {mood} atmosphere.",
        "hook": random.choice(hooks),
        "target_audience": ["EDM listeners", "club music fans", "night-drive playlist listeners", "dark electronic music fans"],
        "video_structure": [
            {"time": "0:00-0:03", "goal": "instant hook/drop preview"},
            {"time": "0:04-0:15", "goal": "brand/title reveal with movement"},
            {"time": "0:16-0:45", "goal": "main groove, intense visuals"},
            {"time": "0:46-1:15", "goal": "variation/drop section"},
            {"time": "end", "goal": "subscribe + playlist CTA"}
        ],
        "script": {
            "onscreen_text": [
                "BANG IT UP MUSIC",
                f"{title_core}",
                "Turn it up.",
                "New electronic music drop.",
                "Subscribe for more."
            ],
            "voiceover_optional": "No voiceover required. Keep music primary."
        },
        "thumbnail_prompt": f"Create a dark neon cyberpunk/industrial music thumbnail for '{title_core}', high contrast, bold readable title, bass wave energy, no copyrighted logos.",
        "seo": {
            "titles": [
                f"{title_core} | Dark {genre} Music Visualizer",
                f"{title_core} - Industrial {genre} Bass Track",
                f"New {genre} Music 2026 | {title_core}",
                f"{title_core} | Night Drive Electronic Music",
                f"BANG IT UP MUSIC - {title_core}"
            ],
            "description": f"{title_core} by BANG IT UP MUSIC. Dark, energetic {genre} track built for night drives, clubs and high-energy playlists.\n\nSubscribe for more electronic music, visualizers and bass-heavy drops.",
            "hashtags": ["#BANGITUPMUSIC", "#EDM", "#TechHouse", "#ElectronicMusic", "#BassMusic", "#MusicVisualizer", "#NewMusic", "#ClubMusic", "#NightDrive", "#DarkElectronic"],
            "tags": ["BANG IT UP MUSIC", genre, "EDM music", "tech house", "industrial electronic", "bass music", "music visualizer", "new electronic music", "night drive music", "club music"]
        },
        "shorts": [
            {"title": f"{title_core} - Drop Preview", "hook": "Wait for the bass hit.", "duration": "12-18 sec"},
            {"title": f"{title_core} - Night Drive Cut", "hook": "This one is for late-night drives.", "duration": "15-25 sec"},
            {"title": f"{title_core} - Visualizer Moment", "hook": "Dark electronic energy.", "duration": "10-20 sec"}
        ],
        "social_posts": {
            "instagram": f"New drop from BANG IT UP MUSIC: {title_core}. Dark {genre} energy. Link in bio. #EDM #NewMusic",
            "tiktok": f"New {genre} drop. Use this sound for night-drive / gym / club edits. #{genre.replace(' ', '')} #BANGITUPMUSIC",
            "x": f"New BANG IT UP MUSIC release idea: {title_core}. Dark {genre} visualizer + Shorts package ready.",
            "reddit_safe": f"I’m working on a dark {genre} visualizer under BANG IT UP MUSIC. Feedback on the mix/visual direction would be appreciated. No spam links unless allowed by the community rules."
        },
        "approval_actions": [
            "approve_create_assets",
            "approve_upload_metadata",
            "approve_schedule_youtube_upload"
        ]
    }
    return concept

def add_to_queue(item):
    queue = load_json(APPROVAL_FILE, [])
    queue.insert(0, item)
    save_json(APPROVAL_FILE, queue)
    return item

def run_initiative_engine():
    videos = []
    channel = {}
    try:
        channel = get_channel()
        videos = get_videos(8)
    except Exception:
        pass
    genres = infer_genre_from_titles(videos)
    latest_views = []
    for v in videos[:5]:
        stats = v.get("statistics", {})
        title = v.get("snippet", {}).get("title", "Untitled")
        latest_views.append({"title": title, "views": int(stats.get("viewCount", 0)) if str(stats.get("viewCount", "0")).isdigit() else 0})
    reason = "Daily initiative: create one new video project draft for review."
    if len(videos) < 3:
        reason = "Channel has limited recent video data. Create a new content draft to maintain publishing cadence."
    concept = create_video_concept(genre=genres[0], mood="dark / high energy")
    concept["initiative_reason"] = reason
    concept["channel_snapshot"] = {
        "title": channel.get("snippet", {}).get("title", "BANG IT UP MUSIC"),
        "subscribers": channel.get("statistics", {}).get("subscriberCount", "unknown"),
        "views": channel.get("statistics", {}).get("viewCount", "unknown"),
        "latest_video_views": latest_views
    }
    add_to_queue(concept)
    history = load_json(HISTORY_FILE, [])
    history.insert(0, {"created_at": concept["created_at"], "action": "created_video_project_draft", "reason": reason, "project_id": concept["id"]})
    save_json(HISTORY_FILE, history[:200])
    return concept

@app.route("/")
def root():
    return redirect("/dashboard")

@app.route("/health")
def health():
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    return jsonify({
        "status": "ok",
        "app": APP_NAME,
        "missing_required_vars": missing,
        "safety_mode": "controlled_autonomy",
        "public_actions_require_approval": True
    })

@app.route("/api/channel")
def api_channel():
    return jsonify(get_channel())

@app.route("/api/videos")
def api_videos():
    return jsonify(get_videos())

@app.route("/api/report")
def api_report():
    channel = get_channel()
    videos = get_videos()
    ideas = []
    for v in videos[:5]:
        title = v.get("snippet", {}).get("title", "")
        views = v.get("statistics", {}).get("viewCount", "0")
        ideas.append({
            "video": title,
            "views": views,
            "recommendation": "Repurpose this into 2 Shorts and test a high-contrast thumbnail/title variant."
        })
    return jsonify({
        "channel": {
            "title": channel.get("snippet", {}).get("title"),
            "subscribers": channel.get("statistics", {}).get("subscriberCount"),
            "views": channel.get("statistics", {}).get("viewCount"),
            "videoCount": channel.get("statistics", {}).get("videoCount")
        },
        "agent_recommendations": ideas,
        "next_actions": [
            "Create one Shorts package from the best-performing recent video.",
            "Prepare one new video concept in the approval queue.",
            "Review titles with stronger first 45 characters.",
            "Post one community prompt asking listeners what style they want next."
        ]
    })

@app.route("/api/seo")
def api_seo():
    title = request.args.get("title", "New BANG IT UP MUSIC Track")
    genre = request.args.get("genre", "EDM")
    c = create_video_concept(seed_title=title, genre=genre)
    return jsonify(c["seo"])

@app.route("/api/shorts")
def api_shorts():
    title = request.args.get("title", "New BANG IT UP MUSIC Track")
    genre = request.args.get("genre", "EDM")
    c = create_video_concept(seed_title=title, genre=genre)
    return jsonify(c["shorts"])

@app.route("/api/distribution")
def api_distribution():
    title = request.args.get("title", "New BANG IT UP MUSIC Track")
    genre = request.args.get("genre", "EDM")
    c = create_video_concept(seed_title=title, genre=genre)
    return jsonify(c["social_posts"])

@app.route("/api/create-video-project", methods=["POST", "GET"])
def api_create_video_project():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title") or request.args.get("title") or None
    genre = payload.get("genre") or request.args.get("genre") or "EDM"
    mood = payload.get("mood") or request.args.get("mood") or "dark energetic"
    item = add_to_queue(create_video_concept(seed_title=title, genre=genre, mood=mood))
    return jsonify(item)

@app.route("/api/run-initiative", methods=["POST", "GET"])
def api_run_initiative():
    return jsonify(run_initiative_engine())

@app.route("/api/approval-queue")
def api_approval_queue():
    return jsonify(load_json(APPROVAL_FILE, []))

@app.route("/api/safety-policy")
def api_safety_policy():
    return jsonify(SAFETY_POLICY)

@app.route("/api/history")
def api_history():
    return jsonify(load_json(HISTORY_FILE, []))

@app.route("/api/approve/<item_id>", methods=["POST"])
def api_approve(item_id):
    queue = load_json(APPROVAL_FILE, [])
    for item in queue:
        if item.get("id") == item_id:
            item["status"] = "approved_for_manual_execution"
            item["approved_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            save_json(APPROVAL_FILE, queue)
            return jsonify({"ok": True, "message": "Approved for manual execution. No public upload was performed automatically.", "item": item})
    return jsonify({"ok": False, "error": "Item not found"}), 404

DASHBOARD = """
<!doctype html>
<html>
<head>
<title>BANG IT UP MUSIC AI Agents v6</title>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
:root{--bg:#070812;--card:#101426;--card2:#151b31;--text:#f5f7ff;--muted:#a6aecb;--neon:#7c3cff;--cyan:#00e5ff;--green:#39ff88;--red:#ff4f81}
*{box-sizing:border-box} body{margin:0;background:radial-gradient(circle at top left,#1d1242,#070812 45%),#070812;color:var(--text);font-family:Inter,Arial,sans-serif}
.header{padding:28px 24px;border-bottom:1px solid #222842;background:rgba(8,10,25,.86);position:sticky;top:0;backdrop-filter:blur(12px);z-index:2}
h1{margin:0;font-size:28px;letter-spacing:.2px}.sub{color:var(--muted);margin-top:8px}
.grid{display:grid;grid-template-columns:280px 1fr;gap:18px;padding:18px}
.panel{background:linear-gradient(180deg,var(--card),#0b0e1b);border:1px solid #222842;border-radius:18px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.btn{width:100%;border:1px solid #30385c;background:#11172d;color:#fff;border-radius:12px;padding:12px 14px;margin:6px 0;text-align:left;cursor:pointer;font-weight:700}
.btn:hover{border-color:var(--cyan);box-shadow:0 0 0 1px rgba(0,229,255,.25)}
.btn.primary{background:linear-gradient(90deg,var(--neon),#00a6ff);border:0;text-align:center}
.row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:14px}
.stat{background:var(--card2);border:1px solid #242b48;border-radius:16px;padding:16px}
.stat b{display:block;font-size:24px;margin-top:8px}
.card{background:#0e1324;border:1px solid #242b48;border-radius:16px;padding:14px;margin:12px 0}
.card img{border-radius:12px;max-width:220px;width:100%;display:block;margin-bottom:8px}
.badge{display:inline-block;border:1px solid #394267;border-radius:999px;padding:4px 9px;color:#cbd4ff;font-size:12px;margin:3px}
pre{white-space:pre-wrap;background:#070a15;border:1px solid #222842;border-radius:14px;padding:14px;overflow:auto}
input{width:100%;background:#090d1b;color:#fff;border:1px solid #293151;border-radius:12px;padding:12px;margin:6px 0 10px}
label{color:#c7d0ef;font-size:13px;font-weight:700}.danger{color:var(--red)}.ok{color:var(--green)}.muted{color:var(--muted)}
@media(max-width:850px){.grid{grid-template-columns:1fr}.row{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="header">
<h1>⚡ BANG IT UP MUSIC AI Agents v6</h1>
<div class="sub">Autonomous Video Creator · Initiative Engine · Approval Queue · YouTube Growth Dashboard</div>
</div>
<div class="grid">
<div class="panel">
<label>Video title seed</label><input id="title" value="New BANG IT UP MUSIC Track"/>
<label>Genre</label><input id="genre" value="EDM"/>
<label>Mood</label><input id="mood" value="dark energetic"/>
<button class="btn" onclick="loadChannel()">Channel</button>
<button class="btn" onclick="loadVideos()">Recent Videos</button>
<button class="btn" onclick="loadReport()">Full Growth Report</button>
<button class="btn" onclick="makeSeo()">SEO Agent</button>
<button class="btn" onclick="makeShorts()">Shorts Agent</button>
<button class="btn" onclick="makeDistribution()">Distribution Agent</button>
<button class="btn primary" onclick="createProject()">Create Video Project</button>
<button class="btn primary" onclick="runInitiative()">Run Initiative Engine</button>
<button class="btn" onclick="loadQueue()">Approval Queue</button>
<button class="btn" onclick="loadSafety()">Safety Policy</button>
</div>
<div>
<div class="row">
<div class="stat">Safety Mode<b class="ok">Approval</b><span class="muted">Public actions need approval</span></div>
<div class="stat">Autonomy<b>Drafts</b><span class="muted">Creates projects and tasks</span></div>
<div class="stat">Blocked<b class="danger">Bots</b><span class="muted">No fake engagement</span></div>
</div>
<div class="panel" id="out"><h2>Ready.</h2><p>Use the buttons to run agents. The system can create video projects by itself, but upload/post actions stay in approval mode.</p></div>
</div>
</div>
<script>
const out=document.getElementById('out');
const title=()=>encodeURIComponent(document.getElementById('title').value);
const genre=()=>encodeURIComponent(document.getElementById('genre').value);
const mood=()=>encodeURIComponent(document.getElementById('mood').value);
async function api(path, opts){const r=await fetch(path, opts||{}); if(!r.ok) throw new Error(await r.text()); return await r.json();}
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function renderJSON(data){out.innerHTML='<pre>'+esc(JSON.stringify(data,null,2))+'</pre>'}
async function loadChannel(){out.innerHTML='Loading channel...'; const d=await api('/api/channel'); out.innerHTML=`<h2>${esc(d.snippet?.title)}</h2><div class="row"><div class="stat">Subscribers<b>${d.statistics?.subscriberCount||0}</b></div><div class="stat">Views<b>${d.statistics?.viewCount||0}</b></div><div class="stat">Videos<b>${d.statistics?.videoCount||0}</b></div></div><pre>${esc(d.snippet?.description||'')}</pre>`}
async function loadVideos(){out.innerHTML='Loading videos...'; const data=await api('/api/videos'); let html='<h2>Recent Videos</h2>'; data.forEach(v=>{html+=`<div class="card"><img src="${v.snippet?.thumbnails?.medium?.url||''}"/><h3>${esc(v.snippet?.title)}</h3><span class="badge">Views: ${v.statistics?.viewCount||0}</span><span class="badge">Likes: ${v.statistics?.likeCount||0}</span><span class="badge">Comments: ${v.statistics?.commentCount||0}</span></div>`}); out.innerHTML=html}
async function loadReport(){out.innerHTML='Generating report...'; const d=await api('/api/report'); renderJSON(d)}
async function makeSeo(){const d=await api(`/api/seo?title=${title()}&genre=${genre()}`); renderJSON(d)}
async function makeShorts(){const d=await api(`/api/shorts?title=${title()}&genre=${genre()}`); renderJSON(d)}
async function makeDistribution(){const d=await api(`/api/distribution?title=${title()}&genre=${genre()}`); renderJSON(d)}
async function createProject(){out.innerHTML='Creating video project...'; const d=await api(`/api/create-video-project?title=${title()}&genre=${genre()}&mood=${mood()}`); renderProject(d)}
async function runInitiative(){out.innerHTML='Initiative engine running...'; const d=await api('/api/run-initiative'); renderProject(d)}
async function loadQueue(){const q=await api('/api/approval-queue'); let html='<h2>Approval Queue</h2>'; if(!q.length) html+='<p>No pending items.</p>'; q.forEach(i=>{html+=`<div class="card"><h3>${esc(i.title)}</h3><p>${esc(i.concept)}</p><span class="badge">${esc(i.status)}</span><span class="badge">${esc(i.risk_level)}</span><h4>Actions requiring approval</h4>${(i.approval_actions||[]).map(a=>`<span class="badge">${esc(a)}</span>`).join('')}<pre>${esc(JSON.stringify(i.seo,null,2))}</pre></div>`}); out.innerHTML=html}
async function loadSafety(){const d=await api('/api/safety-policy'); renderJSON(d)}
function renderProject(d){out.innerHTML=`<h2>${esc(d.title)}</h2><p>${esc(d.concept)}</p><span class="badge">Status: ${esc(d.status)}</span><span class="badge">Approval required: ${d.requires_approval_before_public_action}</span><h3>Structure</h3>${(d.video_structure||[]).map(x=>`<div class="card"><b>${esc(x.time)}</b><p>${esc(x.goal)}</p></div>`).join('')}<h3>SEO</h3><pre>${esc(JSON.stringify(d.seo,null,2))}</pre><h3>Shorts</h3><pre>${esc(JSON.stringify(d.shorts,null,2))}</pre><h3>Thumbnail Prompt</h3><pre>${esc(d.thumbnail_prompt)}</pre>`}
</script>
</body>
</html>
"""

@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
