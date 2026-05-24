from __future__ import annotations


class ThumbnailAgent:
    def recommend(self, title: str, ctr: float | None = None) -> list[str]:
        advice = [
            "Βάλε 2-4 λέξεις μεγάλες πάνω στο thumbnail, όχι πλήρη πρόταση.",
            "Χρησιμοποίησε υψηλή αντίθεση και καθαρό κεντρικό αντικείμενο/πρόσωπο/λογότυπο.",
            "Το thumbnail πρέπει να υπόσχεται το συναίσθημα του track: drop, energy, dark, summer, club κτλ.",
            f"Για το '{title}', δοκίμασε κείμενο: NEW DROP, BASS HIT, CLUB ENERGY ή WAIT FOR DROP.",
        ]
        if ctr is not None and ctr < 4:
            advice.insert(0, "CTR κάτω από 4%: άλλαξε thumbnail και τίτλο μέσα στις επόμενες 24 ώρες.")
        return advice
