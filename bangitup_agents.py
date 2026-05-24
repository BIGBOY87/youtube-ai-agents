
import os
import json
import uuid
import datetime

def _int(v):
    try:
        return int(v)
    except Exception:
        return 0

def _genre_from_text(text):
    t = (text or "").lower()
    if "melodic" in t:
        return "Melodic Techno"
    if "future house" in t:
        return "Future House"
    if "edm" in t:
        return "EDM"
    if "techno" in t:
        return "Techno"
    return "Tech House"

class SEOAgent:
    def generate(self, title, genre, mood="high energy"):
        clean = title.strip() or "New BANG IT UP MUSIC Track"
        return {
            "titles": [
                f"{clean} | Dark {genre} Mix 2026",
                f"{clean} | Night Drive {genre}",
                f"{clean} | BANG IT UP MUSIC"
            ],
            "description": f"{clean} by BANG IT UP MUSIC. {genre} energy, dark atmosphere, heavy bass and underground club mood. Subscribe for weekly underground releases.",
            "hashtags": ["#BANGITUPMUSIC", "#TechHouse", "#EDM", "#MelodicTechno", "#NightDrive"],
            "keywords": [genre, "dark techno", "tech house 2026", "underground music"]
        }

class ShortsAgent:
    def generate(self, title, genre):
        hooks = [
            "Wait for the drop",
            "This bassline gets darker",
            "Would you play this at 2AM?",
            "Night drive energy",
            "Underground club mood"
        ]
        return {
            "source_title": title,
            "shorts": [
                {
                    "hook": h,
                    "caption": f"{h} — {title} #BANGITUPMUSIC #{genre.replace(' ', '')}",
                    "duration": "12-22s",
                    "format": "9:16 vertical",
                    "cta": "Subscribe for weekly underground energy",
                    "suggested_cut": "Use the strongest drop or most energetic 15-25 second section."
                }
                for h in hooks
            ]
        }

class ShortWorkflowAgent:
    def make_short_task(self, video):
        s = video.get("snippet", {})
        st = video.get("statistics", {})
        title = s.get("title", "Untitled")
        desc = s.get("description", "")
        video_id = video.get("id")
        genre = _genre_from_text(title + " " + desc)
        views = _int(st.get("viewCount"))
        likes = _int(st.get("likeCount"))
        comments = _int(st.get("commentCount"))
        seo = SEOAgent().generate(title, genre)
        shorts = ShortsAgent().generate(title, genre)

        priority = "high" if views < 100 else "medium" if views < 1000 else "scale"
        return {
            "task_id": str(uuid.uuid4())[:8],
            "source_video": {
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "views": views,
                "likes": likes,
                "comments": comments
            },
            "priority": priority,
            "required_input": "original MP4 direct URL for this source video",
            "cannot_do": "YouTube API does not provide the uploaded MP4 file. Provide your original MP4/direct URL.",
            "short_upload_template": {
                "title": seo["titles"][1] + " #Shorts",
                "description": seo["description"] + "\\n\\n#Shorts #BANGITUPMUSIC",
                "tags": [x.replace("#", "") for x in seo["hashtags"]] + ["Shorts"],
                "category_id": "10",
                "privacy_status": "private",
                "own_content_confirmed": True
            },
            "shorts_package": shorts,
            "action": "Use /api/shorts/upload-from-url with a direct MP4 URL of the already-cut vertical Short."
        }

    def batch(self, videos):
        tasks = [self.make_short_task(v) for v in videos]
        tasks.sort(key=lambda x: x["source_video"]["views"])
        return {
            "status": "short_tasks_created",
            "count": len(tasks),
            "items": tasks
        }

class DistributionAgent:
    def posts(self, title, genre):
        return {
            "youtube_community": f"Which part of {title} should become the next Short?",
            "instagram": f"{title} — dark {genre} energy. #BANGITUPMUSIC",
            "tiktok": f"Wait for the drop. {title}. #{genre.replace(' ', '')} #EDM"
        }

class GrowthAgent:
    def report(self, channel, videos):
        recs = []
        for v in videos[:10]:
            s = v.get("snippet", {})
            st = v.get("statistics", {})
            views = _int(st.get("viewCount"))
            recs.append({
                "video_id": v.get("id"),
                "title": s.get("title"),
                "views": views,
                "priority": "high" if views < 100 else "medium" if views < 1000 else "scale",
                "recommendation": "Create Short task and upload private test Short."
            })
        return {
            "summary": {
                "title": channel.get("snippet", {}).get("title"),
                "subscribers": channel.get("statistics", {}).get("subscriberCount"),
                "views": channel.get("statistics", {}).get("viewCount"),
                "videos": channel.get("statistics", {}).get("videoCount"),
            },
            "recommendations": recs
        }

class CalendarAgent:
    def weekly(self):
        return [{"day": "Friday", "task": "Publish/schedule Shorts around 19:00"}]

class InitiativeEngine:
    def decide(self, channel, videos):
        return [{"priority": "high", "action": "Run /api/shorts/tasks and create Shorts from low-view existing videos."}]

class ApprovalQueue:
    def __init__(self, path="approval_queue.json"):
        self.path = path

    def _load(self):
        if not os.path.exists(self.path):
            return []
        try:
            return json.load(open(self.path, "r", encoding="utf-8"))
        except Exception:
            return []

    def _save(self, rows):
        json.dump(rows, open(self.path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    def add(self, item):
        rows = self._load()
        item.setdefault("id", str(uuid.uuid4())[:8])
        rows.insert(0, item)
        self._save(rows)
        return item

    def list(self):
        return self._load()
