import re


class TextCleaningService:
    """Normalize and denoise extracted article text."""

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = [line.strip() for line in normalized.split("\n")]

        cleaned_lines = []
        seen = set()
        for line in lines:
            if len(line) < 2:
                continue
            if re.fullmatch(r"[\W_]+", line):
                continue
            # Remove duplicate fragments often found in scraped pages.
            key = line.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned_lines.append(line)

        cleaned = "\n".join(cleaned_lines)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned
