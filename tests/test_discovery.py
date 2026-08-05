from xr_monitor.discovery import release_source
from xr_monitor.models import Source


def test_release_source_uses_a_stable_per_version_id() -> None:
    source = Source(
        id="unity_editor_release_notes",
        name="Unity Editor Release Notes",
        tier="S",
        kind="html",
        url="https://unity.com/releases/editor/whats-new/6000.4.3f1",
        discovery_url="https://unity.com/releases/sitemap/6000.xml",
        content_selector="main",
        access_status="verified_allowed",
        enabled=True,
    )
    result = release_source(source, "https://unity.com/releases/editor/whats-new/6000.5.6f1")
    assert result.id == "unity_editor_release_notes_6000_5_6f1"
    assert result.name.endswith("6000.5.6f1")
