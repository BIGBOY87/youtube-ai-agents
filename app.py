import os, json, datetime, random
from flask import Flask, jsonify, request, render_template_string, redirect
from youtube_client import YoutubeClient
from flask_upload_routes_patch import register_upload_routes
from bangitup_agents import GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent, InitiativeEngine, VideoCreatorAgent, ApprovalQueue, TrendHunter, ThumbnailAgent, SchedulerAgent, SafetyReviewer

app = Flask(__name__)

register_upload_routes(app)

yt = YouTubeClient()
queue = ApprovalQueue()

def missing_vars():
    return [k for k in ["YOUTUBE_API_KEY", "YOUTUBE_CHANNEL_ID"] if not os.getenv(k)]

@app.route('/')
def root():
    return redirect('/dashboard')

@app.route('/health')
def health():
    return jsonify({"status":"ok","service":"youtube-ai-agents-v8-autonomous","missing_required_vars":missing_vars(),"started_at":datetime.datetime.utcnow().isoformat()+"Z"})

@app.route('/api/channel')
def api_channel():
    try: return jsonify(yt.channel())
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route('/api/videos')
def api_videos():
    try: return jsonify(yt.recent_videos(max_results=int(request.args.get('max','12'))))
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route('/api/report')
def api_report():
    try:
        channel = yt.channel(); videos = yt.recent_videos(max_results=12)
        growth = GrowthAgent().report(channel, videos)
        initiatives = InitiativeEngine().decide(channel, videos)
        return jsonify({"channel": channel, "growth_report": growth, "initiatives": initiatives, "agent_status":{"growth": "active", "seo":"active", "shorts":"active", "initiative":"active", "video_creator":"active", "scheduler":"active", "safety":"active"}})
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route('/api/seo')
def api_seo():
    return jsonify(SEOAgent().generate(request.args.get('title','New BANG IT UP MUSIC Track'), request.args.get('genre','Tech House'), request.args.get('mood','dark energy')))

@app.route('/api/shorts')
def api_shorts():
    return jsonify(ShortsAgent().generate(request.args.get('title','New BANG IT UP MUSIC Track'), request.args.get('genre','Tech House')))

@app.route('/api/distribution')
def api_distribution():
    return jsonify(DistributionAgent().posts(request.args.get('title','New BANG IT UP MUSIC Track'), request.args.get('genre','Tech House')))

@app.route('/api/calendar')
def api_calendar():
    return jsonify(CalendarAgent().weekly())

@app.route('/api/trends')
def api_trends():
    return jsonify(TrendHunter().scan(request.args.get('genre','Tech House')))

@app.route('/api/create-video-project')
def api_create_video_project():
    title=request.args.get('title','Autonomous Dark Tech House Release')
    genre=request.args.get('genre','Tech House')
    project = VideoCreatorAgent().create_project(title, genre)
    reviewed = SafetyReviewer().review(project)
    item = queue.add({"type":"video_project", "project":project, "safety_review":reviewed, "status":"needs_approval"})
    return jsonify(item)

@app.route('/api/auto-run')
def api_auto_run():
    try:
        channel = yt.channel(); videos = yt.recent_videos(max_results=12)
        decisions = InitiativeEngine().decide(channel, videos)
        created=[]
        for action in decisions.get('actions', [])[:3]:
            if action.get('create') == 'shorts_package':
                vid_title = action.get('source_title','Recent BANG IT UP MUSIC video')
                item = queue.add({"type":"shorts_package", "source":vid_title, "assets":ShortsAgent().generate(vid_title, 'Tech House'), "status":"needs_approval"})
                created.append(item)
            if action.get('create') == 'video_concept':
                item = queue.add({"type":"video_project", "project":VideoCreatorAgent().create_project(action.get('title','New Dark Tech House Concept'), 'Tech House'), "status":"needs_approval"})
                created.append(item)
        if not created:
            item = queue.add({"type":"daily_growth_plan", "assets":CalendarAgent().weekly(), "status":"needs_approval"})
            created.append(item)
        return jsonify({"status":"completed", "created_items":created, "note":"Public actions remain blocked until you approve them."})
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route('/api/approval-queue')
def api_queue():
    return jsonify(queue.all())

@app.route('/api/approve/<item_id>', methods=['POST','GET'])
def api_approve(item_id):
    return jsonify(queue.approve(item_id))

@app.route('/api/scheduler')
def api_scheduler():
    return jsonify(SchedulerAgent().next_runs())

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD)

DASHBOARD = r'''<!doctype html><html><head><title>BANG IT UP MUSIC AI Agents v8</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#080912;--card:#151622;--muted:#9aa3b2;--txt:#f6f7fb;--p:#8b5cf6;--p2:#22d3ee;--ok:#22c55e;--warn:#f59e0b}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top,#1a1536,#080912 55%);color:var(--txt);font-family:Inter,Arial,sans-serif}.wrap{max-width:1180px;margin:auto;padding:28px}h1{font-size:34px;margin:0 0 8px}.sub{color:var(--muted);margin-bottom:22px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.card{background:linear-gradient(180deg,#191a29,#11121c);border:1px solid #2b2d3b;border-radius:18px;padding:18px;box-shadow:0 20px 50px #0006}.btn{background:linear-gradient(90deg,var(--p),#6d28d9);color:white;border:0;border-radius:12px;padding:11px 14px;font-weight:700;cursor:pointer;margin:4px}.btn.alt{background:#222436}.btn.good{background:linear-gradient(90deg,#16a34a,#22c55e)}input{background:#090a10;color:white;border:1px solid #33384a;border-radius:12px;padding:12px;margin:4px;min-width:220px}pre{white-space:pre-wrap;background:#090a10;border:1px solid #2a2d3a;border-radius:14px;padding:16px;max-height:520px;overflow:auto}.pill{display:inline-block;padding:6px 10px;border-radius:999px;background:#262a3c;color:#d8dcff;margin:3px}.video{display:flex;gap:14px;margin:12px 0;padding:12px;border:1px solid #2a2d3a;border-radius:14px;background:#0d0f18}.video img{width:170px;border-radius:10px}.kpi{font-size:28px;font-weight:800}.small{color:var(--muted);font-size:13px}.top{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}.status{color:var(--ok);font-weight:800}</style></head><body><div class="wrap"><div class="top"><div><h1>BANG IT UP MUSIC AI Agents v8</h1><div class="sub">Autonomous growth system with approval queue. No fake views. No spam. Public actions require approval.</div></div><div class="pill">● Agents Online</div></div>
<div class="grid"><div class="card"><h3>Core Checks</h3><button class="btn" onclick="load('/api/channel','channel')">Channel</button><button class="btn" onclick="load('/api/videos','videos')">Recent Videos</button><button class="btn" onclick="load('/api/report','report')">Growth Report</button></div><div class="card"><h3>Create Assets</h3><input id="title" value="New BANG IT UP MUSIC Track"><input id="genre" value="Tech House"><br><button class="btn" onclick="asset('/api/seo')">SEO</button><button class="btn" onclick="asset('/api/shorts')">Shorts</button><button class="btn" onclick="asset('/api/distribution')">Distribution</button></div><div class="card"><h3>Autonomous Mode</h3><button class="btn good" onclick="load('/api/auto-run','json')">Run Initiative Engine</button><button class="btn" onclick="load('/api/create-video-project','json')">Create Video Project</button><button class="btn alt" onclick="load('/api/approval-queue','queue')">Approval Queue</button></div><div class="card"><h3>Planning</h3><button class="btn" onclick="load('/api/calendar','json')">Calendar</button><button class="btn" onclick="load('/api/trends','json')">Trends</button><button class="btn" onclick="load('/api/scheduler','json')">Scheduler</button></div></div><div class="card" style="margin-top:16px"><h3>Output</h3><div id="out"><span class="small">Click an agent button.</span></div></div></div><script>
async function fetchJson(path){const r=await fetch(path); if(!r.ok) throw new Error(path+' '+r.status); return await r.json()}
function esc(s){return String(s??'').replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]))}
async function load(path,type){out.innerHTML='Loading...';try{const data=await fetchJson(path);render(data,type)}catch(e){out.innerHTML='<pre>'+esc(e)+'</pre>'}}
async function asset(base){const t=encodeURIComponent(title.value);const g=encodeURIComponent(genre.value);return load(`${base}?title=${t}&genre=${g}`,'json')}
function render(data,type){ if(type==='channel'){const s=data.statistics||{}, sn=data.snippet||{}; out.innerHTML=`<div class="grid"><div><div class="small">Channel</div><h2>${esc(sn.title)}</h2><p>${esc(sn.description||'')}</p></div><div><div class="kpi">${s.subscriberCount||0}</div><div class="small">Subscribers</div><div class="kpi">${s.viewCount||0}</div><div class="small">Views</div><div class="kpi">${s.videoCount||0}</div><div class="small">Videos</div></div></div>`;return}
 if(type==='videos'){out.innerHTML=(data||[]).map(v=>`<div class="video"><img src="${v.snippet?.thumbnails?.medium?.url||''}"><div><h3>${esc(v.snippet?.title)}</h3><div class="small">Views: ${v.statistics?.viewCount||0} · Likes: ${v.statistics?.likeCount||0} · Comments: ${v.statistics?.commentCount||0}</div><p>${esc((v.snippet?.description||'').slice(0,220))}</p></div></div>`).join('')||'No videos';return}
 if(type==='queue'){out.innerHTML=(data||[]).map(x=>`<div class="card"><span class="pill">${esc(x.status)}</span><h3>${esc(x.type)}</h3><pre>${esc(JSON.stringify(x,null,2))}</pre><button class="btn good" onclick="load('/api/approve/${x.id}','json')">Approve</button></div>`).join('')||'Approval queue is empty.';return}
 out.innerHTML='<pre>'+esc(JSON.stringify(data,null,2))+'</pre>'}
</script></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','10000')))
