from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    subjects = relationship("Subject", back_populates="case")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    input_type = Column(String(64), nullable=False)
    value = Column(String(512), nullable=False)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="subjects")
    profiles = relationship("Profile", back_populates="subject")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    platform = Column(String(128), nullable=False)
    handle = Column(String(255), nullable=False)
    profile_url = Column(String(1024), nullable=False)
    profile_metadata = Column(JSON, default={})
    authenticity_score = Column(Float, default=0.0)
    influence_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject", back_populates="profiles")


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    category = Column(String(64), nullable=False)
    source = Column(String(255), nullable=False)
    data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    event_type = Column(String(128), nullable=False)
    event_time = Column(DateTime, nullable=False)
    summary = Column(Text, nullable=False)
    details = Column(JSON, default={})


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    identity_confidence = Column(Float, default=0.0)
    bot_likelihood = Column(Float, default=0.0)
    influence_score = Column(Float, default=0.0)
    risk_level = Column(String(32), default="low")
    rationale = Column(Text)
    generated_at = Column(DateTime, default=datetime.utcnow)


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    target = Column(String(512), nullable=False)
    active = Column(Boolean, default=True)
    schedule_cron = Column(String(64), default="0 */6 * * *")
