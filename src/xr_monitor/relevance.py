import re

KEYWORD_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bopenxr\b",
        r"\bmeta\s+quest\b",
        r"\boculus\b",
        r"\bquest\b",
        r"\bandroid\b",
        r"\bxr\b",
        r"\bvr\b",
        r"\bar\b",
    )
)


def extract_xr_relevant_excerpt(content: str, limit: int = 1_500) -> str:
    """Return only source text near XR-related terms; do not infer relevance."""
    positions = sorted(
        {match.start() for pattern in KEYWORD_PATTERNS for match in pattern.finditer(content)}
    )
    if not positions:
        return (
            "No XR, OpenXR, Meta Quest, or Android keyword was found "
            "in the collected official text."
        )
    excerpts: list[str] = []
    for position in positions:
        start = max(0, position - 180)
        end = min(len(content), position + 420)
        excerpt = content[start:end].strip()
        if excerpt not in excerpts:
            excerpts.append(excerpt)
        if len(" … ".join(excerpts)) >= limit:
            break
    return " … ".join(excerpts)[:limit].rstrip()
