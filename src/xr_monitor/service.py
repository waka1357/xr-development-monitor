from __future__ import annotations

from datetime import UTC, datetime

from xr_monitor.classifier import classify
from xr_monitor.collector import CollectionError, Collector, ParserError
from xr_monitor.impact import assess_environment_impact
from xr_monitor.models import HealthState, Source, SourceStatus, UpdateRecord, UserProfile
from xr_monitor.relevance import extract_xr_relevant_excerpt
from xr_monitor.store import JsonStore


def collect_source(
    source: Source, collector: Collector, store: JsonStore, profile: UserProfile | None = None
) -> str:
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
    has_record = any(record.source_id == source.id for record in store.list_records())
    if previous is None or not has_record:
        result = "initial"
    elif previous.content_hash != snapshot.content_hash:
        result = "changed"
    else:
        result = "unchanged"
    record_id = f"{source.id}-{snapshot.content_hash[:12]}"
    if result != "unchanged" or not store.record_exists(record_id):
        store.save_snapshot(snapshot)
        record = UpdateRecord(
            id=record_id,
            kind="initial" if result in {"initial", "unchanged"} else "changed",
            source_id=source.id,
            source_name=source.name,
            detected_at=snapshot.fetched_at,
            source_url=snapshot.url,
            content_hash=snapshot.content_hash,
            official_content=extract_xr_relevant_excerpt(snapshot.normalized_content),
            system_assessment=classify(snapshot.normalized_content),
            environment_impact=assess_environment_impact(source, profile),
        )
        store.save_record(record)
        store.save_status(
            SourceStatus(source_id=source.id, checked_at=datetime.now(UTC), state="ok")
        )
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
