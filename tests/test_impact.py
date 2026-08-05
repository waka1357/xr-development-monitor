from xr_monitor.impact import assess_environment_impact
from xr_monitor.models import Source, UserProfile


def source(version: str) -> Source:
    return Source(
        id="unity_editor_release_notes",
        name="Unity Editor Release Notes",
        tier="S",
        kind="html",
        url=f"https://unity.com/releases/editor/whats-new/{version}",
        content_selector="main",
        access_status="verified_allowed",
        enabled=True,
    )


def test_environment_impact_compares_configured_unity_versions() -> None:
    profile = UserProfile(name="default", active_unity_versions=["6000.4.3f1", "6000.3.18f1"])
    assert assess_environment_impact(source("6000.4.3f1"), profile).level == "confirmed"
    assert assess_environment_impact(source("6000.4.9f1"), profile).level == "likely"
    assert assess_environment_impact(source("6000.5.1f1"), profile).level == "review"


def test_environment_impact_is_unknown_without_a_profile() -> None:
    assert assess_environment_impact(source("6000.4.3f1"), None).level == "unknown"
