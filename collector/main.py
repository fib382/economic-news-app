from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import BaseModel

from collector.config import FRED_SERIES, get_settings
from collector.models import MarketSnapshotDocument, MarketSnapshotItem, NewsItemsDocument, SourceStatus, SourcesDocument
from collector.processing.dedupe import dedupe_news
from collector.processing.report import build_daily_report
from collector.sources.frb import fetch_frb
from collector.sources.fred import fetch_fred
from collector.sources.gdelt import fetch_gdelt


JST = ZoneInfo("Asia/Tokyo")


def main() -> int:
    settings = get_settings()
    now = datetime.now(JST)
    sources: list[SourceStatus] = []
    errors: list[dict[str, str]] = []
    news_items = []
    market_items = []

    try:
        gdelt_items = fetch_gdelt(max_records=settings.gdelt_max_records, timeout=settings.request_timeout)
        news_items.extend(gdelt_items)
        sources.append(_source_status("GDELT", "イラン・中東情勢", "API", "active", len(gdelt_items), now, "ok", "https://api.gdeltproject.org/api/v2/doc/doc"))
    except Exception as exc:
        errors.append({"source": "GDELT", "message": str(exc)})
        sources.append(_source_status("GDELT", "イラン・中東情勢", "API", "error", 0, now, str(exc), "https://api.gdeltproject.org/api/v2/doc/doc"))

    try:
        frb_items = fetch_frb(timeout=settings.request_timeout)
        news_items.extend(frb_items)
        sources.append(_source_status("FRB", "FRB", "RSS", "active", len(frb_items), now, "ok", "https://www.federalreserve.gov/feeds/"))
    except Exception as exc:
        errors.append({"source": "FRB", "message": str(exc)})
        sources.append(_source_status("FRB", "FRB", "RSS", "error", 0, now, str(exc), "https://www.federalreserve.gov/feeds/"))

    try:
        fred_items, message = fetch_fred(settings.fred_api_key, timeout=settings.request_timeout)
        market_items.extend(fred_items)
        status = "active" if settings.fred_api_key else "skipped"
        sources.append(_source_status("FRED", "市場データ", "API", status, len(fred_items), now, message, "https://fred.stlouisfed.org/docs/api/fred/"))
    except Exception as exc:
        errors.append({"source": "FRED", "message": str(exc)})
        sources.append(_source_status("FRED", "市場データ", "API", "error", 0, now, str(exc), "https://fred.stlouisfed.org/docs/api/fred/"))

    news_items = sorted(dedupe_news(news_items), key=lambda item: item.published_at, reverse=True)
    market_items = sorted(_with_market_placeholders(market_items), key=lambda item: item.symbol)

    settings.data_dir.mkdir(parents=True, exist_ok=True)
    _write_json(settings.data_dir / "news_items.json", NewsItemsDocument(generated_at=now, items=news_items))
    _write_json(settings.data_dir / "market_snapshot.json", MarketSnapshotDocument(generated_at=now, items=market_items))
    _write_json(settings.data_dir / "daily_report.json", build_daily_report(news_items, market_items, now))
    _write_json(settings.data_dir / "sources.json", SourcesDocument(generated_at=now, items=sources))
    _write_logs(settings.data_dir / "collector_log.json", now, errors)
    _write_logs(settings.data_dir.parents[1] / "logs" / "latest.json", now, errors)
    return 0


def _source_status(name: str, category: str, method: str, status: str, item_count: int, now: datetime, notes: str, url: str) -> SourceStatus:
    return SourceStatus(name=name, category=category, method=method, status=status, item_count=item_count, last_fetched_at=now, notes=notes[:500], url=url)


def _with_market_placeholders(items: list[MarketSnapshotItem]) -> list[MarketSnapshotItem]:
    by_symbol = {item.symbol: item for item in items}
    for symbol, (name, unit, category) in FRED_SERIES.items():
        if symbol not in by_symbol:
            by_symbol[symbol] = MarketSnapshotItem(
                symbol=symbol,
                name=name,
                source="FRED",
                value=None,
                unit=unit,
                date=None,
                change_1d=None,
                category=category,
            )
    return list(by_symbol.values())


def _write_json(path: Path, document: BaseModel) -> None:
    path.write_text(
        json.dumps(document.model_dump(mode="json"), ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def _write_logs(path: Path, now: datetime, errors: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generated_at": now.isoformat(), "errors": errors}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
