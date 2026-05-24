from datetime import datetime, timezone

from collector.models import NewsItem
from collector.processing.dedupe import dedupe_news, normalize_title


def item(title: str, url: str) -> NewsItem:
    return NewsItem(
        id="",
        source="GDELT",
        source_type="news_api",
        title=title,
        url=url,
        published_at=datetime(2026, 5, 24, tzinfo=timezone.utc),
        fetched_at=datetime(2026, 5, 24, tzinfo=timezone.utc),
    )


def test_normalize_title_removes_punctuation() -> None:
    assert normalize_title("Iran: Sanctions, Again!") == "iran sanctions again"


def test_dedupe_by_url() -> None:
    result = dedupe_news([item("Iran news", "https://example.com/a"), item("Different title", "https://example.com/a")])
    assert len(result) == 1
    assert result[0].id


def test_dedupe_by_similar_title() -> None:
    result = dedupe_news(
        [
            item("Federal Reserve signals rate cut debate", "https://example.com/a"),
            item("Federal Reserve signals rate cut debate.", "https://example.com/b"),
        ]
    )
    assert len(result) == 1

