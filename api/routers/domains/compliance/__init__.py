"""
Compliance domain — PDPL, security, privacy, data quality, reliability.
مجال الامتثال — PDPL، الأمان، الخصوصية، جودة البيانات، الموثوقية.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    evidence_events,
    governance_risk_dashboard,
    playbooks,
    proof_ledger,
    reliability_os,
    security_privacy,
    service_quality,
    vertical_playbooks,
)

_ROUTERS = [
    governance_risk_dashboard.router,
    evidence_events.router,
    playbooks.router,
    security_privacy.router,
    proof_ledger.router,
    reliability_os.router,
    service_quality.router,
    vertical_playbooks.router,
]


def get_routers() -> list[APIRouter]:
    """Return all compliance-domain routers."""
    return _ROUTERS
