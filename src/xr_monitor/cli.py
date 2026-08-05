from __future__ import annotations

import argparse
from pathlib import Path

from xr_monitor.collector import CollectionError, HtmlCollector
from xr_monitor.config import load_sources
from xr_monitor.service import collect_source, diff_source
from xr_monitor.site import build_site
from xr_monitor.store import JsonStore


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(prog="xr-monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("collect", "diff"):
        sub = subparsers.add_parser(command)
        scope = sub.add_mutually_exclusive_group(required=True)
        scope.add_argument("--source")
        scope.add_argument("--schedule", choices=["daily"])
    subparsers.add_parser("build-site")
    args = parser.parse_args()
    root = _project_root()
    if args.command == "build-site":
        print(f"Built site: {build_site(root)}")
        return
    sources = load_sources(root / "config" / "sources.yml")
    if args.source:
        if args.source not in sources:
            parser.error(f"unknown source: {args.source}")
        selected = [sources[args.source]]
    else:
        selected = [source for source in sources.values() if source.enabled]
    collector = HtmlCollector()
    store = JsonStore(root / "data")
    failed = False
    for source in selected:
        try:
            if args.command == "collect":
                result = collect_source(source, collector, store)
            else:
                result = diff_source(source, collector, store)
            print(f"{source.id}: {result}")
        except CollectionError as error:
            failed = True
            print(f"{source.id}: failed: {error}")
    if failed:
        raise SystemExit(1)
