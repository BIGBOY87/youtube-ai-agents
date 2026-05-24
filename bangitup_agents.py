
import os
import json
import uuid
import datetime

def _int(v):
    try:
        return int(v)
    except Exception:
        return 0

class SEOAgent:
    def generate(self, title, genre, mood="high energy"):
        clean = title.strip() or "New BANG IT UP MUSIC Track"
        return {
            "titles": [
                f"{clean} | Dark {genre} Mix 2026",
                f"{clean} | Night Drive {genre}",
                f"{clean} | BANG IT UP MUSIC"
            ],
            "description": f"{clean} by BANG IT UP MUSIC. {genre} energy, dark atmosphere, heavy bass and underground club mood.",
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
                    "cta": "Subscribe for weekly underground energy"
                }
                for h in hooks
            ]
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
            likes = _int(st.get("likeCount"))
            comments = _int(st.get("commentCount"))
            priority = "high" if views < 100 else "medium" if views < 1000 else "scale"
            recs.append({
                "video_id": v.get("id"),
                "title": s.get("title"),
                "views": views,
                "likes": likes,
                "comments": comments,
                "priority": priority,
                "recommendation": "Create Shorts package and stronger title/thumbnail test."
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

class RepurposeAgent:
    def repurpose_video(self, video):
        s = video.get("snippet", {})
        st = video.get("statistics", {})
        title = s.get("title", "Untitled")
        description = s.get("description", "")
        video_id = video.get("id")
        views = _int(st.get("viewCount"))
        likes = _int(st.get("likeCount"))
        comments = _int(st.get("commentCount"))

        genre = "Tech House"
        if "melodic" in (title + description).lower():
            genre = "Melodic Techno"
        if "edm" in (title + description).lower():
            genre = "EDM"

        shorts = ShortsAgent().generate(title, genre)
        seo = SEOAgent().generate(title, genre)
        distribution = DistributionAgent().posts(title, genre)

        if views < 100:
            action = "Repurpose immediately into Shorts. Low reach means the idea needs new entry points."
        elif views < 1000:
            action = "Create 2 Shorts and test one title variant."
        else:
            action = "Scale. Create multiple Shorts from this format."

        return {
            "source_video": {
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "views": views,
                "likes": likes,
                "comments": comments
            },
            "priority_action": action,
            "shorts_package": shorts,
            "seo_refresh": seo,
            "distribution_posts": distribution,
            "production_note": "To create the actual Short video, provide the original MP4/direct URL. YouTube API metadata alone cannot cut the existing YouTube video file."
        }

    def repurpose_batch(self, videos):
        rows = [self.repurpose_video(v) for v in videos]
        rows.sort(key=lambda x: x["source_video"]["views"])
        return {
            "status": "repurpose_plan_created",
            "count": len(rows),
            "items": rows
        }

class CalendarAgent:
    def weekly(self):
        return [{"day": "Friday", "task": "Publish/schedule at 19:00"}]

class InitiativeEngine:
    def decide(self, channel, videos):
        return [{"priority": "high", "action": "Run /api/repurpose-existing and create Shorts packages from lowest-view videos."}]

class VideoCreatorAgent:
    def create_project(self, title, genre):
        seo = SEOAgent().generate(title, genre)
        return {
            "id": str(uuid.uuid4())[:8],
            "title": seo["titles"][0],
            "genre": genre,
            "seo": seo,
            "required_input": "direct MP4 URL"
        }

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
