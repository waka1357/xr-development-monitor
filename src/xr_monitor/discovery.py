from __future__ import annotations

import re

import httpx

from xr_monitor.collector import CollectionError
from xr_monitor.models import Source

RELEASE_URL = re.compile(r"https://unity\.com/releases/editor/whats-new/(6000\.\d+\.\d+f\d+)")


def discover_unity_6_release_urls(source: Source) -> list[str]:
    if source.discovery_url is None or source.access_status != "verified_allowed":
        raise CollectionError(f"source discovery is not enabled: {source.id}")
    try:
        response = httpx.get(
            str(source.discovery_url),
            timeout=20.0,
            headers={"User-Agent": "XR-Development-Monitor/0.1 (official-source monitoring)"},
        )
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise CollectionError(f"discovery request failed: {error}") from error
    return list(dict.fromkeys(match.group(0) for match in RELEASE_URL.finditer(response.text)))
