from __future__ import annotations


class PromotionAgent:
    def social_posts(self, title: str, url: str = "https://www.youtube.com/@BANGITUPMUSIC") -> dict[str, str]:
        return {
            "youtube_community": f"Νέο drop: {title}. Ποιο σημείο να κάνω Short; Άκου εδώ: {url}",
            "instagram": f"New drop από BANG IT UP MUSIC: {title}. Save το reel αν σου κόλλησε. Link στο bio / YouTube.",
            "tiktok": f"Αν αυτό το beat σου δίνει energy, χρησιμοποίησέ το σε video και κάνε tag @BANGITUPMUSIC. Track: {title}",
            "reddit_discord_safe": (
                f"Έφτιαξα ένα νέο {title} track και ψάχνω ειλικρινές feedback από άτομα που ακούνε independent music. "
                "Δεν κάνω spam—αν ταιριάζει στο community, ευχαρίστως να ακούσω γνώμες."
            ),
        }

    def weekly_plan(self) -> list[str]:
        return [
            "Δευτέρα: ανέβασε 1 Short από το καλύτερο hook παλιού ή νέου βίντεο.",
            "Τρίτη: κάνε Community post με poll: ποιο vibe θέλει το κοινό στο επόμενο drop;",
            "Τετάρτη: βρες 10 μικρά μουσικά κανάλια για πιθανή συνεργασία και στείλε προσωποποιημένο μήνυμα.",
            "Πέμπτη: δημοσίευσε Short με ερώτηση: Rate this beat 1-10.",
            "Παρασκευή: ανανέωσε title/description σε 1 παλιό βίντεο με χαμηλό CTR.",
            "Σάββατο: κάνε playlist pitching σε νόμιμες open-submission playlists.",
            "Κυριακή: έλεγξε analytics και κράτα 3 συμπεράσματα για το επόμενο upload.",
        ]
