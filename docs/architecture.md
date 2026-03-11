# Nexus1 Architecture Diagram

```mermaid
flowchart LR
    A[Input Identifiers] --> B[FastAPI API Layer]
    B --> C[Case Management Service]
    B --> D[Identity Discovery Engine]
    D --> E[Collector Plugins\n(public sources only)]
    E --> F[(PostgreSQL)]
    E --> G[(ElasticSearch)]
    E --> H[(Neo4j)]
    B --> I[AI Processing Layer\nNLP + IMINT + Metadata]
    I --> F
    I --> H
    B --> J[Timeline Engine]
    J --> F
    B --> K[Risk & Influence Scoring]
    K --> F
    L[Celery Worker] --> E
    L --> J
    M[React Dashboard] --> B
    B --> N[Report Generator\nHTML/PDF/JSON/CSV]
```

## Public Data Guardrails
- Collectors are constrained to public endpoints and open datasets.
- No credential stuffing, auth bypass, or protected endpoint harvesting.
- Breach intelligence references only public leak indexes and redacts secrets.
