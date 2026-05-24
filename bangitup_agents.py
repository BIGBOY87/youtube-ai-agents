
import os,json,uuid,datetime
class SEOAgent:
    def generate(self,title,genre,mood="high energy"):
        clean=title.strip() or "New BANG IT UP MUSIC Track"
        return {"titles":[f"{clean} | Dark {genre} Mix 2026",f"{clean} | Night Drive {genre}",f"{clean} | BANG IT UP MUSIC"],"description":f"{clean} by BANG IT UP MUSIC. {genre} energy, dark atmosphere, heavy bass and underground club mood.","hashtags":["#BANGITUPMUSIC","#TechHouse","#EDM","#MelodicTechno"],"keywords":[genre,"dark techno","tech house 2026"]}
class ShortsAgent:
    def generate(self,title,genre): return {"source_title":title,"shorts":[{"hook":h,"caption":f"{h} — {title} #BANGITUPMUSIC","duration":"12-22s"} for h in ["Wait for the drop","This bassline gets darker","Would you play this at 2AM?"]]}
class DistributionAgent:
    def posts(self,title,genre): return {"youtube_community":f"New {genre} energy is coming.","instagram":f"{title} #BANGITUPMUSIC","tiktok":f"Wait for the drop. {title}"}
class CalendarAgent:
    def weekly(self): return [{"day":"Friday","task":"Publish/schedule at 19:00"}]
class GrowthAgent:
    def report(self,channel,videos): return {"summary":{"title":channel.get("snippet",{}).get("title"),"subscribers":channel.get("statistics",{}).get("subscriberCount")},"recommendations":[{"video":v.get("snippet",{}).get("title"),"views":v.get("statistics",{}).get("viewCount"),"recommendation":"Repurpose into Shorts"} for v in videos[:5]]}
class ThumbnailAgent:
    def prompt(self,title): return f"Dark neon club thumbnail for {title}"
class InitiativeEngine:
    def decide(self,channel,videos): return [{"priority":"high","action":"Generate MP4 visualizer and prepare private upload"}]
class VideoCreatorAgent:
    def create_project(self,title,genre):
        seo=SEOAgent().generate(title,genre)
        return {"id":str(uuid.uuid4())[:8],"title":seo["titles"][0],"genre":genre,"seo":seo,"thumbnail_prompt":ThumbnailAgent().prompt(title)}
class SchedulerAgent:
    def daily_plan(self): return {"evening":"Recommend publish around 19:00"}
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
    def approve(self,item_id): return {"status":"approved","id":item_id}
