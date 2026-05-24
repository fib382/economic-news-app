from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import feedparser
import requests
from dateutil import parser

from collector.models import NewsItem
from collector.processing.classify import classify_text, tags_for_text
from collector.processing.importance import score_news_importance
from collector.processing.summarize import market_impact_for_category, template_summary


FRB_FEEDS = [
    "https://www.federalreserve.gov/feeds/press_all.xml",
    "https://www.federalreserve.gov/feeds/speeches.xml",
    "https://www.federalreserve.gov/feeds/testimony.xml",
]
JST = ZoneInfo("Asia/Tokyo")


def fetch_frb(timeout: int = 20) -> list[NewsItem]:
    fetched_at = datetime.now(JST)
    items: list[NewsItem] = []
    for feed_url in FRB_FEEDS:
        response = requests.get(feed_url, headers={"User-Agent": "economic-news-app-collector/1.0"}, timeout=timeout)
        response.raise_for_status()
        parsed = feedparser.parse(response.content)
        if parsed.bozo and not parsed.entries:
            continue
        for entry in parsed.entries[:30]:
            title = entry.get("title", "")
            url = entry.get("link", "")
            if not title or not url:
                continue
            published_at = _parse_entry_date(entry)
            summary_text = _strip_summary(entry.get("summary", ""))
            category = classify_text(title, summary_text) if "federal reserve" not in title.lower() else "FRB"
            if category == "その他":
                category = "FRB"
            item = NewsItem(
                id="",
                source="FRB",
                source_type="rss",
                title=title,
                summary=summary_text or template_summary(title, category),
                url=url,
                published_at=published_at,
                fetched_at=fetched_at,
                language="en",
                country="US",
                category=category,
                confidence="high",
                market_impact=market_impact_for_category(category),
                tags=tags_for_text(title, summary_text),
            )
            item.importance = score_news_importance(item)
            items.append(item)
    return items


def _parse_entry_date(entry: dict) -> datetime:
    for key in ("published", "updated", "created"):
        value = entry.get(key)
        if value:
            try:
                return parser.parse(value)
            except (TypeError, ValueError):
                pass
    return datetime.now(ZoneInfo("UTC"))


def _strip_summary(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())[:500]
