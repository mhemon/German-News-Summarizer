def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes."""
    word_count = len(text.split())
    return max(1, round(word_count / words_per_minute))


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain or "Unknown"
    except Exception:
        return "Unknown"


def is_url(text: str) -> bool:
    """Check if text is a URL."""
    return text.strip().startswith(("http://", "https://", "www."))
