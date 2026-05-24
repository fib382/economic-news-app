from __future__ import annotations

from collector.models import Category


CATEGORY_KEYWORDS: list[tuple[Category, tuple[str, ...]]] = [
    ("イラン・中東情勢", ("iran", "israel", "hormuz", "missile", "nuclear", "sanctions", "tehran", "iaea", "ceasefire", "retaliation")),
    ("FRB", ("fomc", "federal reserve", "jerome powell", "powell", "rate cut", "rate hike", "fed funds", "balance sheet")),
    ("経済指標", ("cpi", "pce", "gdp", "payroll", "payrolls", "unemployment", "retail sales", "inflation data")),
    ("債券", ("treasury yield", "bond", "10-year", "2-year", "yield curve", "yields")),
    ("為替", ("usd", "jpy", "usd/jpy", "currency", "exchange rate", "yen", "dollar")),
    ("株式", ("s&p", "s&p 500", "nasdaq", "dow", "equities", "stocks", "stock market")),
    ("原油・エネルギー", ("wti", "brent", "oil", "gas", "eia", "crude", "energy")),
    ("要人発言", ("white house", "treasury", "state department", "remarks", "speech", "testimony", "statement")),
]


def classify_text(title: str, summary: str = "", tags: list[str] | None = None) -> Category:
    haystack = " ".join([title, summary, " ".join(tags or [])]).lower()
    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "その他"


def tags_for_text(title: str, summary: str = "") -> list[str]:
    haystack = f"{title} {summary}".lower()
    tags: list[str] = []
    for _, keywords in CATEGORY_KEYWORDS:
        for keyword in keywords:
            if keyword in haystack:
                label = keyword.upper() if keyword in {"cpi", "pce", "gdp", "wti", "eia", "usd", "jpy"} else keyword.title()
                if label not in tags:
                    tags.append(label)
    return tags[:8]

