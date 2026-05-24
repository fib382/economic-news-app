from collector.processing.classify import classify_text, tags_for_text


def test_classifies_middle_east_news() -> None:
    assert classify_text("Iran sanctions and Israel tensions rise") == "イラン・中東情勢"


def test_classifies_frb_news() -> None:
    assert classify_text("FOMC statement points to rate cut debate") == "FRB"


def test_classifies_market_categories() -> None:
    assert classify_text("Treasury yield climbs for 10-year bond") == "債券"
    assert classify_text("USD JPY exchange rate moves sharply") == "為替"
    assert classify_text("WTI oil rises after EIA report") == "原油・エネルギー"


def test_tags_are_limited_and_derived() -> None:
    tags = tags_for_text("Powell discusses FOMC inflation and rate cut")
    assert "Fomc" in tags
    assert len(tags) <= 8

