from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT_DIR / "public" / "data"


KEYWORDS = [
    "Iran",
    "Israel",
    "Middle East",
    "Strait of Hormuz",
    "Hormuz",
    "Tehran",
    "nuclear facility",
    "IAEA",
    "sanctions",
    "missile attack",
    "oil supply",
    "ceasefire",
    "retaliation",
    "Federal Reserve",
    "FOMC",
    "Jerome Powell",
    "inflation",
    "rate cut",
    "rate hike",
    "Treasury yield",
    "USD JPY",
    "S&P 500",
    "Nasdaq",
    "VIX",
    "WTI",
    "Brent",
]


FRED_SERIES = {
    "DGS2": ("米2年債利回り", "%", "債券"),
    "DGS10": ("米10年債利回り", "%", "債券"),
    "DGS30": ("米30年債利回り", "%", "債券"),
    "FEDFUNDS": ("FF金利", "%", "FRB"),
    "CPIAUCSL": ("CPI", "index", "経済指標"),
    "PCEPI": ("PCE価格指数", "index", "経済指標"),
    "UNRATE": ("失業率", "%", "経済指標"),
    "PAYEMS": ("非農業部門雇用者数", "thousands", "経済指標"),
    "SP500": ("S&P500", "index", "株式"),
    "VIXCLS": ("VIX", "index", "株式"),
    "DEXJPUS": ("USD/JPY", "JPY", "為替"),
    "DCOILWTICO": ("WTI原油", "USD/bbl", "原油・エネルギー"),
}


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    fred_api_key: str | None
    request_timeout: int
    gdelt_max_records: int


def get_settings() -> Settings:
    data_dir = Path(os.getenv("COLLECTOR_DATA_DIR", str(DEFAULT_DATA_DIR))).resolve()
    return Settings(
        data_dir=data_dir,
        fred_api_key=os.getenv("FRED_API_KEY") or None,
        request_timeout=int(os.getenv("COLLECTOR_TIMEOUT_SECONDS", "20")),
        gdelt_max_records=int(os.getenv("GDELT_MAX_RECORDS", "50")),
    )

