"""Canonical Customer Operations event contract (19 fields).

Relationship and consent are SEPARATE truth states:
- Public contact != relationship: customer/partner requires relationship
  evidence (an evidence item from a relationship-capable source).
  Public sources (official_public_site, search_api_result,
  customer_provided_url, blocked_*) can never mint a relationship.
- Relationship != consent: consent (even granted) never substitutes for
  relationship evidence, and consent state (unknown/withdrawn/expired)
  never erases a separately evidenced relationship.
- Channel permission still depends on consent: WhatsApp actions beyond
  hold/ask/escalate require granted consent regardless of relationship.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

RelationshipState = Literal[
    "unknown", "prospect", "lead", "customer", "former_customer", "partner"
]
ConsentState = Literal["unknown", "not_asked", "granted", "withdrawn", "expired"]
OpsChannel = Literal["web", "email", "whatsapp", "phone_requested", "partner_intro"]
OpsLocale = Literal["ar", "en"]
DataClass = Literal["public", "internal", "confidential", "restricted"]
OpsPriority = Literal["p0", "p1", "p2", "p3"]
EffectClass = Literal[
    "read", "recommend", "draft", "approved_send_manual", "internal_execute"
]
ResponseState = Literal["answer", "ask", "action_draft", "escalate", "hold"]

CANONICAL_EVENT_FIELDS: tuple[str, ...] = (
    "trace_id",
    "account_id",
    "contact_id",
    "relationship_state",
    "consent_state",
    "channel",
    "locale",
    "sector",
    "intent",
    "data_class",
    "case_id",
    "priority",
    "effect_class",
    "allowed_tools",
    "knowledge_snapshot",
    "owner",
    "verifier",
    "response_state",
    "evidence",
)

# Sources that can independently evidence a customer/partner relationship.
# Public/research sources are deliberately absent: they can never mint one.
RELATIONSHIP_EVIDENCE_SOURCES: frozenset[str] = frozenset({
    "crm_record",
    "signed_contract",
    "customer_confirmed_relationship",
    "partner_agreement",
    "delivery_record",
    "payment_record",
})

# Sources that must NEVER count as relationship evidence (public contact,
# research, or blocked provenance).
NON_RELATIONSHIP_SOURCES: frozenset[str] = frozenset({
    "official_public_site",
    "search_api_result",
    "customer_provided_url",
    "customer_uploaded_file",
    "manually_entered_note",
    "internal_doc",
    "blocked_scraping_source",
    "blocked_personal_data_source",
})


def has_relationship_evidence(evidence: list[EvidenceItem]) -> bool:
    """True iff at least one evidence item comes from a relationship-capable
    source. Public/research sources never qualify, even at high levels."""
    return any(e.source in RELATIONSHIP_EVIDENCE_SOURCES for e in evidence)


# effect_class -> permitted tool surface (draft-first; send never automatic)
EFFECT_TOOL_MAP: dict[str, tuple[str, ...]] = {
    "read": ("knowledge_v10.retrieve", "market_intelligence.read"),
    "recommend": ("knowledge_v10.retrieve", "market_intelligence.read", "service_catalog.read"),
    "draft": (
        "knowledge_v10.retrieve",
        "support_os.draft_response",
        "distribution_os.draft_quality",
        "approval_center.create",
    ),
    "approved_send_manual": (
        "approval_center.create",
        "channel_policy_gateway.check",
    ),
    "internal_execute": (
        "knowledge_v10.retrieve",
        "revenue_memory.append_event",
        "proof_ledger.record",
        "agent_observability.record_trace",
    ),
}


def new_trace_id() -> str:
    return f"cop_{uuid.uuid4().hex[:16]}"


def new_case_id() -> str:
    return f"case_{uuid.uuid4().hex[:12]}"


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1, max_length=512)
    uri: str = ""
    excerpt: str = Field(default="", max_length=2000)
    evidence_level: Literal["L0", "L1", "L2", "L3", "L4", "L5"] = "L0"
    retrieved_at: str = ""
    current_only: bool = True


class KnowledgeSnapshotRef(BaseModel):
    """Frozen pointer to current-only retrieval. Empty chunk list = HOLD/ASK."""

    model_config = ConfigDict(extra="forbid")

    snapshot_id: str = ""
    retrieved_at: str = ""
    as_of: str = ""
    chunk_ids: list[str] = Field(default_factory=list)
    source_types: list[str] = Field(default_factory=list)
    current_only: bool = True


class CustomerOpsEvent(BaseModel):
    """One canonical customer-operations event. Extra fields forbidden."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    trace_id: str = Field(default_factory=new_trace_id, min_length=1)
    account_id: str = Field(min_length=1, max_length=128)
    contact_id: str = Field(min_length=1, max_length=128)
    relationship_state: RelationshipState = "unknown"
    consent_state: ConsentState = "unknown"
    channel: OpsChannel = "web"
    locale: OpsLocale = "ar"
    sector: str = Field(default="technology_saas", min_length=1, max_length=64)
    intent: str = Field(default="unknown", min_length=1, max_length=64)
    data_class: DataClass = "internal"
    case_id: str = Field(default_factory=new_case_id, min_length=1)
    priority: OpsPriority = "p2"
    effect_class: EffectClass = "read"
    allowed_tools: list[str] = Field(default_factory=list)
    knowledge_snapshot: KnowledgeSnapshotRef = Field(default_factory=KnowledgeSnapshotRef)
    owner: str = Field(default="customer_ops_kernel", min_length=1, max_length=128)
    verifier: str = Field(default="founder", min_length=1, max_length=128)
    response_state: ResponseState = "ask"
    evidence: list[EvidenceItem] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    @model_validator(mode="after")
    def _enforce_kernel_law(self) -> CustomerOpsEvent:
        # Public contact != relationship: customer/partner requires
        # relationship evidence from a relationship-capable source.
        # Consent (even granted) never substitutes; unknown/withdrawn/
        # expired consent never erases a separately evidenced relationship.
        if self.relationship_state in ("customer", "partner"):
            if not has_relationship_evidence(self.evidence):
                raise ValueError(
                    "relationship_state=customer/partner requires relationship "
                    "evidence (e.g. source=crm_record/signed_contract); public "
                    "contact and consent never mint a relationship"
                )
        # WhatsApp permission still depends on channel consent: without
        # granted consent only HOLD/ASK/ESCALATE are representable.
        if self.channel == "whatsapp" and self.consent_state != "granted":
            if self.response_state in ("answer", "action_draft"):
                raise ValueError("whatsapp without granted consent must HOLD/ASK/ESCALATE")
        # allowed_tools must stay within the effect_class surface.
        permitted = set(EFFECT_TOOL_MAP[self.effect_class])
        unknown_tools = [t for t in self.allowed_tools if t not in permitted]
        if unknown_tools:
            raise ValueError(f"allowed_tools outside effect_class surface: {unknown_tools}")
        return self

    def to_envelope_data(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def to_revenue_memory_ref(self) -> dict[str, Any]:
        """Map onto revenue_memory subject addressing (no new store)."""
        return {
            "customer_id": self.account_id,
            "subject_type": "customer",
            "subject_id": self.contact_id,
            "correlation_id": self.trace_id,
            "causation_id": self.case_id,
        }
