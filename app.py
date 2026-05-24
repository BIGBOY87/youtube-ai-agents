
import os, datetime
from flask import Flask, jsonify, request, redirect, render_template_string
from youtube_client import YouTubeClient
from bangitup_agents import GrowthAgent, SEOAgent, ShortsAgent, DistributionAgent, CalendarAgent, InitiativeEngine, VideoCreatorAgent, ApprovalQueue, SchedulerAgent
from upload_routes import register_upload_routes
from video_generator import generate_visualizer_video

app=Flask(__name__)
yt=YouTubeClient(); queue=ApprovalQueue(); register_upload_routes(app)

@app.route("/")
def root(): return redirect("/dashboard")
@app.route("/health")
def health(): return jsonify({"status":"ok","service":"youtube-ai-agents-v11-video-generator-upload","started_at":datetime.datetime.utcnow().isoformat()+"Z"})
@app.route("/api/channel")
def api_channel():
    try: return jsonify(yt.channel())
    except Exception as e: return jsonify({"error":str(e)}),500
@app.route("/api/videos")
def api_videos():
    try: return jsonify(yt.recent_videos(int(request.args.get("max","12"))))
    except Exception as e: return jsonify({"error":str(e)}),500
@app.route("/api/report")
def api_report():
    try:
        c=yt.channel(); v=yt.recent_videos(12)
        return jsonify({"growth_report":GrowthAgent().report(c,v),"initiatives":InitiativeEngine().decide(c,v),"agent_status":{"video_generator":"active","upload":"active"}})
    except Exception as e: return jsonify({"error":str(e)}),500
@app.route("/api/seo")
def api_seo(): return jsonify(SEOAgent().generate(request.args.get("title","New Track"),request.args.get("genre","Tech House")))
@app.route("/api/shorts")
def api_shorts(): return jsonify(ShortsAgent().generate(request.args.get("title","New Track"),request.args.get("genre","Tech House")))
@app.route("/api/distribution")
def api_distribution(): return jsonify(DistributionAgent().posts(request.args.get("title","New Track"),request.args.get("genre","Tech House")))
@app.route("/api/calendar")
def api_calendar(): return jsonify(CalendarAgent().weekly())
@app.route("/api/generate-video")
def api_generate_video():
    try:
        title=request.args.get("title","BANG IT UP MUSIC - Night Drive"); genre=request.args.get("genre","Tech House")
        seconds=max(5,min(int(request.args.get("seconds","20")),60))
        video_file=generate_visualizer_video(title,genre,seconds)
        seo=SEOAgent().generate(title,genre)
        project={"title":seo["titles"][0],"description":seo["description"],"tags":[x.replace("#","") for x in seo["hashtags"]],"category_id":"10","privacy_status":request.args.get("privacy","private"),"video_file":video_file,"own_content_confirmed":True}
        queue.add({"type":"generated_video","status":"ready_for_upload","project":project})
        return jsonify({"status":"video_generated","project":project})
    except Exception as e: return jsonify({"error":str(e)}),500
@app.route("/api/auto-run")
def api_auto_run():
    title=request.args.get("title","Autonomous Dark Tech House Night Drive Concept"); genre="Tech House"
    if os.getenv("AUTO_GENERATE_MP4","false").lower()=="true":
        video_file=generate_visualizer_video(title,genre,int(os.getenv("AUTO_VIDEO_SECONDS","20")))
        seo=SEOAgent().generate(title,genre)
        project={"title":seo["titles"][0],"description":seo["description"],"tags":[x.replace("#","") for x in seo["hashtags"]],"category_id":"10","privacy_status":os.getenv("DEFAULT_UPLOAD_PRIVACY","private"),"video_file":video_file,"own_content_confirmed":True}
    else:
        project=VideoCreatorAgent().create_project(title,genre)
    item={"created_at":datetime.datetime.utcnow().isoformat()+"Z","type":"auto_run","status":"ready_for_upload","project":project}
    queue.add(item); return jsonify({"status":"completed","created_items":[item]})
@app.route("/api/approval-queue")
def api_queue(): return jsonify(queue.list())
@app.route("/dashboard")
def dashboard(): return render_template_string("""<h1>BANG IT UP MUSIC AI Agents v11</h1><button onclick="go('/api/generate-video?title=Test%20Track&genre=Tech%20House&seconds=20')">Generate MP4</button><button onclick="go('/api/upload/status')">Upload Status</button><button onclick="go('/api/auto-run')">Auto Run</button><pre id=o>Ready</pre><script>async function go(p){o.textContent='Loading';let r=await fetch(p);o.textContent=JSON.stringify(await r.json(),null,2)}</script>""")
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","10000")))
