from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime

import httpx
from bs4 import BeautifulSoup

from xr_monitor.models import Snapshot, Source
from xr_monitor.normalizer import content_hash, normalize_html_text


class CollectionError(RuntimeError):
    pass


class ParserError(CollectionError):
    pass


class Collector(ABC):
    @abstractmethod
    def collect(self, source: Source) -> Snapshot:
        """Fetch a source and return an unpersisted snapshot."""
        raise NotImplementedError


class HtmlCollector(Collector):
    def __init__(self, *, timeout_seconds: float = 20.0) -> None:
        self.timeout_seconds = timeout_seconds

    def extract(self, html: str, selector: str) -> str:
        document = BeautifulSoup(html, "html.parser")
        matches = document.select(selector)
        if not matches:
            raise ParserError(f"selector returned no content: {selector}")
        normalized = normalize_html_text(" ".join(node.get_text(" ") for node in matches))
        if not normalized:
            raise ParserError("selector returned only empty content")
        return normalized

    def collect(self, source: Source) -> Snapshot:
        if source.access_status != "verified_allowed":
            raise CollectionError(f"source is not permitted for automated collection: {source.id}")
        if not source.enabled or source.url is None:
            raise CollectionError(f"source is not enabled: {source.id}")
        try:
            response = httpx.get(
                str(source.url),
                timeout=self.timeout_seconds,
                follow_redirects=True,
                headers={"User-Agent": "XR-Development-Monitor/0.1 (official-source monitoring)"},
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise CollectionError(f"request failed: {error}") from error
        content = self.extract(response.text, source.content_selector)
        return Snapshot(
            source_id=source.id,
            fetched_at=datetime.now(UTC),
            url=source.url,
            content_hash=content_hash(content),
            normalized_content=content,
        )
