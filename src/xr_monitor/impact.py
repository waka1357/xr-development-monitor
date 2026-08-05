from __future__ import annotations

import re

from xr_monitor.models import EnvironmentImpact, Source, UserProfile

UNITY_VERSION = re.compile(r"\b(6000\.\d+\.\d+f\d+)\b")


def assess_environment_impact(source: Source, profile: UserProfile | None) -> EnvironmentImpact:
    """Return a configuration comparison, not a claim about release-note contents."""
    if profile is None or not profile.active_unity_versions:
        return EnvironmentImpact(
            level="unknown", reason="No active Unity Editor version is configured."
        )
    match = UNITY_VERSION.search(str(source.url))
    if match is None:
        return EnvironmentImpact(
            level="unknown",
            reason="The update URL does not identify a Unity Editor release version.",
        )
    release_version = match.group(1)
    if release_version in profile.active_unity_versions:
        return EnvironmentImpact(
            level="confirmed",
            reason=(
                "Configured active Unity Editor version matches this release: "
                f"{release_version}."
            ),
        )
    release_stream = ".".join(release_version.split(".")[:2])
    active_streams = {".".join(version.split(".")[:2]) for version in profile.active_unity_versions}
    if release_stream in active_streams:
        return EnvironmentImpact(
            level="likely",
            reason=(
                f"This release is in Unity {release_stream}; an active configured editor "
                "is in the same release stream."
            ),
        )
    return EnvironmentImpact(
        level="review",
        reason=(
            "This release targets a different Unity release stream than the configured "
            "active editors; review it before planning an upgrade."
        ),
    )
