from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from zoneinfo import ZoneInfo

from collector.models import DailyReportDocument, DailyReportSection, MarketSnapshotItem, NewsItem


JST = ZoneInfo("Asia/Tokyo")
CATEGORY_ORDER = ["イラン・中東情勢", "FRB", "経済指標", "債券", "為替", "株式", "原油・エネルギー", "要人発言", "その他"]


def build_daily_report(items: list[NewsItem], markets: list[MarketSnapshotItem], now: datetime | None = None) -> DailyReportDocument:
    generated_at = now or datetime.now(JST)
    grouped: dict[str, list[NewsItem]] = defaultdict(list)
    for item in sorted(items, key=lambda value: value.published_at, reverse=True):
        grouped[item.category].append(item)

    sections: list[DailyReportSection] = []
    for category in CATEGORY_ORDER:
        category_items = grouped.get(category, [])
        if not category_items:
            continue
        top = sorted(category_items, key=lambda value: ("ABC".index(value.importance), value.published_at), reverse=False)[:5]
        importance = "A" if any(item.importance == "A" for item in top) else "B" if any(item.importance == "B" for item in top) else "C"
        summary = _section_summary(category, top)
        sections.append(DailyReportSection(title=category, summary=summary, importance=importance, source_item_ids=[item.id for item in top]))

    headline = _headline(sections)
    executive_summary = _executive_summary(sections, markets)
    return DailyReportDocument(
        date=date.fromisoformat(generated_at.date().isoformat()),
        generated_at=generated_at,
        headline=headline,
        executive_summary=executive_summary,
        sections=sections,
        watch_points=_watch_points(items, markets),
    )


def _section_summary(category: str, items: list[NewsItem]) -> str:
    if not items:
        return f"{category}の新規材料は限定的です。"
    titles = " / ".join(item.title for item in items[:3])
    return f"{category}では、{titles} が主な確認材料です。"


def _headline(sections: list[DailyReportSection]) -> str:
    important = [section.title for section in sections if section.importance == "A"]
    if important:
        return f"{'、'.join(important[:2])}が市場の主な焦点"
    return "公開情報をもとに主要材料を整理"


def _executive_summary(sections: list[DailyReportSection], markets: list[MarketSnapshotItem]) -> str:
    a_count = sum(1 for section in sections if section.importance == "A")
    market_bits = [f"{item.name}: {item.value}{item.unit}" for item in markets[:4] if item.value is not None]
    market_text = "、".join(market_bits) if market_bits else "市場データは未取得または限定的です"
    return f"重要度Aのテーマは{a_count}件です。{market_text}。投資判断ではなく、公開情報の整理として確認してください。"


def _watch_points(items: list[NewsItem], markets: list[MarketSnapshotItem]) -> list[str]:
    points = ["米10年債利回りの変化", "原油価格の反応", "FRB高官発言"]
    if any(item.category == "イラン・中東情勢" for item in items):
        points.insert(0, "中東情勢とホルムズ海峡関連ニュース")
    if any(item.symbol == "DEXJPUS" for item in markets):
        points.append("USD/JPYの変化")
    return points[:6]

