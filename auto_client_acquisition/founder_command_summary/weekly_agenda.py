"""Pre-populated weekly operating meeting agenda (10 sections)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_command_summary.engagement_registry import (
    EngagementSnapshot,
)


def build_weekly_operating_agenda(snapshots: dict[str, EngagementSnapshot]) -> dict[str, Any]:
    """Ten-section agenda aligned with Operating Rhythm / weekly council."""
    n = len(snapshots)
    finalized = sum(1 for s in snapshots.values() if s.finalize_done)
    proofed = sum(1 for s in snapshots.values() if s.proof_generated)
    return {
        "agenda_type": "weekly_operating_meeting",
        "engagements_active": n,
        "sections": [
            {"id": 1, "title_ar": "أعلى القرارات", "title_en": "Top decisions", "prompt": "اقتصار على 3–5 قرارات فقط.", "metrics": {"open_engagements": n}},
            {"id": 2, "title_ar": "الإيراد وجودته", "title_en": "Revenue quality", "prompt": "Bad revenue filter + فرص retainer.", "metrics": {}},
            {"id": 3, "title_ar": "التسليم", "title_en": "Delivery", "prompt": f"{finalized}/{n} engagements finalized.", "metrics": {"finalized": finalized}},
            {"id": 4, "title_ar": "Proof والقيمة", "title_en": "Proof & value", "prompt": f"{proofed}/{n} proof packs generated.", "metrics": {"proof_packs": proofed}},
            {"id": 5, "title_ar": "الحوكمة", "title_en": "Governance", "prompt": "مراجعة قرارات DRAFT_ONLY وموافقات.", "metrics": {}},
            {"id": 6, "title_ar": "تبني العملاء", "title_en": "Adoption", "prompt": "Adoption vs proof strength.", "metrics": {}},
            {"id": 7, "title_ar": "التمييز كمنتج", "title_en": "Productization", "prompt": "ما تكرر ≥3 مرات؟", "metrics": {}},
            {"id": 8, "title_ar": "رأس المال والأصول", "title_en": "Capital assets", "prompt": "Trust + Product/Knowledge لكل engagement.", "metrics": {}},
            {"id": 9, "title_ar": "قائمة التوقف", "title_en": "Stop list", "prompt": "ما نتوقف عن فعله هذا الأسبوع.", "metrics": {}},
            {"id": 10, "title_ar": "المخاطر والاعتماديات", "title_en": "Risks & dependencies", "prompt": "Incident-to-asset + بوابات الدفع.", "metrics": {}},
        ],
    }
