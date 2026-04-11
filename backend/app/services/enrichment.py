import re
from collections import Counter

try:
    import yake
except ModuleNotFoundError:
    yake = None


class EnrichmentService:
    """Keyword, entity, and tone enrichment."""

    @staticmethod
    def extract_keywords(text: str, language: str, top_k: int = 8) -> list[str]:
        if not text.strip():
            return []

        if yake is None:
            return EnrichmentService._fallback_keywords(text=text, language=language, top_k=top_k)

        lang = "de" if language == "de" else "en"
        extractor = yake.KeywordExtractor(lan=lang, n=1, top=top_k)
        ranked = extractor.extract_keywords(text)
        return [kw for kw, _ in ranked]

    @staticmethod
    def _fallback_keywords(text: str, language: str, top_k: int) -> list[str]:
        stopwords_de = {
            "der", "die", "das", "und", "oder", "ein", "eine", "ist", "im", "in", "den", "dem",
            "von", "mit", "auf", "fur", "für", "an", "als", "auch", "zu", "des", "dass", "sich", "es",
        }
        stopwords_en = {
            "the", "and", "or", "a", "an", "is", "in", "on", "for", "to", "of", "that", "with", "as",
        }
        stopwords = stopwords_de if language == "de" else stopwords_en

        tokens = re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", text.lower())
        counts = Counter(token for token in tokens if token not in stopwords)
        return [word for word, _ in counts.most_common(top_k)]

    @staticmethod
    def extract_entities(text: str) -> dict:
        # Lightweight fallback entity extraction based on title-case sequences and org suffixes.
        candidates = re.findall(r"\b(?:[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+){0,2})\b", text)

        org_markers = {"GmbH", "AG", "SE", "Ministerium", "Partei", "Bank", "University"}
        organizations = sorted({c for c in candidates if any(marker in c for marker in org_markers)})

        # Heuristic split for names and locations.
        people = sorted({c for c in candidates if len(c.split()) >= 2 and c not in organizations})[:10]

        location_hints = {
            "Berlin", "Hamburg", "München", "Deutschland", "Europa", "Frankfurt", "Paris", "Brüssel"
        }
        locations = sorted({c for c in candidates if c in location_hints})

        return {
            "people": people,
            "organizations": organizations,
            "locations": locations,
        }

    @staticmethod
    def classify_tone(text: str, language: str) -> str:
        lowered = text.lower()
        positive_words = {
            "erfolg", "wachstum", "verbessert", "stabil", "positiv", "chance", "strong", "improves",
            "growth", "success", "positive", "stable",
        }
        negative_words = {
            "krise", "verlust", "rückgang", "negativ", "risiko", "konflikt", "crisis", "decline",
            "loss", "negative", "risk", "conflict",
        }

        tokens = re.findall(r"[a-zA-ZäöüÄÖÜß]+", lowered)
        counts = Counter(tokens)

        pos_score = sum(counts[word] for word in positive_words)
        neg_score = sum(counts[word] for word in negative_words)

        if pos_score > neg_score + 1:
            return "positive"
        if neg_score > pos_score + 1:
            return "negative"
        return "neutral"
