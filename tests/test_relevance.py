from xr_monitor.relevance import extract_xr_relevant_excerpt


def test_extracts_text_near_xr_keyword() -> None:
    content = "General note. " + "x" * 250
    content += " Android XR builds now support a new validation rule. "
    result = extract_xr_relevant_excerpt(content)
    assert "Android XR builds" in result


def test_does_not_infer_relevance_when_no_keyword_exists() -> None:
    assert "No XR" in extract_xr_relevant_excerpt("Only animation and audio changes.")


def test_does_not_match_ar_or_vr_inside_unrelated_words() -> None:
    content = "Shader variants improve artwork and virtualized rendering."
    assert "No XR" in extract_xr_relevant_excerpt(content)


def test_finds_a_later_xr_match_after_an_earlier_match() -> None:
    content = "Quest settings. " + "x" * 1_000 + " OpenXR validation changed."
    result = extract_xr_relevant_excerpt(content)
    assert "OpenXR validation changed" in result
