"""Machine Registry loader + validator for the Execution Assurance System.

The registry (dealix/registers/machine_registry.yaml) is the source of
truth for every operational machine: its goal, owner, inputs, outputs,
KPIs, Definition of Done, failure modes, honest 0-5 maturity score, and
acceptance gate.

This module loads that YAML into typed, frozen dataclasses and validates
it against the anti-fake-green invariants. It has no heavy dependencies
so it is safe to import from tests and from the scorecard engine.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# ── Canonical evidence-event vocabulary ──────────────────────────────
# Every machine's `evidence_event_names` must be drawn from this set.
# These are business-flow events; each is stored in the Evidence Ledger
# under an EvidenceType category (see EVENT_EVIDENCE_CATEGORY below).
CANONICAL_EVIDENCE_EVENTS: frozenset[str] = frozenset(
    {
        "lead_captured",
        "message_prepared",
        "message_sent",
        "meeting_booked",
        "meeting_done",
        "scope_requested",
        "ticket_received",
        "ticket_answered",
        "ticket_escalated",
        "knowledge_gap_logged",
        "content_published",
        "affiliate_referral",
        "commission_calculated",
        "compliance_violation",
        "partner_application",
        "approval_requested",
        "approval_granted",
        "approval_rejected",
        "governance_decision",
        "delivery_kickoff",
        "proof_pack_assembled",
        "proof_pack_sent",
        "upsell_candidate",
        "invoice_sent",
        "invoice_paid",
    }
)

# Each canonical event maps to an Evidence Ledger category (the string
# values of evidence_control_plane_os.EvidenceType). Used by the audit.
EVENT_EVIDENCE_CATEGORY: dict[str, str] = {
    "lead_captured": "source",
    "message_prepared": "output",
    "message_sent": "output",
    "meeting_booked": "output",
    "meeting_done": "output",
    "scope_requested": "output",
    "ticket_received": "source",
    "ticket_answered": "output",
    "ticket_escalated": "governance_decision",
    "knowledge_gap_logged": "risk",
    "content_published": "output",
    "affiliate_referral": "source",
    "commission_calculated": "value",
    "compliance_violation": "risk",
    "partner_application": "source",
    "approval_requested": "approval",
    "approval_granted": "approval",
    "approval_rejected": "approval",
    "governance_decision": "governance_decision",
    "delivery_kickoff": "output",
    "proof_pack_assembled": "proof",
    "proof_pack_sent": "proof",
    "upsell_candidate": "decision",
    "invoice_sent": "output",
    "invoice_paid": "value",
}

# The 10 machines that MUST be present in the registry.
EXPECTED_MACHINE_IDS: tuple[str, ...] = (
    "sales_autopilot",
    "support_autopilot",
    "marketing_factory",
    "affiliate_machine",
    "partner_channel",
    "media_engine",
    "delivery_factory",
    "billing_ops",
    "governance_layer",
    "evidence_ledger",
)

_DEFAULT_PATH = (
    Path(__file__).resolve().parents[2]
    / "dealix"
    / "registers"
    / "machine_registry.yaml"
)


# ── Typed structures ─────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class DodItem:
    """One Definition-of-Done checklist item for a machine."""

    id: str
    text: str
    met: bool
    evidence_ref: str


@dataclass(frozen=True, slots=True)
class Kpi:
    """One measurable KPI for a machine."""

    name: str
    target: str
    unit: str
    current: str | None


@dataclass(frozen=True, slots=True)
class MachineSpec:
    """Declarative specification of one operational machine."""

    id: str
    name: str
    goal: str
    owner: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    kpis: tuple[Kpi, ...]
    scorecard_target: int
    maturity_score: int
    maturity_rationale: str
    definition_of_done: tuple[DodItem, ...]
    failure_modes: tuple[str, ...]
    nist: dict[str, str]
    acceptance_gate: tuple[str, ...]
    evidence_event_names: tuple[str, ...]
    approval_required_actions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MachineRegistry:
    """The full set of machines plus registry metadata."""

    schema_version: str
    last_reviewed: str
    maturity_levels: dict[int, str]
    machines: tuple[MachineSpec, ...]

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(m.id for m in self.machines)

    def get(self, machine_id: str) -> MachineSpec | None:
        for m in self.machines:
            if m.id == machine_id:
                return m
        return None


# ── Loading ──────────────────────────────────────────────────────────
def _as_str_tuple(value: Any) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(str(v) for v in value)


def _parse_machine(raw: dict[str, Any]) -> MachineSpec:
    kpis = tuple(
        Kpi(
            name=str(k.get("name", "")),
            target=str(k.get("target", "")),
            unit=str(k.get("unit", "")),
            current=None if k.get("current") is None else str(k.get("current")),
        )
        for k in (raw.get("kpis") or [])
    )
    dod = tuple(
        DodItem(
            id=str(d.get("id", "")),
            text=str(d.get("text", "")),
            met=bool(d.get("met", False)),
            evidence_ref=str(d.get("evidence_ref") or ""),
        )
        for d in (raw.get("definition_of_done") or [])
    )
    nist_raw = raw.get("nist") or {}
    nist = {str(k): str(v) for k, v in nist_raw.items()}
    return MachineSpec(
        id=str(raw.get("id", "")),
        name=str(raw.get("name", "")),
        goal=str(raw.get("goal", "")),
        owner=str(raw.get("owner") or ""),
        inputs=_as_str_tuple(raw.get("inputs")),
        outputs=_as_str_tuple(raw.get("outputs")),
        kpis=kpis,
        scorecard_target=int(raw.get("scorecard_target", 0)),
        maturity_score=int(raw.get("maturity_score", 0)),
        maturity_rationale=str(raw.get("maturity_rationale", "")),
        definition_of_done=dod,
        failure_modes=_as_str_tuple(raw.get("failure_modes")),
        nist=nist,
        acceptance_gate=_as_str_tuple(raw.get("acceptance_gate")),
        evidence_event_names=_as_str_tuple(raw.get("evidence_event_names")),
        approval_required_actions=_as_str_tuple(
            raw.get("approval_required_actions")
        ),
    )


def load_machine_registry(path: str | Path | None = None) -> MachineRegistry:
    """Load and parse the machine registry YAML.

    Raises FileNotFoundError if the registry file is missing — a missing
    registry is a hard failure, never silently empty.
    """
    registry_path = Path(path) if path else _DEFAULT_PATH
    if not registry_path.exists():
        raise FileNotFoundError(f"machine registry not found: {registry_path}")
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    levels_raw = data.get("maturity_levels") or {}
    maturity_levels = {int(k): str(v) for k, v in levels_raw.items()}
    machines = tuple(
        _parse_machine(m) for m in (data.get("machines") or [])
    )
    return MachineRegistry(
        schema_version=str(data.get("schema_version", "")),
        last_reviewed=str(data.get("last_reviewed", "")),
        maturity_levels=maturity_levels,
        machines=machines,
    )


# ── Validation (anti-fake-green invariants) ─────────────────────────
def validate_registry(reg: MachineRegistry) -> tuple[bool, list[str]]:
    """Validate the registry against the assurance invariants.

    Returns (ok, errors). The most important invariant: a Definition-of-Done
    item may only be `met: true` if it carries a concrete `evidence_ref`.
    """
    errors: list[str] = []

    found = set(reg.ids)
    for expected in EXPECTED_MACHINE_IDS:
        if expected not in found:
            errors.append(f"missing required machine: {expected}")
    duplicates = [mid for mid in reg.ids if reg.ids.count(mid) > 1]
    for dup in sorted(set(duplicates)):
        errors.append(f"duplicate machine id: {dup}")

    for m in reg.machines:
        prefix = f"machine '{m.id}'"
        if not m.owner.strip():
            errors.append(f"{prefix}: owner is empty")
        if not 0 <= m.maturity_score <= 5:
            errors.append(
                f"{prefix}: maturity_score {m.maturity_score} out of range 0-5"
            )
        if not 0 <= m.scorecard_target <= 5:
            errors.append(
                f"{prefix}: scorecard_target {m.scorecard_target} out of range 0-5"
            )
        if not m.acceptance_gate:
            errors.append(f"{prefix}: acceptance_gate is empty")
        if not m.definition_of_done:
            errors.append(f"{prefix}: definition_of_done is empty")
        if not m.goal.strip():
            errors.append(f"{prefix}: goal is empty")

        dod_ids = [d.id for d in m.definition_of_done]
        for dup in sorted({i for i in dod_ids if dod_ids.count(i) > 1}):
            errors.append(f"{prefix}: duplicate DoD item id: {dup}")

        for d in m.definition_of_done:
            # The core anti-fake-green invariant.
            if d.met and not d.evidence_ref.strip():
                errors.append(
                    f"{prefix}: DoD item '{d.id}' is met:true with no evidence_ref"
                )

        for event in m.evidence_event_names:
            if event not in CANONICAL_EVIDENCE_EVENTS:
                errors.append(
                    f"{prefix}: unknown evidence event '{event}'"
                )

    return (not errors, errors)


__all__ = [
    "CANONICAL_EVIDENCE_EVENTS",
    "EVENT_EVIDENCE_CATEGORY",
    "EXPECTED_MACHINE_IDS",
    "DodItem",
    "Kpi",
    "MachineRegistry",
    "MachineSpec",
    "load_machine_registry",
    "validate_registry",
]
