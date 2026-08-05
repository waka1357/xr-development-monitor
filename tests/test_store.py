from datetime import UTC, datetime
from pathlib import Path

from xr_monitor.models import Snapshot
from xr_monitor.store import JsonStore


def test_snapshot_does_not_persist_full_source_content(tmp_path: Path) -> None:
    store = JsonStore(tmp_path)
    full_content = "official source content that must not be committed in full"
    store.save_snapshot(
        Snapshot(
            source_id="example",
            fetched_at=datetime.now(UTC),
            url="https://example.com/source",
            content_hash="a" * 64,
            content_excerpt="official source content",
            normalized_content=full_content,
        )
    )
    stored = (tmp_path / "snapshots" / "example.json").read_text(encoding="utf-8")
    assert full_content not in stored
    assert "official source content" in stored
