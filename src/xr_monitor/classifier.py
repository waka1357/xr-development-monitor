from xr_monitor.models import Severity, SystemAssessment

RULES: tuple[tuple[str, tuple[str, ...], Severity], ...] = (
    ("breaking_change", ("breaking change", "incompatible", "not compatible"), "high"),
    ("deprecation", ("deprecated", "deprecation"), "high"),
    ("security", ("security", "vulnerability", "cve-"), "high"),
    ("migration", ("migration guide", "migrate your"), "medium"),
)


def classify(content: str) -> SystemAssessment:
    lowered = content.lower()
    matches = [
        (category, severity)
        for category, terms, severity in RULES
        if any(term in lowered for term in terms)
    ]
    if not matches:
        return SystemAssessment(
            categories=["documentation"], severity="info", reason="No Phase 2 rule keyword matched."
        )
    categories = [category for category, _ in matches]
    severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    severity = max((severity for _, severity in matches), key=severity_order.__getitem__)
    return SystemAssessment(
        categories=categories,
        severity=severity,
        reason="Matched configured Phase 2 keyword rules.",
    )
