import os
import json
import math
import datetime as dt
from typing import Any, Dict, List, Optional

import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "").strip()
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "").strip()
AUTO_MODE = os.getenv("AUTO_MODE", "false").lower() == "true"

YT_BASE = "https://www.googleapis.com/youtube/v3"


def _missing_vars() -> List[str]:
    missing = []
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "placeholder":
        missing.append("YOUTUBE_API_KEY")
    if not YOUTUBE_CHANNEL_ID or YOUTUBE_CHANNEL_ID == "placeholder":
        missing.append("YOUTUBE_CHANNEL_ID")
    return missing


def yt_get(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if _missing_vars():
        raise RuntimeError("Missing required YouTube environment variables")
    params = dict(params)
    params["key"] = YOUTUBE_API_KEY
    r = requests.get(f"{YT_BASE}/{endpoint}", params=params, timeout=20)
    if r.status_code >= 400:
        raise RuntimeError(f"YouTube API error {r.status_code}: {r.text[:500]}")
    return r.json()


def get_channel() -> Dict[str, Any]:
    data = yt_get("channels", {
        "part": "snippet,statistics,brandingSettings,contentDetails",
        "id": YOUTUBE_CHANNEL_ID,
        "maxResults": 1,
    })
    items = data.get("items", [])
    if not items:
        raise RuntimeError("Channel not found. Check YOUTUBE_CHANNEL_ID.")
    return items[0]


def get_recent_videos(limit: int = 12) -> List[Dict[str, Any]]:
    search = yt_get("search", {
        "part": "snippet",
        "channelId": YOUTUBE_CHANNEL_ID,
        "order": "date",
        "type": "video",
        "maxResults": min(limit, 25),
    })
    ids = [x["id"]["videoId"] for x in search.get("items", []) if x.get("id", {}).get("videoId")]
    if not ids:
        return []
    videos = yt_get("videos", {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(ids),
        "maxResults": len(ids),
    })
    return videos.get("items", [])


def n_int(x: Any) -> int:
    try:
        return int(x)
    except Exception:
        return 0


def format_video_card(v: Dict[str, Any]) -> Dict[str, Any]:
    sn = v.get("snippet", {})
    st = v.get("statistics", {})
    thumbs = sn.get("thumbnails", {})
    thumb = (thumbs.get("medium") or thumbs.get("high") or thumbs.get("default") or {}).get("url", "")
    return {
        "id": v.get("id"),
        "title": sn.get("title", "Untitled"),
        "publishedAt": sn.get("publishedAt", ""),
        "thumbnail": thumb,
        "views": n_int(st.get("viewCount")),
        "likes": n_int(st.get("likeCount")),
        "comments": n_int(st.get("commentCount")),
        "description": sn.get("description", "")[:300],
        "url": f"https://www.youtube.com/watch?v={v.get('id')}",
    }


def generate_seo(title: str, genre: str = "EDM") -> Dict[str, Any]:
    base = title.strip() or "New BANG IT UP MUSIC Track"
    genre = genre.strip() or "EDM"
    power_words = ["Official Visualizer", "Bass Boosted", "Club Mix", "Dark Energy", "Underground Mix"]
    titles = [
        f"{base} | {genre} {power_words[0]}",
        f"{base} - {genre} Track for Night Drives",
        f"{base} | Dark {genre} / Industrial Club Energy",
        f"BANG IT UP MUSIC - {base} ({genre} Mix)",
        f"{base} | Viral {genre} Beat 2026",
    ]
    hashtags = ["#BANGITUPMUSIC", f"#{genre.replace(' ', '')}", "#NewMusic", "#ElectronicMusic", "#MusicProducer", "#ClubMusic", "#BassMusic", "#YouTubeMusic", "#Shorts", "#ViralMusic", "#EDM", "#TechHouse"]
    tags = ["BANG IT UP MUSIC", base, genre, "new music", "electronic music", "club music", "industrial tech house", "bass music", "music 2026", "youtube music", "viral song", "edm mix", "producer", "underground music", "night drive music"]
    description = f"""{base} by BANG IT UP MUSIC.

A high-energy {genre} release built for clubs, night drives, gym sessions and underground playlists.

Listen, comment your favorite part, and subscribe for more new drops from BANG IT UP MUSIC.

Follow the channel:
https://www.youtube.com/@BANGITUPMUSIC

Hashtags:
{' '.join(hashtags[:8])}
"""
    return {
        "titles": titles,
        "description": description,
        "hashtags": hashtags,
        "tags": tags,
        "pinned_comment": f"Which part of {base} hits hardest? Drop a timestamp and subscribe for the next release.",
        "thumbnail_text": [base.upper()[:24], "DARK CLUB ENERGY", "NEW DROP"],
    }


def generate_shorts(title: str, genre: str = "EDM") -> Dict[str, Any]:
    title = title.strip() or "New BANG IT UP MUSIC Track"
    hooks = [
        f"Wait for the drop in {title}...",
        "This bassline changes the whole mood.",
        "POV: midnight drive, full volume.",
        "Industrial club energy in 15 seconds.",
        "This part deserves headphones.",
        "When the beat finally opens up.",
        "Dark room. Heavy bass. No talking.",
        "Save this for your night playlist.",
    ]
    captions = [
        f"{title} is out now. Full track on BANG IT UP MUSIC.",
        f"New {genre} energy. Link in channel.",
        "Would you play this in the club?",
        "Drop a 🔥 if this hits.",
    ]
    plan = [
        {"short": 1, "angle": "drop teaser", "length": "12-18s", "cta": "Full version on YouTube"},
        {"short": 2, "angle": "bassline loop", "length": "8-12s", "cta": "Save for later"},
        {"short": 3, "angle": "visualizer moment", "length": "15-25s", "cta": "Comment your timestamp"},
        {"short": 4, "angle": "night drive vibe", "length": "10-20s", "cta": "Subscribe for more"},
    ]
    return {"hooks": hooks, "captions": captions, "shorts_plan": plan}


def distribution_pack(title: str, genre: str = "EDM") -> Dict[str, Any]:
    title = title.strip() or "New BANG IT UP MUSIC Track"
    return {
        "youtube_community": f"New drop from BANG IT UP MUSIC: {title}. Should the next one go darker, faster, or more melodic?",
        "instagram": f"{title} is out now. Dark {genre} energy from BANG IT UP MUSIC. #BANGITUPMUSIC #NewMusic #{genre.replace(' ', '')}",
        "tiktok": f"POV: the beat kicks in at midnight. {title} by BANG IT UP MUSIC. #{genre.replace(' ', '')} #newmusic #bass",
        "x": f"New BANG IT UP MUSIC release: {title}. Dark {genre} energy. Listen on YouTube.",
        "reddit_safe": f"I released a new {genre} track called {title}. Looking for honest feedback on the mix, drop, and visualizer. No spam — feedback welcome.",
        "discord": f"New track live: {title}. If you like dark {genre}/club energy, check it out and tell me which timestamp hits hardest.",
    }


def growth_report() -> Dict[str, Any]:
    channel = get_channel()
    videos = get_recent_videos(10)
    cards = [format_video_card(v) for v in videos]
    total_recent_views = sum(v["views"] for v in cards)
    avg_views = math.floor(total_recent_views / max(len(cards), 1))
    top = sorted(cards, key=lambda x: x["views"], reverse=True)[:3]
    recommendations = []
    if avg_views < 1000:
        recommendations.append("Increase Shorts output: 2-3 Shorts per full track for 14 days.")
    recommendations.append("Use the best-performing title patterns from the top 3 videos for the next upload.")
    recommendations.append("Add a pinned comment asking for timestamp feedback to increase comments.")
    recommendations.append("Create one Community poll per release: darker / faster / melodic / club version.")
    recommendations.append("Repurpose every visualizer into 4 Shorts: drop, intro vibe, bassline, final hook.")
    return {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "channel": {
            "title": channel.get("snippet", {}).get("title"),
            "subscribers": n_int(channel.get("statistics", {}).get("subscriberCount")),
            "views": n_int(channel.get("statistics", {}).get("viewCount")),
            "videos": n_int(channel.get("statistics", {}).get("videoCount")),
        },
        "recent_average_views": avg_views,
        "top_recent_videos": top,
        "recommendations": recommendations,
        "safe_autonomy": {
            "auto_allowed": ["analytics reports", "SEO drafts", "Shorts ideas", "content calendar", "distribution drafts"],
            "approval_required": ["uploads", "title/description changes", "comment replies", "public posts"],
            "blocked": ["fake views", "fake subscribers", "spam comments", "mass DMs", "artificial engagement"],
        },
    }


def calendar_plan() -> List[Dict[str, str]]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tasks = [
        "Publish 1 Short from latest track",
        "Community poll: choose next vibe",
        "Upload/prepare full track or visualizer",
        "Comment engagement: reply to real comments",
        "Release teaser Short with hook",
        "Playlist/outreach research without spam",
        "Weekly analytics review and next plan",
    ]
    return [{"day": d, "task": t, "status": "planned"} for d, t in zip(days, tasks)]



def initiative_engine() -> Dict[str, Any]:
    """Creates safe autonomous work items when the channel needs action.
    It never performs uploads, comments, title edits, or public posts directly.
    """
    report = growth_report()
    top_titles = [v["title"] for v in report.get("top_recent_videos", [])]
    avg = report.get("recent_average_views", 0)
    subs = report.get("channel", {}).get("subscribers", 0)
    now = dt.datetime.utcnow().isoformat() + "Z"
    initiatives: List[Dict[str, Any]] = []

    # Always useful autonomous drafts
    initiatives.append({
        "id": "daily-growth-report",
        "priority": "high",
        "status": "auto_created_draft",
        "agent": "Daily Growth Agent",
        "trigger": "Daily channel check",
        "action": "Create daily growth report and recommendation set",
        "output": report.get("recommendations", []),
        "requires_approval": False,
    })

    if avg < 1000:
        initiatives.append({
            "id": "shorts-boost-campaign",
            "priority": "high",
            "status": "auto_created_draft",
            "agent": "Shorts Factory Agent",
            "trigger": f"Recent average views are {avg}",
            "action": "Create 7-day Shorts boost campaign from best tracks",
            "output": [
                "Post 2 Shorts/day for 7 days",
                "Use the top 3 recent tracks as source material",
                "Hook in first 1.5 seconds",
                "CTA: Full track on BANG IT UP MUSIC",
            ],
            "requires_approval": False,
        })

    initiatives.append({
        "id": "seo-refresh",
        "priority": "medium",
        "status": "needs_approval",
        "agent": "SEO Agent",
        "trigger": "Weekly metadata optimization window",
        "action": "Draft new SEO titles/descriptions for low-performing videos",
        "output": generate_seo(top_titles[0] if top_titles else "New BANG IT UP MUSIC Track", "Industrial Tech House"),
        "requires_approval": True,
        "reason": "Changing titles/descriptions is public-facing and should be approved.",
    })

    initiatives.append({
        "id": "community-poll",
        "priority": "medium",
        "status": "needs_approval",
        "agent": "Community Agent",
        "trigger": "Audience engagement needed",
        "action": "Draft a YouTube Community poll",
        "output": {
            "poll": "What should the next BANG IT UP MUSIC drop be?",
            "options": ["Darker", "Faster", "More melodic", "Harder bass"],
        },
        "requires_approval": True,
        "reason": "Public posting requires approval.",
    })

    initiatives.append({
        "id": "collab-research",
        "priority": "low",
        "status": "auto_created_draft",
        "agent": "Collaboration Agent",
        "trigger": "Weekly organic reach expansion",
        "action": "Prepare collaboration/outreach templates without sending them automatically",
        "output": [
            "Find 10 similar music channels/playlists manually or via future search integration",
            "Send only personalized non-spam messages",
            "Offer a remix, playlist swap, or honest feedback exchange",
        ],
        "requires_approval": False,
    })

    return {
        "generated_at": now,
        "mode": "controlled_autonomy",
        "auto_mode_enabled": AUTO_MODE,
        "summary": "The agent creates drafts and work items automatically when action is useful. Risky public actions remain locked behind approval.",
        "initiatives": initiatives,
        "hard_blocks": [
            "fake views",
            "fake subscribers",
            "spam comments",
            "mass DMs",
            "artificial engagement",
            "unapproved public uploads/posts",
        ],
    }


def automation_schedule() -> List[Dict[str, Any]]:
    return [
        {"time": "09:00", "agent": "Daily Growth Agent", "task": "Read channel stats and create report", "mode": "auto_draft"},
        {"time": "10:00", "agent": "Trend/SEO Agent", "task": "Create SEO and keyword opportunities", "mode": "auto_draft"},
        {"time": "12:00", "agent": "Shorts Agent", "task": "Generate 2 Shorts concepts from top/recent tracks", "mode": "auto_draft"},
        {"time": "18:00", "agent": "Community Agent", "task": "Draft community post or poll", "mode": "approval_required"},
        {"time": "21:00", "agent": "Review Agent", "task": "Summarize actions waiting for approval", "mode": "auto_draft"},
    ]


def safe_action_policy() -> Dict[str, Any]:
    return {
        "auto_create_without_approval": [
            "analytics reports",
            "SEO drafts",
            "Shorts ideas",
            "distribution copy drafts",
            "calendar tasks",
            "approval queue items",
            "collaboration templates",
        ],
        "approval_required_before_execution": [
            "upload video",
            "schedule public video",
            "change video title/description/tags",
            "reply to comments",
            "post community update",
            "post to external platforms",
        ],
        "blocked_forever": [
            "fake views/subscribers",
            "comment spam",
            "mass DMs",
            "engagement pods/bots",
            "misleading metadata unrelated to the music",
        ],
    }


@app.route("/")
def root():
    return Response("""<!doctype html><html><head><meta http-equiv='refresh' content='0;url=/dashboard'></head><body>Redirecting to <a href='/dashboard'>dashboard</a></body></html>""", mimetype="text/html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "missing_required_vars": _missing_vars(), "auto_mode": AUTO_MODE})


@app.route("/api/channel")
def api_channel():
    try:
        return jsonify(get_channel())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/videos")
def api_videos():
    try:
        limit = int(request.args.get("limit", 12))
        return jsonify(get_recent_videos(limit))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/report")
def api_report():
    try:
        return jsonify(growth_report())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/seo")
def api_seo():
    return jsonify(generate_seo(request.args.get("title", ""), request.args.get("genre", "EDM")))


@app.route("/api/shorts")
def api_shorts():
    return jsonify(generate_shorts(request.args.get("title", ""), request.args.get("genre", "EDM")))


@app.route("/api/distribution")
def api_distribution():
    return jsonify(distribution_pack(request.args.get("title", ""), request.args.get("genre", "EDM")))


@app.route("/api/calendar")
def api_calendar():
    return jsonify(calendar_plan())


@app.route("/api/approval-queue")
def api_approval():
    title = request.args.get("title", "New BANG IT UP MUSIC Track")
    genre = request.args.get("genre", "EDM")
    return jsonify([
        {"type": "SEO Update", "status": "needs_approval", "action": "Apply suggested title/description", "risk": "medium", "preview": generate_seo(title, genre)["titles"][0]},
        {"type": "Shorts Campaign", "status": "safe_auto_draft", "action": "Create 4 Shorts ideas", "risk": "low", "preview": generate_shorts(title, genre)["hooks"][0]},
        {"type": "Community Post", "status": "needs_approval", "action": "Post poll to YouTube Community", "risk": "medium", "preview": distribution_pack(title, genre)["youtube_community"]},
        {"type": "Upload", "status": "locked", "action": "Upload/schedule video", "risk": "high", "preview": "Requires OAuth upload scope and explicit approval."},
    ])


@app.route("/api/initiatives")
def api_initiatives():
    try:
        return jsonify(initiative_engine())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/automation-schedule")
def api_automation_schedule():
    return jsonify(automation_schedule())


@app.route("/api/safety-policy")
def api_safety_policy():
    return jsonify(safe_action_policy())


@app.route("/dashboard")
def dashboard():
    return Response(DASHBOARD_HTML, mimetype="text/html")


DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>BANG IT UP MUSIC AI Agents v4</title>
<style>
:root{--bg:#080812;--panel:#111326;--panel2:#171a33;--text:#f4f6ff;--muted:#9aa3c7;--line:#2a2f55;--pink:#ff2bd6;--cyan:#28e8ff;--green:#42f58d;--orange:#ffb84d;--red:#ff5f73}
*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,Segoe UI,Arial;background:radial-gradient(circle at 20% 0%,#24104d 0,#080812 35%),radial-gradient(circle at 90% 15%,#0b4b58 0,#080812 28%);color:var(--text)}
a{color:var(--cyan)}.wrap{max-width:1180px;margin:0 auto;padding:24px}.hero{display:grid;grid-template-columns:1.25fr .75fr;gap:18px;margin-bottom:18px}.card{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.035));border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 22px 70px rgba(0,0,0,.32);backdrop-filter: blur(10px)}
.brand{font-size:13px;color:var(--cyan);letter-spacing:.16em;text-transform:uppercase}.h1{font-size:42px;line-height:1.02;margin:8px 0 10px;font-weight:900}.sub{color:var(--muted);max-width:720px;line-height:1.55}.pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.pill{border:1px solid var(--line);background:#0c0f20;border-radius:99px;padding:8px 10px;color:#cbd2ff;font-size:13px}.status{display:grid;gap:10px}.status .row{display:flex;justify-content:space-between;border-bottom:1px solid #24294c;padding:8px 0;color:var(--muted)}.ok{color:var(--green);font-weight:800}.grid{display:grid;grid-template-columns:280px 1fr;gap:18px}.side{position:sticky;top:16px;height:fit-content}.input{width:100%;padding:12px 14px;border:1px solid var(--line);background:#0b0e1e;color:var(--text);border-radius:14px;margin:7px 0 12px}button{width:100%;border:0;border-radius:14px;padding:12px 14px;margin:6px 0;background:linear-gradient(135deg,var(--pink),#6b5cff);color:white;font-weight:800;cursor:pointer}button.secondary{background:#151936;border:1px solid var(--line);color:#dfe5ff}button:hover{filter:brightness(1.08)}.out{min-height:520px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.metric{background:var(--panel2);border:1px solid var(--line);border-radius:18px;padding:16px}.metric .num{font-size:28px;font-weight:900}.metric .label{color:var(--muted);font-size:13px}.video{overflow:hidden}.video img{width:100%;border-radius:14px;border:1px solid var(--line)}.video h3{font-size:15px;line-height:1.25}.video p{color:var(--muted);font-size:13px}.list{display:grid;gap:10px}.item{background:#101429;border:1px solid var(--line);border-radius:16px;padding:14px}.item strong{color:#fff}.tag{display:inline-block;background:#0c2440;border:1px solid #195473;color:#c9f7ff;border-radius:999px;padding:5px 8px;margin:4px;font-size:12px}.risk-low{color:var(--green)}.risk-medium{color:var(--orange)}.risk-high{color:var(--red)}pre{white-space:pre-wrap;background:#080b18;border:1px solid var(--line);border-radius:16px;padding:14px;overflow:auto}.copy{width:auto;padding:8px 10px;font-size:12px;margin-left:8px;background:#20264a}.footer{color:var(--muted);font-size:12px;margin-top:20px;text-align:center}@media(max-width:850px){.hero,.grid{grid-template-columns:1fr}.h1{font-size:32px}.side{position:relative;top:0}}
</style>
</head>
<body>
<div class="wrap">
  <section class="hero">
    <div class="card">
      <div class="brand">BANG IT UP MUSIC · AI Growth OS v5</div>
      <div class="h1">Autonomous YouTube AI Agents</div>
      <div class="sub">A safe initiative engine for organic YouTube growth: it detects when action is needed, creates campaigns/drafts automatically, and keeps public actions behind approval. No fake views, no fake subscribers, no spam.</div>
      <div class="pills"><span class="pill">SEO Agent</span><span class="pill">Shorts Agent</span><span class="pill">Growth Agent</span><span class="pill">Approval Mode</span><span class="pill">Render Live</span><span class="pill">Initiative Engine</span></div>
    </div>
    <div class="card status" id="statusBox"><div class="row"><span>Server</span><span class="ok">checking...</span></div></div>
  </section>
  <section class="grid">
    <aside class="card side">
      <label>Track title</label>
      <input class="input" id="title" value="New BANG IT UP MUSIC Track" />
      <label>Genre</label>
      <input class="input" id="genre" value="Industrial Tech House" />
      <button onclick="loadChannel()">Channel</button>
      <button onclick="loadVideos()">Recent Videos</button>
      <button onclick="loadReport()">Full Growth Report</button>
      <button onclick="loadSEO()">SEO Agent</button>
      <button onclick="loadShorts()">Shorts Agent</button>
      <button onclick="loadDistribution()">Distribution Agent</button>
      <button onclick="loadCalendar()">Content Calendar</button>
      <button onclick="loadApproval()">Approval Queue</button>
      <button onclick="loadInitiatives()">Initiative Engine</button>
      <button onclick="loadSchedule()">Auto Schedule</button>
      <button onclick="loadSafety()">Safety Policy</button>
      <button class="secondary" onclick="window.open('/health','_blank')">Health Check</button>
    </aside>
    <main class="card out" id="out"><h2>Ready.</h2><p class="sub">Choose an agent from the left. The system will read your YouTube API data and generate safe growth actions.</p></main>
  </section>
  <div class="footer">Controlled autonomy: drafts and reports can be automated. Uploads, public posts, title changes and comment replies require approval.</div>
</div>
<script>
const out=document.getElementById('out');
const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const fmt=n=>Number(n||0).toLocaleString();
async function api(path){const r=await fetch(path); const j=await r.json(); if(!r.ok) throw new Error(j.error||r.statusText); return j;}
function params(){return `title=${encodeURIComponent(document.getElementById('title').value)}&genre=${encodeURIComponent(document.getElementById('genre').value)}`}
async function init(){try{const h=await api('/health');document.getElementById('statusBox').innerHTML=`<div class="row"><span>Server</span><span class="ok">OK</span></div><div class="row"><span>Missing vars</span><span>${esc(h.missing_required_vars.join(', ')||'none')}</span></div><div class="row"><span>Auto mode</span><span>${h.auto_mode?'ON':'OFF'}</span></div>`}catch(e){document.getElementById('statusBox').innerHTML=`<div class="row"><span>Server</span><span class="risk-high">ERROR</span></div><pre>${esc(e.message)}</pre>`}}
function loading(name){out.innerHTML=`<h2>${name}</h2><p class="sub">Loading...</p>`}
function error(e){out.innerHTML=`<h2>Error</h2><pre>${esc(e.message||e)}</pre>`}
async function loadChannel(){loading('Channel');try{const c=await api('/api/channel');const s=c.statistics||{}, sn=c.snippet||{}, th=((sn.thumbnails||{}).medium||(sn.thumbnails||{}).default||{}).url||'';out.innerHTML=`<h2>${esc(sn.title)}</h2><div class="cards"><div class="metric"><div class="num">${fmt(s.subscriberCount)}</div><div class="label">Subscribers</div></div><div class="metric"><div class="num">${fmt(s.viewCount)}</div><div class="label">Total views</div></div><div class="metric"><div class="num">${fmt(s.videoCount)}</div><div class="label">Videos</div></div></div><br>${th?`<img src="${esc(th)}" style="border-radius:18px;border:1px solid var(--line)">`:''}<p class="sub">${esc(sn.description||'')}</p>`}catch(e){error(e)}}
async function loadVideos(){loading('Recent Videos');try{const data=await api('/api/videos?limit=12');out.innerHTML=`<h2>Recent Videos</h2><div class="cards">${data.map(v=>{const sn=v.snippet||{}, st=v.statistics||{}, th=((sn.thumbnails||{}).medium||(sn.thumbnails||{}).default||{}).url||'';return `<div class="metric video"><img src="${esc(th)}"><h3>${esc(sn.title)}</h3><p>Views: ${fmt(st.viewCount)} · Likes: ${fmt(st.likeCount)} · Comments: ${fmt(st.commentCount)}</p><a target="_blank" href="https://youtube.com/watch?v=${esc(v.id)}">Open video</a></div>`}).join('')}</div>`}catch(e){error(e)}}
async function loadReport(){loading('Growth Report');try{const r=await api('/api/report');out.innerHTML=`<h2>Full Growth Report</h2><div class="cards"><div class="metric"><div class="num">${fmt(r.channel.subscribers)}</div><div class="label">Subscribers</div></div><div class="metric"><div class="num">${fmt(r.channel.views)}</div><div class="label">Channel views</div></div><div class="metric"><div class="num">${fmt(r.recent_average_views)}</div><div class="label">Avg recent views</div></div></div><h3>Recommendations</h3><div class="list">${r.recommendations.map(x=>`<div class="item">${esc(x)}</div>`).join('')}</div><h3>Top Recent Videos</h3><div class="cards">${r.top_recent_videos.map(v=>`<div class="metric video"><img src="${esc(v.thumbnail)}"><h3>${esc(v.title)}</h3><p>${fmt(v.views)} views</p></div>`).join('')}</div><h3>Safety Rules</h3><pre>${esc(JSON.stringify(r.safe_autonomy,null,2))}</pre>`}catch(e){error(e)}}
async function loadSEO(){loading('SEO Agent');try{const s=await api('/api/seo?'+params());out.innerHTML=`<h2>SEO Agent</h2><h3>Titles</h3><div class="list">${s.titles.map(x=>`<div class="item"><strong>${esc(x)}</strong></div>`).join('')}</div><h3>Description <button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('desc').innerText)">Copy</button></h3><pre id="desc">${esc(s.description)}</pre><h3>Hashtags</h3>${s.hashtags.map(x=>`<span class="tag">${esc(x)}</span>`).join('')}<h3>Tags</h3><pre>${esc(s.tags.join(', '))}</pre><h3>Pinned Comment</h3><div class="item">${esc(s.pinned_comment)}</div>`}catch(e){error(e)}}
async function loadShorts(){loading('Shorts Agent');try{const s=await api('/api/shorts?'+params());out.innerHTML=`<h2>Shorts Agent</h2><h3>Hooks</h3><div class="list">${s.hooks.map(x=>`<div class="item">${esc(x)}</div>`).join('')}</div><h3>Shorts Plan</h3><div class="cards">${s.shorts_plan.map(x=>`<div class="metric"><strong>Short #${x.short}</strong><p>${esc(x.angle)}</p><p class="sub">${esc(x.length)} · ${esc(x.cta)}</p></div>`).join('')}</div><h3>Captions</h3><pre>${esc(s.captions.join('\n'))}</pre>`}catch(e){error(e)}}
async function loadDistribution(){loading('Distribution Agent');try{const d=await api('/api/distribution?'+params());out.innerHTML=`<h2>Distribution Agent</h2><div class="list">${Object.entries(d).map(([k,v])=>`<div class="item"><strong>${esc(k)}</strong><p>${esc(v)}</p></div>`).join('')}</div>`}catch(e){error(e)}}
async function loadCalendar(){loading('Content Calendar');try{const c=await api('/api/calendar');out.innerHTML=`<h2>7-Day Content Calendar</h2><div class="list">${c.map(x=>`<div class="item"><strong>${esc(x.day)}</strong><p>${esc(x.task)}</p><span class="tag">${esc(x.status)}</span></div>`).join('')}</div>`}catch(e){error(e)}}
async function loadApproval(){loading('Approval Queue');try{const q=await api('/api/approval-queue?'+params());out.innerHTML=`<h2>Approval Queue</h2><p class="sub">This is where autonomous actions become safe. The agent drafts; you approve risky public actions.</p><div class="list">${q.map(x=>`<div class="item"><strong>${esc(x.type)}</strong> · <span class="risk-${esc(x.risk)}">${esc(x.risk)}</span><p>${esc(x.action)}</p><p class="sub">Status: ${esc(x.status)}</p><pre>${esc(x.preview)}</pre></div>`).join('')}</div>`}catch(e){error(e)}}

async function loadInitiatives(){loading('Initiative Engine');try{const d=await api('/api/initiatives');out.innerHTML=`<h2>Initiative Engine</h2><p class="sub">${esc(d.summary)}</p><div class="cards"><div class="metric"><div class="num">${d.initiatives.length}</div><div class="label">Created initiatives</div></div><div class="metric"><div class="num">${d.auto_mode_enabled?'ON':'SAFE'}</div><div class="label">Autonomy mode</div></div></div><h3>Created Work Items</h3><div class="list">${d.initiatives.map(x=>`<div class="item"><strong>${esc(x.agent)}</strong> · <span class="tag">${esc(x.priority)}</span><p><b>Trigger:</b> ${esc(x.trigger)}</p><p><b>Action:</b> ${esc(x.action)}</p><p class="sub">Status: ${esc(x.status)} · Approval: ${x.requires_approval?'required':'not required'}</p><pre>${esc(typeof x.output==='string'?x.output:JSON.stringify(x.output,null,2))}</pre></div>`).join('')}</div><h3>Hard Blocks</h3>${d.hard_blocks.map(x=>`<span class="tag">${esc(x)}</span>`).join('')}` }catch(e){error(e)}}
async function loadSchedule(){loading('Auto Schedule');try{const s=await api('/api/automation-schedule');out.innerHTML=`<h2>Daily Auto Schedule</h2><p class="sub">These are recurring jobs the agent can prepare automatically. Public actions stay in approval mode.</p><div class="list">${s.map(x=>`<div class="item"><strong>${esc(x.time)} · ${esc(x.agent)}</strong><p>${esc(x.task)}</p><span class="tag">${esc(x.mode)}</span></div>`).join('')}</div>`}catch(e){error(e)}}
async function loadSafety(){loading('Safety Policy');try{const p=await api('/api/safety-policy');out.innerHTML=`<h2>Safety Policy</h2><div class="cards"><div class="metric"><h3>Auto Draft</h3>${p.auto_create_without_approval.map(x=>`<span class="tag">${esc(x)}</span>`).join('')}</div><div class="metric"><h3>Needs Approval</h3>${p.approval_required_before_execution.map(x=>`<span class="tag">${esc(x)}</span>`).join('')}</div><div class="metric"><h3>Blocked</h3>${p.blocked_forever.map(x=>`<span class="tag">${esc(x)}</span>`).join('')}</div></div>`}catch(e){error(e)}}

init();
</script>
</body></html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
