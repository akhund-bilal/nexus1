from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class InputType(str, Enum):
    username = "username"
    full_name = "full_name"
    alias = "alias"
    email = "email"
    phone = "phone"
    profile_url = "profile_url"
    domain = "domain"
    image = "image"
    location = "location"
    organization = "organization"


class Identifier(BaseModel):
    input_type: InputType
    value: str = Field(min_length=2, max_length=512)


class SearchRequest(BaseModel):
    case_name: str
    description: str | None = None
    identifiers: list[Identifier]


class ProfileOut(BaseModel):
    platform: str
    handle: str
    profile_url: str
    authenticity_score: float
    influence_score: float


class TimelineEventOut(BaseModel):
    event_type: str
    event_time: datetime
    summary: str


class RiskOut(BaseModel):
    identity_confidence: float
    bot_likelihood: float
    influence_score: float
    risk_level: str
    rationale: str


class SearchResponse(BaseModel):
    case_id: int
    profiles: list[ProfileOut]
    timeline: list[TimelineEventOut]
    findings: list[dict]
    geo_signals: list[dict]
    relationships: list[dict]
    web_results: list[dict]
    risk: RiskOut


class DashboardSummary(BaseModel):
    active_cases: int
    tracked_entities: int
    flagged_findings: int
    total_data_points: int
    recent_cases: list[dict]
    high_severity_findings: list[dict]


class ExportResponse(BaseModel):
    case_id: int
    format: str
    path: str
