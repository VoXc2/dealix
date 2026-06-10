"""
Evidence levels for Proof Events — L0–L5.

Rules (product):
  L0/L1 — لا تُستخدم في تسويق خارجي
  L2 — داخلي
  L3 — دليل مبيعات خاص بالعميل
  L4 — دراسة حالة عامة (بعد موافقة)
  L5 — دليل توسعة / إيراد (بعد التزام كتابي ودفع حيث ينطبق)
"""

from __future__ import annotations

from enum import IntEnum


class EvidenceLevel(IntEnum):
    L0_PLANNED = 0
    L1_INTERNAL_DRAFT = 1
    L2_CUSTOMER_REVIEWED = 2
    L3_CUSTOMER_APPROVED = 3
    L4_PUBLIC_APPROVED = 4
    L5_REVENUE_EXPANSION = 5


EVIDENCE_LEVEL_DESCRIPTIONS_AR: dict[int, str] = {
    0: "مخطط — لم يُنفَّذ بعد",
    1: "مسودة داخلية — غير جاهزة للعميل",
    2: "راجعها العميل — خاص",
    3: "وافق العميل — يُسمح باستخدامه في مبيعات خاصة",
    4: "موافقة نشر عام — دراسة حالة",
    5: "دليل إيراد/توسعة — بعد التزام وتتبع",
}

EVIDENCE_LEVEL_DESCRIPTIONS_EN: dict[int, str] = {
    0: "Planned — not executed",
    1: "Internal draft — not customer-ready",
    2: "Customer reviewed — private",
    3: "Customer approved — private sales proof",
    4: "Public publish approved — case study",
    5: "Revenue/expansion evidence — after written commitment / payment where applicable",
}


def assert_public_proof_allowed(level: int, *, consent_public: bool) -> None:
    """Raise ValueError if attempting public marketing below L4 or without consent."""
    if level < EvidenceLevel.L4_PUBLIC_APPROVED:
        raise ValueError("public_proof_requires_L4_minimum")
    if not consent_public:
        raise ValueError("public_proof_requires_explicit_consent")
