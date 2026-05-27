import os, json, requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.base = "https://www.googleapis.com/youtube/v3"

    def _credentials(self):
        raw = os.getenv("YOUTUBE_TOKEN_JSON", "").strip()
        if raw:
            return Credentials.from_authorized_user_info(json.loads(raw), SCOPES)
        if os.path.exists("token.json"):
            return Credentials.from_authorized_user_file("token.json", SCOPES)
        return None

    def videos_by_ids(self, ids):
        if isinstance(ids, str):
            ids = [ids]
        if not self.api_key:
            raise RuntimeError("Missing YOUTUBE_API_KEY")
        r = requests.get(self.base + "/videos", params={
            "part": "snippet,statistics,contentDetails,status",
            "id": ",".join(ids),
            "key": self.api_key
        }, timeout=20)
        r.raise_for_status()
        return r.json().get("items", [])

    def my_channel(self):
        creds = self._credentials()
        if not creds:
            raise RuntimeError("Missing OAuth token for /api/channel")
        yt = build("youtube", "v3", credentials=creds)
        return yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
