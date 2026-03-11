from collections import Counter

from textblob import TextBlob


def analyze_posts(posts: list[str]) -> dict:
    blob = TextBlob(" ".join(posts))
    polarity = blob.sentiment.polarity
    words = [w.lower() for w in blob.words if len(w) > 3]
    top_keywords = [w for w, _ in Counter(words).most_common(10)]
    return {
        "sentiment": round(polarity, 3),
        "top_keywords": top_keywords,
        "language": str(blob.detect_language()) if posts else "unknown",
    }
