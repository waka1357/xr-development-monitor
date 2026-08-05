from xr_monitor.relevance import extract_xr_relevant_excerpt


def test_extracts_text_near_xr_keyword() -> None:
    content = "General note. " + "x" * 250
    content += " Android XR builds now support a new validation rule. "
    result = extract_xr_relevant_excerpt(content)
    assert "Android XR builds" in result


def test_does_not_infer_relevance_when_no_keyword_exists() -> None:
    assert "No XR" in extract_xr_relevant_excerpt("Only animation and audio changes.")
