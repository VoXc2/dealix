"""Shared seed builder for Saudi data-flow register entries (issue #918).

Single source of truth for the seed JSON so tests and runtime stay in sync.
Each entry is intentionally minimal: it documents what *category* exists, where it
goes, and what's pending. It is NOT a claim of completed legal review.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "privacy" / "data_flow_register_seed.json"

_COMMON_PROCESSORS: dict[str, Any] = {
    "railway_postgres": {
        "name": "Railway Inc.",
        "role_in_flow": "processor",
        "region": "us-west-1",
        "safeguards": "Postgres with row-level security, tenant_id enforced",
        "dpa_signed": True,
        "dpa_ref": "DPA-RAILWAY-REF",
    },
    "vercel_hosting": {
        "name": "Vercel Inc.",
        "role_in_flow": "processor",
        "region": "us-east-1",
        "safeguards": "Edge caching disabled for authenticated routes",
        "dpa_signed": True,
        "dpa_ref": "DPA-VERCEL-REF",
    },
    "llm_providers": [
        {
            "name": "OpenAI",
            "role_in_flow": "sub_processor",
            "region": "us-east-1",
            "safeguards": "Zero retention on API tier, no training on inputs",
            "dpa_signed": True,
            "dpa_ref": "DPA-OPENAI-REF",
        }
    ],
    "email_service": {
        "name": "Resend",
        "role_in_flow": "processor",
        "region": "us-east-1",
        "safeguards": "DKIM/SPF configured, unsubscribe enforced",
        "dpa_signed": True,
        "dpa_ref": "DPA-RESEND-REF",
    },
    "whatsapp_bsp": {
        "name": "Meta WhatsApp Business",
        "role_in_flow": "processor",
        "region": "multi-region",
        "safeguards": "WhatsApp Business Policy; no automation, opt-in only",
        "dpa_signed": False,
        "dpa_ref": "PENDING-META-DPA",
    },
    "calendar": {
        "name": "Google Calendar",
        "role_in_flow": "processor",
        "region": "global",
        "safeguards": "OAuth 2.0 scoped read/write",
        "dpa_signed": True,
        "dpa_ref": "DPA-GOOGLE-REF",
    },
    "analytics": {
        "name": "PostHog",
        "role_in_flow": "processor",
        "region": "eu-central-1",
        "safeguards": "IP anonymization enabled",
        "dpa_signed": True,
        "dpa_ref": "DPA-POSTHOG-REF",
    },
    "payment_provider": {
        "name": "Moyasar",
        "role_in_flow": "processor",
        "region": "sa-central-1",
        "safeguards": "PCI-DSS Level 1; CVV/PAN never stored",
        "dpa_signed": True,
        "dpa_ref": "DPA-MOYASAR-REF",
    },
}


def _base(
    flow_id: str,
    category: str,
    purpose: str,
    fields: list[str],
    retention_days: int,
    deletion: str = "anonymize",
    lawful_basis: str = "legitimate_interest",
    notes: str = "",
) -> dict[str, Any]:
    """Build a minimal-but-complete DataFlowEntry for the given category."""
    return {
        "flow_id": flow_id,
        "category": category,
        "controller_role": "controller",
        "purpose": purpose,
        "lawful_basis": lawful_basis,
        "source": {"system": "internal", "method": "derived"},
        "fields": fields,
        "recipients": [
            {
                "name": "Railway PostgreSQL",
                "role": "processor",
                "region": "us-west-1",
                "safeguards": "Tenant-scoped RLS; soft-delete honored",
            }
        ],
        "processors": _COMMON_PROCESSORS,
        "region": "us-west-1",
        "retention_days": retention_days,
        "retention_trigger": "last_interaction",
        "deletion_method": deletion,
        "consent_capture": {
            "required": True,
            "method": "explicit_checkbox",
            "timestamp_field": "consent_timestamp",
            "evidence_ref": "consent_record_id",
        },
        "data_subject_path": {
            "access": "POST /api/v1/data-subject/access",
            "rectification": "POST /api/v1/data-subject/rectify",
            "deletion": "POST /api/v1/data-subject/delete",
            "portability": "GET /api/v1/data-subject/export",
        },
        "cross_border_transfer": {
            "occurs": True,
            "mechanism": "standard_contractual_clauses",
            "safeguards": "SCCs signed; counsel review pending",
            "counsel_review_ref": "PENDING-COUNSEL-REVIEW",
        },
        "review_status": "draft",
        "notes": notes or "Tenant isolation via row-level security; approval-gated writes.",
    }


def build_seed() -> list[dict[str, Any]]:
    """Return the canonical seed entries for the data-flow register."""
    return [
        _base(
            "DF-COMPANY-001",
            "company_facts",
            "Saudi company registration, industry, and size facts for B2B qualification",
            ["cr_number", "legal_name", "industry_code", "employee_band", "city"],
            retention_days=1825,
        ),
        _base(
            "DF-CONTACT-001",
            "business_contact_data",
            "B2B contact details for opportunities and outreach",
            ["full_name", "work_email", "work_phone", "job_title", "company_id"],
            retention_days=1095,
        ),
        _base(
            "DF-MSG-001",
            "message_content",
            "Inbound/outbound email and support message content for service delivery",
            ["subject", "body_excerpt", "channel", "direction"],
            retention_days=730,
        ),
        _base(
            "DF-APPROVAL-001",
            "approvals",
            "Founder/admin approval decisions and audit trail",
            ["action_type", "approved_by", "decision", "reason_hash"],
            retention_days=1825,
            deletion="hard_delete",
        ),
        _base(
            "DF-PROPOSAL-001",
            "proposals",
            "Commercial proposals and pricing scopes sent to prospects",
            ["proposal_id", "client_id", "amount_sar", "status"],
            retention_days=1095,
        ),
        _base(
            "DF-PAYMENT-001",
            "payments",
            "Payment transactions, invoices, and refund records (Moyasar through Moyasar)",
            ["transaction_ref", "amount_sar", "currency", "status", "moyasar_id"],
            retention_days=2555,
            lawful_basis="contract",
        ),
        _base(
            "DF-SUPPORT-001",
            "support",
            "Support tickets and resolutions for customer success",
            ["ticket_id", "severity", "category", "resolution_notes"],
            retention_days=730,
        ),
        _base(
            "DF-TELEMETRY-001",
            "telemetry",
            "Product usage metrics, error rates, and system health indicators",
            ["event_name", "timestamp", "user_agent_hash", "session_id"],
            retention_days=365,
            deletion="aggregate_only",
        ),
        _base(
            "DF-PROMPT-001",
            "model_prompts",
            "Prompts sent to LLM providers for company brain and agent reasoning",
            ["prompt_hash", "model", "token_count", "safety_flags"],
            retention_days=90,
            deletion="hard_delete",
        ),
        _base(
            "DF-AUDIT-001",
            "audit_logs",
            "System-wide audit log of data access and mutations",
            ["actor_id", "action", "resource", "tenant_id", "timestamp"],
            retention_days=1825,
            deletion="hard_delete",
        ),
        _base(
            "DF-CONSENT-001",
            "consent_records",
            "Consent capture records (Saudi PDPA Article 5)",
            ["subject_id", "consent_type", "granted_at", "method", "evidence_hash"],
            retention_days=1825,
            lawful_basis="consent",
        ),
    ]


def load_seed() -> list[dict[str, Any]]:
    """Load seed from disk, or raise if missing."""
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def main() -> int:
    """Self-test: verify the programmatic seed matches the JSON on disk."""
    on_disk = load_seed()
    built = build_seed()
    if on_disk != built:
        print("FAIL seed mismatch: JSON on disk != generated seed. Re-sync.")
        return 1
    print(f"PASS seed_consistency ({len(on_disk)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
