"""Client Handoff — Stage 6 (Deliver) packet generator.

حزمة التسليم النهائية للعميل في المرحلة السادسة.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class HandoffPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: str = Field(default_factory=lambda: f"hand_{uuid4().hex[:12]}")
    project_id: str
    title_ar: str
    title_en: str
    deliverables_links: list[str] = Field(default_factory=list)
    executive_report_link: str | None = None
    training_video_link: str | None = None
    runbook_link: str | None = None
    sop_link: str | None = None
    audit_log_link: str | None = None
    proof_pack_link: str | None = None
    customer_contacts: list[str] = Field(default_factory=list)
    dealix_contacts: list[str] = Field(default_factory=list)
    next_step_summary_ar: str
    next_step_summary_en: str
    signed_off: bool = False
    signed_at: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def mark_signed(self) -> HandoffPacket:
        return self.model_copy(
            update={"signed_off": True, "signed_at": datetime.now(UTC).isoformat()}
        )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def build_handoff(
    project_id: str,
    title_ar: str,
    title_en: str,
    next_step_summary_ar: str,
    next_step_summary_en: str,
    deliverables_links: list[str] | None = None,
    **extras: str | None,
) -> HandoffPacket:
    """Assemble a handoff packet. Caller persists + signs."""
    return HandoffPacket(
        project_id=project_id,
        title_ar=title_ar,
        title_en=title_en,
        deliverables_links=list(deliverables_links or []),
        executive_report_link=extras.get("executive_report_link"),
        training_video_link=extras.get("training_video_link"),
        runbook_link=extras.get("runbook_link"),
        sop_link=extras.get("sop_link"),
        audit_log_link=extras.get("audit_log_link"),
        proof_pack_link=extras.get("proof_pack_link"),
        customer_contacts=[],
        dealix_contacts=[],
        next_step_summary_ar=next_step_summary_ar,
        next_step_summary_en=next_step_summary_en,
    )
