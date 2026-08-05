from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field

SourceTier = Literal["S", "A", "B"]
SourceKind = Literal["html"]
HealthState = Literal["ok", "unconfigured", "fetch_failed", "parser_broken"]
AccessStatus = Literal["verified_allowed", "requires_permission", "unverified"]
RecordKind = Literal["initial", "changed"]
Severity = Literal["critical", "high", "medium", "low", "info"]


class Source(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    name: str
    tier: SourceTier
    kind: SourceKind
    url: AnyHttpUrl | None = None
    content_selector: str
    access_status: AccessStatus = "unverified"
    enabled: bool = False
    disabled_reason: str | None = None


class Snapshot(BaseModel):
    source_id: str
    fetched_at: datetime
    url: AnyHttpUrl
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    normalized_content: str


class SourceStatus(BaseModel):
    source_id: str
    checked_at: datetime
    state: HealthState
    message: str | None = None
    http_status: int | None = None


class SystemAssessment(BaseModel):
    """Rule-based assessment; it is never an official source statement."""

    categories: list[str]
    severity: Severity
    reason: str


class UpdateRecord(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_-]+$")
    kind: RecordKind
    source_id: str
    source_name: str
    detected_at: datetime
    source_url: AnyHttpUrl
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    official_content: str
    system_assessment: SystemAssessment
