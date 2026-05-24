import os
import json
import datetime
import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
COMPETITOR_CHANNEL_IDS = [x.strip() for x in os.getenv("COMPETITOR_CHANNEL_IDS", "").split(",") if x.strip()]

YOUTUBE_BASE = "https://www.googleapis.com/youtube/v3"

def missing_vars():
    return [k for k in ["YOUTUBE_API_KEY", "YOUTUBE_CHANNEL_ID"] if not os.getenv(k)]

def yt_get(endpoint, params):
    params = dict(params)
    params["key"] = YOUTUBE_API_KEY
    r = requests.get(f"{YOUTUBE_BASE}/{endpoint}", params=params, timeout=20)
    if not r.ok:
        return {"error": r.text, "status_code": r.status_code}
    return r.json()

def channel(channel_id=None):
    cid = channel_id or YOUTUBE_CHANNEL_ID
    data = yt_get("channels", {
        "part": "snippet,statistics,brandingSettings,contentDetails",
        "id": cid
    })
    items = data.get("items", [])
    if not items:
        return {"error": "Channel not found", "raw": data}
    return items[0]

def recent_videos(max_results=10, channel_id=None):
    cid = channel_id or YOUTUBE_CHANNEL_ID
    search = yt_get("search", {
        "part": "snippet",
        "channelId": cid,
        "order": "date",
        "type": "video",
        "maxResults": max_results
    })
    ids = [i["id"]["videoId"] for i in search.get("items", []) if i.get("id", {}).get("videoId")]
    if not ids:
        return []
    details = yt_get("videos", {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(ids)
    })
    return details.get("items", [])

def safe_int(x):
    try:
        return int(x)
    except Exception:
        return 0

def video_score(v):
    s = v.get("statistics", {})
    views = safe_int(s.get("viewCount"))
    likes = safe_int(s.get("likeCount"))
    comments = safe_int(s.get("commentCount"))
    return views + likes * 20 + comments * 50

def top_videos(videos, limit=5):
    return sorted(videos, key=video_score, reverse=True)[:limit]

def fallback_seo(title, genre, mood="high energy"):
    title = title or "New BANG IT UP MUSIC Track"
    genre = genre or "EDM"
    keywords = [genre, "tech house", "melodic techno", "dark club music", "festival vibe", "BANG IT UP MUSIC"]
    return {
        "agent": "SEO Agent",
        "titles": [
            f"{title} | {genre} Anthem 2026",
            f"{title} - Dark {genre} / Club Mix",
            f"{title} | BANG IT UP MUSIC Official Release",
            f"{genre} Energy: {title}",
            f"{title} | Underground {genre} Music"
        ],
        "description": (
            f"{title} by BANG IT UP MUSIC.\n\n"
            f"Original {genre} track with {mood} energy, heavy bass and night-drive atmosphere.\n\n"
            "Subscribe for weekly Tech House, Melodic Techno, EDM and underground festival vibes.\n"
            "Turn it up. Feel it. Bang it up."
        ),
        "hashtags": ["#BANGITUPMUSIC", "#EDM", "#TechHouse", "#MelodicTechno", "#DarkTechno", "#FestivalMusic", "#ClubMusic", "#ElectronicMusic", "#NewMusic", "#Music2026"],
        "tags": keywords + ["new music", "underground music", "bass", "night drive", "cyberpunk music"],
        "pinned_comment": f"Where should this track be played: club, car, gym, or festival? 🔥"
    }

def fallback_shorts(title, genre):
    title = title or "New Track"
    genre = genre or "EDM"
    hooks = [
        f"Wait for the bass drop in {title}.",
        f"This {genre} drop hits harder at night.",
        "Use headphones for this one.",
        "POV: the club lights turn red.",
        "Would you play this at 2AM?"
    ]
    return {
        "agent": "Shorts Agent",
        "shorts": [
            {"hook": h, "caption": f"{title} | {genre} energy. #Shorts #BANGITUPMUSIC", "length": "12-20 sec"}
            for h in hooks
        ]
    }

def fallback_distribution(title, genre):
    return {
        "agent": "Distribution Agent",
        "tiktok": f"{title} is built for late-night {genre} energy. Would you play this? #edm #techhouse",
        "instagram": f"New BANG IT UP MUSIC release: {title}. Dark energy, heavy bass, underground vibe.",
        "facebook": f"New track from BANG IT UP MUSIC: {title}. Listen and tell us where this belongs: club, car, gym, or festival.",
        "x": f"{title} // {genre} // BANG IT UP MUSIC. Turn it up.",
        "reddit_safe": f"I produce {genre}/electronic music under BANG IT UP MUSIC. I’d appreciate feedback on this track: {title}."
    }

def calendar():
    return {
        "agent": "Content Planner Agent",
        "weekly_plan": [
            {"day": "Monday", "task": "Publish 1 Short from strongest drop", "goal": "Retention test"},
            {"day": "Tuesday", "task": "Community post: poll about next genre", "goal": "Engagement"},
            {"day": "Wednesday", "task": "Upload full track or visualizer", "goal": "Watch time"},
            {"day": "Thursday", "task": "Post behind-the-scenes / DAW screenshot", "goal": "Artist identity"},
            {"day": "Friday", "task": "Release 2 Shorts during evening hours", "goal": "Discovery"},
            {"day": "Saturday", "task": "Comment on 10 relevant music channels, no spam", "goal": "Organic discovery"},
            {"day": "Sunday", "task": "Review views, likes, comments and plan next track", "goal": "Optimization"}
        ]
    }

def build_report():
    ch = channel()
    vids = recent_videos(12)
    tops = top_videos(vids, 5)
    stats = ch.get("statistics", {}) if isinstance(ch, dict) else {}
    return {
        "agent": "Growth Report Agent",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "channel": {
            "title": ch.get("snippet", {}).get("title"),
            "subscribers": stats.get("subscriberCount"),
            "views": stats.get("viewCount"),
            "video_count": stats.get("videoCount")
        },
        "top_recent_videos": [
            {
                "title": v.get("snippet", {}).get("title"),
                "views": v.get("statistics", {}).get("viewCount", "0"),
                "likes": v.get("statistics", {}).get("likeCount", "0"),
                "comments": v.get("statistics", {}).get("commentCount", "0"),
                "recommendation": "Make 2 Shorts from this style and reuse the best keywords."
            } for v in tops
        ],
        "recommendations": [
            "Keep titles under 65 characters with genre + mood + brand.",
            "Create Shorts from the first 8 seconds and from the strongest drop.",
            "Use consistent tags: Tech House, Melodic Techno, Dark Techno, EDM, Club Music.",
            "Add a pinned comment question to increase comment velocity.",
            "Publish Shorts within 24 hours after each full track."
        ]
    }

def competitors():
    out = []
    for cid in COMPETITOR_CHANNEL_IDS:
        try:
            out.append({"channel": channel(cid), "recent_videos": recent_videos(5, cid)})
        except Exception as e:
            out.append({"channel_id": cid, "error": str(e)})
    return out

@app.route("/")
def index():
    return render_template_string("""
<!doctype html><html><head><title>BANG IT UP MUSIC AI Agents v3</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#0b0b10;color:#f4f4f5;margin:0;padding:32px}
.card{background:#171720;border:1px solid #2c2c36;border-radius:16px;padding:20px;margin:16px 0}
a{color:#a78bfa}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
</style></head><body>
<h1>BANG IT UP MUSIC AI Agents v3</h1>
<p>Service online. Use the dashboard below.</p>
<div class="grid">
<div class="card"><h3>Dashboard</h3><a href="/dashboard">/dashboard</a></div>
<div class="card"><h3>Health</h3><a href="/health">/health</a></div>
<div class="card"><h3>Channel</h3><a href="/api/channel">/api/channel</a></div>
<div class="card"><h3>Videos</h3><a href="/api/videos">/api/videos</a></div>
<div class="card"><h3>Report</h3><a href="/api/report">/api/report</a></div>
</div></body></html>
""")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "youtube-ai-agents-v3", "missing_required_vars": missing_vars(), "started_at": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/api/channel")
def api_channel():
    try:
        return jsonify(channel())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/videos")
def api_videos():
    try:
        max_results = int(request.args.get("max", "10"))
        return jsonify(recent_videos(max_results=max_results))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/report")
def api_report():
    try:
        return jsonify(build_report())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/seo")
def api_seo():
    return jsonify(fallback_seo(request.args.get("title", "New BANG IT UP MUSIC Track"), request.args.get("genre", "EDM"), request.args.get("mood", "high energy")))

@app.route("/api/shorts")
def api_shorts():
    return jsonify(fallback_shorts(request.args.get("title", "New Track"), request.args.get("genre", "EDM")))

@app.route("/api/distribution")
def api_distribution():
    return jsonify(fallback_distribution(request.args.get("title", "New Track"), request.args.get("genre", "EDM")))

@app.route("/api/calendar")
def api_calendar():
    return jsonify(calendar())

@app.route("/api/competitors")
def api_competitors():
    return jsonify(competitors())

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<!doctype html><html><head><title>BANG IT UP MUSIC AI Agents Dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#08080d;color:#f5f5f5;margin:0;padding:24px}
h1{font-size:28px}.card{background:#171720;border:1px solid #30303a;border-radius:16px;padding:16px;margin:14px 0}
button{background:#7c3aed;color:#fff;border:0;border-radius:10px;padding:10px 14px;margin:4px;cursor:pointer;font-weight:bold}
input{background:#0e0e12;color:#fff;border:1px solid #333;border-radius:8px;padding:10px;margin:4px;min-width:240px}
pre{white-space:pre-wrap;background:#0f0f14;border-radius:12px;padding:14px}
.video{display:flex;gap:14px;border:1px solid #333;border-radius:12px;padding:10px;margin:10px 0;background:#101018}
.video img{width:180px;border-radius:8px}.muted{color:#b5b5c3}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
</style></head><body>
<h1>BANG IT UP MUSIC AI Agents Dashboard</h1>
<div class="card">
<button onclick="load('/api/channel')">Channel</button>
<button onclick="load('/api/videos')">Recent Videos</button>
<button onclick="load('/api/report')">Full Growth Report</button>
<button onclick="load('/api/calendar')">Calendar</button>
<button onclick="load('/api/competitors')">Competitors</button>
</div>
<div class="card">
<h3>Generate Campaign Assets</h3>
<input id="title" value="New BANG IT UP MUSIC Track" placeholder="Track title">
<input id="genre" value="EDM" placeholder="Genre">
<input id="mood" value="high energy" placeholder="Mood">
<button onclick="load('/api/seo?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value)+'&mood='+encodeURIComponent(mood.value))">SEO</button>
<button onclick="load('/api/shorts?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Shorts</button>
<button onclick="load('/api/distribution?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Distribution</button>
</div>
<div id="out" class="card">Click a button.</div>
<script>
const out = document.getElementById("out");
function esc(x){return String(x ?? "").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
function renderChannel(data){
  const s=data.statistics||{}, sn=data.snippet||{};
  out.innerHTML = `<h2>${esc(sn.title)}</h2>
  <p class="muted">${esc(sn.description||"")}</p>
  <div class="grid">
    <div class="card"><b>Subscribers</b><br>${esc(s.subscriberCount||"hidden")}</div>
    <div class="card"><b>Total Views</b><br>${esc(s.viewCount||"0")}</div>
    <div class="card"><b>Videos</b><br>${esc(s.videoCount||"0")}</div>
  </div>`;
}
function renderVideos(data){
  let html="<h2>Recent Videos</h2>";
  data.forEach(v=>{
    const sn=v.snippet||{}, st=v.statistics||{}, th=sn.thumbnails?.medium?.url || sn.thumbnails?.default?.url || "";
    html += `<div class="video">${th?`<img src="${esc(th)}">`:""}<div>
      <h3>${esc(sn.title)}</h3>
      <p class="muted">${esc((sn.description||"").slice(0,220))}</p>
      <p>Views: ${esc(st.viewCount||"0")} | Likes: ${esc(st.likeCount||"0")} | Comments: ${esc(st.commentCount||"0")}</p>
      <p><b>Agent Suggestion:</b> Make 2 Shorts from this title/style and reuse the top genre keywords.</p>
    </div></div>`;
  });
  out.innerHTML=html;
}
function renderReport(data){
  let html=`<h2>Growth Report</h2><div class="grid">
    <div class="card"><b>Subscribers</b><br>${esc(data.channel?.subscribers)}</div>
    <div class="card"><b>Views</b><br>${esc(data.channel?.views)}</div>
    <div class="card"><b>Videos</b><br>${esc(data.channel?.video_count)}</div>
  </div><h3>Top Recent Videos</h3>`;
  (data.top_recent_videos||[]).forEach(v=>{html+=`<div class="card"><b>${esc(v.title)}</b><br>Views: ${esc(v.views)} | Likes: ${esc(v.likes)} | Comments: ${esc(v.comments)}<br>${esc(v.recommendation)}</div>`});
  html += "<h3>Recommendations</h3><ul>"+(data.recommendations||[]).map(r=>`<li>${esc(r)}</li>`).join("")+"</ul>";
  out.innerHTML=html;
}
function renderCalendar(data){
  out.innerHTML="<h2>Weekly Content Calendar</h2>"+(data.weekly_plan||[]).map(x=>`<div class="card"><b>${esc(x.day)}</b><br>${esc(x.task)}<br><span class="muted">${esc(x.goal)}</span></div>`).join("");
}
function renderGeneric(data){out.innerHTML="<pre>"+esc(JSON.stringify(data,null,2))+"</pre>";}
async function load(path){
  out.innerHTML="Loading...";
  try{
    const r=await fetch(path);
    const data=await r.json();
    if(path.includes("/api/channel")) return renderChannel(data);
    if(path.includes("/api/videos")) return renderVideos(data);
    if(path.includes("/api/report")) return renderReport(data);
    if(path.includes("/api/calendar")) return renderCalendar(data);
    return renderGeneric(data);
  }catch(e){out.innerHTML="<b>Error:</b> "+esc(e.toString());}
}
</script></body></html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
