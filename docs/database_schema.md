# Database Schema

## PostgreSQL Tables
- `cases`: investigation cases.
- `subjects`: target identifiers.
- `profiles`: discovered public accounts.
- `evidence`: normalized artifacts.
- `timeline_events`: chronological events.
- `risk_scores`: calculated risk and influence metrics.
- `watchlists`: monitoring targets.

## Neo4j Graph Model
Nodes:
- `Person`, `Account`, `Organization`, `Domain`, `Location`, `Image`, `Event`

Edges:
- `OWNS`, `WORKS_FOR`, `FOLLOWS`, `MENTIONS`, `POSTED_FROM`, `RELATED_TO`

## ElasticSearch Indices
- `osint_profiles`
- `osint_posts`
- `osint_leak_references`
- `osint_entities`
