
import os, json, uuid, datetime

def _int(v):
    try: return int(v)
    except Exception: return 0

def _genre(text):
    t=(text or "").lower()
    if "melodic" in t: return "Melodic Techno"
    if "future house" in t: return "Future House"
    if "edm" in t: return "EDM"
    if "techno" in t: return "Techno"
    return "Tech House"

class SEOAgent:
    def generate(self,title,genre,mood="high energy"):
        clean=title.strip() or "New BANG IT UP MUSIC Track"
        return {"titles":[f"{clean} | Dark {genre} Mix 2026",f"{clean} | Night Drive {genre}",f"{clean} | BANG IT UP MUSIC"],"description":f"{clean} by BANG IT UP MUSIC. {genre} energy, dark atmosphere, heavy bass and underground club mood. Subscribe for weekly underground releases.","hashtags":["#BANGITUPMUSIC","#TechHouse","#EDM","#MelodicTechno","#NightDrive"],"keywords":[genre,"dark techno","tech house 2026","underground music"]}

class ShortsAgent:
    def generate(self,title,genre):
        hooks=["Wait for the drop","This bassline gets darker","Would you play this at 2AM?","Night drive energy","Underground club mood"]
        return {"source_title":title,"shorts":[{"hook":h,"caption":f"{h} — {title} #BANGITUPMUSIC #{genre.replace(' ','')}","duration":"12-22s","format":"9:16 vertical","suggested_cut":"Use strongest drop / most energetic 15-25 sec"} for h in hooks]}

class ShortWorkflowAgent:
    def make_short_task(self,video):
        s=video.get("snippet",{}); st=video.get("statistics",{})
        title=s.get("title","Untitled"); desc=s.get("description",""); vid=video.get("id")
        genre=_genre(title+" "+desc); seo=SEOAgent().generate(title,genre)
        return {"task_id":str(uuid.uuid4())[:8],"source_video":{"video_id":vid,"youtube_url":f"https://www.youtube.com/watch?v={vid}","title":title,"views":_int(st.get("viewCount"))},"required_input":"original local MP4 or direct Short MP4 URL","local_command_example":f'python local_short_factory.py --input "C:\\\\Videos\\\\SOURCE.mp4" --title "{title[:40]}" --start 30 --duration 20',"upload_endpoint":"/api/shorts/upload-from-url","short_upload_template":{"title":seo["titles"][1]+" #Shorts","description":seo["description"]+"\\n\\n#Shorts #BANGITUPMUSIC","tags":[x.replace("#","") for x in seo["hashtags"]]+["Shorts"],"privacy_status":"private","own_content_confirmed":True},"shorts_package":ShortsAgent().generate(title,genre)}
    def batch(self,videos):
        tasks=[self.make_short_task(v) for v in videos]
        tasks.sort(key=lambda x:x["source_video"]["views"])
        return {"status":"short_tasks_created","count":len(tasks),"items":tasks}

class GrowthAgent:
    def report(self,channel,videos):
        return {"summary":{"title":channel.get("snippet",{}).get("title"),"subscribers":channel.get("statistics",{}).get("subscriberCount")},"recommendations":[{"video_id":v.get("id"),"title":v.get("snippet",{}).get("title"),"views":_int(v.get("statistics",{}).get("viewCount")),"recommendation":"Create local Short and upload private"} for v in videos[:10]]}

class InitiativeEngine:
    def decide(self,channel,videos): return [{"priority":"high","action":"Run /api/shorts/tasks, cut local MP4 with local_short_factory.py, upload private Short"}]

class ApprovalQueue:
    def __init__(self,path="approval_queue.json"): self.path=path
    def _load(self):
        if not os.path.exists(self.path): return []
        try: return json.load(open(self.path,"r",encoding="utf-8"))
        except Exception: return []
    def _save(self,rows): json.dump(rows,open(self.path,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    def add(self,item):
        rows=self._load(); item.setdefault("id",str(uuid.uuid4())[:8]); rows.insert(0,item); self._save(rows); return item
    def list(self): return self._load()
