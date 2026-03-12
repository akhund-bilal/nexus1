# Nexus1 — OSINT Social Media Intelligence Platform

A working, modular OSINT investigation platform using **publicly available data only**.

## What is now working
- Full FastAPI investigation workflow with case creation, profile discovery, timeline, findings, and risk scoring.
- Dashboard summary API for active cases, tracked entities, flagged findings, and recent activity.
- Case endpoints for listing and retrieving case details.
- SQLite default for local run (no external DB required), with PostgreSQL support in Docker.
- Cyber-style React dashboard (sidebar, KPI cards, recent cases, high severity findings) with live API integration.

## Run locally
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Backend: `http://localhost:8000/api/v1`
Frontend: `http://localhost:5173`

## Run with Docker
```bash
docker compose up --build
```

## Public-only compliance
- No auth bypass
- No private data exfiltration
- No account takeover/hacking
- No plaintext password exposure
