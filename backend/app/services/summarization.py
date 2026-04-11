import importlib
import json
import re
from collections import Counter
from typing import List
from urllib.parse import quote
from urllib.request import urlopen

httpx = None
GoogleTranslator = None

try:
    httpx = importlib.import_module("httpx")
except ModuleNotFoundError:
    pass

try:
    deep_translator_module = importlib.import_module("deep_translator")
    GoogleTranslator = deep_translator_module.GoogleTranslator
except ModuleNotFoundError:
    pass

from app.core.config import settings


STOPWORDS_DE = {
    "der", "die", "das", "und", "oder", "ein", "eine", "ist", "im", "in", "den", "dem",
    "von", "mit", "auf", "für", "an", "als", "auch", "zu", "des", "dass", "sich", "es",
}

STOPWORDS_EN = {
    "the", "and", "or", "a", "an", "is", "in", "on", "for", "to", "of", "that", "with", "as",
}

LENGTH_TO_SENTENCES = {
    "short": 2,
    "medium": 4,
    "detailed": 7,
}


class SummarizationService:
    """Generate German and English summaries with LLM-first, local-fallback logic."""

    @staticmethod
    def summarize_german(text: str, summary_length: str) -> str:
        llm_result = SummarizationService._summarize_with_llm(
            text=text,
            target_language="de",
            summary_length=summary_length,
        )
        if llm_result:
            return llm_result

        if not text.strip():
            return ""

        return SummarizationService._extractive_summary(
            text=text,
            sentence_count=LENGTH_TO_SENTENCES.get(summary_length, 4),
            language="de",
        )

    @staticmethod
    def summarize_english(text: str, summary_length: str, source_language: str) -> str:
        llm_result = SummarizationService._summarize_with_llm(
            text=text,
            target_language="en",
            summary_length=summary_length,
        )
        if llm_result:
            return llm_result

        # Fallback: summarize first, then translate for German input.
        local_source_summary = SummarizationService._extractive_summary(
            text=text,
            sentence_count=LENGTH_TO_SENTENCES.get(summary_length, 4),
            language="de" if source_language == "de" else "en",
        )

        source_is_german = source_language == "de" or (
            source_language == "unknown" and SummarizationService._looks_german(text)
        )

        if source_is_german:
            translated = SummarizationService._translate_de_to_en(local_source_summary)
            if translated:
                return translated
            return "English translation unavailable. Configure an LLM API key or install deep-translator."

        return local_source_summary

    @staticmethod
    def _summarize_with_llm(text: str, target_language: str, summary_length: str) -> str | None:
        if httpx is None:
            return None

        api_key = settings.openai_api_key or settings.openrouter_api_key
        if not api_key:
            return None

        base_url = settings.openai_base_url
        model_name = settings.openai_model

        if settings.openrouter_api_key:
            base_url = settings.openrouter_base_url
            model_name = settings.openrouter_model

        if not base_url:
            return None

        length_instruction = {
            "short": "2-3 sentences",
            "medium": "4-6 sentences",
            "detailed": "7-10 sentences",
        }.get(summary_length, "4-6 sentences")

        language_instruction = "German" if target_language == "de" else "English"

        prompt = (
            f"Summarize the news article in {language_instruction}. "
            f"Keep it factual and concise in {length_instruction}. "
            "Return only the summary text.\n\n"
            f"Article:\n{text[:12000]}"
        )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a precise news summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        if settings.openrouter_api_key:
            headers["HTTP-Referer"] = settings.app_url
            headers["X-Title"] = "German News Summarizer"

        try:
            with httpx.Client(timeout=40.0) as client:
                response = client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                return content
        except Exception:
            return None

    @staticmethod
    def _extractive_summary(text: str, sentence_count: int, language: str) -> str:
        sentences = SummarizationService._split_sentences(text)
        sentences = [s for s in sentences if 6 <= len(s.split()) <= 45]
        if len(sentences) <= sentence_count:
            return " ".join(sentences)

        words = re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", text.lower())
        stopwords = STOPWORDS_DE if language == "de" else STOPWORDS_EN
        freq = Counter(word for word in words if word not in stopwords)
        if not freq:
            return " ".join(sentences[:sentence_count])

        sentence_scores: List[tuple[int, float]] = []
        for idx, sentence in enumerate(sentences):
            sentence_words = re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", sentence.lower())
            if not sentence_words:
                sentence_scores.append((idx, 0.0))
                continue
            score = sum(freq.get(word, 0) for word in sentence_words) / len(sentence_words)
            # Add a small lead bias to keep summaries coherent.
            if idx < 3:
                score *= 1.12
            sentence_scores.append((idx, score))

        top_indices = sorted(
            [idx for idx, _ in sorted(sentence_scores, key=lambda item: item[1], reverse=True)[:sentence_count]]
        )
        selected = [sentences[idx] for idx in top_indices]
        return " ".join(selected)

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        parts = re.split(r"(?<=[.!?])\s+", text.strip())
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _looks_german(text: str) -> bool:
        lowered = f" {text.lower()} "
        if any(ch in lowered for ch in ["ä", "ö", "ü", "ß"]):
            return True
        de_markers = [" und ", " der ", " die ", " das ", " nicht ", " ist ", " mit ", " auf "]
        return sum(lowered.count(marker) for marker in de_markers) >= 4

    @staticmethod
    def _translate_de_to_en(text: str) -> str | None:
        if not text.strip():
            return None

        # First choice: deep-translator if installed.
        if GoogleTranslator is not None:
            try:
                return GoogleTranslator(source="de", target="en").translate(text)
            except Exception:
                pass

        # Second choice: public MyMemory API fallback via stdlib.
        # Keep payload small for URL-based GET endpoint reliability.
        query = quote(text[:1200])
        url = f"https://api.mymemory.translated.net/get?q={query}&langpair=de|en"
        try:
            with urlopen(url, timeout=12) as response:
                payload = json.loads(response.read().decode("utf-8", errors="ignore"))
            translated = payload.get("responseData", {}).get("translatedText", "").strip()
            if translated:
                return translated
        except Exception:
            return None

        return None
