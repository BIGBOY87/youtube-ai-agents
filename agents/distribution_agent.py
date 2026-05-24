from __future__ import annotations


class DistributionAgent:
    def package(self, title: str, url: str = "https://www.youtube.com/@BANGITUPMUSIC") -> dict[str, str]:
        return {
            "tiktok": f"Αυτό το drop θέλει ακουστικά. Track: {title}. Full στο YouTube: {url} #NewMusic #MusicTok",
            "instagram_reel": f"New energy από BANG IT UP MUSIC. Save αν σου κόλλησε. Track: {title}. #reels #newmusic",
            "facebook": f"Νέο track από BANG IT UP MUSIC: {title}. Άκουσέ το εδώ: {url}",
            "x_twitter": f"New drop: {title} — BANG IT UP MUSIC. Full track: {url} #NewMusic",
            "discord": f"Έριξα νέο track: {title}. Θα ήθελα honest feedback, ειδικά για drop/mix/energy. {url}",
            "reddit_safe": f"Έφτιαξα ένα νέο track ({title}) και ψάχνω ειλικρινές feedback από fans/producers. Δεν είναι promo spam· θέλω γνώμη για mix και hook. {url}",
        }
