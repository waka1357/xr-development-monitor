from pathlib import Path

from xr_monitor.config import load_sources


def test_loads_initial_official_sources() -> None:
    path = Path(__file__).parents[1] / "config" / "sources.yml"
    sources = load_sources(path)
    assert set(sources) == {
        "unity_editor_release_notes",
        "unity_openxr_plugin",
        "meta_horizon_developer_release_notes",
    }
    assert sources["unity_editor_release_notes"].access_status == "verified_allowed"
    assert sources["unity_editor_release_notes"].enabled
    assert not sources["unity_openxr_plugin"].enabled
    assert sources["unity_openxr_plugin"].disabled_reason is not None
    assert not sources["meta_horizon_developer_release_notes"].enabled
    assert sources["meta_horizon_developer_release_notes"].access_status == "requires_permission"
