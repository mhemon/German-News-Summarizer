from dataclasses import dataclass
from html import unescape
from urllib.request import Request, urlopen

import re

try:
    import trafilatura
except ModuleNotFoundError:
    trafilatura = None

from app.utils.helpers import extract_domain


@dataclass
class ExtractedArticle:
    title: str
    source: str
    article_text: str


class ExtractionService:
    """Extract article text and metadata from URLs."""

    BOILERPLATE_PATTERNS = [
        r"you need to enable javascript",
        r"zum inhalt springen",
        r"zur hauptnavigation springen",
        r"zu weiteren angeboten",
        r"cookie",
        r"datenschutz",
        r"impressum",
        r"newsletter",
    ]

    @staticmethod
    def extract_from_url(url: str) -> ExtractedArticle:
        if trafilatura is None:
            return ExtractionService._extract_with_stdlib(url)

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError("Unable to fetch article URL")

        # Prefer metadata-aware extraction so we get a title when possible.
        metadata = trafilatura.extract_metadata(downloaded)
        extracted = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            output_format="txt",
            with_metadata=False,
        )

        if not extracted or len(extracted.split()) < 40:
            raise ValueError("Could not extract enough article content from URL")

        title = (metadata.title if metadata and metadata.title else "Extracted Article").strip()
        source = extract_domain(url)

        return ExtractedArticle(
            title=title,
            source=source,
            article_text=extracted,
        )

    @staticmethod
    def _extract_with_stdlib(url: str) -> ExtractedArticle:
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )
            with urlopen(req, timeout=15) as response:
                raw_html = response.read().decode("utf-8", errors="ignore")
        except Exception as exc:
            raise ValueError(f"Unable to fetch article URL: {exc}")

        title_match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, flags=re.IGNORECASE | re.DOTALL)
        title = unescape(title_match.group(1)).strip() if title_match else "Extracted Article"

        html = re.sub(r"<script[^>]*>.*?</script>", " ", raw_html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.IGNORECASE | re.DOTALL)

        # Prefer semantic article block when available.
        article_match = re.search(r"<article[^>]*>(.*?)</article>", html, flags=re.IGNORECASE | re.DOTALL)
        extraction_scope = article_match.group(1) if article_match else html

        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", extraction_scope, flags=re.IGNORECASE | re.DOTALL)
        cleaned_paragraphs = []
        seen = set()

        for paragraph in paragraphs:
            text = re.sub(r"<[^>]+>", " ", paragraph)
            text = unescape(text)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text.split()) < 8:
                continue
            lowered = text.lower()
            if any(re.search(pattern, lowered) for pattern in ExtractionService.BOILERPLATE_PATTERNS):
                continue
            key = lowered[:180]
            if key in seen:
                continue
            seen.add(key)
            cleaned_paragraphs.append(text)

        text = "\n".join(cleaned_paragraphs)

        # Last-resort fallback: strip tags from entire page.
        if len(text.split()) < 80:
            stripped = re.sub(r"<[^>]+>", " ", html)
            stripped = unescape(stripped)
            stripped = re.sub(r"\s+", " ", stripped).strip()
            text = stripped

        if len(text.split()) < 80:
            raise ValueError(
                "Could not extract enough article content from URL with fallback parser. "
                "Install trafilatura for better extraction quality."
            )

        return ExtractedArticle(
            title=title,
            source=extract_domain(url),
            article_text=text,
        )
