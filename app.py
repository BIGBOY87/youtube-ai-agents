import os
from flask import Flask, jsonify, request, render_template_string
from youtube_client import YouTubeClient
from bangitup_agents import ReportOrchestrator, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent, CollaborationAgent, TrendAgent

app = Flask(__name__)
yt = YouTubeClient()
orchestrator = ReportOrchestrator()

def missing_vars():
    return [k for k in ["YOUTUBE_API_KEY", "YOUTUBE_CHANNEL_ID"] if not os.getenv(k)]

@app.route("/")
def index():
    return render_template_string("""
<!doctype html><html><head><title>BANG IT UP MUSIC AI Agents v2</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{font-family:Arial;background:#0b0b10;color:#f4f4f5;margin:0;padding:32px}.card{background:#171720;border:1px solid #2c2c36;border-radius:16px;padding:20px;margin:16px 0}a{color:#9d7cff}.ok{color:#61d394}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
</style></head><body><h1>BANG IT UP MUSIC AI Agents v2</h1><p class="ok">Service online.</p><div class="grid"><div class="card"><h3>Health</h3><a href="/health">/health</a></div><div class="card"><h3>Channel</h3><a href="/api/channel">/api/channel</a></div><div class="card"><h3>Recent Videos</h3><a href="/api/videos">/api/videos</a></div><div class="card"><h3>Full Report</h3><a href="/api/report">/api/report</a></div><div class="card"><h3>Dashboard</h3><a href="/dashboard">/dashboard</a></div></div></body></html>
""")

@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"youtube-ai-agents-v2","missing_required_vars":missing_vars()})

@app.route("/api/channel")
def api_channel():
    try: return jsonify(yt.channel())
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route("/api/videos")
def api_videos():
    try: return jsonify(yt.recent_videos(max_results=int(request.args.get("max","10"))))
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route("/api/report")
def api_report():
    try:
        channel = yt.channel(); videos = yt.recent_videos(max_results=12)
        trend_agent = TrendAgent(); trend_data = {}
        for q in trend_agent.query_list():
            try: trend_data[q] = yt.search_trends(q, max_results=5)
            except Exception: trend_data[q] = []
        return jsonify(orchestrator.full_report(channel, videos, trend_data))
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route("/api/seo")
def api_seo():
    return jsonify(SEOAgent().generate(request.args.get("title","New Music Release"), request.args.get("genre","music"), request.args.get("mood","high energy")))

@app.route("/api/shorts")
def api_shorts():
    return jsonify(ShortsAgent().generate(request.args.get("title","New Music Release"), request.args.get("genre","music")))

@app.route("/api/distribution")
def api_distribution():
    return jsonify(DistributionAgent().posts(request.args.get("title","New Music Release"), request.args.get("genre","music")))

@app.route("/api/calendar")
def api_calendar():
    return jsonify(CalendarAgent().weekly())

@app.route("/api/collaboration")
def api_collaboration():
    return jsonify(CollaborationAgent().suggest(request.args.get("genre","music")))

@app.route("/api/competitors")
def api_competitors():
    ids = [x.strip() for x in os.getenv("COMPETITOR_CHANNEL_IDS","").split(",") if x.strip()]
    out=[]
    for cid in ids:
        try: out.append({"channel_id":cid,"channel":yt.channel(channel_id=cid),"videos":yt.recent_videos(5, channel_id=cid)})
        except Exception as e: out.append({"channel_id":cid,"error":str(e)})
    return jsonify(out)

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<!doctype html><html><head><title>BANG IT UP MUSIC Dashboard</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{font-family:Arial;background:#0b0b10;color:#f4f4f5;margin:0;padding:24px}.card{background:#171720;border:1px solid #2c2c36;border-radius:16px;padding:16px;margin:14px 0}button{padding:10px 14px;border-radius:10px;border:0;background:#7c3aed;color:white;cursor:pointer}pre{white-space:pre-wrap;background:#0e0e14;padding:16px;border-radius:12px;overflow:auto;max-height:500px}input{padding:10px;border-radius:10px;border:1px solid #333;background:#111;color:white;margin:4px;width:250px}
</style></head><body><h1>BANG IT UP MUSIC AI Agents Dashboard</h1><div class="card"><button onclick="load('/api/channel')">Channel</button><button onclick="load('/api/videos')">Recent Videos</button><button onclick="load('/api/report')">Full Growth Report</button><button onclick="load('/api/calendar')">Calendar</button></div><div class="card"><h3>Generate Campaign Assets</h3><input id="title" placeholder="Track title" value="New BANG IT UP MUSIC Track"><input id="genre" placeholder="Genre" value="EDM"><button onclick="load('/api/seo?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">SEO</button><button onclick="load('/api/shorts?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Shorts</button><button onclick="load('/api/distribution?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Distribution</button></div><pre id="out">Click a button.</pre><script>async function load(path){out.textContent='Loading...';try{const r=await fetch(path);const j=await r.json();out.textContent=JSON.stringify(j,null,2)}catch(e){out.textContent=e.toString()}}</script></body></html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","10000")))
