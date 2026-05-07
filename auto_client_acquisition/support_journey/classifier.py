"""Stage classifier — wraps support_os.classifier and adds the journey stage."""
from __future__ import annotations

from typing import Any

# Map support_os category → journey stage
_CATEGORY_TO_STAGE: dict[str, str] = {
    "diagnostic_question": "pre_sales",
    "upgrade_question": "pre_sales",
    "onboarding": "onboarding",
    "connector_setup": "onboarding",
    "technical_issue": "delivery",
    "proof_pack_question": "proof",
    "billing": "billing",
    "payment": "billing",
    "refund": "billing",
    "privacy_pdpl": "privacy",
    "angry_customer": "delivery",
    "unknown": "pre_sales",
}


def classify_with_stage(message_text: str) -> dict[str, Any]:
    """Classify the message via existing support_os, then add journey stage."""
    from auto_client_acquisition.support_os.classifier import classify_message
    classification = classify_message(message_text)
    stage = _CATEGORY_TO_STAGE.get(classification.category, "pre_sales")
    return {
        "category": classification.category,
        "confidence": classification.confidence,
        "is_arabic": classification.is_arabic,
        "needs_human_immediately": classification.needs_human_immediately,
        "journey_stage": stage,
        "matched_terms": list(classification.matched_terms),
    }
