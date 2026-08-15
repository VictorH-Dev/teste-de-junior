
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class IndicatorType(StrEnum):

    HASH = "hash"
    IP = "ip"
    DOMAIN = "domain"


class ConfidenceLevel(StrEnum):

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Priority(StrEnum):

    CRITICAL = "Critico"
    HIGH = "Alto"
    MEDIUM = "Medio"
    LOW = "Baixo"


class Severity(StrEnum):

    CRITICAL = "critical"
    SUSPICIOUS = "suspicious"
    CLEAN = "clean"


class Alert(BaseModel):

    id: str
    name: str
    sha256: str
    source_ip: str
    domain: str
    confidence: ConfidenceLevel
    timestamp: str


class Indicator(BaseModel):

    type: IndicatorType
    value: str
    matched: bool = False
    severity: Severity = Severity.CLEAN
    reason: str | None = None


class KnownIOC(BaseModel):

    type: IndicatorType
    value: str
    reason: str
    severity: Severity


class AlertResult(BaseModel):

    alert_id: str
    alert_name: str
    confidence: ConfidenceLevel
    indicators: list[Indicator]
    risk_score: int = Field(ge=0)
    priority: Priority


class ReportSummary(BaseModel):

    total_alerts: int
    critical_indicators: int
    clean_indicators: int


class Report(BaseModel):

    summary: ReportSummary
    alerts: list[AlertResult]
