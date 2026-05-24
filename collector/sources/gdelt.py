from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from dateutil import parser

from collector.config import KEYWORDS
from collector.models import NewsItem
from collector.processing.classify import classify_text, tags_for_text
from collector.processing.importance import score_news_importance
from collector.processing.summarize import market_impact_for_category, template_summary


GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
JST = ZoneInfo("Asia/Tokyo")


def fetch_gdelt(max_records: int = 50, timeout: int = 20) -> list[NewsItem]:
    response = _request_gdelt(_build_query(KEYWORDS[:14]), max_records, timeout)
    articles = response.json().get("articles", [])
    fetched_at = datetime.now(JST)
    items: list[NewsItem] = []
    for article in articles:
        title = article.get("title") or ""
        url = article.get("url") or ""
        if not title or not url:
            continue
        published_at = _parse_gdelt_date(article.get("seendate"))
        category = classify_text(title)
        item = NewsItem(
            id="",
            source="GDELT",
            source_type="news_api",
            title=title,
            summary=template_summary(title, category),
            url=url,
            published_at=published_at,
            fetched_at=fetched_at,
            language=article.get("language") or "en",
            country=article.get("sourceCountry") or "",
            category=category,
            confidence="medium",
            market_impact=market_impact_for_category(category),
            tags=tags_for_text(title),
        )
        item.importance = score_news_importance(item)
        items.append(item)
    return items


def _request_gdelt(query: str, max_records: int, timeout: int) -> requests.Response:
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_records,
        "sort": "HybridRel",
    }
    headers = {"User-Agent": "economic-news-app-collector/1.0"}
    try:
        response = requests.get(GDELT_DOC_URL, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException:
        fallback = _build_query(["Iran", "Israel", "Hormuz", "sanctions", "nuclear"])
        response = requests.get(
            GDELT_DOC_URL,
            params={**params, "query": fallback, "maxrecords": min(max_records, 20)},
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        return response


def _build_query(keywords: list[str]) -> str:
    return "(" + " OR ".join(f'"{keyword}"' if " " in keyword else keyword for keyword in keywords) + ")"


def _parse_gdelt_date(value: str | None) -> datetime:
    if not value:
        return datetime.now(ZoneInfo("UTC"))
    try:
        return parser.parse(value)
    except (TypeError, ValueError):
        return datetime.now(ZoneInfo("UTC"))
