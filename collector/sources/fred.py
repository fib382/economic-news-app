from __future__ import annotations

from datetime import datetime

import requests

from collector.config import FRED_SERIES
from collector.models import MarketSnapshotItem


FRED_OBSERVATIONS_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred(api_key: str | None, timeout: int = 20) -> tuple[list[MarketSnapshotItem], str]:
    if not api_key:
        return [], "FRED_API_KEY is not set; skipped FRED market snapshot."

    items: list[MarketSnapshotItem] = []
    for symbol, (name, unit, category) in FRED_SERIES.items():
        response = requests.get(
            FRED_OBSERVATIONS_URL,
            params={
                "series_id": symbol,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 10,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        observations = [obs for obs in response.json().get("observations", []) if obs.get("value") not in {None, "."}]
        if not observations:
            continue
        latest = observations[0]
        previous = observations[1] if len(observations) > 1 else None
        value = _float_or_none(latest.get("value"))
        previous_value = _float_or_none(previous.get("value")) if previous else None
        change_1d = round(value - previous_value, 4) if value is not None and previous_value is not None else None
        items.append(
            MarketSnapshotItem(
                symbol=symbol,
                name=name,
                source="FRED",
                value=value,
                unit=unit,
                date=datetime.strptime(latest["date"], "%Y-%m-%d").date(),
                change_1d=change_1d,
                category=category,
            )
        )
    return items, "ok"


def _float_or_none(value: str | None) -> float | None:
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None

