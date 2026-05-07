"""customer_safe_labels — bilingual labels + internal-term scrubber.

Used by every customer-facing renderer to:
1. Convert internal module names → customer-visible Arabic/English labels
2. Strip internal terminology (v11/v12/v13/v14/router/verifier/growth_beast/
   stacktrace/pytest/internal_error) from any text before display
"""
from __future__ import annotations

import re
from typing import Any

from auto_client_acquisition.integration_upgrade.schemas import SafeLabel

# Internal terms to NEVER show to customers (case-insensitive substring scrub)
_INTERNAL_TERMS = (
    "v11", "v12", "v13", "v14", "v12.5",
    "router", "verifier", "growth_beast",
    "stacktrace", "pytest", "internal_error",
    "auto_client_acquisition", "_safe", "compliance_os_v12",
)
_INTERNAL_RE = re.compile(
    "|".join(re.escape(t) for t in _INTERNAL_TERMS),
    re.IGNORECASE,
)

# Internal-name → bilingual customer label
_LABEL_TABLE: dict[str, SafeLabel] = {
    "leadops_spine": SafeLabel(
        label_ar="تأهيل الفرص", label_en="Opportunity qualification",
        source_internal="leadops_spine",
    ),
    "customer_brain": SafeLabel(
        label_ar="ذاكرة العميل التشغيليّة", label_en="Customer operating memory",
        source_internal="customer_brain",
    ),
    "service_sessions": SafeLabel(
        label_ar="جلسات الخدمة", label_en="Service sessions",
        source_internal="service_sessions",
    ),
    "approval_center": SafeLabel(
        label_ar="مركز القرارات", label_en="Decisions center",
        source_internal="approval_center",
    ),
    "payment_ops": SafeLabel(
        label_ar="حالة الدفع", label_en="Payment state",
        source_internal="payment_ops",
    ),
    "proof_ledger": SafeLabel(
        label_ar="سجلّ الأدلّة", label_en="Proof ledger",
        source_internal="proof_ledger",
    ),
    "support_inbox": SafeLabel(
        label_ar="قسم الدعم", label_en="Support inbox",
        source_internal="support_inbox",
    ),
    "executive_pack_v2": SafeLabel(
        label_ar="ملخّص تنفيذي", label_en="Executive summary",
        source_internal="executive_pack_v2",
    ),
    "case_study_engine": SafeLabel(
        label_ar="دراسات الحالة", label_en="Case studies",
        source_internal="case_study_engine",
    ),
    "growth_beast": SafeLabel(
        label_ar="رادار النمو", label_en="Growth radar",
        source_internal="growth_beast",
    ),
    "company_growth_beast": SafeLabel(
        label_ar="رادار نمو الشركة", label_en="Company growth radar",
        source_internal="company_growth_beast",
    ),
    "ai_workforce": SafeLabel(
        label_ar="فريق الـ AI", label_en="AI workforce",
        source_internal="ai_workforce",
    ),
    "executive_command_center": SafeLabel(
        label_ar="مركز القيادة التنفيذي",
        label_en="Executive Command Center",
        source_internal="executive_command_center",
    ),
    "full_ops_radar": SafeLabel(
        label_ar="رادار العمليّات الكاملة",
        label_en="Full-Ops Radar",
        source_internal="full_ops_radar",
    ),
    "unified_operating_graph": SafeLabel(
        label_ar="خريطة عمليّات الشركة",
        label_en="Operating Graph",
        source_internal="unified_operating_graph",
    ),
}


def customer_safe_label(internal_name: str) -> dict[str, Any]:
    """Return a bilingual customer-facing label for an internal name.

    Unknown names get a generic safe label (never echoes the internal name).
    """
    label = _LABEL_TABLE.get(internal_name)
    if label is None:
        label = SafeLabel(
            label_ar="قسم تشغيلي",
            label_en="Operations section",
            source_internal=internal_name,
        )
    return label.model_dump(mode="json")


def hide_internal_terms(text: str) -> str:
    """Scrub internal terms from any string before customer display."""
    if not text:
        return text
    return _INTERNAL_RE.sub("[—]", text)
