
import os, json, uuid

def _int(v):
    try:
        return int(v)
    except Exception:
        return 0

class ShortWorkflowAgent:
    def make_short_task(self, video):
        s = video.get("snippet", {})
        st = video.get("statistics", {})
        title = s.get("title", "Untitled")
        video_id = video.get("id")
        return {
            "task_id": str(uuid.uuid4())[:8],
            "source_video": {
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "views": _int(st.get("viewCount"))
            },
            "required_input": "original local MP4 or direct Short MP4 URL",
            "local_command_example": f'python local_short_factory.py --input "C:\\\\Videos\\\\SOURCE.mp4" --title "{title[:40]}" --start 30 --duration 20',
            "upload_endpoint": "/api/shorts/upload-from-url",
            "short_upload_template": {
                "title": f"{title[:80]} #Shorts",
                "description": f"{title} by BANG IT UP MUSIC. #Shorts #BANGITUPMUSIC",
                "tags": ["BANGITUPMUSIC", "Shorts", "TechHouse", "EDM"],
                "privacy_status": "private",
                "own_content_confirmed": True
            }
        }

    def batch(self, videos):
        tasks = [self.make_short_task(v) for v in videos]
        tasks.sort(key=lambda x: x["source_video"]["views"])
        return {"status": "short_tasks_created", "count": len(tasks), "items": tasks}

class GrowthAgent:
    def report(self, channel, videos):
        return {
            "summary": {
                "title": channel.get("snippet", {}).get("title"),
                "subscribers": channel.get("statistics", {}).get("subscriberCount")
            },
            "recommendations": [
                {"video_id": v.get("id"), "title": v.get("snippet", {}).get("title"), "views": _int(v.get("statistics", {}).get("viewCount")), "recommendation": "Create local Short and upload private"}
                for v in videos[:10]
            ]
        }

class InitiativeEngine:
    def decide(self, channel, videos):
        return [{"priority": "high", "action": "Scheduler should create Shorts tasks daily."}]

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
