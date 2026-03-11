from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.collectors.base import MockCollector
from app.core.database import Base, engine, get_db
from app.models.entities import Case, Profile, RiskScore, Subject, TimelineEvent
from app.schemas.osint import RiskOut, SearchRequest, SearchResponse, TimelineEventOut
from app.services.identity import identity_confidence
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

    for ident in req.identifiers:
        subject = Subject(case_id=case.id, input_type=ident.input_type.value, value=ident.value)
        db.add(subject)
        artifacts = await collector.collect(ident)
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

    avg_conf = sum(p.authenticity_score for p in profiles_out) / max(len(profiles_out), 1)
    risk = RiskScore(
        case_id=case.id,
        identity_confidence=round(avg_conf, 3),
        bot_likelihood=round(max(0.0, 1 - avg_conf), 3),
        influence_score=round(sum(p.influence_score for p in profiles_out) / max(len(profiles_out), 1), 3),
        risk_level="medium" if avg_conf < 0.7 else "low",
        rationale="Risk is derived from public-profile consistency and account activity indicators.",
    )
    db.add(risk)
    db.commit()

    report_payload = {
        "case_name": case.name,
        "description": case.description or "",
        "profiles": [
            {
                "platform": p.platform,
                "handle": p.handle,
                "profile_url": p.profile_url,
            }
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
        timeline=[
            TimelineEventOut(event_type=e.event_type, event_time=e.event_time, summary=e.summary)
            for e in timeline_out
        ],
        risk=RiskOut(
            identity_confidence=risk.identity_confidence,
            bot_likelihood=risk.bot_likelihood,
            influence_score=risk.influence_score,
            risk_level=risk.risk_level,
            rationale=risk.rationale,
        ),
    )


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "public_data_only": True}
