"""Baseline tasks for lesson 4."""

import json


def count_selected(media_ids: list[str]) -> int:
    """Return the number of distinct media items."""
    return len(set(media_ids))


def group_by_gallery(media: list[dict]) -> dict[str, list[str]]:
    """Map each gallery id to the list of media ids in it, in input order."""
    result: dict[str, list[str]] = {}
    for item in media:
        result.setdefault(item["gallery_id"], []).append(item["id"])
    return result


def total_price(prices_minor: list[int | None]) -> int:
    """Return the sum of the prices, ignoring None values."""
    return sum(price for price in prices_minor if price is not None)


def first_missing(required: list[str], present: list[str]) -> str | None:
    """Return the first item in `required` that is not in `present`, or None."""
    present_items = set(present)
    for item in required:
        if item not in present_items:
            return item
    return None


def load_events(path) -> list[dict]:
    """Read a UTF-8 JSON file, so Hebrew titles stay intact."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)