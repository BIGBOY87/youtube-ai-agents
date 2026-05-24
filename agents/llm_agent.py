from __future__ import annotations

import json
import subprocess
from typing import Any


class LocalLLMAgent:
    """Optional Ollama-powered brain. Safe fallback when Ollama is not installed."""

    def __init__(self, model: str = "llama3.1:8b") -> None:
        self.model = model

    def available(self) -> bool:
        try:
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=6)
            return result.returncode == 0
        except Exception:
            return False

    def generate(self, prompt: str, fallback: str = "") -> str:
        if not self.available():
            return fallback or "Ollama δεν βρέθηκε. Χρησιμοποιώ rule-based προτάσεις."
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return fallback or result.stderr.strip()
        except Exception as exc:
            return fallback or f"Ollama unavailable: {exc}"

    def strategy_from_context(self, context: dict[str, Any]) -> str:
        prompt = """
Είσαι νόμιμος YouTube Growth Strategist για μουσικό κανάλι.
Μη προτείνεις fake views, fake subscribers, spam comments ή bots.
Δώσε συγκεκριμένο ελληνικό πλάνο 7 ημερών με Shorts, τίτλους, thumbnails, community posts και συνεργασίες.
Context JSON:
""" + json.dumps(context, ensure_ascii=False, indent=2)
        return self.generate(prompt, fallback="Δεν υπάρχει Ollama. Άνοιξε το dashboard/report για rule-based πλάνο 7 ημερών.")
