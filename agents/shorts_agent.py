from __future__ import annotations


class ShortsAgent:
    def generate(self, title: str, genre: str = "music", mood: str = "high energy") -> list[dict[str, str]]:
        return [
            {
                "hook": "Wait for the drop...",
                "concept": f"15s Short με build-up από το '{title}' και cut ακριβώς στο drop.",
                "caption": f"Το drop στο {title} χτυπάει δυνατά. #Shorts #BANGITUPMUSIC",
            },
            {
                "hook": "POV: μπαίνει αυτό το beat στο club",
                "concept": f"Visual loop με club/nightlife vibe και το πιο δυνατό ρεφρέν του {genre} track.",
                "caption": f"POV: αυτό παίζει τέρμα. {mood} energy only.",
            },
            {
                "hook": "Rate this beat 1-10",
                "concept": "Short που ζητά σχόλια, όχι spam: φυσικό engagement με ερώτηση.",
                "caption": "Rate this beat 1-10. Θες full version; Subscribe.",
            },
            {
                "hook": "This part needs headphones",
                "concept": "Close-up visualizer/audio spectrum με την πιο καθαρή μελωδική στιγμή.",
                "caption": "Headphones on. Πες μου αν το νιώθεις.",
            },
            {
                "hook": "New sound from BANG IT UP MUSIC",
                "concept": "Branding Short για discovery: logo/channel name στο πρώτο δευτερόλεπτο.",
                "caption": "New sound. New energy. BANG IT UP MUSIC.",
            },
        ]
