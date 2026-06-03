"""Map governance friction signals to product surface names (compliance-to-product)."""

from __future__ import annotations

# (governance_need_slug, product_artifact_slug)
COMPLIANCE_NEED_TO_PRODUCT: tuple[tuple[str, str], ...] = (
    ("source_clarity", "source_passport_panel"),
    ("ai_visibility", "ai_run_ledger"),
    ("human_review", "approval_center"),
    ("proof_of_value", "proof_timeline"),
    ("governance_reporting", "compliance_report"),
    ("education", "academy_module"),
    ("audit_export", "audit_export"),
)


def product_artifact_for_need(need: str) -> str | None:
    for need_slug, product_slug in COMPLIANCE_NEED_TO_PRODUCT:
        if need_slug == need:
            return product_slug
    return None


def all_governance_needs() -> tuple[str, ...]:
    return tuple(n for n, _ in COMPLIANCE_NEED_TO_PRODUCT)
