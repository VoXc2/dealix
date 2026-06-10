"""Wave 13 Phase 8 — Customer Proof Maturity composite score.

Composite from:
  - proof_event_count_by_level (L0-L5 distribution)
  - publishable_count (events ≥ L4 with consent)
  - consent_signed_count

Buckets: pre_proof / early_proof / mature_proof / case_study_ready

Article 8: is_estimate=True; case_study_ready requires L4+ AND consent.
Article 11: ~100 LOC; deterministic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

ProofMaturityBucket = Literal[
    "pre_proof",         # 0 proof events
    "early_proof",       # 1-3 events, mostly L1-L2
    "mature_proof",      # ≥3 events, ≥1 at L3+
    "case_study_ready",  # ≥1 event at L4+ AND consent_granted
]


@dataclass(slots=True)
class ProofMaturityAssessment:
    customer_id: str
    score: float  # 0-100
    bucket: ProofMaturityBucket
    proof_event_count: int
    max_evidence_level: int  # 0-5
    publishable_count: int  # events ≥ L4 with consent
    consent_signed_count: int
    drivers: list[str]
    recommended_action_ar: str
    recommended_action_en: str
    is_estimate: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bucket_for(
    *,
    proof_count: int,
    max_level: int,
    publishable_count: int,
    consent_signed_count: int,
) -> ProofMaturityBucket:
    """Per spec: case_study_ready requires L4+ AND consent."""
    if publishable_count >= 1 and consent_signed_count >= 1 and max_level >= 4:
        return "case_study_ready"
    if proof_count >= 3 and max_level >= 3:
        return "mature_proof"
    if proof_count >= 1:
        return "early_proof"
    return "pre_proof"


def _recommended_action(bucket: ProofMaturityBucket) -> tuple[str, str]:
    if bucket == "case_study_ready":
        return (
            "ابدأ بناء case study علني. اعرض على العميل صياغة أوّليّة.",
            "Start building public case study. Show customer initial draft.",
        )
    if bucket == "mature_proof":
        return (
            "اطلب موافقة العميل لرفع مستوى Proof Pack إلى L4 (إثبات قابل للنشر).",
            "Request customer consent to upgrade Proof Pack to L4 (publishable).",
        )
    if bucket == "early_proof":
        return (
            "ركّز على توثيق ٢-٣ proof events إضافية في الأسبوع القادم.",
            "Focus on documenting 2-3 more proof events in the coming week.",
        )
    return (
        "ابدأ بـ Free Diagnostic أو Proof Sprint لإنشاء أوّل proof event.",
        "Start with Free Diagnostic or Proof Sprint to create first proof event.",
    )


def compute_proof_maturity(
    *,
    customer_id: str,
    proof_event_count: int = 0,
    max_evidence_level: int = 0,
    publishable_count: int = 0,
    consent_signed_count: int = 0,
) -> ProofMaturityAssessment:
    """Compute Proof Maturity composite (0-100).

    Score = min(100, proof_event_count * 8 + max_level * 10 + publishable * 15)
    Bucket determined per spec rules above.
    """
    score = (
        proof_event_count * 8
        + max_evidence_level * 10
        + publishable_count * 15
        + consent_signed_count * 5
    )
    score = min(100.0, max(0.0, float(score)))

    bucket = _bucket_for(
        proof_count=proof_event_count,
        max_level=max_evidence_level,
        publishable_count=publishable_count,
        consent_signed_count=consent_signed_count,
    )
    rec_ar, rec_en = _recommended_action(bucket)

    drivers: list[str] = []
    if proof_event_count == 0:
        drivers.append("No proof events recorded yet")
    else:
        drivers.append(f"{proof_event_count} proof events recorded")
    if max_evidence_level >= 4:
        drivers.append(f"Highest evidence level: L{max_evidence_level} (publishable)")
    elif max_evidence_level > 0:
        drivers.append(f"Highest evidence level: L{max_evidence_level}")
    if consent_signed_count >= 1:
        drivers.append(f"{consent_signed_count} signed consent(s) on file")

    return ProofMaturityAssessment(
        customer_id=customer_id,
        score=score,
        bucket=bucket,
        proof_event_count=int(proof_event_count),
        max_evidence_level=int(max_evidence_level),
        publishable_count=int(publishable_count),
        consent_signed_count=int(consent_signed_count),
        drivers=drivers,
        recommended_action_ar=rec_ar,
        recommended_action_en=rec_en,
        is_estimate=True,
    )
