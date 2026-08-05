from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from xr_monitor.models import UpdateRecord
from xr_monitor.store import JsonStore


def _excerpt(content: str, length: int = 500) -> str:
    return content if len(content) <= length else f"{content[:length].rstrip()}…"


def _record_view(record: UpdateRecord) -> dict[str, object]:
    return {
        "id": record.id,
        "kind": record.kind,
        "source_id": record.source_id,
        "source_name": record.source_name,
        "detected_at": record.detected_at.strftime("%Y-%m-%d %H:%M UTC"),
        "source_url": str(record.source_url),
        "official_content": _excerpt(record.official_content),
        "assessment": record.system_assessment.model_dump(),
    }


def build_site(project_root: Path) -> Path:
    store = JsonStore(project_root / "data")
    records = [_record_view(record) for record in store.list_records()]
    statuses = [status.model_dump(mode="json") for status in store.list_statuses()]
    output = project_root / "site"
    details = output / "updates"
    details.mkdir(parents=True, exist_ok=True)
    environment = Environment(
        loader=FileSystemLoader(project_root / "templates"), autoescape=select_autoescape(["html"])
    )
    context = {"records": records, "statuses": statuses}
    (output / "index.html").write_text(
        environment.get_template("index.html").render(**context), encoding="utf-8"
    )
    for record in records:
        (details / f"{record['id']}.html").write_text(
            environment.get_template("detail.html").render(record=record), encoding="utf-8"
        )
    (output / "search-index.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return output
