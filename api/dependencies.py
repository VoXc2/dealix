"""FastAPI dependencies — dependency injection for services."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Cookie, Header, HTTPException, status

from auto_client_acquisition.agents.proposal import ProposalAgent
from auto_client_acquisition.pipeline import AcquisitionPipeline
from autonomous_growth.agents.content import ContentCreatorAgent
from autonomous_growth.agents.sector_intel import SectorIntelAgent
from autonomous_growth.orchestrator import GrowthOrchestrator
from dealix.auth.magic_link import MagicLinkPayload, verify

# Cookie name shared with the frontend (assets/js/auth.js).
SESSION_COOKIE = "dlx_session"


def _try_decode(token: str | None) -> MagicLinkPayload | None:
    if not token:
        return None
    try:
        p = verify(token)
    except ValueError:
        return None
    if p.kind != "session":
        return None
    return p


def get_optional_partner(
    dlx_session: str | None = Cookie(default=None, alias=SESSION_COOKIE),
    authorization: str | None = Header(default=None),
) -> MagicLinkPayload | None:
    """Resolve the current partner if a valid session cookie/header is present."""
    token = dlx_session
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization[len("Bearer ") :].strip()
    return _try_decode(token)


def require_partner(
    payload: MagicLinkPayload | None = None,
    dlx_session: str | None = Cookie(default=None, alias=SESSION_COOKIE),
    authorization: str | None = Header(default=None),
) -> MagicLinkPayload:
    """Require an authenticated partner. 401 otherwise."""
    if payload is None:
        token = dlx_session
        if not token and authorization and authorization.lower().startswith("bearer "):
            token = authorization[len("Bearer ") :].strip()
        payload = _try_decode(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not_authenticated")
    return payload


def require_partner_scope(
    partner_id: str,
    payload: MagicLinkPayload,
) -> MagicLinkPayload:
    """Ensure the authenticated partner is acting on its OWN partner_id."""
    if payload.sub != partner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="partner_scope_mismatch")
    return payload


@lru_cache(maxsize=1)
def get_acquisition_pipeline() -> AcquisitionPipeline:
    return AcquisitionPipeline()


@lru_cache(maxsize=1)
def get_growth_orchestrator() -> GrowthOrchestrator:
    return GrowthOrchestrator()


@lru_cache(maxsize=1)
def get_sector_intel_agent() -> SectorIntelAgent:
    return SectorIntelAgent()


@lru_cache(maxsize=1)
def get_content_agent() -> ContentCreatorAgent:
    return ContentCreatorAgent()


@lru_cache(maxsize=1)
def get_proposal_agent() -> ProposalAgent:
    return ProposalAgent()
