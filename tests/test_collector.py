from pathlib import Path

import pytest

from xr_monitor.collector import HtmlCollector, ParserError

FIXTURES = Path(__file__).parent / "fixtures"


def test_html_collector_normalizes_fixture() -> None:
    html = (FIXTURES / "release_notes_v1.html").read_text(encoding="utf-8")
    actual = HtmlCollector().extract(html, "article")
    assert actual == "Unity 6000.4.3f1 Fixed an XR Android rendering issue."


def test_html_collector_rejects_missing_selector() -> None:
    with pytest.raises(ParserError, match="selector returned no content"):
        HtmlCollector().extract("<html><body>empty</body></html>", "article")
