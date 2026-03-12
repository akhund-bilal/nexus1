from urllib.parse import parse_qs, quote_plus, urlparse

import httpx
from bs4 import BeautifulSoup


DUCKDUCKGO_HTML = "https://duckduckgo.com/html/?q={query}"


def _normalize_duckduckgo_url(url: str) -> str:
    if not url:
        return url

    if url.startswith("//"):
        url = f"https:{url}"

    parsed = urlparse(url)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        uddg = qs.get("uddg")
        if uddg and uddg[0]:
            return uddg[0]
    return url


async def search_public_web(query: str, limit: int = 8) -> list[dict]:
    """Run a public web search (no auth, no private APIs) and return top results."""
    if not query.strip():
        return []

    url = DUCKDUCKGO_HTML.format(query=quote_plus(query.strip()))
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Nexus1OSINT/1.0; +https://example.org)"
    }

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for item in soup.select(".result"):
        link = item.select_one("a.result__a")
        snippet = item.select_one(".result__snippet")
        if not link:
            continue

        href = _normalize_duckduckgo_url((link.get("href") or "").strip())
        title = link.get_text(" ", strip=True)
        description = snippet.get_text(" ", strip=True) if snippet else ""

        if not href or not title:
            continue

        results.append(
            {
                "title": title,
                "url": href,
                "snippet": description,
                "source": "duckduckgo_public",
            }
        )

        if len(results) >= limit:
            break

    return results
