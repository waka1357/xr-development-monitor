KEYWORDS = ("xr", "openxr", "meta quest", "oculus", "quest", "android", "vr", "ar")


def extract_xr_relevant_excerpt(content: str, limit: int = 1_500) -> str:
    """Return only source text near XR-related terms; do not infer relevance."""
    lowered = content.lower()
    positions = sorted(
        {lowered.find(keyword) for keyword in KEYWORDS if lowered.find(keyword) >= 0}
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
