from __future__ import annotations

import re
from difflib import SequenceMatcher

from collector.models import NewsItem, make_news_id


_NON_WORD_RE = re.compile(r"[^a-z0-9]+")


def normalize_title(title: str) -> str:
    return _NON_WORD_RE.sub(" ", title.lower()).strip()


def assign_id(item: NewsItem) -> NewsItem:
    item.id = make_news_id(item.source, normalize_title(item.title), item.published_at, str(item.url))
    return item


def dedupe_news(items: list[NewsItem], similarity_threshold: float = 0.94) -> list[NewsItem]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    kept: list[NewsItem] = []

    for item in items:
        url_key = str(item.url).rstrip("/")
        title_key = normalize_title(item.title)
        if url_key and url_key in seen_urls:
            continue
        if title_key and title_key in seen_titles:
            continue
        if any(_similar(title_key, normalize_title(existing.title)) >= similarity_threshold for existing in kept):
            continue

        kept.append(assign_id(item))
        if url_key:
            seen_urls.add(url_key)
        if title_key:
            seen_titles.add(title_key)

    return kept


def _similar(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()

