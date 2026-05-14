"""Trust Pack assembler — enterprise procurement-ready evidence bundle.

Produces a single markdown document covering:
  1. What Dealix does (one paragraph, bilingual AR + EN)
  2. What Dealix refuses (the 11 non-negotiables, each with the test that enforces it)
  3. Data handling (PDPL alignment, sub-processors, retention)
  4. Source Passport policy
  5. Governance Runtime (7 decisions + sample matrix)
  6. AI Run Ledger (proof_ledger schema)
  7. Human oversight (approval_center)
  8. Approval workflow
  9. Proof Pack standard
 10. Incident response
 11. Client responsibilities

Output is markdown — convert to PDF externally with weasyprint or pandoc.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


_NON_NEGOTIABLES = (
    ("No scraping", "tests/test_no_scraping_engine.py"),
    ("No cold WhatsApp automation", "tests/test_no_cold_whatsapp.py"),
    ("No LinkedIn automation", "tests/test_no_linkedin_automation.py"),
    ("No fake / un-sourced claims", "tests/test_no_guaranteed_claims.py"),
    ("No guaranteed sales outcomes", "tests/test_no_guaranteed_claims.py"),
    ("No PII in logs", "api/middleware/bopla_redaction.py + friction_log/sanitizer.py"),
    ("No source-less knowledge answers", "tests/test_no_source_passport_no_ai.py"),
    ("No external action without approval", "tests/test_pii_external_requires_approval.py"),
    ("No agent without identity", "auto_client_acquisition/agent_governance/"),
    ("No project without Proof Pack", "tests/test_proof_pack_required.py"),
    ("No project without Capital Asset", "auto_client_acquisition/capital_os/capital_ledger.py"),
)


@dataclass
class TrustPack:
    customer_handle: str
    generated_at: str = ""
    sections: dict[str, str] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_handle": self.customer_handle,
            "generated_at": self.generated_at,
            "sections": dict(self.sections),
            "governance_decision": self.governance_decision,
        }

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Dealix Trust Pack — {self.customer_handle}")
        lines.append(f"_Generated: {self.generated_at}_")
        lines.append("")
        for key in (
            "what_dealix_does",
            "what_dealix_refuses",
            "data_handling",
            "source_passport_policy",
            "governance_runtime",
            "ai_run_ledger",
            "human_oversight",
            "approval_workflow",
            "proof_pack_standard",
            "incident_response",
            "client_responsibilities",
        ):
            title = key.replace("_", " ").title()
            lines.append(f"## {title}")
            lines.append(self.sections.get(key, "(section pending)"))
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._"
        )
        return "\n".join(lines)


def _what_dealix_does() -> str:
    return (
        "Dealix is a Saudi Governed AI Operations company. We sell operating "
        "capability + auditable proof for B2B revenue, knowledge, governance, "
        "and operations workflows. Every output carries a GovernanceDecision "
        "envelope. PDPL-native, ZATCA-compliant, Arabic-first.\n\n"
        "Dealix شركة تشغيل ذكاء اصطناعي محكوم سعودية. نبيع قدرة تشغيلية "
        "وأدلة قابلة للتدقيق لعمليات الإيراد والمعرفة والحوكمة. كل مخرج "
        "يحمل قرار حوكمة. متوافقون مع نظام حماية البيانات الشخصية وفوترة "
        "ZATCA، وعربياً أولاً."
    )


def _what_dealix_refuses() -> str:
    lines = ["The 11 non-negotiables, enforced by code:"]
    for rule, enforcement in _NON_NEGOTIABLES:
        lines.append(f"- **{rule}** — enforced by `{enforcement}`")
    lines.append("")
    lines.append("اللاءات الإحدى عشر — مُنفَّذة في الكود:")
    return "\n".join(lines)


def _data_handling() -> str:
    return (
        "- Data minimization at intake: PII columns flagged before any AI use.\n"
        "- Source Passport required on every dataset (`data_os.SourcePassport`).\n"
        "- PII redaction at log + export boundaries (`api/middleware/bopla_redaction.py`).\n"
        "- Retention policy per engagement (`project_duration` default).\n"
        "- Sub-processors: Anthropic, OpenAI (LLM), Moyasar (payments), Gmail (email).\n"
        "- Customer data is NEVER used to train models.\n"
        "- PDPL Article 5 (consent) / 13 (erasure) / 14 (portability) / 18 (audit) / 21 (breach) honored."
    )


def _source_passport_policy() -> str:
    return (
        "Every dataset entering Dealix has a SourcePassport with: source_id, "
        "source_type, owner, allowed_use, contains_pii, sensitivity, "
        "ai_access_allowed, external_use_allowed, retention_policy.\n\n"
        "No passport → governance_os.decide returns BLOCK.\n"
        "Invalid passport → BLOCK with reasons.\n"
        "PII + external_use → REQUIRE_APPROVAL.\n"
        "Sensitivity=high → REQUIRE_APPROVAL.\n"
        "See `docs/04_data_os/SOURCE_PASSPORT.md`."
    )


def _governance_runtime() -> str:
    return (
        "Seven decisions: ALLOW, ALLOW_WITH_REVIEW, DRAFT_ONLY, REQUIRE_APPROVAL, "
        "REDACT, BLOCK, ESCALATE.\n\n"
        "Composition: `governance_os.decide(action, context)` consults "
        "channel_policy_gateway (cold/automation rules), safe_send_gateway "
        "(quiet hours + opt-out), claim_safety (guarantee detection), and "
        "data_os.source_passport (validation + approval rules).\n\n"
        "See `docs/05_governance_os/RUNTIME_GOVERNANCE.md`."
    )


def _ai_run_ledger() -> str:
    return (
        "Every AI invocation is recorded in `proof_ledger` (JSONL + Postgres "
        "backends). Schema: id, event_type, customer_handle, summary_ar/en "
        "(redacted), evidence_source, confidence, consent_for_publication, "
        "approval_status, risk_level, payload, created_at.\n\n"
        "Tamper-evident: each record is HMAC-signed (`proof_ledger/hmac_signing.py`)."
    )


def _human_oversight() -> str:
    return (
        "Every external-bound output passes through `approval_center` before "
        "send. Founder reviews drafts, governance decisions, and proof packs. "
        "Internal AI agents queue drafts; they never send autonomously."
    )


def _approval_workflow() -> str:
    return (
        "1. Internal agent generates draft → `approval_center.queue(draft)`.\n"
        "2. Founder reviews via `/api/v1/approval-center/pending`.\n"
        "3. Founder approves or rejects → status logged.\n"
        "4. Approved drafts pass through `safe_send_gateway` (consent, quiet "
        "hours, suppression) before actual send.\n"
        "5. Every transition emits a ProofEvent."
    )


def _proof_pack_standard() -> str:
    return (
        "14-section schema (see `docs/07_proof_os/PROOF_PACK_STANDARD.md`). "
        "Score: 25% source coverage + 25% output quality + 20% governance "
        "integrity + 15% value evidence + 15% capital asset creation.\n\n"
        "Tier: ≥85 case_candidate, 70-84 sales_support, 55-69 internal_learning, "
        "<55 weak.\n\nNever published without source_refs and explicit "
        "consent_for_publication."
    )


def _incident_response() -> str:
    return (
        "1. Detection (alarms in `observability_v10`).\n"
        "2. Triage within 4 hours.\n"
        "3. Customer notification within 72 hours (PDPL Article 21).\n"
        "4. Root cause + corrective action recorded in `friction_log` + capital ledger.\n"
        "5. Public changelog entry (anonymized) within 14 days."
    )


def _client_responsibilities() -> str:
    return (
        "- Provide a valid Source Passport per dataset.\n"
        "- Designate a workflow owner for any retainer engagement.\n"
        "- Approve drafts within agreed SLA (default 48h).\n"
        "- Notify Dealix of any consent changes (opt-out, deletion request).\n"
        "- Use Dealix outputs as drafts — final external send is a client decision."
    )


def assemble_trust_pack(*, customer_handle: str = "(prospective)") -> TrustPack:
    """Compose a Trust Pack. All content is methodology — no real customer data."""
    return TrustPack(
        customer_handle=customer_handle,
        generated_at=datetime.now(timezone.utc).isoformat(),
        sections={
            "what_dealix_does": _what_dealix_does(),
            "what_dealix_refuses": _what_dealix_refuses(),
            "data_handling": _data_handling(),
            "source_passport_policy": _source_passport_policy(),
            "governance_runtime": _governance_runtime(),
            "ai_run_ledger": _ai_run_ledger(),
            "human_oversight": _human_oversight(),
            "approval_workflow": _approval_workflow(),
            "proof_pack_standard": _proof_pack_standard(),
            "incident_response": _incident_response(),
            "client_responsibilities": _client_responsibilities(),
        },
        governance_decision="allow_with_review",
    )


__all__ = ["TrustPack", "assemble_trust_pack"]
