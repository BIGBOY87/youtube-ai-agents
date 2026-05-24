import os
import requests

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "")
        self.base = "https://www.googleapis.com/youtube/v3"

    def _get(self, path, params):
        if not self.api_key:
            raise RuntimeError("Missing YOUTUBE_API_KEY")
        params = dict(params)
        params["key"] = self.api_key
        r = requests.get(self.base + path, params=params, timeout=20)
        r.raise_for_status()
        return r.json()

    def channel(self, channel_id=None):
        cid = channel_id or self.channel_id
        if not cid:
            raise RuntimeError("Missing YOUTUBE_CHANNEL_ID")
        data = self._get("/channels", {"part": "snippet,statistics,brandingSettings,contentDetails", "id": cid})
        items = data.get("items", [])
        if not items:
            raise RuntimeError("Channel not found")
        return items[0]

    def recent_videos(self, max_results=12, channel_id=None):
        cid = channel_id or self.channel_id
        if not cid:
            raise RuntimeError("Missing YOUTUBE_CHANNEL_ID")
        search = self._get("/search", {"part": "snippet", "channelId": cid, "order": "date", "maxResults": max_results, "type": "video"})
        ids = [i["id"]["videoId"] for i in search.get("items", []) if i.get("id", {}).get("videoId")]
        if not ids:
            return []
        details = self._get("/videos", {"part": "snippet,statistics,contentDetails,status", "id": ",".join(ids)})
        return details.get("items", [])
