from __future__ import annotations

from datetime import UTC, datetime

from xr_monitor.collector import CollectionError, Collector, ParserError
from xr_monitor.models import HealthState, Source, SourceStatus
from xr_monitor.store import JsonStore


def collect_source(source: Source, collector: Collector, store: JsonStore) -> str:
    try:
        snapshot = collector.collect(source)
    except CollectionError as error:
        if isinstance(error, ParserError):
            state: HealthState = "parser_broken"
        elif source.enabled:
            state = "fetch_failed"
        else:
            state = "unconfigured"
        status = SourceStatus(
            source_id=source.id,
            checked_at=datetime.now(UTC),
            state=state,
            message=str(error),
        )
        store.save_status(status)
        store.append_log({"source_id": source.id, "result": "failed", "message": str(error)})
        raise

    previous = store.read_snapshot(source.id)
    if previous is None:
        result = "initial"
    elif previous.content_hash != snapshot.content_hash:
        result = "changed"
    else:
        result = "unchanged"
    store.save_snapshot(snapshot)
    store.save_status(SourceStatus(source_id=source.id, checked_at=datetime.now(UTC), state="ok"))
    store.append_log(
        {"source_id": source.id, "result": result, "content_hash": snapshot.content_hash}
    )
    return result


def diff_source(source: Source, collector: Collector, store: JsonStore) -> str:
    previous = store.read_snapshot(source.id)
    if previous is None:
        return "missing_snapshot"
    current = collector.collect(source)
    return "changed" if current.content_hash != previous.content_hash else "unchanged"
