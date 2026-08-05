from pathlib import Path

import yaml

from xr_monitor.models import Source, UserProfile


def load_sources(path: Path) -> dict[str, Source]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ValueError("sources.yml must contain a 'sources' list")
    sources = [Source.model_validate(item) for item in raw["sources"]]
    result = {source.id: source for source in sources}
    if len(result) != len(sources):
        raise ValueError("source ids must be unique")
    return result


def load_user_profile(path: Path) -> UserProfile:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("profile"), dict):
        raise ValueError("user-profile.yml must contain a 'profile' mapping")
    profile = raw["profile"]
    editors = profile.get("unity_editors", [])
    if not isinstance(editors, list):
        raise ValueError("profile.unity_editors must be a list")
    active_versions = [
        editor["version"]
        for editor in editors
        if isinstance(editor, dict)
        and editor.get("status") == "active"
        and isinstance(editor.get("version"), str)
    ]
    return UserProfile(
        name=str(profile.get("name", "default")), active_unity_versions=active_versions
    )
