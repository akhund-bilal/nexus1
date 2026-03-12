from collections import Counter
import re

POSITIVE_WORDS = {
    "good", "great", "excellent", "safe", "trusted", "secure", "positive", "success", "strong", "improved"
}
NEGATIVE_WORDS = {
    "bad", "risky", "fraud", "threat", "malicious", "negative", "weak", "breach", "danger", "suspicious"
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]{3,}", text.lower())


def _infer_language_local(text: str) -> str:
    if not text.strip():
        return "unknown"

    lowered = text.lower()
    ascii_ratio = sum(1 for ch in lowered if ord(ch) < 128) / max(len(lowered), 1)
    common_english_markers = [" the ", " and ", " with ", " for ", " from "]

    if ascii_ratio > 0.9 and any(token in f" {lowered} " for token in common_english_markers):
        return "en"
    return "und"


def _simple_sentiment(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    score = (pos - neg) / max(len(tokens), 1)
    return max(-1.0, min(1.0, round(score, 3)))


def analyze_posts(posts: list[str]) -> dict:
    corpus = " ".join(posts)
    tokens = _tokenize(corpus)
    top_keywords = [w for w, _ in Counter(tokens).most_common(10)]

    return {
        "sentiment": _simple_sentiment(tokens),
        "top_keywords": top_keywords,
        "language": _infer_language_local(corpus),
    }
