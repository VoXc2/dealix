"""Agent Registry accessor + the canonical 12-agent seed — doctrine #9.

Exposes ``register`` / ``get`` / ``list`` / ``verify`` over a process-scoped
:class:`PostgresAgentRegistry`. ``verify`` hard-fails when owner or scope is
empty. ``seed_default_agents`` registers the 12 existing Dealix agents with
a named owner, an explicit scope and an audit hook.
"""
from __future__ import annotations

import logging
import os

from auto_client_acquisition.agent_registry.registry_postgres import (
    AgentRegistryError,
    PostgresAgentRegistry,
)
from auto_client_acquisition.agent_registry.schemas import AgentSpec, RiskClass

_LOG = logging.getLogger(__name__)

_DEFAULT_REGISTRY: PostgresAgentRegistry | None = None


# The 12 canonical Dealix agents (auto_client_acquisition/agents/ + base).
# Each carries a named owner + explicit scope + audit hook (doctrine #9).
_SEED_AGENTS: tuple[dict[str, object], ...] = (
    {"agent_name": "intake", "scope": "normalize inbound lead payloads into Lead records",
     "allowed_tools": ["read_internal_docs"], "risk_class": "safe_auto"},
    {"agent_name": "icp_matcher", "scope": "score a lead against the ICP profile",
     "allowed_tools": ["read_internal_docs"], "risk_class": "safe_auto"},
    {"agent_name": "pain_extractor", "scope": "extract pain signals from lead messages",
     "allowed_tools": ["read_internal_docs"], "risk_class": "safe_auto"},
    {"agent_name": "qualification", "scope": "run BANT qualification on a lead",
     "allowed_tools": ["read_internal_docs"], "risk_class": "draft_only"},
    {"agent_name": "proposal", "scope": "draft a proposal page for a qualified lead",
     "allowed_tools": ["draft_message"], "risk_class": "draft_only"},
    {"agent_name": "crm", "scope": "create and update CRM deal records",
     "allowed_tools": ["read_internal_docs"], "risk_class": "approval_required"},
    {"agent_name": "booking", "scope": "draft discovery-call booking suggestions",
     "allowed_tools": ["draft_message"], "risk_class": "draft_only"},
    {"agent_name": "outreach", "scope": "draft outreach messages (never live-send)",
     "allowed_tools": ["draft_message", "draft_email"], "risk_class": "approval_required"},
    {"agent_name": "followup", "scope": "draft follow-up messages on stalled leads",
     "allowed_tools": ["draft_message"], "risk_class": "approval_required"},
    {"agent_name": "prospector", "scope": "rank existing accounts for prioritization",
     "allowed_tools": ["read_internal_docs"], "risk_class": "draft_only"},
    {"agent_name": "rules_router", "scope": "route a lead to the next governed action",
     "allowed_tools": ["read_internal_docs"], "risk_class": "safe_auto"},
    {"agent_name": "base", "scope": "shared agent base behaviours (not directly invoked)",
     "allowed_tools": [], "risk_class": "blocked"},
)

_DEFAULT_OWNER = "founder"
_DEFAULT_AUDIT_HOOK = "default_audit_hook"


def _registry_url() -> str:
    explicit = os.getenv("DEALIX_AGENT_REGISTRY_DB_URL")
    if explicit:
        return explicit
    try:
        from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
        from core.config.settings import get_settings

        url = getattr(get_settings(), "database_url", "") or ""
        if url:
            return sync_sqlalchemy_url(url)
    except Exception:  # noqa: BLE001
        pass
    return "sqlite:///:memory:"


def _should_autocreate(url: str) -> bool:
    return ":memory:" in url or url.startswith("sqlite:")


def get_default_registry() -> PostgresAgentRegistry:
    """Return the process-scoped Agent Registry singleton."""
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        url = _registry_url()
        try:
            _DEFAULT_REGISTRY = PostgresAgentRegistry(
                database_url=url, create_tables=_should_autocreate(url)
            )
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("agent_registry_unavailable:%s", type(exc).__name__)
            _DEFAULT_REGISTRY = PostgresAgentRegistry(
                database_url="sqlite:///:memory:", create_tables=True
            )
    return _DEFAULT_REGISTRY


def reset_default_registry() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT_REGISTRY
    _DEFAULT_REGISTRY = None


def register(spec: AgentSpec) -> AgentSpec:
    """Register one agent into the default registry."""
    return get_default_registry().register(spec)


def get(agent_name: str) -> AgentSpec | None:
    """Fetch one agent spec by name."""
    return get_default_registry().get(agent_name)


def list_agents(*, include_disabled: bool = True) -> list[AgentSpec]:
    """Return all registered agents."""
    return get_default_registry().list(include_disabled=include_disabled)


def verify(agent_name: str) -> bool:
    """True only when the agent exists, is enabled and carries owner + scope."""
    return get_default_registry().verify(agent_name)


def seed_default_agents(
    *, registry: PostgresAgentRegistry | None = None
) -> list[AgentSpec]:
    """Register the 12 canonical Dealix agents with owner + scope + audit hook."""
    target = registry or get_default_registry()
    out: list[AgentSpec] = []
    for raw in _SEED_AGENTS:
        spec = AgentSpec(
            agent_name=str(raw["agent_name"]),
            owner=_DEFAULT_OWNER,
            scope=str(raw["scope"]),
            allowed_tools=list(raw.get("allowed_tools") or []),  # type: ignore[arg-type]
            risk_class=str(raw["risk_class"]),  # type: ignore[arg-type]
            audit_hook=_DEFAULT_AUDIT_HOOK,
        )
        out.append(target.register(spec))
    return out


SEED_AGENT_NAMES: tuple[str, ...] = tuple(str(a["agent_name"]) for a in _SEED_AGENTS)

__all__ = [
    "AgentRegistryError",
    "AgentSpec",
    "RiskClass",
    "SEED_AGENT_NAMES",
    "get",
    "get_default_registry",
    "list_agents",
    "register",
    "reset_default_registry",
    "seed_default_agents",
    "verify",
]
