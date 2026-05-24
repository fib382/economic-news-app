from __future__ import annotations

import hashlib
from datetime import date as Date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


Category = Literal[
    "イラン・中東情勢",
    "要人発言",
    "FRB",
    "米国経済",
    "為替",
    "債券",
    "株式",
    "原油・エネルギー",
    "経済指標",
    "その他",
]
Importance = Literal["A", "B", "C"]
Confidence = Literal["low", "medium", "high"]


class MarketImpact(BaseModel):
    fx: str = ""
    bonds: str = ""
    stocks: str = ""
    commodities: str = ""


class NewsItem(BaseModel):
    model_config = ConfigDict(json_encoders={HttpUrl: str})

    id: str
    source: str
    source_type: str
    title: str
    summary: str = ""
    url: HttpUrl | str
    published_at: datetime
    fetched_at: datetime
    language: str = "en"
    country: str = ""
    category: Category = "その他"
    importance: Importance = "C"
    confidence: Confidence = "medium"
    market_impact: MarketImpact = Field(default_factory=MarketImpact)
    tags: list[str] = Field(default_factory=list)


class NewsItemsDocument(BaseModel):
    generated_at: datetime
    items: list[NewsItem] = Field(default_factory=list)


class MarketSnapshotItem(BaseModel):
    symbol: str
    name: str
    source: str
    value: float | None = None
    unit: str = ""
    date: Date | str | None = None
    change_1d: float | None = None
    category: Category = "その他"


class MarketSnapshotDocument(BaseModel):
    generated_at: datetime
    items: list[MarketSnapshotItem] = Field(default_factory=list)


class DailyReportSection(BaseModel):
    title: str
    summary: str
    importance: Importance = "C"
    source_item_ids: list[str] = Field(default_factory=list)


class DailyReportDocument(BaseModel):
    date: Date | str
    generated_at: datetime
    headline: str
    executive_summary: str
    sections: list[DailyReportSection] = Field(default_factory=list)
    watch_points: list[str] = Field(default_factory=list)


class SourceStatus(BaseModel):
    name: str
    category: str = "その他"
    method: str
    priority: Importance = "A"
    status: Literal["active", "optional", "planned", "skipped", "error"]
    item_count: int = 0
    last_fetched_at: datetime
    notes: str = ""
    url: str = ""


class SourcesDocument(BaseModel):
    generated_at: datetime
    items: list[SourceStatus] = Field(default_factory=list)


def make_news_id(source: str, normalized_title: str, published_at: datetime | str, url: str) -> str:
    raw = f"{source}|{normalized_title}|{published_at}|{url}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
