\
import os
from datetime import datetime, timezone
from typing import Dict, Any

from youtube_uploader import upload_video

BLOCKED_TERMS = [
    "fake views",
    "fake subscribers",
    "sub4sub",
    "guaranteed viral",
    "clickbait scam",
]

def validate_project(project: Dict[str, Any]) -> tuple[bool, str]:
    title = str(project.get("title", "")).strip()
    description = str(project.get("description", "")).strip()
    combined = (title + " " + description).lower()

    if not title:
        return False, "Missing title."

    if not project.get("video_file"):
        return False, "Missing video_file MP4 path."

    if os.getenv("PUBLIC_POSTS_REQUIRE_OWN_CONTENT", "true").lower() == "true":
        if project.get("own_content_confirmed") is not True:
            return False, "Own content confirmation required."

    for term in BLOCKED_TERMS:
        if term in combined:
            return False, f"Blocked unsafe term: {term}"

    return True, "Allowed."

class PublicPublishAgent:
    def __init__(self):
        self.upload_enabled = os.getenv("YOUTUBE_UPLOAD_ENABLED", "false").lower() == "true"
        self.auto_public = os.getenv("AUTO_PUBLIC_MODE", "false").lower() == "true"
        self.auto_approve = os.getenv("AUTO_APPROVE_UPLOADS", "false").lower() == "true"

    def publish(self, project: Dict[str, Any]) -> Dict[str, Any]:
        if not self.upload_enabled:
            return {"status": "blocked", "reason": "YOUTUBE_UPLOAD_ENABLED is not true."}

        if not self.auto_public:
            return {"status": "blocked", "reason": "AUTO_PUBLIC_MODE is not true."}

        if not self.auto_approve:
            return {"status": "needs_approval", "reason": "AUTO_APPROVE_UPLOADS is false."}

        allowed, reason = validate_project(project)
        if not allowed:
            return {"status": "blocked", "reason": reason}

        result = upload_video(
            video_file=project["video_file"],
            title=project["title"],
            description=project.get("description", ""),
            tags=project.get("tags", []),
            category_id=str(project.get("category_id", "10")),
            privacy_status=project.get("privacy_status", "private"),
            publish_at=project.get("publish_at"),
        )

        return {
            "status": "published_or_uploaded",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }
