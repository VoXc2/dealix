"""Content Factory — proof → ar/en article + founder post + FAQ, atomization, no copy-paste spam."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class ContentAtom(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    atom_id: str
    locale: str  # ar, en
    type: str  # article, founder_post, faq, sales_enablement
    title: str
    body: str
    source_proof_id: str = UNKNOWN
    sector: str = UNKNOWN
    proof_ref: str = UNKNOWN
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

class ContentFactory:
    def atomize(self, proof: dict[str, Any]) -> list[ContentAtom]:
        # One high-quality proof → 4 atoms, no duplication, each with unique value
        proof_id = proof.get("proof_id", "proof_unknown")
        sector = proof.get("sector", UNKNOWN)
        problem = proof.get("problem", UNKNOWN)
        result = proof.get("result", UNKNOWN)
        base_hash = hashlib.sha256(proof_id.encode()).hexdigest()[:8]
        atoms: list[ContentAtom] = []
        # AR article
        atoms.append(ContentAtom(
            atom_id=f"atom_{base_hash}_ar_article",
            locale="ar",
            type="article",
            title=f"كيف حللنا {problem} في {sector} — دراسة حالة",
            body=f"منهجية: {proof.get('intervention', UNKNOWN)} — نتيجة: {result} — دليل: {proof.get('evidence_ref', UNKNOWN)} — لا نعد بROI بدون دليل.",
            source_proof_id=proof_id,
            sector=sector,
            proof_ref=proof.get("evidence_ref", UNKNOWN),
        ))
        # EN article
        atoms.append(ContentAtom(
            atom_id=f"atom_{base_hash}_en_article",
            locale="en",
            type="article",
            title=f"How we solved {problem} in {sector} — case study",
            body=f"Method: {proof.get('intervention', UNKNOWN)} — Result: {result} — Evidence: {proof.get('evidence_ref', UNKNOWN)} — no ROI promise without evidence.",
            source_proof_id=proof_id,
            sector=sector,
            proof_ref=proof.get("evidence_ref", UNKNOWN),
        ))
        # Founder post draft (short, insight)
        atoms.append(ContentAtom(
            atom_id=f"atom_{base_hash}_founder_post",
            locale="ar",
            type="founder_post",
            title=f"درس من {sector}: {problem}",
            body=f"تعلم: {result} — التالي: تشخيص D1 قبل أي توسع. لا proof → لا upsell.",
            source_proof_id=proof_id,
            sector=sector,
            proof_ref=proof.get("evidence_ref", UNKNOWN),
        ))
        # FAQ
        atoms.append(ContentAtom(
            atom_id=f"atom_{base_hash}_faq",
            locale="ar",
            type="faq",
            title=f"الأسئلة الشائعة: {problem}",
            body=f"س: ما تكلفة {problem}؟ ج: نطاق {proof.get('expected_impact_range', 'UNKNOWN')} — يتطلب اكتشاف.",
            source_proof_id=proof_id,
            sector=sector,
            proof_ref=proof.get("evidence_ref", UNKNOWN),
        ))
        return atoms

    def to_dict(self, atoms: list[ContentAtom]) -> dict[str, Any]:
        return {"atoms": [a.model_dump(mode="json") for a in atoms], "count": len(atoms)}

__all__ = ["ContentFactory", "ContentAtom", "UNKNOWN"]
