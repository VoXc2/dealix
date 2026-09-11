"""SaaS Onboarding — self-serve, data isolation, entitlements, guided setup."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.saas_foundation import SaaSControlPlane, TenantTier, Tenant

UNKNOWN = "UNKNOWN"

class OnboardingStep(StrEnum):
    ACCOUNT_CREATED = "account_created"
    SECTOR_SELECTED = "sector_selected"
    DIAGNOSTIC_COMPLETED = "diagnostic_completed"
    WORKSPACE_READY = "workspace_ready"
    FIRST_PROOF = "first_proof"
    BILLING_ACTIVE = "billing_active"

class OnboardingSession(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    tenant_id: str
    sector: str = UNKNOWN
    current_step: OnboardingStep = OnboardingStep.ACCOUNT_CREATED
    completed_steps: list[OnboardingStep] = Field(default_factory=list)
    data_isolation_verified: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def advance(self, step: OnboardingStep) -> None:
        if step not in self.completed_steps:
            self.completed_steps.append(step)
        self.current_step = step

class SaaSOnboardingEngine:
    def __init__(self, control_plane: SaaSControlPlane | None = None) -> None:
        self.cp = control_plane or SaaSControlPlane()
        self.sessions: dict[str, OnboardingSession] = {}

    def start(self, tenant_name: str, sector: str, tier: TenantTier = TenantTier.STARTER) -> OnboardingSession:
        tenant = self.cp.create_tenant(tenant_name, sector, tier)
        session_id = f"onb_{hashlib.sha256(tenant.tenant_id.encode()).hexdigest()[:8]}"
        session = OnboardingSession(session_id=session_id, tenant_id=tenant.tenant_id, sector=sector)
        # Verify data isolation
        session.data_isolation_verified = bool(tenant.data_isolation_key)
        session.advance(OnboardingStep.SECTOR_SELECTED)
        self.sessions[session_id] = session
        return session

    def complete_diagnostic(self, session_id: str) -> OnboardingSession | None:
        sess = self.sessions.get(session_id)
        if not sess:
            return None
        sess.advance(OnboardingStep.DIAGNOSTIC_COMPLETED)
        sess.advance(OnboardingStep.WORKSPACE_READY)
        return sess

    def activate_billing(self, session_id: str, amount_sar: float) -> OnboardingSession | None:
        sess = self.sessions.get(session_id)
        if not sess:
            return None
        self.cp.bill(sess.tenant_id, amount_sar)
        sess.advance(OnboardingStep.BILLING_ACTIVE)
        return sess

    def to_dict(self, session_id: str) -> dict[str, Any] | None:
        sess = self.sessions.get(session_id)
        return sess.model_dump(mode="json") if sess else None

__all__ = ["SaaSOnboardingEngine", "OnboardingSession", "OnboardingStep", "UNKNOWN"]
