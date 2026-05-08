"""Anti-Waste Engine — reject pipeline steps that violate golden-chain rules."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


@dataclass(frozen=True)
class AntiWasteViolation:
    code: str
    detail_ar: str
    detail_en: str


def validate_pipeline_step(
    *,
    has_decision_passport: bool,
    lead_source: str | None,
    action_external: bool,
    upsell_attempt: bool,
    proof_event_count: int,
    evidence_level_for_public: int = 0,
    public_marketing_attempt: bool = False,
    feature_request_count: int = 0,
) -> list[AntiWasteViolation]:
    """Return violations (empty if OK). Pure checks."""
    v: list[AntiWasteViolation] = []

    if action_external and not has_decision_passport:
        v.append(
            AntiWasteViolation(
                "no_passport_no_action",
                "لا إجراء خارجي بدون Decision Passport",
                "No external action without Decision Passport.",
            )
        )

    blocked_sources = {"cold_whatsapp", "scraping", "purchased_list", "linkedin_automation"}
    src = (lead_source or "").lower()
    if src in blocked_sources:
        v.append(
            AntiWasteViolation(
                "blocked_source",
                f"مصدر ممنوع: {src}",
                f"Blocked ingestion source: {src}",
            )
        )

    if upsell_attempt and proof_event_count < 1:
        v.append(
            AntiWasteViolation(
                "upsell_without_proof",
                "لا upsell بدون Proof Event مسجّل",
                "No upsell without at least one Proof Event.",
            )
        )

    if public_marketing_attempt and evidence_level_for_public < int(
        EvidenceLevel.L4_PUBLIC_APPROVED
    ):
        v.append(
            AntiWasteViolation(
                "public_proof_below_L4",
                "لا نشر عام بدون موافقة ومستوى دليل L4+",
                "No public marketing below evidence level L4 with consent.",
            )
        )

    if feature_request_count > 0 and feature_request_count < 3:
        # Not a violation — product rule is "defer unless 3 customers"; informational only
        pass

    return v
