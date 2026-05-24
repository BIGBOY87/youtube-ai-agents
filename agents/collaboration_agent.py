from __future__ import annotations


class CollaborationAgent:
    def targets_and_message(self, genre: str = "music") -> dict[str, object]:
        return {
            "targets": [
                "μικρά μουσικά YouTube κανάλια 1k-20k subs",
                "DJs που ανεβάζουν mixes",
                "playlist curators με open submissions",
                "visualizer creators",
                "χορευτές/creators που χρησιμοποιούν beats σε Shorts/Reels",
            ],
            "message_template": (
                "Γεια σου, είμαι από BANG IT UP MUSIC. Έχω ένα νέο {genre} track και πιστεύω ότι ταιριάζει με το κοινό σου. "
                "Αν σου αρέσει, μπορούμε να κάνουμε ένα Short/remix/cross-post. Δεν ζητάω spam, μόνο πραγματική συνεργασία."
            ).format(genre=genre),
        }
