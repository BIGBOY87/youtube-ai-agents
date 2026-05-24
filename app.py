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
body{font-family:Arial;background:#0b0b10;color:#f4f4f5;margin:0;padding:32px}.card{background:#171720;border:1px solid #2c2c36;border-radius:16px;padding:20px;margin:16px 0}a{color:#9d7cff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
</style></head><body><h1>BANG IT UP MUSIC AI Agents v2</h1><p class="ok">Service online.</p><div class="grid"><div class="card"><h3>Health</h3><a href="/health">/health</a></div><div class="card"><h3>Channel</h3><a href="/api/channel">/api/channel</a></div><div class="card"><h3>Recent Videos</h3><a href="/api/videos">/api/videos</a></div><div class="card"><h3>Full Report</h3><a href="/api/report">/api/report</a></div><div class="card"><h3>Dashboard</h3><a href="/dashboard">/dashboard</a></div></div></body></html>
""")


@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"youtube-ai-agents-v2","missing_required_vars":missing_vars()})


@app.route("/api/channel")
def api_channel():
    try:
        return jsonify(yt.channel())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/videos")
def api_videos():
    try:
        return jsonify(yt.recent_videos(max_results=int(request.args.get("max","10"))))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/report")
def api_report():
    try:
        channel = yt.channel()
        videos = yt.recent_videos(max_results=12)
        trend_agent = TrendAgent()
        trend_data = {}
        for q in trend_agent.query_list():
            try:
                trend_data[q] = yt.search_trends(q, max_results=5)
            except Exception:
                trend_data[q] = []
        return jsonify(orchestrator.full_report(channel, videos, trend_data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
        try:
            out.append({"channel_id":cid,"channel":yt.channel(channel_id=cid),"videos":yt.recent_videos(5, channel_id=cid)})
        except Exception as e:
            out.append({"channel_id":cid,"error":str(e)})
    return jsonify(out)


@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<!doctype html><html><head><title>BANG IT UP MUSIC Dashboard</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{font-family:Arial;background:#0b0b10;color:#f4f4f5;margin:0;padding:24px}.card{background:#171720;border:1px solid #2c2c36;border-radius:16px;padding:16px;margin:14px 0}button{padding:10px 14px;border:0;border-radius:10px;background:#7c3aed;color:white;font-weight:700;cursor:pointer}input{padding:10px;border-radius:10px;border:1px solid #333;background:#111;color:white;margin:4px;width:250px}pre{white-space:pre-wrap;background:#09090d;border-radius:10px;padding:14px}.video{display:flex;gap:14px;align-items:flex-start;border:1px solid #333;border-radius:14px;padding:12px;margin:12px 0;background:#11111a}.video img{width:220px;max-width:40%;border-radius:10px}.stat{display:inline-block;margin:6px 12px 6px 0;padding:8px 10px;border-radius:999px;background:#24243a}.muted{color:#b8b8c6}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.asset{border:1px solid #333;border-radius:12px;padding:12px;background:#11111a;margin:10px 0}
</style></head><body><h1>BANG IT UP MUSIC AI Agents Dashboard</h1>
<div class="card"><button onclick="load('/api/channel')">Channel</button> <button onclick="load('/api/videos')">Recent Videos</button> <button onclick="load('/api/report')">Full Growth Report</button> <button onclick="load('/api/calendar')">Calendar</button></div>
<div class="card"><h3>Generate Campaign Assets</h3><input id="title" placeholder="Track title" value="New BANG IT UP MUSIC Track"><input id="genre" placeholder="Genre" value="EDM"><button onclick="load('/api/seo?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">SEO</button><button onclick="load('/api/shorts?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Shorts</button><button onclick="load('/api/distribution?title='+encodeURIComponent(title.value)+'&genre='+encodeURIComponent(genre.value))">Distribution</button></div>
<div id="out" class="card">Click a button.</div>
<script>
function esc(x){return String(x ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function stat(label,value){return `<span class="stat"><b>${esc(label)}:</b> ${esc(value ?? '0')}</span>`;}
function pre(data){return `<pre>${esc(JSON.stringify(data,null,2))}</pre>`;}

async function load(path){
  const out=document.getElementById('out');
  out.innerHTML='Loading...';
  try{
    const r=await fetch(path);
    const data=await r.json();
    if(!r.ok || data.error){ out.innerHTML='<h3>Error</h3>'+pre(data); return; }

    if(path.includes('/api/channel')){
      const s=data.snippet||{}; const st=data.statistics||{}; const img=s.thumbnails?.medium?.url || s.thumbnails?.default?.url || '';
      out.innerHTML=`<h2>${esc(s.title||'Channel')}</h2>${img?`<img src="${esc(img)}" style="width:180px;border-radius:14px">`:''}<p class="muted">${esc(s.description||'')}</p><div>${stat('Subscribers',st.subscriberCount)}${stat('Views',st.viewCount)}${stat('Videos',st.videoCount)}</div>`;
      return;
    }

    if(path.includes('/api/videos')){
      let arr=Array.isArray(data)?data:[];
      let html=`<h2>Recent Videos</h2><p class="muted">${arr.length} videos loaded from YouTube API.</p>`;
      arr.forEach(v=>{ const sn=v.snippet||{}; const st=v.statistics||{}; const img=sn.thumbnails?.medium?.url || sn.thumbnails?.default?.url || ''; html+=`<div class="video">${img?`<img src="${esc(img)}">`:''}<div><h3>${esc(sn.title||'Untitled')}</h3><p class="muted">${esc(sn.publishedAt||'')}</p><p>${esc((sn.description||'').slice(0,260))}</p><div>${stat('Views',st.viewCount)}${stat('Likes',st.likeCount)}${stat('Comments',st.commentCount)}</div></div></div>`; });
      out.innerHTML=html; return;
    }

    if(path.includes('/api/seo') || path.includes('/api/shorts') || path.includes('/api/distribution') || path.includes('/api/calendar') || path.includes('/api/report')){
      out.innerHTML='<h2>Agent Output</h2>'+renderObject(data);
      return;
    }

    out.innerHTML=pre(data);
  }catch(e){out.innerHTML='<h3>Frontend Error</h3><pre>'+esc(e.toString())+'</pre>';}
}
function renderObject(obj){
  if(Array.isArray(obj)) return obj.map(x=>`<div class="asset">${renderObject(x)}</div>`).join('');
  if(obj && typeof obj==='object'){
    return Object.entries(obj).map(([k,v])=>`<div class="asset"><h3>${esc(k)}</h3>${typeof v==='object'?renderObject(v):`<p>${esc(v)}</p>`}</div>`).join('');
  }
  return `<p>${esc(obj)}</p>`;
}
</script></body></html>
""")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","10000")))
