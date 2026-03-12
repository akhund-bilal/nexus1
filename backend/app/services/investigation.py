from datetime import datetime, timedelta

from app.schemas.osint import Identifier


def synthesize_findings(identifier: Identifier) -> dict:
    seed = identifier.value.strip().lower().replace(" ", "_").replace("@", "")
    now = datetime.utcnow()
    findings = [
        {
            "severity": "high",
            "title": "Domain registered near profile creation window",
            "description": f"Public records suggest '{seed}.net' registration within 48h of first profile activity.",
            "time": (now - timedelta(days=3)).isoformat(),
        },
        {
            "severity": "medium",
            "title": "Cross-platform alias reuse",
            "description": f"Alias pattern '{seed}' appears in multiple public communities.",
            "time": (now - timedelta(days=2)).isoformat(),
        },
        {
            "severity": "low",
            "title": "Timezone consistency",
            "description": "Posting times indicate consistent UTC+2 behavioral window.",
            "time": (now - timedelta(days=1)).isoformat(),
        },
    ]

    geo_signals = [
        {"signal": "timezone_inference", "value": "UTC+2", "confidence": 0.71},
        {"signal": "language_region", "value": "en-EU", "confidence": 0.62},
    ]

    relationships = [
        {"source": seed, "target": f"{seed}_dev", "kind": "follows"},
        {"source": seed, "target": "cyber_forum_group", "kind": "member_of"},
        {"source": seed, "target": "oss_project_x", "kind": "contributed_to"},
    ]

    return {
        "findings": findings,
        "geo_signals": geo_signals,
        "relationships": relationships,
    }
