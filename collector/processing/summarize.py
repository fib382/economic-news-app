from __future__ import annotations

from collector.models import MarketImpact, NewsItem


def template_summary(title: str, category: str) -> str:
    return f"{category}に関する公開情報です。見出し: {title}"


def market_impact_for_category(category: str) -> MarketImpact:
    if category == "イラン・中東情勢":
        return MarketImpact(
            fx="リスク回避の円買いとドル買いが交錯する可能性",
            bonds="米国債はリスク回避で買われる可能性",
            stocks="株式にはリスクオフ圧力",
            commodities="原油・金には上昇圧力",
        )
    if category == "FRB":
        return MarketImpact(
            fx="米金利見通しを通じてドル相場に影響する可能性",
            bonds="政策金利見通しに応じて利回りが変動する可能性",
            stocks="割引率と景気見通しを通じて株式に影響する可能性",
            commodities="ドル変動を通じて商品価格に波及する可能性",
        )
    return MarketImpact(
        fx="為替市場への影響は内容次第",
        bonds="債券市場への影響は内容次第",
        stocks="株式市場への影響は内容次第",
        commodities="商品市場への影響は内容次第",
    )


def maybe_gemini_summary(item: NewsItem) -> NewsItem:
    """Stub for future Gemini integration; deliberately keeps free local fallback."""
    return item

