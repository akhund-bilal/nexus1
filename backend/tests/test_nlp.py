from app.services.nlp import analyze_posts


def test_analyze_posts_is_local_only_shape() -> None:
    result = analyze_posts([
        "This is a public open source intelligence test post.",
        "We analyze timeline and entities for investigations.",
    ])

    assert "sentiment" in result
    assert "top_keywords" in result
    assert result["language"] in {"en", "und", "unknown"}
