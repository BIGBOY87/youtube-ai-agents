from datetime import datetime

def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default

class GrowthAgent:
    name = "Growth Agent"
    def summarize(self, channel, videos):
        stats = channel.get("statistics", {})
        rows = []
        for v in videos:
            s = v.get("statistics", {})
            sn = v.get("snippet", {})
            rows.append({
                "title": sn.get("title"),
                "publishedAt": sn.get("publishedAt"),
                "views": safe_int(s.get("viewCount")),
                "likes": safe_int(s.get("likeCount")),
                "comments": safe_int(s.get("commentCount")),
                "id": v.get("id")
            })
        rows.sort(key=lambda x: x["views"], reverse=True)
        avg = round(sum(v["views"] for v in rows) / len(rows), 1) if rows else 0
        return {
            "channel_title": channel.get("snippet", {}).get("title"),
            "subscribers": safe_int(stats.get("subscriberCount")),
            "total_views": safe_int(stats.get("viewCount")),
            "total_videos": safe_int(stats.get("videoCount")),
            "avg_recent_views": avg,
            "top_recent_videos": rows[:3],
            "recommendations": [
                "Create 3-5 Shorts from every full music upload.",
                "Use stronger first 2 seconds: drop, bassline, hook, or visual switch.",
                "Update weak titles after 48 hours if views are below recent average.",
                "Pin a comment asking viewers to rate the drop or choose the next genre."
            ]
        }

class SEOAgent:
    def generate(self, title, genre="music", mood="high energy"):
        base = title.strip() or "New Music Release"
        genre = genre.strip() or "Music"
        mood = mood.strip() or "High Energy"
        hashtags = [f"#{genre.replace(' ','')}", "#NewMusic", "#Music2026", "#BANGITUPMUSIC", "#YouTubeMusic", "#Shorts", "#ViralMusic", "#Producer", "#DJ", "#OfficialMusic"]
        return {
            "titles": [
                f"{base} | {genre} Music 2026",
                f"{base} - {mood} {genre} Track",
                f"{base} 🔥 New {genre} Release",
                f"{genre} Mix 2026 - {base}",
                f"{base} | BANG IT UP MUSIC Official"
            ],
            "description": f"{base}\n\nNew {genre} release by BANG IT UP MUSIC. Mood: {mood}.\n\nListen, comment your favorite part, and subscribe for more releases.\n\n" + " ".join(hashtags[:8]),
            "hashtags": hashtags,
            "tags": [genre, f"{genre} 2026", "new music", "bang it up music", "youtube music", "viral music", "official music", "music video", mood, "shorts music", "dj music", "producer music"],
            "pinned_comment": f"Which part hits harder in '{base}' — intro, drop, or outro?"
        }

class ShortsAgent:
    def generate(self, title, genre="music"):
        hooks = ["Wait for the drop...", "This bassline changes everything.", "Use headphones for this part.", "Would you play this in the car?", "Rate this drop from 1-10.", "POV: the beat finally hits.", "This needs to be louder.", "New sound from BANG IT UP MUSIC."]
        return {"title": title, "ideas": [{"short": i+1, "hook": h, "caption": f"{h} #{genre.replace(' ','')} #Shorts #NewMusic", "structure": "0-2s hook, 2-12s strongest music moment, 12-18s visual switch, final CTA: subscribe for full track"} for i,h in enumerate(hooks)]}

class ThumbnailAgent:
    def recommendations(self):
        return {"rules": ["Use 2-4 words maximum.", "High contrast subject/background.", "Make the genre obvious.", "Avoid small unreadable text.", "Test another thumbnail after 24-48h if views are low."], "text_ideas": ["NEW DROP", "BASS BOOST", "2026 MIX", "HARD BEAT", "VIRAL SOUND"]}

class TrendAgent:
    def query_list(self):
        return ["new edm music 2026", "viral music shorts", "trap beat 2026", "house music 2026", "bass boosted music"]
    def summarize_search(self, trends):
        examples = []
        for q, items in trends.items():
            for item in items[:2]:
                sn = item.get("snippet", {})
                examples.append({"query": q, "title": sn.get("title"), "channel": sn.get("channelTitle")})
        return {"recommended_keywords": self.query_list(), "observed_examples": examples[:10], "actions": ["Create one Short using a trend keyword in the first 40 characters.", "Use one genre keyword and one emotion keyword in each title.", "Extract format patterns only; do not copy competitors."]}

class DistributionAgent:
    def posts(self, title, genre="music"):
        return {"tiktok": f"New {genre} sound just dropped. Would you use this in a video? #newmusic #producer #{genre.replace(' ','')}", "instagram": f"{title} is live. Save this if the drop hits. #BANGITUPMUSIC #NewMusic", "facebook": f"New release from BANG IT UP MUSIC: {title}. Listen and tell me which part hits hardest.", "x": f"New track: {title}. High-energy {genre}. Full version on YouTube.", "reddit_safe": f"I made a new {genre} track and I’m looking for honest feedback on the mix/drop. No spam—happy to hear critiques."}

class CalendarAgent:
    def weekly(self):
        return [{"day": d, "task": t, "goal": g} for d,t,g in [
            ("Mon", "Upload 1 Short from strongest drop", "Discovery"),
            ("Tue", "Community poll: choose next genre", "Engagement"),
            ("Wed", "Post TikTok/Reel caption from Distribution Agent", "Cross-platform"),
            ("Thu", "Review top 3 videos and update weak titles", "Optimization"),
            ("Fri", "Publish new visualizer or music clip", "Upload"),
            ("Sat", "Comment meaningfully on 10 similar channels", "Community"),
            ("Sun", "Generate weekly report and next-week plan", "Analysis")
        ]]

class CollaborationAgent:
    def suggest(self, genre="music"):
        return {"targets": [f"{genre} playlist curators", "small music reaction channels", "visualizer creators", "DJs with 1k-20k subscribers", "producers who post remix challenges"], "message": f"Hi, I make {genre} under BANG IT UP MUSIC. I liked your content and think our audiences overlap. Open to a playlist swap, feedback exchange, or simple collab?"}

class ReportOrchestrator:
    def __init__(self):
        self.growth = GrowthAgent()
        self.seo = SEOAgent()
        self.shorts = ShortsAgent()
        self.thumbnail = ThumbnailAgent()
        self.trend = TrendAgent()
        self.distribution = DistributionAgent()
        self.calendar = CalendarAgent()
        self.collaboration = CollaborationAgent()

    def full_report(self, channel, videos, trend_data=None):
        trend_data = trend_data or {}
        return {"generated_at": datetime.utcnow().isoformat() + "Z", "agents": ["Growth", "SEO", "Shorts", "Thumbnail", "Trend", "Distribution", "Calendar", "Collaboration"], "growth": self.growth.summarize(channel, videos), "thumbnail": self.thumbnail.recommendations(), "trends": self.trend.summarize_search(trend_data), "calendar": self.calendar.weekly(), "collaboration": self.collaboration.suggest("music")}
