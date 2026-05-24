import datetime, uuid, json, os

class GrowthAgent:
    def report(self, channel, videos):
        recs=[]
        for v in videos[:5]:
            title=v.get("snippet",{}).get("title","Untitled")
            views=int(v.get("statistics",{}).get("viewCount","0") or 0)
            recs.append({"video":title,"views":views,"recommendation":"Repurpose this into 2 Shorts and test a stronger thumbnail/title variant." if views<100 else "Use this format as a reference for the next upload."})
        return {"summary":{"title":channel.get("snippet",{}).get("title"),"subscribers":channel.get("statistics",{}).get("subscriberCount"),"views":channel.get("statistics",{}).get("viewCount"),"videoCount":channel.get("statistics",{}).get("videoCount")},"recommendations":recs,"next_actions":["Create one Shorts package from the best-performing recent video.","Prepare one new video concept in the approval queue.","Review titles with stronger first 45 characters.","Post one community prompt asking listeners what style they want next."]}

class SEOAgent:
    def generate(self,title,genre,mood="high energy"):
        clean=title.strip() or "New BANG IT UP MUSIC Track"
        return {"titles":[f"{clean} | Dark {genre} Mix 2026",f"{clean} | Night Drive {genre}",f"{clean} | BANG IT UP MUSIC",f"{clean} | Underground {genre} Release",f"{clean} | Heavy Bass {genre} Anthem"],"description":f"{clean} by BANG IT UP MUSIC. {genre} energy, dark atmosphere, heavy bass and underground club mood. Subscribe for weekly music releases.","hashtags":["#BANGITUPMUSIC","#TechHouse","#EDM","#MelodicTechno","#UndergroundMusic","#BassMusic","#NightDrive"],"keywords":[genre,"dark techno","tech house 2026","underground club music","bass drop"]}

class ShortsAgent:
    def generate(self,title,genre):
        hooks=["Wait for the drop","This bassline gets darker","Would you play this at 2AM?","Headphones recommended","Underground club energy"]
        return {"source_title":title,"shorts":[{"hook":h,"caption":f"{h} — {title} #BANGITUPMUSIC #{genre.replace(' ','')}","duration":"12-22s"} for h in hooks]}

class DistributionAgent:
    def posts(self,title,genre):
        return {"youtube_community":f"New {genre} energy is coming. Which vibe should BANG IT UP MUSIC drop next?","instagram":f"{title} — dark {genre} energy. #BANGITUPMUSIC","tiktok":f"Wait for the drop. {title}. #{genre.replace(' ','')} #EDM","x":f"{title} is built for night drives and underground speakers.","discord":f"New BANG IT UP MUSIC concept ready: {title}. Feedback welcome."}

class CalendarAgent:
    def weekly(self):
        return [{"day":"Monday","task":"Review analytics and pick strongest recent track."},{"day":"Tuesday","task":"Create 2 Shorts from the selected track."},{"day":"Wednesday","task":"Publish community post / poll."},{"day":"Thursday","task":"Prepare next video title, thumbnail prompt and description."},{"day":"Friday","task":"Publish main video or schedule for 19:00."},{"day":"Saturday","task":"Push Shorts and distribution captions."},{"day":"Sunday","task":"Review performance and create next queue item."}]

class ThumbnailAgent:
    def prompt(self,title): return f"High contrast dark neon club thumbnail for {title}, bold readable title, purple/cyan accents, industrial underground mood."

class InitiativeEngine:
    def decide(self,channel,videos):
        return [{"priority":"high","action":"Create a Shorts package from the latest track."},{"priority":"medium","action":"Generate 3 SEO title variants for low-view videos."},{"priority":"medium","action":"Prepare one new autonomous video concept for approval."}]

class VideoCreatorAgent:
    def create_project(self,title,genre):
        seo=SEOAgent().generate(title,genre); shorts=ShortsAgent().generate(title,genre); thumb=ThumbnailAgent().prompt(title)
        return {"id":str(uuid.uuid4())[:8],"created_at":datetime.datetime.utcnow().isoformat()+"Z","concept":f"A dark high-energy {genre} release for night drives and underground club listeners.","title":seo["titles"][0],"genre":genre,"script":"Intro hook 0-3s, main drop preview 3-15s, visualizer section 15-45s, CTA 45-55s.","seo":seo,"shorts_package":shorts,"thumbnail_prompt":thumb,"upload_metadata":{"privacy":"private_until_approved","suggested_time":"19:00 local time"}}

class SchedulerAgent:
    def daily_plan(self):
        return {"morning":"Check analytics and create one queue item if latest video underperforms.","afternoon":"Generate Shorts captions and distribution copy.","evening":"Recommend publishing/scheduling window around 19:00."}

class ApprovalQueue:
    def __init__(self,path="approval_queue.json"): self.path=path
    def _load(self):
        if not os.path.exists(self.path): return []
        try:
            with open(self.path,"r",encoding="utf-8") as f: return json.load(f)
        except Exception: return []
    def _save(self,rows):
        with open(self.path,"w",encoding="utf-8") as f: json.dump(rows,f,ensure_ascii=False,indent=2)
    def add(self,item):
        rows=self._load()
        if "id" not in item: item["id"]=str(uuid.uuid4())[:8]
        rows.insert(0,item); self._save(rows); return item
    def list(self): return self._load()
    def approve(self,item_id):
        rows=self._load()
        for row in rows:
            if row.get("id")==item_id:
                row["status"]="approved"; row["approved_at"]=datetime.datetime.utcnow().isoformat()+"Z"; self._save(rows); return row
        return {"error":"item not found"}
