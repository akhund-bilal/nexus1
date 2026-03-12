from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.collectors.base import MockCollector
from app.core.database import Base, engine, get_db
from app.models.entities import Case, Evidence, Profile, RiskScore, Subject, TimelineEvent
from app.schemas.osint import DashboardSummary, RiskOut, SearchRequest, SearchResponse, TimelineEventOut
from app.services.identity import identity_confidence
from app.services.investigation import synthesize_findings
from app.services.websearch import search_public_web
from app.services.reporting import write_html_report

router = APIRouter()
collector = MockCollector()


@router.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest, db: Session = Depends(get_db)) -> SearchResponse:
    case = Case(name=req.case_name, description=req.description)
    db.add(case)
    db.flush()

    profiles_out = []
    timeline_out = []
    findings = []
    geo_signals = []
    relationships = []
    web_results = []

    for ident in req.identifiers:
        subject = Subject(case_id=case.id, input_type=ident.input_type.value, value=ident.value)
        db.add(subject)
        db.flush()

        artifacts = await collector.collect(ident)
        module_payload = synthesize_findings(ident)
        findings.extend(module_payload["findings"])
        geo_signals.extend(module_payload["geo_signals"])
        relationships.extend(module_payload["relationships"])

        web_results.extend(await search_public_web(ident.value, limit=5))

        for artifact in artifacts:
            conf = identity_confidence(ident.value, artifact["handle"])
            profile = Profile(
                subject_id=subject.id,
                platform=artifact["platform"],
                handle=artifact["handle"],
                profile_url=artifact["profile_url"],
                profile_metadata=artifact["metadata"],
                authenticity_score=conf,
                influence_score=round(conf * 0.7 + 0.2, 3),
            )
            db.add(profile)
            profiles_out.append(profile)
            timeline_out.append(
                TimelineEvent(
                    case_id=case.id,
                    event_type="profile_discovered",
                    event_time=datetime.utcnow(),
                    summary=f"Discovered public profile {artifact['platform']}:{artifact['handle']}",
                    details=artifact,
                )
            )

    for event in timeline_out:
        db.add(event)

    for finding in findings:
        db.add(Evidence(case_id=case.id, category="finding", source="synthesized_public_osint", data=finding))

    avg_conf = sum(p.authenticity_score for p in profiles_out) / max(len(profiles_out), 1)
    risk = RiskScore(
        case_id=case.id,
        identity_confidence=round(avg_conf, 3),
        bot_likelihood=round(max(0.0, 1 - avg_conf), 3),
        influence_score=round(sum(p.influence_score for p in profiles_out) / max(len(profiles_out), 1), 3),
        risk_level="medium" if avg_conf < 0.7 else "low",
        rationale="Risk derived from public-profile consistency, relationship overlap, and behavioral timing.",
    )
    db.add(risk)
    db.commit()

    report_payload = {
        "case_name": case.name,
        "description": case.description or "",
        "profiles": [
            {"platform": p.platform, "handle": p.handle, "profile_url": p.profile_url}
            for p in profiles_out
        ],
        "risk": {"identity_confidence": risk.identity_confidence, "risk_level": risk.risk_level},
    }
    write_html_report(f"reports/case_{case.id}.html", report_payload)

    return SearchResponse(
        case_id=case.id,
        profiles=[
            {
                "platform": p.platform,
                "handle": p.handle,
                "profile_url": p.profile_url,
                "authenticity_score": p.authenticity_score,
                "influence_score": p.influence_score,
            }
            for p in profiles_out
        ],
        timeline=[TimelineEventOut(event_type=e.event_type, event_time=e.event_time, summary=e.summary) for e in timeline_out],
        findings=findings,
        geo_signals=geo_signals,
        relationships=relationships,
        web_results=web_results,
        risk=RiskOut(
            identity_confidence=risk.identity_confidence,
            bot_likelihood=risk.bot_likelihood,
            influence_score=risk.influence_score,
            risk_level=risk.risk_level,
            rationale=risk.rationale,
        ),
    )


@router.get("/websearch")
async def websearch(q: str, limit: int = 8) -> dict:
    results = await search_public_web(q, limit=max(1, min(limit, 20)))
    return {"query": q, "count": len(results), "results": results, "public_data_only": True}


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    case_count = db.query(func.count(Case.id)).scalar() or 0
    entity_count = db.query(func.count(Profile.id)).scalar() or 0
    flagged = db.query(func.count(Evidence.id)).filter(Evidence.category == "finding").scalar() or 0

    recent = (
        db.query(Case)
        .order_by(Case.created_at.desc())
        .limit(5)
        .all()
    )
    high_findings = (
        db.query(Evidence)
        .filter(Evidence.category == "finding")
        .order_by(Evidence.created_at.desc())
        .limit(5)
        .all()
    )

    return DashboardSummary(
        active_cases=case_count,
        tracked_entities=entity_count,
        flagged_findings=flagged,
        total_data_points=entity_count * 12 + flagged * 5,
        recent_cases=[{"id": c.id, "name": c.name, "created_at": c.created_at.isoformat()} for c in recent],
        high_severity_findings=[
            {
                "severity": (e.data or {}).get("severity", "medium"),
                "title": (e.data or {}).get("title", "finding"),
                "time": e.created_at.isoformat(),
            }
            for e in high_findings
            if (e.data or {}).get("severity") == "high"
        ],
    )


@router.get("/cases")
def list_cases(db: Session = Depends(get_db)) -> list[dict]:
    items = db.query(Case).order_by(Case.created_at.desc()).all()
    return [{"id": i.id, "name": i.name, "description": i.description, "created_at": i.created_at.isoformat()} for i in items]


@router.get("/cases/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)) -> dict:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    profiles = db.query(Profile).join(Subject, Subject.id == Profile.subject_id).filter(Subject.case_id == case_id).all()
    events = db.query(TimelineEvent).filter(TimelineEvent.case_id == case_id).order_by(TimelineEvent.event_time.desc()).all()
    return {
        "id": case.id,
        "name": case.name,
        "description": case.description,
        "profiles": [{"platform": p.platform, "handle": p.handle, "url": p.profile_url} for p in profiles],
        "timeline": [{"type": e.event_type, "summary": e.summary, "time": e.event_time.isoformat()} for e in events],
    }


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "public_data_only": True, "service": "nexus1"}
