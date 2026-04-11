try:
    from langdetect import LangDetectException, detect
except ModuleNotFoundError:
    LangDetectException = Exception
    detect = None

import re


class LanguageService:
    """Language detection with safe fallback."""

    @staticmethod
    def detect_language(text: str) -> str:
        if not text.strip():
            return "unknown"

        if detect is None:
            return LanguageService._heuristic_detect(text)

        try:
            return detect(text)
        except LangDetectException:
            return LanguageService._heuristic_detect(text)

    @staticmethod
    def _heuristic_detect(text: str) -> str:
        lowered = f" {text.lower()} "
        if any(ch in lowered for ch in ["ä", "ö", "ü", "ß"]):
            return "de"

        de_markers = [" und ", " der ", " die ", " das ", " nicht ", " ist ", " mit ", " auf ", "eine ", "einer "]
        en_markers = [" the ", " and ", " is ", " not ", " with ", " for ", " on ", " of ", " in "]

        de_score = sum(lowered.count(marker) for marker in de_markers)
        en_score = sum(lowered.count(marker) for marker in en_markers)

        # Token-level reinforcement for common function words.
        tokens = re.findall(r"[a-zA-ZäöüÄÖÜß]+", lowered)
        de_token_words = {"und", "der", "die", "das", "nicht", "ist", "mit", "auf", "eine", "einer"}
        en_token_words = {"the", "and", "is", "not", "with", "for", "on", "of", "in"}
        de_score += sum(1 for token in tokens if token in de_token_words)
        en_score += sum(1 for token in tokens if token in en_token_words)

        if de_score >= en_score + 2:
            return "de"
        if en_score >= de_score + 2:
            return "en"
        return "unknown"
