"""Auditability Card — per-agent audit configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditabilityCard:
    agent_id: str
    agent_name: str
    owner: str
    audit_scope: tuple[str, ...]
    logs_required: bool
    tamper_evident_records: bool
    external_actions_allowed: bool
    responsibility_owner: str
    reconstruction_required: bool
    retention_policy: str

    def __post_init__(self) -> None:
        if not self.agent_id:
            raise ValueError("agent_id_required")
        if not self.audit_scope:
            raise ValueError("audit_scope_required")
        if not self.responsibility_owner:
            raise ValueError("responsibility_owner_required")
        # Doctrine: production agents must require reconstruction.
        if not self.reconstruction_required:
            raise ValueError("reconstruction_required_for_production_agents")
