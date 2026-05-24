from __future__ import annotations

from typing import Any


class AnalyticsAgent:
    def recommend_from_summary(self, report: dict[str, Any]) -> list[str]:
        raw = report.get("raw", {})
        rows = raw.get("rows", [])
        if not rows:
            return ["Δεν υπάρχουν αρκετά analytics rows. Τρέξε ξανά όταν περάσουν 48 ώρες από τα uploads."]

        total_views = sum(float(row[1]) for row in rows if len(row) > 1)
        total_minutes = sum(float(row[2]) for row in rows if len(row) > 2)
        gained = sum(float(row[4]) for row in rows if len(row) > 4)
        lost = sum(float(row[5]) for row in rows if len(row) > 5)
        avg_minutes_per_view = total_minutes / total_views if total_views else 0

        advice = [
            f"Σύνολο views περιόδου: {int(total_views)}.",
            f"Καθαροί subscribers: {int(gained - lost)}.",
            f"Μέσος χρόνος ανά view: {avg_minutes_per_view:.2f} λεπτά.",
        ]

        if total_views < 500:
            advice.append("Προτεραιότητα: περισσότερα Shorts και πιο καθαρά keywords στον τίτλο.")
        if avg_minutes_per_view < 0.5:
            advice.append("Retention χαμηλό: βάλε δυνατό hook στα πρώτα 3 δευτερόλεπτα και κόψε αργά intro.")
        if gained <= lost:
            advice.append("Subscriber conversion χαμηλό: πρόσθεσε σαφές subscribe CTA στο pinned comment και στο τέλος του βίντεο.")
        if total_views >= 500 and gained > lost:
            advice.append("Κλιμάκωση: κάνε 3 παραλλαγές Shorts από το video που έφερε τα περισσότερα views.")

        return advice
