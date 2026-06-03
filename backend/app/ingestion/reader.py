from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class IngestionError:
    feed: str
    index: int
    error: str


def read_json_feed(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Feed {path} must contain a JSON array")
    return data


def read_all_feeds(feeds_dir: Path) -> list[tuple[str, list[dict]]]:
    if not feeds_dir.exists():
        return []
    feeds: list[tuple[str, list[dict]]] = []
    for path in sorted(feeds_dir.glob("*.json")):
        feeds.append((path.name, read_json_feed(path)))
    return feeds
