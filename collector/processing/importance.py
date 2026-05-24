from __future__ import annotations

from collector.models import Importance, MarketSnapshotItem, NewsItem


A_TERMS = (
    "hormuz",
    "nuclear facility",
    "retaliation",
    "ceasefire",
    "fomc statement",
    "fomc minutes",
    "jerome powell",
    "policy rate",
    "cpi",
    "pce",
    "payrolls",
    "gdp",
    "retail sales",
)
B_TERMS = (
    "fed",
    "federal reserve",
    "powell",
    "treasury",
    "state department",
    "white house",
    "eia",
    "oil inventory",
    "sanctions",
    "speech",
)
GEOPOLITICAL_A_TERMS = ("iran", "israel", "united states", "sanctions", "missile", "nuclear", "hormuz")


def score_news_importance(item: NewsItem) -> Importance:
    haystack = f"{item.title} {item.summary} {' '.join(item.tags)}".lower()
    if any(term in haystack for term in A_TERMS):
        return "A"
    if item.category == "イラン・中東情勢" and sum(1 for term in GEOPOLITICAL_A_TERMS if term in haystack) >= 2:
        return "A"
    if item.source == "FRB" and ("fomc" in haystack or "powell" in haystack or "rate" in haystack):
        return "A"
    if any(term in haystack for term in B_TERMS):
        return "B"
    return "C"


def score_market_importance(item: MarketSnapshotItem) -> Importance:
    if item.change_1d is None or item.value is None:
        return "C"
    change = abs(item.change_1d)
    if item.symbol in {"DGS10", "DGS2", "DGS30"} and change >= 0.10:
        return "A"
    if item.symbol == "DEXJPUS" and item.value and change / item.value >= 0.01:
        return "A"
    if item.symbol in {"SP500", "VIXCLS"} and item.value and change / item.value >= 0.015:
        return "A"
    if item.symbol == "DCOILWTICO" and item.value and change / item.value >= 0.02:
        return "A"
    if change > 0:
        return "B"
    return "C"

