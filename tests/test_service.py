from datetime import UTC, datetime
from pathlib import Path

import pytest

from xr_monitor.collector import CollectionError, Collector, ParserError
from xr_monitor.models import Snapshot, Source
from xr_monitor.normalizer import content_hash
from xr_monitor.service import collect_source, diff_source
from xr_monitor.store import JsonStore


class FixtureCollector(Collector):
    def __init__(self, content: str) -> None:
        self.content = content

    def collect(self, source: Source) -> Snapshot:
        return Snapshot(
            source_id=source.id,
            fetched_at=datetime.now(UTC),
            url="https://example.com/release-notes",
            content_hash=content_hash(self.content),
            content_excerpt=self.content,
            normalized_content=self.content,
        )


class FailingCollector(Collector):
    def collect(self, source: Source) -> Snapshot:
        raise CollectionError("fixture request failed")


class BrokenParserCollector(Collector):
    def collect(self, source: Source) -> Snapshot:
        raise ParserError("fixture parser failed")


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


def test_initial_then_unchanged_then_changed(tmp_path: Path) -> None:
    store = JsonStore(tmp_path)
    assert collect_source(source(), FixtureCollector("version 1"), store) == "initial"
    assert len(store.list_records()) == 1
    assert collect_source(source(), FixtureCollector("version 1"), store) == "unchanged"
    assert diff_source(source(), FixtureCollector("version 2"), store) == "changed"
    assert collect_source(source(), FixtureCollector("version 2"), store) == "changed"
    assert len(store.list_records()) == 2


def test_failure_keeps_previous_snapshot_and_records_status(tmp_path: Path) -> None:
    store = JsonStore(tmp_path)
    collect_source(source(), FixtureCollector("known good"), store)
    with pytest.raises(CollectionError):
        collect_source(source(), FailingCollector(), store)
    snapshot = store.read_snapshot(source().id)
    status = store.read_status(source().id)
    assert snapshot is not None
    assert snapshot.content_excerpt == "known good"
    assert status is not None
    assert status.state == "fetch_failed"


def test_parser_failure_is_recorded_separately(tmp_path: Path) -> None:
    store = JsonStore(tmp_path)
    with pytest.raises(ParserError):
        collect_source(source(), BrokenParserCollector(), store)
    status = store.read_status(source().id)
    assert status is not None
    assert status.state == "parser_broken"
