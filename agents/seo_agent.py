from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SEOInput:
    title: str
    genre: str = "music"
    mood: str = "high energy"
    audience: str = "music listeners, creators, DJs"
    language: str = "el"


class SEOAgent:
    def generate(self, item: SEOInput) -> dict[str, object]:
        clean_title = self._clean(item.title)
        genre = item.genre.strip() or "music"
        mood = item.mood.strip() or "high energy"

        titles = [
            f"{clean_title} | {genre} Music 2026",
            f"{clean_title} - {mood.title()} {genre} Track",
            f"BANG IT UP MUSIC - {clean_title} ({genre})",
            f"{clean_title} 🔥 Official Music Video | BANG IT UP MUSIC",
            f"New {genre} Music: {clean_title} | Viral Energy Track",
        ]

        hashtags = self._unique([
            "#BANGITUPMUSIC", "#NewMusic", "#MusicVideo", "#ViralMusic", "#YouTubeMusic",
            f"#{self._tag(genre)}", f"#{self._tag(mood)}", "#Shorts", "#Reels", "#TikTokMusic",
            "#DJMusic", "#MusicProducer", "#Playlist", "#IndependentArtist", "#FreshMusic",
        ])

        tags = self._unique([
            "BANG IT UP MUSIC", clean_title, genre, mood, "new music", "music video",
            "viral song", "youtube music", "independent music", "party music", "dj music",
            "shorts music", "reels music", "tiktok music", "playlist music", "new song 2026",
            "energetic music", "club music", "music promotion", "official track",
        ])

        description = f"""{clean_title} από BANG IT UP MUSIC.

Αν σου αρέσει το {genre} με {mood} ατμόσφαιρα, κάνε subscribe και άφησε σχόλιο με το σημείο που σου κόλλησε περισσότερο.

Listen / Watch more:
- YouTube channel: https://www.youtube.com/@BANGITUPMUSIC

Suggested for fans of: {item.audience}

{ ' '.join(hashtags[:10]) }
""".strip()

        pinned_comment = (
            f"Ποιο σημείο του '{clean_title}' να γίνει Short; Γράψε timestamp και κάνε subscribe "
            "για το επόμενο drop. 🔥"
        )

        return {
            "titles": titles,
            "description": description,
            "hashtags": hashtags,
            "tags": tags,
            "pinned_comment": pinned_comment,
            "keywords": [genre, mood, clean_title, "BANG IT UP MUSIC", "new music", "music shorts"],
        }

    @staticmethod
    def _clean(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip()) or "New Track"

    @staticmethod
    def _tag(text: str) -> str:
        return re.sub(r"[^A-Za-z0-9Α-Ωα-ω]", "", text.title())[:40] or "Music"

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        seen = set()
        out = []
        for value in values:
            key = value.lower()
            if key not in seen:
                seen.add(key)
                out.append(value)
        return out
