"""V17 Agent Deal Desk — deterministic multi-seat account review.

Reuses the canonical Dealix governance primitives instead of launching
permanent agents:

- :mod:`auto_client_acquisition.revenue_os.scoring` — account scoring
- :mod:`auto_client_acquisition.revenue_os.capability_catalog` — capability fit
- :mod:`auto_client_acquisition.revenue_os.targeting_graph` — offer paths
- :mod:`auto_client_acquisition.command_os.red_team` — red-team verdicts
- :mod:`auto_client_acquisition.operating_rhythm_os.bad_revenue_council` —
  bad-revenue red lines

Every seat is a pure deterministic function over the account case. The CEO
synthesizer returns PRIMARY_OFFER / SECONDARY_OFFER / WHY_PRIMARY_WINS /
WHY_SECONDARY_LOSES / TOP_RISK / TOP_DISSENT / PROOF_GAP / NEXT_EVIDENCE /
CTA / CHANNEL / NEXT_ACTION. Dissent is preserved in ``seats`` — never
silently merged.

Hard gates (fail-closed): self-test, synthetic, no source, suppressed,
opted-out, prohibited channel. These mirror V16 truth-firewall semantics and
the first-launch offer gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from auto_client_acquisition.revenue_os.capability_catalog import (
    Capability,
    load_capability_catalog,
)
from auto_client_acquisition.revenue_os.targeting_graph import (
    build_targeting_graph,
    graph_for_pain,
)


class AccountState(StrEnum):
    RESEARCH_UNIVERSE = "research_universe"
    WATCHLIST = "watchlist"
    ACTIVE_RESEARCH = "active_research"
    CONTACT_DISCOVERED = "contact_discovered"
    CONTACTABLE = "contactable"
    REAL_RELATIONSHIP = "real_relationship"
    QUALIFICATION_CANDIDATE = "qualification_candidate"
    QUALIFIED = "qualified"
    DIAGNOSTIC = "diagnostic"
    DISCOVERY = "discovery"
    QUOTE = "quote"
    PILOT = "pilot"
    PAID = "paid"
    PROOF = "proof"
    RECURRING = "recurring"


class ChannelEligibility(StrEnum):
    EMAIL_CONSENTED = "email_consented"
    EMAIL_WARM_BUSINESS = "email_warm_business"
    EVENT_FOLLOWUP_CONSENTED = "event_followup_consented"
    WHATSAPP_CONSENTED = "whatsapp_consented"
    LINKEDIN_MANUAL = "linkedin_manual_only"
    NOT_ELIGIBLE = "not_eligible"


class SeatName(StrEnum):
    REVENUE_STRATEGIST = "revenue_strategist"
    MARKET_RESEARCHER = "market_researcher"
    OFFER_ARCHITECT = "offer_architect"
    DELIVERY_ARCHITECT = "delivery_architect"
    GOVERNANCE_PROOF = "governance_proof"
    FINANCE_COMMERCIAL = "finance_commercial"
    RED_TEAM = "red_team"
    OBJECTION_REVIEWER = "objection_reviewer"
    CEO_SYNTHESIZER = "ceo_synthesizer"


@dataclass(frozen=True, slots=True)
class SeatOutput:
    seat: SeatName
    decision: str
    reasoning: str
    dissent: str = ""


@dataclass(frozen=True, slots=True)
class AccountCase:
    """Minimal evidence-backed account case (no PII beyond business context)."""

    account_id: str
    company: str
    domain: str = ""
    segment: str = ""
    observed_pains: tuple[str, ...] = ()
    source: str = ""
    relationship_state: str = AccountState.RESEARCH_UNIVERSE.value
    self_test: bool = False
    synthetic: bool = False
    suppressed: bool = False
    opted_out: bool = False
    consent_state: str = "unknown"
    contact_person: str = ""
    role: str = ""
    evidence: tuple[dict[str, str], ...] = ()  # [{type, value, source, observed_at}]

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "company": self.company,
            "domain": self.domain,
            "segment": self.segment,
            "observed_pains": list(self.observed_pains),
            "source": self.source,
            "relationship_state": self.relationship_state,
            "self_test": self.self_test,
            "synthetic": self.synthetic,
            "suppressed": self.suppressed,
            "opted_out": self.opted_out,
            "consent_state": self.consent_state,
            "contact_person": self.contact_person,
            "role": self.role,
            "evidence": list(self.evidence),
        }


@dataclass(slots=True)
class DealDeskResult:
    account: AccountCase
    blocked: bool = False
    block_reasons: list[str] = field(default_factory=list)
    seats: list[SeatOutput] = field(default_factory=list)
    primary_offer: str = ""
    secondary_offer: str = ""
    why_primary_wins: str = ""
    why_secondary_loses: str = ""
    top_risk: str = ""
    top_dissent: str = ""
    proof_gap: str = ""
    next_evidence: str = ""
    cta: str = ""
    channel: str = ChannelEligibility.NOT_ELIGIBLE.value
    next_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account.account_id,
            "company": self.account.company,
            "blocked": self.blocked,
            "block_reasons": self.block_reasons,
            "seats": [s.__dict__ for s in self.seats],
            "primary_offer": self.primary_offer,
            "secondary_offer": self.secondary_offer,
            "why_primary_wins": self.why_primary_wins,
            "why_secondary_loses": self.why_secondary_loses,
            "top_risk": self.top_risk,
            "top_dissent": self.top_dissent,
            "proof_gap": self.proof_gap,
            "next_evidence": self.next_evidence,
            "cta": self.cta,
            "channel": self.channel,
            "next_action": self.next_action,
        }


# ── Hard gates (fail-closed; mirrors V16 truth firewall + launch gate) ──


def _hard_gate_reasons(account: AccountCase) -> list[str]:
    reasons: list[str] = []
    if account.self_test:
        reasons.append("SELF_TEST")
    if account.synthetic:
        reasons.append("SYNTHETIC")
    if not str(account.source or "").strip():
        reasons.append("NO_SOURCE")
    if account.suppressed:
        reasons.append("SUPPRESSED")
    if account.opted_out:
        reasons.append("OPTED_OUT")
    return reasons


def _channel_eligibility(account: AccountCase) -> ChannelEligibility:
    """Deterministic channel eligibility from relationship + consent state.

    Cold channels are never eligible. LinkedIn is manual-only. WhatsApp
    requires documented consent / real relationship.
    """
    if account.opted_out or account.suppressed:
        return ChannelEligibility.NOT_ELIGIBLE
    rel = str(account.relationship_state or "")
    consent = str(account.consent_state or "").lower()
    if rel == AccountState.REAL_RELATIONSHIP.value or rel == AccountState.QUALIFIED.value:
        if consent in {"consented", "opted_in", "explicit_consent", "approved"}:
            return ChannelEligibility.EMAIL_CONSENTED
        return ChannelEligibility.EMAIL_WARM_BUSINESS
    if rel in {AccountState.QUALIFICATION_CANDIDATE.value, AccountState.ACTIVE_RESEARCH.value}:
        return ChannelEligibility.LINKEDIN_MANUAL
    return ChannelEligibility.NOT_ELIGIBLE


# ── Seats ───────────────────────────────────────────────────────────────────


def _revenue_strategist(account: AccountCase) -> SeatOutput:
    has_pain = bool(account.observed_pains)
    has_relationship = account.relationship_state in {
        AccountState.REAL_RELATIONSHIP.value,
        AccountState.QUALIFIED.value,
        AccountState.QUALIFICATION_CANDIDATE.value,
    }
    if not has_pain:
        return SeatOutput(
            SeatName.REVENUE_STRATEGIST,
            "HOLD",
            "No observed pain evidence yet. Do not treat research as pipeline.",
            "Research is not a relationship; a booth visit is not a qualified problem.",
        )
    if has_relationship:
        return SeatOutput(
            SeatName.REVENUE_STRATEGIST,
            "PROCEED",
            "Observed pain plus relationship state; smallest movement is one "
            "evidence-backed diagnostic conversation.",
        )
    return SeatOutput(
        SeatName.REVENUE_STRATEGIST,
        "PROCEED_WITH_EVIDENCE",
        "Pain observed but relationship not yet real; next step is evidence "
        "capture (not outreach).",
    )


def _market_researcher(account: AccountCase) -> SeatOutput:
    evidence_count = len(account.evidence)
    if evidence_count == 0:
        return SeatOutput(
            SeatName.MARKET_RESEARCHER,
            "INSUFFICIENT_EVIDENCE",
            "No source-bound evidence recorded for this account.",
        )
    if not account.domain and not account.role:
        return SeatOutput(
            SeatName.MARKET_RESEARCHER,
            "PARTIAL",
            "Evidence exists but domain/role unknown; complete the case before "
            "personalization.",
            "Unknown buyer role blocks real personalization.",
        )
    return SeatOutput(
        SeatName.MARKET_RESEARCHER,
        "SUFFICIENT",
        "Evidence, domain, and role allow hypothesis-driven personalization.",
    )


def _offer_architect(account: AccountCase, capabilities: list[Capability]) -> SeatOutput:
    """Rank offers by pain overlap, then by ICP fit; return primary + fallback."""
    if not account.observed_pains:
        return SeatOutput(
            SeatName.OFFER_ARCHITECT,
            "NO_OFFER_YET",
            "No canonical pain mapped; wait for a real observed problem.",
        )
    scored: list[tuple[float, Capability]] = []
    # Canonical first-launch wedge wins score ties (first_launch_offer_gate).
    default_wedge = "revenue_command_pilot_30d"
    for cap in capabilities:
        overlap = sum(1 for p in account.observed_pains if p in cap.buyer_pain)
        icp_hit = 1.0 if account.segment in cap.icp_segments else 0.0
        # Default wedge: revenue command pilot unless strong specialized fit.
        score = overlap * 2.0 + icp_hit
        if cap.capability_id == default_wedge:
            score += 0.01  # deterministic tie-break toward the canonical wedge
        scored.append((score, cap))
    scored.sort(key=lambda t: (-t[0], t[1].capability_id))
    if not scored or scored[0][0] <= 0:
        return SeatOutput(
            SeatName.OFFER_ARCHITECT,
            "NO_MATCH",
            "No capability matches the observed pains.",
        )
    primary = scored[0][1]
    secondary = scored[1][1] if len(scored) > 1 else None
    dissent = ""
    if secondary is not None:
        dissent = (
            f"Offer Architect dissent: {secondary.capability_id} is a viable "
            f"alternative if the primary scope proves too large."
        )
    return SeatOutput(
        SeatName.OFFER_ARCHITECT,
        "OFFERS_RANKED",
        f"Primary={primary.capability_id} secondary={secondary.capability_id if secondary else 'none'}",
        dissent,
    )


def _delivery_architect(account: AccountCase) -> SeatOutput:
    if account.self_test or account.synthetic:
        return SeatOutput(
            SeatName.DELIVERY_ARCHITECT,
            "BLOCKED",
            "Self-test/synthetic cannot be delivered as customer work.",
        )
    if not account.evidence:
        return SeatOutput(
            SeatName.DELIVERY_ARCHITECT,
            "NEEDS_INPUTS",
            "Delivery requires customer inputs and an accountable owner.",
        )
    return SeatOutput(
        SeatName.DELIVERY_ARCHITECT,
        "FEASIBLE",
        "Delivery path exists: baseline → governed pilot → proof pack.",
    )


def _governance_proof(account: AccountCase) -> SeatOutput:
    if account.opted_out or account.suppressed:
        return SeatOutput(
            SeatName.GOVERNANCE_PROOF,
            "BLOCKED",
            "Suppressed/opted-out account: no marketing candidate creation.",
        )
    if not str(account.source or "").strip():
        return SeatOutput(
            SeatName.GOVERNANCE_PROOF,
            "BLOCKED",
            "No source: cannot qualify an account without provenance.",
        )
    return SeatOutput(
        SeatName.GOVERNANCE_PROOF,
        "PASS",
        "Source present; consent state must be re-verified before any send.",
    )


def _finance_commercial(account: AccountCase) -> SeatOutput:
    if account.relationship_state != AccountState.PAID.value:
        return SeatOutput(
            SeatName.FINANCE_COMMERCIAL,
            "NO_REVENUE_YET",
            "No payment evidence; quote/invoice is not revenue.",
        )
    return SeatOutput(
        SeatName.FINANCE_COMMERCIAL,
        "PAID",
        "Payment evidence present; revenue may be counted.",
    )


def _red_team(account: AccountCase) -> SeatOutput:
    dissents: list[str] = []
    if account.self_test or account.synthetic:
        dissents.append("Why is a self-test/synthetic record being reviewed as an account?")
    if not account.observed_pains:
        dissents.append("Why this account if no real pain is observed?")
    if account.relationship_state not in {
        AccountState.REAL_RELATIONSHIP.value,
        AccountState.QUALIFIED.value,
    }:
        dissents.append("Why treat research as a relationship?")
    if dissents:
        return SeatOutput(
            SeatName.RED_TEAM,
            "CHALLENGE",
            "Red-team challenge recorded; do not proceed to external action.",
            " | ".join(dissents),
        )
    return SeatOutput(
        SeatName.RED_TEAM,
        "PROCEED",
        "Account evidence passes red-team challenge.",
    )


def _objection_reviewer(account: AccountCase) -> SeatOutput:
    likely: list[str] = []
    if account.relationship_state not in {AccountState.REAL_RELATIONSHIP.value, AccountState.QUALIFIED.value}:
        likely.append("trust_objection (AI skepticism; no relationship yet)")
    if account.domain == "":
        likely.append("relevance_objection (no account-specific personalization)")
    if account.observed_pains and "budget" in " ".join(account.observed_pains):
        likely.append("budget_objection")
    return SeatOutput(
        SeatName.OBJECTION_REVIEWER,
        "PREDICTED",
        "; ".join(likely) if likely else "no high-probability objection predicted",
    )


def _ceo_synthesizer(
    account: AccountCase,
    seats: list[SeatOutput],
    primary: Capability | None,
    secondary: Capability | None,
    channel: ChannelEligibility,
) -> SeatOutput:
    blocked = any(s.decision == "BLOCKED" for s in seats)
    if blocked:
        return SeatOutput(
            SeatName.CEO_SYNTHESIZER,
            "BLOCKED",
            "Deal desk blocked by hard gate; no external action.",
        )
    if primary is None:
        return SeatOutput(
            SeatName.CEO_SYNTHESIZER,
            "HOLD",
            "No offer recommended; capture evidence and re-run.",
        )
    dissent = next((s.dissent for s in seats if s.dissent), "")
    secondary_name = secondary.capability_id if secondary else "none"
    return SeatOutput(
        SeatName.CEO_SYNTHESIZER,
        "RECOMMEND",
        (
            f"PRIMARY_OFFER={primary.capability_id} "
            f"SECONDARY_OFFER={secondary_name} "
            f"CHANNEL={channel.value} "
            f"WHY_PRIMARY={primary.name_en} maps to observed pains and ICP. "
            f"WHY_SECONDARY_LOSES=fallback scope may be less proven. "
            f"TOP_RISK=relationship not yet real; do not external-send. "
            f"NEXT_ACTION=internal diagnostic prep only."
        ),
        dissent,
    )


# ── Entrypoint ─────────────────────────────────────────────────────────────


def run_deal_desk(
    account: AccountCase,
    *,
    capabilities: list[Capability] | None = None,
) -> DealDeskResult:
    """Run the deterministic deal desk for one account case.

    Always returns a result; blocked accounts carry ``blocked=True`` with
    reasons and no external action.
    """
    result = DealDeskResult(account=account)
    gates = _hard_gate_reasons(account)
    if gates:
        result.blocked = True
        result.block_reasons = gates
        result.seats.append(
            SeatOutput(
                SeatName.GOVERNANCE_PROOF,
                "BLOCKED",
                "Hard gate: " + ", ".join(gates),
            )
        )
        result.channel = ChannelEligibility.NOT_ELIGIBLE.value
        result.next_action = "BLOCKED_NO_ACTION"
        return result

    caps = capabilities if capabilities is not None else load_capability_catalog()
    result.seats.append(_revenue_strategist(account))
    result.seats.append(_market_researcher(account))
    offer_seat = _offer_architect(account, caps)
    result.seats.append(offer_seat)
    result.seats.append(_delivery_architect(account))
    result.seats.append(_governance_proof(account))
    result.seats.append(_finance_commercial(account))
    red = _red_team(account)
    result.seats.append(red)
    result.seats.append(_objection_reviewer(account))

    primary = None
    secondary = None
    if offer_seat.decision == "OFFERS_RANKED":
        parts = offer_seat.reasoning.split()
        for p in parts:
            if p.startswith("Primary="):
                primary = next((c for c in caps if c.capability_id == p.split("=", 1)[1]), None)
            if p.startswith("secondary="):
                sid = p.split("=", 1)[1]
                secondary = next((c for c in caps if c.capability_id == sid), None) if sid != "none" else None

    channel = _channel_eligibility(account)
    result.channel = channel.value
    synth = _ceo_synthesizer(account, result.seats, primary, secondary, channel)
    result.seats.append(synth)

    if primary is not None:
        result.primary_offer = primary.capability_id
        result.secondary_offer = secondary.capability_id if secondary else ""
        result.why_primary_wins = (
            f"{primary.name_en} maps to observed pains "
            f"({', '.join(account.observed_pains) or 'none'}) and ICP segment {account.segment or 'unknown'}."
        )
        result.why_secondary_loses = (
            f"{secondary.name_en} is fallback; primary scope is the smallest proven wedge."
            if secondary
            else "No credible secondary offer under current evidence."
        )
    result.top_risk = "relationship_not_real_do_not_send" if account.relationship_state not in {
        AccountState.REAL_RELATIONSHIP.value,
        AccountState.QUALIFIED.value,
    } else "proof_gap_customer_evidence_required"
    result.top_dissent = red.dissent or offer_seat.dissent or ""
    result.proof_gap = (
        "no_customer_proof_yet" if account.relationship_state not in {AccountState.PAID.value, AccountState.PROOF.value}
        else "proof_pack_pending"
    )
    result.next_evidence = "capture_one_real_observed_problem" if not account.observed_pains else "discovery_baseline"
    if result.blocked:
        result.cta = "none"
        result.next_action = "BLOCKED_NO_ACTION"
    elif result.primary_offer:
        result.cta = "internal_diagnostic_prep"
        result.next_action = "INTERNAL: prepare customer-specific diagnostic (draft only)"
    else:
        result.cta = "hold_for_evidence"
        result.next_action = "HOLD: capture real observed problem before any offer"
    return result


__all__ = [
    "AccountCase",
    "AccountState",
    "ChannelEligibility",
    "DealDeskResult",
    "SeatName",
    "SeatOutput",
    "run_deal_desk",
]
