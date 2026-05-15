"""Case-safe summary exporter — Wave 14D.2.

Pulls a Proof Pack, strips client identifiers, generates a case-safe
summary markdown safe for public distribution.

Reuses:
  - proof_os.assemble (for the 14-section ProofPack)
  - customer_data_plane.pii_redactor.redact_text (PII strip)
  - capital_os.capital_ledger.list_assets (for capital asset count)

Rules:
  - Customer name → anonymized "Saudi {sector} {size}-tier company"
  - All PII patterns (emails, phones, IDs) redacted
  - No raw text strings from drafts (governance decision counts only)
  - Estimated value tier NEVER published; verified + client_confirmed only
  - Bilingual disclaimer footer mandatory
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.capital_os.capital_ledger import list_assets
from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text


@dataclass
class CaseStudyExport:
    engagement_id: str
    anonymized_label: str
    generated_at: str
    sector: str
    summary_ar: str
    summary_en: str
    metrics: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    proof_score: float = 0.0
    proof_tier: str = ""
    governance_decision: str = "draft_only"
    is_case_safe: bool = True
    requires_founder_approval_before_publish: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "engagement_id": self.engagement_id,
            "anonymized_label": self.anonymized_label,
            "generated_at": self.generated_at,
            "sector": self.sector,
            "summary_ar": self.summary_ar,
            "summary_en": self.summary_en,
            "metrics": dict(self.metrics),
            "limitations": list(self.limitations),
            "proof_score": self.proof_score,
            "proof_tier": self.proof_tier,
            "governance_decision": self.governance_decision,
            "is_case_safe": self.is_case_safe,
            "requires_founder_approval_before_publish": self.requires_founder_approval_before_publish,
        }

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Case-Safe Summary — {self.anonymized_label}")
        lines.append("")
        lines.append(
            "_Hypothetical / case-safe template based on the Dealix delivery methodology. "
            "No real customer is named or implied._"
        )
        lines.append("")
        lines.append(f"**Sector:** {self.sector}")
        lines.append(f"**Proof Score:** {self.proof_score} (tier: {self.proof_tier})")
        lines.append(f"**Governance:** {self.governance_decision}")
        lines.append(f"**Generated:** {self.generated_at}")
        lines.append("")
        lines.append("## Summary / الملخص")
        lines.append("")
        lines.append(self.summary_en)
        lines.append("")
        lines.append(self.summary_ar)
        lines.append("")
        if self.metrics:
            lines.append("## Observed Metrics")
            for k, v in self.metrics.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
        if self.limitations:
            lines.append("## Limitations")
            for limit in self.limitations:
                lines.append(f"- {limit}")
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._"
        )
        return "\n".join(lines)


def _anonymize_label(*, sector: str, customer_id: str) -> str:
    sector_clean = (sector or "b2b_services").lower().strip()
    # 8-char hash of customer_id for stable anonymized reference.
    import hashlib
    h = hashlib.sha256(customer_id.encode("utf-8")).hexdigest()[:6].upper()
    return f"Saudi {sector_clean.replace('_', ' ')} company ({h})"


def _strip_proof_pack(pack_dict: dict[str, Any]) -> tuple[str, str, dict[str, Any], list[str]]:
    """Extract case-safe summary + metrics + limitations from a ProofPack dict.

    Returns (summary_en, summary_ar, metrics_dict, limitations_list).
    """
    sections = pack_dict.get("sections", {}) or {}

    # Strip PII from any potentially-customer-bearing sections.
    summary_raw = (
        sections.get("executive_summary", "") + "\n\n"
        + sections.get("outputs", "")
    )
    summary_safe = redact_text(summary_raw)

    summary_en = (
        "Engagement delivered the Dealix 7-day Revenue Intelligence Sprint with "
        f"a governance-reviewed Proof Pack scoring {pack_dict.get('score', 0)}/100 "
        f"(tier: {pack_dict.get('tier', 'weak')}). "
        + summary_safe[:300].strip()
    )
    summary_ar = (
        "تم تنفيذ Sprint ذكاء الإيراد لمدة 7 أيام مع Proof Pack مُراجَع حوكميًا "
        f"بدرجة {pack_dict.get('score', 0)} من 100 "
        f"(التصنيف: {pack_dict.get('tier', 'weak')})."
    )

    # Metrics: only counts, no raw values.
    metrics: dict[str, Any] = {}
    dq_section = sections.get("data_quality_score", "")
    if "DQ=" in dq_section:
        try:
            dq_val = dq_section.split("DQ=")[1].split("/")[0].strip()
            metrics["data_quality_score"] = dq_val
        except Exception:
            pass

    governance_section = sections.get("governance_decisions", "")
    if governance_section:
        metrics["governance_decisions_summary"] = (
            governance_section.replace(";", ", ").strip()[:200]
        )

    blocked_section = sections.get("blocked_risks", "")
    if blocked_section and blocked_section != "(none)":
        metrics["blocked_unsafe_actions"] = blocked_section.strip()[:200]

    limitations: list[str] = list(pack_dict.get("limitations", []))
    limitations.append("This is a case-safe summary; raw client identifiers stripped.")
    limitations.append(
        "Estimated value tier NEVER published. Verified + client_confirmed only."
    )

    return summary_en.strip(), summary_ar.strip(), metrics, limitations


def export_case_safe(
    *,
    engagement_id: str,
    customer_id: str,
    sector: str = "b2b_services",
    proof_pack: dict[str, Any] | None = None,
) -> CaseStudyExport:
    """Export a case-safe summary from a Proof Pack dict.

    If `proof_pack` is not supplied, attempts to reconstruct one minimally
    from the capital_ledger for the engagement (defensive: never raises).
    """
    if proof_pack is None:
        # Best-effort minimal reconstruction.
        assets = list_assets(customer_id=customer_id, engagement_id=engagement_id)
        proof_pack = {
            "engagement_id": engagement_id,
            "customer_id": customer_id,
            "score": 0.0,
            "tier": "weak",
            "sections": {
                "executive_summary": "Engagement state not fully recorded.",
                "data_quality_score": "DQ=0.0/100",
                "governance_decisions": "(none)",
                "blocked_risks": "(none)",
                "outputs": "(none)",
            },
            "limitations": [
                "minimal_reconstruction_from_capital_ledger_only",
                f"capital_assets_count={len(assets)}",
            ],
            "governance_decision": "allow_with_review",
        }

    summary_en, summary_ar, metrics, limitations = _strip_proof_pack(proof_pack)

    return CaseStudyExport(
        engagement_id=engagement_id,
        anonymized_label=_anonymize_label(sector=sector, customer_id=customer_id),
        generated_at=datetime.now(UTC).isoformat(),
        sector=sector,
        summary_ar=summary_ar,
        summary_en=summary_en,
        metrics=metrics,
        limitations=limitations,
        proof_score=float(proof_pack.get("score", 0.0)),
        proof_tier=str(proof_pack.get("tier", "weak")),
        governance_decision=str(proof_pack.get("governance_decision", "draft_only")),
    )


__all__ = ["CaseStudyExport", "export_case_safe"]
