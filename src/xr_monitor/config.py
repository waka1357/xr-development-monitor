from pathlib import Path

import yaml

from xr_monitor.models import Source


def load_sources(path: Path) -> dict[str, Source]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ValueError("sources.yml must contain a 'sources' list")
    sources = [Source.model_validate(item) for item in raw["sources"]]
    result = {source.id: source for source in sources}
    if len(result) != len(sources):
        raise ValueError("source ids must be unique")
    return result
