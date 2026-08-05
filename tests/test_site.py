from datetime import UTC, datetime
from pathlib import Path

from xr_monitor.collector import Collector
from xr_monitor.models import Snapshot, Source
from xr_monitor.normalizer import content_hash
from xr_monitor.service import collect_source
from xr_monitor.site import build_site
from xr_monitor.store import JsonStore


class FixtureCollector(Collector):
    def collect(self, source: Source) -> Snapshot:
        content = "A fixed OpenXR issue."
        return Snapshot(
            source_id=source.id,
            fetched_at=datetime.now(UTC),
            url="https://example.com/release-notes",
            content_hash=content_hash(content),
            normalized_content=content,
        )


def source() -> Source:
    return Source(
        id="unity_editor_release_notes",
        name="Unity Editor Release Notes",
        tier="S",
        kind="html",
        url="https://example.com/release-notes",
        content_selector="article",
        access_status="verified_allowed",
        enabled=True,
    )


def test_build_site_writes_html_and_search_index(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    collect_source(source(), FixtureCollector(), JsonStore(data_dir))
    template_dir = Path(__file__).parents[1] / "templates"
    (tmp_path / "templates").mkdir()
    for template in template_dir.glob("*.html"):
        target = tmp_path / "templates" / template.name
        target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    output = build_site(tmp_path)
    assert (output / "index.html").exists()
    assert list((output / "updates").glob("*.html"))
    assert "XR Development Monitor" in (output / "index.html").read_text(encoding="utf-8")
    assert (output / "search-index.json").exists()
