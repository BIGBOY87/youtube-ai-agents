\
import os
import json
import tempfile
from typing import Dict, Any, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def _load_token_from_env_or_file() -> Credentials:
    """
    Supports:
    - YOUTUBE_TOKEN_JSON: full token.json content as environment variable
    - token.json file in working directory (local only)
    """
    raw = os.getenv("YOUTUBE_TOKEN_JSON", "").strip()

    if raw:
        data = json.loads(raw)
        return Credentials.from_authorized_user_info(data, SCOPES)

    if os.path.exists("token.json"):
        return Credentials.from_authorized_user_file("token.json", SCOPES)

    raise RuntimeError("Missing OAuth token. Set YOUTUBE_TOKEN_JSON env var or provide token.json locally.")

def get_youtube_upload_service():
    creds = _load_token_from_env_or_file()
    return build("youtube", "v3", credentials=creds)

def upload_video(
    video_file: str,
    title: str,
    description: str,
    tags: Optional[List[str]] = None,
    category_id: str = "10",
    privacy_status: str = "private",
    publish_at: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Uploads a video to YouTube using videos.insert.

    privacy_status:
    - private
    - unlisted
    - public

    publish_at:
    RFC3339 datetime. If set, privacyStatus must usually be private for scheduled publish.
    """
    if not os.path.exists(video_file):
        raise FileNotFoundError(f"Video file not found: {video_file}")

    if privacy_status not in {"private", "unlisted", "public"}:
        raise ValueError("privacy_status must be private, unlisted, or public")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    if publish_at:
        body["status"]["publishAt"] = publish_at
        body["status"]["privacyStatus"] = "private"

    youtube = get_youtube_upload_service()

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    return {
        "status": "uploaded",
        "video_id": response.get("id"),
        "youtube_url": f"https://www.youtube.com/watch?v={response.get('id')}",
        "raw": response,
    }
