"""The 7-gate map — Dealix's proof-before-scale progression (doctrine §14).

Each gate is a checkpoint. A gate passes only when its criterion is met by real
operating signals — never by aspiration. Build only past Gate 7.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Gate:
    number: int
    name_ar: str
    name_en: str
    criterion_ar: str
    criterion_en: str


GATES: tuple[Gate, ...] = (
    Gate(
        1,
        "إثبات السوق الأول",
        "First Market Proof",
        "٥ رسائل مُرسَلة وأول رد أو صمت مُصنَّف.",
        "5 messages sent and the first reply or silence classified.",
    ),
    Gate(
        2,
        "إثبات الاجتماع",
        "Meeting Proof",
        "حالة used_in_meeting (L5) تحققت.",
        "used_in_meeting (L5) reached.",
    ),
    Gate(
        3,
        "إثبات السحب",
        "Pull Proof",
        "حالة scope_requested (L6) تحققت.",
        "scope_requested (L6) reached.",
    ),
    Gate(
        4,
        "إثبات الإيراد",
        "Revenue Proof",
        "حالة invoice_paid (L7 مؤكد) تحققت.",
        "invoice_paid (L7 confirmed) reached.",
    ),
    Gate(
        5,
        "القابلية للتكرار",
        "Repeatability",
        "نفس العرض بِيع مرتين.",
        "The same offer sold twice.",
    ),
    Gate(
        6,
        "الاحتفاظ المتكرر",
        "Retainer",
        "قيمة شهرية متكررة قائمة.",
        "A recurring monthly value engagement is live.",
    ),
    Gate(
        7,
        "إشارة المنصة",
        "Platform Signal",
        "workflow يدوي تكرر ٣ مرات أو أكثر.",
        "A manual workflow repeated 3+ times.",
    ),
)


def evaluate_gates(
    *,
    messages_sent: int = 0,
    classified_replies: int = 0,
    used_in_meeting: int = 0,
    scope_requested: int = 0,
    invoice_paid: int = 0,
    offer_sold_twice: bool = False,
    repeated_workflows: int = 0,
) -> list[dict[str, object]]:
    """Evaluate all 7 gates against current operating signals."""
    passed = {
        1: messages_sent >= 5 and classified_replies >= 1,
        2: used_in_meeting >= 1,
        3: scope_requested >= 1,
        4: invoice_paid >= 1,
        5: offer_sold_twice,
        6: invoice_paid >= 1 and offer_sold_twice,
        7: repeated_workflows >= 3,
    }
    return [
        {
            "number": g.number,
            "name_ar": g.name_ar,
            "name_en": g.name_en,
            "criterion_ar": g.criterion_ar,
            "criterion_en": g.criterion_en,
            "passed": bool(passed[g.number]),
        }
        for g in GATES
    ]
