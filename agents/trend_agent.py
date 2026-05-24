from __future__ import annotations


class TrendAgent:
    def ideas(self, genre: str = "EDM / Trap / Club", mood: str = "high energy") -> dict[str, list[str]]:
        genre_clean = genre or "music"
        return {
            "keywords": [
                f"new {genre_clean} music", f"{genre_clean} beat", f"viral {genre_clean}",
                "club music 2026", "bass boosted music", "music shorts", "dance challenge beat",
                "playlist music", "independent music", "new drop"
            ],
            "short_formats": [
                "Wait for the drop στα πρώτα 2 δευτερόλεπτα",
                "Rate this beat 1-10",
                "POV club entrance με το drop",
                "Before/After: raw beat → final master",
                "Visualizer loop με έντονο hook",
            ],
            "hashtags": ["#NewMusic", "#Shorts", "#MusicProducer", "#DJMusic", "#ClubMusic", "#ViralMusic", "#BANGITUPMUSIC"],
        }
