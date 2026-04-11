from app.models.schemas import Entity
from app.services.enrichment import EnrichmentService
from app.services.extraction import ExtractionService
from app.services.language import LanguageService
from app.services.summarization import SummarizationService
from app.services.text_cleaning import TextCleaningService
from app.utils.helpers import estimate_reading_time, is_url


class AnalysisService:
    """Production-style analysis pipeline for German news summarization."""

    @staticmethod
    def analyze(
        input_text: str,
        mode: str = "auto",
        summary_length: str = "medium",
    ) -> dict:
        resolved_is_url = is_url(input_text) if mode == "auto" else mode == "url"

        if resolved_is_url:
            extracted = ExtractionService.extract_from_url(input_text.strip())
            title = extracted.title
            source = extracted.source
            article_text_raw = extracted.article_text
        else:
            title = "Pasted Article"
            source = "Direct Input"
            article_text_raw = input_text

        article_text = TextCleaningService.clean(article_text_raw)
        if len(article_text.split()) < 40:
            raise ValueError("Input is too short after cleaning. Please provide a longer article.")

        language = LanguageService.detect_language(article_text)

        german_summary = SummarizationService.summarize_german(
            text=article_text,
            summary_length=summary_length,
        )
        english_summary = SummarizationService.summarize_english(
            text=article_text,
            summary_length=summary_length,
            source_language=language,
        )

        keywords = EnrichmentService.extract_keywords(article_text, language=language)
        entity_result = EnrichmentService.extract_entities(article_text)
        entities = Entity(**entity_result)

        reading_time = estimate_reading_time(article_text)
        tone = EnrichmentService.classify_tone(article_text, language=language)

        return {
            "title": title,
            "source": source,
            "language": language,
            "article_text": article_text,
            "reading_time_minutes": reading_time,
            "german_summary": german_summary,
            "english_summary": english_summary,
            "keywords": keywords,
            "entities": entities,
            "tone": tone,
        }
