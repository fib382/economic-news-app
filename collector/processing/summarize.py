from __future__ import annotations

import json
import logging
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


def translate_and_analyze_news_with_gemini(items: list[NewsItem], api_key: str | None) -> list[NewsItem]:
    """Translates and analyzes a list of NewsItems into Japanese using the Gemini API.

    Uses Structured Outputs to ensure precise JSON response format matching the NewsItem models.
    Falls back gracefully to the original NewsItems if the API key is missing or an error occurs.
    """
    if not api_key:
        logging.info("Gemini API key is not configured. Using local fallback.")
        return items

    if not items:
        return items

    # Process the top 30 most recent items to optimize cost and performance
    sorted_items = sorted(items, key=lambda x: x.published_at, reverse=True)
    items_to_translate = sorted_items[:30]
    items_to_keep = sorted_items[30:]

    results: dict[str, NewsItem] = {item.id: item for item in items_to_translate}
    batch_size = 5

    for i in range(0, len(items_to_translate), batch_size):
        batch = items_to_translate[i : i + batch_size]
        try:
            _process_batch(batch, api_key, results)
        except Exception as exc:
            logging.error(f"Error processing Gemini translation batch starting at index {i}: {exc}")

    # Combine translated items with those we kept (to keep the list length consistent)
    final_list = [results[item.id] for item in items_to_translate] + items_to_keep
    return sorted(final_list, key=lambda x: x.published_at, reverse=True)


def _process_batch(batch: list[NewsItem], api_key: str, results: dict[str, NewsItem]) -> None:
    import requests

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    articles_data = []
    for item in batch:
        articles_data.append({
            "id": item.id,
            "title": item.title,
            "summary": item.summary,
            "category": item.category,
            "source": item.source,
        })

    prompt = (
        "You are an expert financial and geopolitical analyst translating global macroeconomic news into professional Japanese.\n"
        "Analyze and translate the following news articles. For each article, provide:\n"
        "1. A natural, professional Japanese headline ('title').\n"
        "2. A concise 1-2 sentence Japanese summary ('summary') (approx. 100-150 characters).\n"
        "3. The best category ('category') matching one of the Allowed Categories.\n"
        "4. The importance ('importance'): A, B, or C.\n"
        "5. The potential market impact ('market_impact') for FX, bonds, stocks, and commodities in Japanese.\n"
        "6. Relevant keywords/tags in Japanese ('tags') (up to 5 tags).\n\n"
        f"Articles to process:\n{json.dumps(articles_data, ensure_ascii=False, indent=2)}\n\n"
        "Allowed Categories: ['イラン・中東情勢', '要人発言', 'FRB', '米国経済', '為替', '債券', '株式', '原油・エネルギー', '経済指標', 'その他']\n"
        "Allowed Importance: ['A', 'B', 'C']\n"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "translated_items": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "original_id": {"type": "STRING", "description": "The exact ID from the input article."},
                                "title": {"type": "STRING", "description": "Natural Japanese translation of the headline."},
                                "summary": {"type": "STRING", "description": "Concise Japanese summary (1-2 sentences, 100-150 characters)."},
                                "category": {
                                    "type": "STRING",
                                    "enum": ["イラン・中東情勢", "要人発言", "FRB", "米国経済", "為替", "債券", "株式", "原油・エネルギー", "経済指標", "その他"],
                                },
                                "importance": {
                                    "type": "STRING",
                                    "enum": ["A", "B", "C"],
                                },
                                "market_impact": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "fx": {"type": "STRING"},
                                        "bonds": {"type": "STRING"},
                                        "stocks": {"type": "STRING"},
                                        "commodities": {"type": "STRING"},
                                    },
                                    "required": ["fx", "bonds", "stocks", "commodities"],
                                },
                                "tags": {
                                    "type": "ARRAY",
                                    "items": {"type": "STRING"},
                                },
                            },
                            "required": ["original_id", "title", "summary", "category", "importance", "market_impact", "tags"],
                        },
                    }
                },
                "required": ["translated_items"],
            },
        },
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    response_data = response.json()
    candidates = response_data.get("candidates", [])
    if not candidates:
        raise ValueError("No candidates returned from Gemini API.")

    part_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    if not part_text:
        raise ValueError("Empty response text from Gemini API.")

    parsed = json.loads(part_text)
    translated_items = parsed.get("translated_items", [])

    for t_item in translated_items:
        orig_id = t_item.get("original_id")
        if orig_id in results:
            orig = results[orig_id]
            results[orig_id] = NewsItem(
                id=orig.id,
                source=orig.source,
                source_type=orig.source_type,
                title=t_item.get("title", orig.title),
                summary=t_item.get("summary", orig.summary),
                url=orig.url,
                published_at=orig.published_at,
                fetched_at=orig.fetched_at,
                language="ja",
                country=orig.country,
                category=t_item.get("category", orig.category),
                importance=t_item.get("importance", orig.importance),
                confidence="high",
                market_impact=MarketImpact(
                    fx=t_item.get("market_impact", {}).get("fx", orig.market_impact.fx),
                    bonds=t_item.get("market_impact", {}).get("bonds", orig.market_impact.bonds),
                    stocks=t_item.get("market_impact", {}).get("stocks", orig.market_impact.stocks),
                    commodities=t_item.get("market_impact", {}).get("commodities", orig.market_impact.commodities),
                ),
                tags=t_item.get("tags", orig.tags),
            )
