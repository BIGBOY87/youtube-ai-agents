from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from googleapiclient.discovery import build

from .auth import get_credentials


class YouTubeClient:
    def __init__(self) -> None:
        creds = get_credentials()
        self.youtube = build("youtube", "v3", credentials=creds)
        self.analytics = build("youtubeAnalytics", "v2", credentials=creds)

    def my_channel(self) -> dict[str, Any]:
        response = self.youtube.channels().list(
            part="snippet,statistics,contentDetails,brandingSettings",
            mine=True,
            maxResults=1,
        ).execute()
        items = response.get("items", [])
        if not items:
            raise RuntimeError("No authenticated YouTube channel found for this Google account.")
        return items[0]

    def recent_videos(self, max_results: int = 10) -> list[dict[str, Any]]:
        channel = self.my_channel()
        uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        playlist_response = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist,
            maxResults=max_results,
        ).execute()
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]
        if not video_ids:
            return []
        videos_response = self.youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids),
            maxResults=max_results,
        ).execute()
        return videos_response.get("items", [])

    def analytics_summary(self, days: int = 28) -> dict[str, Any]:
        end = date.today() - timedelta(days=2)  # Analytics can lag; avoid partial latest data.
        start = end - timedelta(days=days)
        result = self.analytics.reports().query(
            ids="channel==MINE",
            startDate=start.isoformat(),
            endDate=end.isoformat(),
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments,shares",
            dimensions="day",
            sort="day",
        ).execute()
        return {"start": start.isoformat(), "end": end.isoformat(), "raw": result}

    def top_videos_by_views(self, days: int = 28, max_results: int = 10) -> dict[str, Any]:
        end = date.today() - timedelta(days=2)
        start = end - timedelta(days=days)
        result = self.analytics.reports().query(
            ids="channel==MINE",
            startDate=start.isoformat(),
            endDate=end.isoformat(),
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained",
            dimensions="video",
            sort="-views",
            maxResults=max_results,
        ).execute()
        return {"start": start.isoformat(), "end": end.isoformat(), "raw": result}
