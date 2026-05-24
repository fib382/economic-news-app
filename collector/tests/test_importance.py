from datetime import date, datetime, timezone

from collector.models import MarketSnapshotItem, NewsItem
from collector.processing.importance import score_market_importance, score_news_importance


def news(title: str, category: str = "その他", source: str = "GDELT") -> NewsItem:
    return NewsItem(
        id="",
        source=source,
        source_type="news_api",
        title=title,
        url="https://example.com/a",
        published_at=datetime(2026, 5, 24, tzinfo=timezone.utc),
        fetched_at=datetime(2026, 5, 24, tzinfo=timezone.utc),
        category=category,
    )


def test_scores_major_fomc_news_a() -> None:
    assert score_news_importance(news("FOMC statement discusses policy rate", source="FRB")) == "A"


def test_scores_geopolitical_cluster_a() -> None:
    assert score_news_importance(news("Iran and Israel trade missile warnings", category="イラン・中東情勢")) == "A"


def test_scores_minor_news_c() -> None:
    assert score_news_importance(news("Regional market commentary")) == "C"


def test_scores_10y_yield_move_a() -> None:
    item = MarketSnapshotItem(
        symbol="DGS10",
        name="米10年債利回り",
        source="FRED",
        value=4.45,
        unit="%",
        date=date(2026, 5, 23),
        change_1d=0.11,
        category="債券",
    )
    assert score_market_importance(item) == "A"

