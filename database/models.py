from sqlalchemy import (
    Column, String, Integer, Boolean,
    DateTime, Text, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class PreComputedScore(Base):
    """
    Nightly burnout risk scores per team member.
    Populated by Azure Functions Timer Trigger.
    Never contains raw Graph API data.
    """
    __tablename__ = "pre_computed_scores"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id       = Column(String(20), nullable=False, index=True)
    computed_at     = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    score           = Column(Integer, nullable=False)
    risk_tier       = Column(String(10), nullable=False)
    trend_delta     = Column(Integer, nullable=True)
    trend_direction = Column(String(10), nullable=True)
    signal_summary  = Column(JSON, nullable=True)


class RoleBaseline(Base):
    """
    Expected workload ranges per role and department.
    Used to contextualise raw signals against role norms.
    """
    __tablename__ = "role_baselines"

    id                   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_type            = Column(String(50), nullable=False)
    department           = Column(String(50), nullable=False)
    expected_meeting_hrs = Column(Integer, nullable=False)
    focus_time_min_hrs   = Column(Integer, nullable=False)
    overload_threshold   = Column(Integer, nullable=False)
    context_notes        = Column(Text, nullable=True)


class Employee(Base):
    """
    Synthetic employee registry. NO real PII.
    Placeholder identifiers only — EMP-001, EMP-002 etc.
    """
    __tablename__ = "employees"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id    = Column(String(20), unique=True, nullable=False)
    display_name = Column(String(50), nullable=False)
    role_type    = Column(String(50), nullable=False)
    department   = Column(String(50), nullable=False)
    manager_id   = Column(String(20), nullable=True)
    is_active    = Column(Boolean, default=True)


class EmployeePreference(Base):
    """
    Employee opt-in preferences for the Employee Agent.
    Consent is explicit, reversible, and timestamped.
    """
    __tablename__ = "employee_preferences"

    member_id         = Column(String(20), primary_key=True)
    opted_in          = Column(Boolean, nullable=False, default=False)
    opted_in_at       = Column(DateTime(timezone=True), nullable=True)
    alert_threshold   = Column(String(10), default="MODERATE")
    notification_pref = Column(String(20), default="AGENT_ONLY")


class InterventionLog(Base):
    """
    Immutable audit trail of every manager action.
    Anonymised — no raw signal data stored here.
    """
    __tablename__ = "intervention_log"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manager_id      = Column(String(20), nullable=False)
    action_type     = Column(String(50), nullable=False)
    risk_tier       = Column(String(10), nullable=True)
    context_summary = Column(Text, nullable=True)
    created_at      = Column(DateTime(timezone=True), nullable=False, server_default=func.now())