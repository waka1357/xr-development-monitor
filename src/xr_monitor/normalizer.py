import hashlib
import re


def normalize_html_text(text: str) -> str:
    """Normalize extracted text so insignificant HTML whitespace does not create a change."""
    return re.sub(r"\s+", " ", text).strip()


def content_hash(normalized_content: str) -> str:
    return hashlib.sha256(normalized_content.encode("utf-8")).hexdigest()
