from __future__ import annotations


class PlannerAgent:
    def seven_day_plan(self, title: str = "new track") -> list[str]:
        return [
            f"Ημέρα 1: Δημοσίευσε Short 'Wait for the drop' για {title} και pinned comment με ερώτηση.",
            "Ημέρα 2: Community poll: ποιο vibe θέλετε στο επόμενο drop;",
            "Ημέρα 3: Άλλαξε/δοκίμασε δεύτερο title + thumbnail αν το CTR είναι χαμηλό.",
            "Ημέρα 4: Ανέβασε 2ο Short με 'Rate this beat 1-10'.",
            "Ημέρα 5: Στείλε 5 προσωποποιημένα collaboration messages.",
            "Ημέρα 6: Κάνε playlist pitching σε νόμιμες φόρμες/open submissions.",
            "Ημέρα 7: Δες analytics, κράτα top 3 lessons και φτιάξε νέο campaign.",
        ]
