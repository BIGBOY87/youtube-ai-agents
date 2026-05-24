import os
import requests

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

class YouTubeClient:
    def __init__(self, api_key=None, channel_id=None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY", "")
        self.channel_id = channel_id or os.getenv("YOUTUBE_CHANNEL_ID", "")

    def _get(self, path, params):
        if not self.api_key:
            raise RuntimeError("Missing YOUTUBE_API_KEY")
        params = {**params, "key": self.api_key}
        r = requests.get(f"{YOUTUBE_API_BASE}/{path}", params=params, timeout=20)
        r.raise_for_status()
        return r.json()

    def channel(self, channel_id=None):
        cid = channel_id or self.channel_id
        if not cid:
            raise RuntimeError("Missing YOUTUBE_CHANNEL_ID")
        data = self._get("channels", {
            "part": "snippet,statistics,brandingSettings,contentDetails",
            "id": cid
        })
        items = data.get("items", [])
        return items[0] if items else {}

    def recent_videos(self, max_results=12, channel_id=None):
        cid = channel_id or self.channel_id
        search = self._get("search", {
            "part": "snippet",
            "channelId": cid,
            "maxResults": max_results,
            "order": "date",
            "type": "video"
        })
        ids = [item["id"]["videoId"] for item in search.get("items", []) if item.get("id", {}).get("videoId")]
        if not ids:
            return []
        details = self._get("videos", {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(ids)
        })
        return details.get("items", [])

    def search_trends(self, query, max_results=10):
        data = self._get("search", {
            "part": "snippet",
            "q": query,
            "maxResults": max_results,
            "order": "relevance",
            "type": "video",
            "videoCategoryId": "10"
        })
        return data.get("items", [])
