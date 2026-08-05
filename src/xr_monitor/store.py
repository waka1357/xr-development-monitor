from __future__ import annotations

import json
from pathlib import Path

from xr_monitor.models import Snapshot, SourceStatus


class JsonStore:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    def _snapshot_path(self, source_id: str) -> Path:
        return self.data_dir / "snapshots" / f"{source_id}.json"

    def _status_path(self, source_id: str) -> Path:
        return self.data_dir / "source-status" / f"{source_id}.json"

    def read_snapshot(self, source_id: str) -> Snapshot | None:
        path = self._snapshot_path(source_id)
        if not path.exists():
            return None
        return Snapshot.model_validate_json(path.read_text(encoding="utf-8"))

    def save_snapshot(self, snapshot: Snapshot) -> None:
        path = self._snapshot_path(snapshot.source_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")

    def save_status(self, status: SourceStatus) -> None:
        path = self._status_path(status.source_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(status.model_dump_json(indent=2), encoding="utf-8")

    def read_status(self, source_id: str) -> SourceStatus | None:
        path = self._status_path(source_id)
        if not path.exists():
            return None
        return SourceStatus.model_validate_json(path.read_text(encoding="utf-8"))

    def append_log(self, event: dict[str, object]) -> None:
        path = self.data_dir / "logs" / "collection.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
