"""Decision Passport + Golden Chain + Evidence catalog (Revenue OS)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.proof_engine.evidence import (
    EVIDENCE_LEVEL_DESCRIPTIONS_AR,
    EVIDENCE_LEVEL_DESCRIPTIONS_EN,
    EvidenceLevel,
)

router = APIRouter(prefix="/api/v1/decision-passport", tags=["Decision Passport"])


GOLDEN_CHAIN_AR = (
    "إشارة السوق → عميل محتمل → جواز قرار → إجراء معتمد → تسليم → إثبات → توسعة → تعلّم"
)
GOLDEN_CHAIN_EN = (
    "Market signal → Lead → Decision Passport → Approved action → Delivery → "
    "Proof → Expansion → Learning"
)


@router.get("/golden-chain")
async def golden_chain() -> dict[str, Any]:
    """السلسلة الذهبية — مرجع منتج ثابت."""
    return {
        "chain_ar": GOLDEN_CHAIN_AR,
        "chain_en": GOLDEN_CHAIN_EN,
        "rule": "No Decision Passport = No Action",
        "rule_ar": "بدون جواز قرار لا يُنفَّذ إجراء خارجي",
    }


@router.get("/evidence-levels")
async def evidence_levels() -> dict[str, Any]:
    """مستويات أدلة الـ Proof — L0–L5."""
    return {
        "levels": [
            {
                "level": int(lev),
                "name": lev.name,
                "description_ar": EVIDENCE_LEVEL_DESCRIPTIONS_AR.get(int(lev), ""),
                "description_en": EVIDENCE_LEVEL_DESCRIPTIONS_EN.get(int(lev), ""),
            }
            for lev in EvidenceLevel
        ],
    }
