# Nexus1 — OSINT Social Media Intelligence Platform

Nexus1 is a modular, public-data-only OSINT investigation platform that ingests identifiers (username, name, email, phone, domain, profile URL, location, organization), discovers related public artifacts, correlates entities, and generates intelligence-ready case outputs.

## Features Implemented
- FastAPI backend with investigation workflows and case persistence.
- Plugin-based collector interface (public sources only).
- Identity confidence scoring and risk/influence scoring.
- Timeline event engine for discovered artifacts.
- Report generation (HTML scaffold + sample report).
- Multi-database deployment stack (PostgreSQL, Redis, Neo4j, ElasticSearch, RabbitMQ).
- Celery worker scaffold for automation/watchlist scheduling.
- React dashboard for search and profile visualization.

## Repository Layout
- `backend/`: API, services, collectors, worker, tests.
- `frontend/`: React dashboard.
- `docs/`: architecture, schema, API docs.
- `reports/`: generated and sample reports.

## Quickstart
```bash
docker compose up --build
```

Backend:
- `http://localhost:8000/api/v1/health`

Frontend:
- `http://localhost:5173`

## Public-Only Compliance
This platform is intentionally constrained to legally and ethically compliant OSINT techniques:
- no authentication bypass,
- no hacking or account takeover,
- no private data exfiltration,
- no plaintext password exposure.

## Example API Call
```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "case_name": "Demo Investigation",
    "description": "Public profile discovery",
    "identifiers": [{"input_type": "username", "value": "janedoe"}]
  }'
```
