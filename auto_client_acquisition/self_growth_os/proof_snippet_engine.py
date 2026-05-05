"""Proof-snippet engine — converts a typed ProofEvent dict into a
publishable snippet, gated by the safe-publishing-gate and the
customer's consent flag.

This is the seed of the future ProofEvent ledger. Today it operates
on a single dict in-memory; the public API stays the same when the
real Postgres-backed ledger lands later.

Strict rules:
  - Customer name is NEVER published unless ``consent_for_publication`` is True.
  - Numbers are kept honest (ratios, counts, ranges) — never invented.
  - Forbidden vocabulary (نضمن / guaranteed / blast / scrape / cold)
    cannot pass the gate.
  - Every output carries ``approval_status=approval_required`` —
    even after the gate passes, the founder approves before any
    external publication.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.self_growth_os.safe_publishing_gate import check_text
from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    Language,
    PublishingDecision,
    RiskLevel,
    ServiceBundle,
)


REQUIRED_FIELDS = (
    "event_type",
    "service_id",
    "outcome_metric",
    "outcome_value",
    "consent_for_publication",
)


@dataclass(frozen=True)
class ProofSnippetResult:
    decision: str  # PublishingDecision value
    approval_status: str
    snippet_ar: str
    snippet_en: str
    audience: str  # "internal_only" | "public_with_consent"
    forbidden_tokens_found: list[str]
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "approval_status": self.approval_status,
            "snippet_ar": self.snippet_ar,
            "snippet_en": self.snippet_en,
            "audience": self.audience,
            "forbidden_tokens_found": self.forbidden_tokens_found,
            "notes": self.notes,
        }


def _validate(event: dict[str, Any]) -> list[str]:
    missing = [f for f in REQUIRED_FIELDS if f not in event]
    return missing


def _anonymize_customer(event: dict[str, Any]) -> str:
    """If consent missing OR consent=False, return an anonymized handle."""
    if not event.get("consent_for_publication"):
        # Use customer_anonymized if provided; else generic handle.
        return str(event.get("customer_anonymized") or "Saudi B2B customer")
    name = str(event.get("customer_display_name") or event.get("customer_anonymized") or "")
    return name or "Saudi B2B customer"


def _format_outcome(event: dict[str, Any]) -> tuple[str, str]:
    """Render the outcome metric into bilingual phrasing.
    Honest ranges only — never invent values.
    """
    metric = str(event.get("outcome_metric", "outcome"))
    value = event.get("outcome_value", "—")
    sla = event.get("sla_period_days")
    sla_part_ar = f" خلال {sla} أيام" if sla else ""
    sla_part_en = f" within {sla} days" if sla else ""
    return (
        f"{value} {metric}{sla_part_ar}",
        f"{value} {metric}{sla_part_en}",
    )


def _service_title_pair(event: dict[str, Any]) -> tuple[str, str]:
    sid = event.get("service_id") or "service"
    bundle = event.get("service_bundle") or "service"
    # Lookup from matrix would be ideal; for an MVP, use the slug.
    title_ar = f"خدمة {sid}"
    title_en = f"{sid.replace('_', ' ').title()} service"
    return title_ar, title_en


def render(event: dict[str, Any]) -> ProofSnippetResult:
    """Render one ProofEvent dict into a typed snippet result.

    Caller is responsible for persisting the result. This function
    is pure — no DB write, no external send.
    """
    missing = _validate(event)
    if missing:
        return ProofSnippetResult(
            decision=PublishingDecision.BLOCKED.value,
            approval_status=ApprovalStatus.BLOCKED.value,
            snippet_ar="",
            snippet_en="",
            audience="invalid",
            forbidden_tokens_found=[],
            notes=f"missing required fields: {missing}",
        )

    customer = _anonymize_customer(event)
    outcome_ar, outcome_en = _format_outcome(event)
    svc_ar, svc_en = _service_title_pair(event)

    snippet_ar = (
        f"عميل {customer} استخدم {svc_ar} وحقّق {outcome_ar}. النتيجة موثَّقة في "
        f"Proof Pack موقَّع من العميل."
    )
    snippet_en = (
        f"Customer {customer} used {svc_en} and recorded {outcome_en}. "
        f"Result is documented in a customer-signed Proof Pack."
    )

    # Run both snippets through the safe-publishing gate.
    ar_check = check_text(snippet_ar, language=Language.AR)
    en_check = check_text(snippet_en, language=Language.EN)
    forbidden = list(set(ar_check.forbidden_tokens_found + en_check.forbidden_tokens_found))

    if forbidden:
        return ProofSnippetResult(
            decision=PublishingDecision.BLOCKED.value,
            approval_status=ApprovalStatus.BLOCKED.value,
            snippet_ar=snippet_ar,
            snippet_en=snippet_en,
            audience="invalid",
            forbidden_tokens_found=forbidden,
            notes=(
                "rendered snippet contains forbidden vocabulary — "
                "rephrase the input event description."
            ),
        )

    audience = "public_with_consent" if event.get("consent_for_publication") else "internal_only"
    notes = ""
    if audience == "internal_only":
        notes = (
            "consent_for_publication=False → audience=internal_only; "
            "do NOT share externally without written customer consent."
        )

    return ProofSnippetResult(
        decision=PublishingDecision.ALLOWED_DRAFT.value,
        approval_status=ApprovalStatus.APPROVAL_REQUIRED.value,
        snippet_ar=snippet_ar,
        snippet_en=snippet_en,
        audience=audience,
        forbidden_tokens_found=[],
        notes=notes,
    )


def render_batch(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Render many events at once. Useful for the founder's weekly
    Proof Pack assembly."""
    results = [render(e).to_dict() for e in events]
    public = sum(1 for r in results if r["audience"] == "public_with_consent")
    internal = sum(1 for r in results if r["audience"] == "internal_only")
    blocked = sum(1 for r in results if r["decision"] == "blocked")
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": {
            "total": len(results),
            "public_with_consent": public,
            "internal_only": internal,
            "blocked": blocked,
        },
        "results": results,
    }


def render_pack(
    events: list[dict[str, Any]],
    customer_handle: str = "Saudi B2B customer",
    period_label: str = "",
) -> dict[str, Any]:
    """Assemble many ProofEvents into a single customer-shareable pack.

    Returns a typed dict with bilingual markdown documents. Every
    individual event is rendered through ``render()``; the resulting
    snippets are then composed into one document per language. The
    full document is re-checked through the safe-publishing gate so
    a forbidden-word that survives single-event rendering still gets
    blocked at pack level.

    Pack-level decision/audience logic:
      - audience = ``public_with_consent`` only if EVERY event has
        ``consent_for_publication=True`` AND no event was blocked.
      - audience = ``internal_only`` if any event has consent=False
        but NO event is blocked.
      - audience = ``invalid`` if ANY event was blocked OR the events
        list is empty.

    Always returns ``approval_status=approval_required`` — even a
    fully-consented public-ready pack must be founder-approved
    before any external publication.
    """
    if not events:
        return {
            "schema_version": 1,
            "generated_at": datetime.now(UTC).isoformat(),
            "customer_handle": customer_handle,
            "period_label": period_label,
            "decision": PublishingDecision.BLOCKED.value,
            "approval_status": ApprovalStatus.BLOCKED.value,
            "audience": "invalid",
            "events": [],
            "summary_ar": "",
            "summary_en": "",
            "markdown_ar": "",
            "markdown_en": "",
            "notes": "events list empty",
        }

    rendered = [render(e) for e in events]
    rendered_dicts = [r.to_dict() for r in rendered]

    blocked = [r for r in rendered if r.decision == PublishingDecision.BLOCKED.value]
    if blocked:
        # Surface every blocking reason so the caller can rephrase / fix inputs.
        forbidden_all = []
        for r in blocked:
            forbidden_all.extend(r.forbidden_tokens_found)
        return {
            "schema_version": 1,
            "generated_at": datetime.now(UTC).isoformat(),
            "customer_handle": customer_handle,
            "period_label": period_label,
            "decision": PublishingDecision.BLOCKED.value,
            "approval_status": ApprovalStatus.BLOCKED.value,
            "audience": "invalid",
            "events": rendered_dicts,
            "summary_ar": "",
            "summary_en": "",
            "markdown_ar": "",
            "markdown_en": "",
            "forbidden_tokens_found": sorted(set(forbidden_all)),
            "notes": (
                f"{len(blocked)} of {len(events)} events were blocked — "
                "fix the offending inputs (forbidden tokens or missing "
                "required fields) before re-assembling the pack."
            ),
        }

    # Aggregate per-language snippets.
    period_part = f" ({period_label})" if period_label else ""
    title_ar = f"حزمة الأدلّة — {customer_handle}{period_part}"
    title_en = f"Proof Pack — {customer_handle}{period_part}"
    summary_ar = (
        f"يلخّص هذا المستند {len(rendered)} حدثاً موثَّقاً قُدِّم لـ "
        f"{customer_handle}. كلّ حدث له مصدر داخل المنصّة + موافقة "
        f"العميل (حيث ينطبق)."
    )
    summary_en = (
        f"This document summarizes {len(rendered)} documented events "
        f"delivered to {customer_handle}. Every event has a source "
        f"inside the platform + customer sign-off where applicable."
    )

    md_ar_lines = [
        f"# {title_ar}",
        "",
        summary_ar,
        "",
        "## الأحداث الموثَّقة",
        "",
    ]
    md_en_lines = [
        f"# {title_en}",
        "",
        summary_en,
        "",
        "## Documented events",
        "",
    ]
    for i, r in enumerate(rendered, 1):
        md_ar_lines.append(f"### {i}. {r.snippet_ar}")
        md_ar_lines.append("")
        md_en_lines.append(f"### {i}. {r.snippet_en}")
        md_en_lines.append("")

    md_ar_lines.append("---")
    md_ar_lines.append(f"_توقيع العميل مطلوب قبل أيّ نشر خارجي. هذه النسخة تتطلّب موافقة المؤسس._")
    md_en_lines.append("---")
    md_en_lines.append(f"_Customer sign-off required before external publication. This draft requires founder approval._")

    markdown_ar = "\n".join(md_ar_lines)
    markdown_en = "\n".join(md_en_lines)

    # Pack-level safety re-check. Single events passed individually, but
    # composition could surprise — re-run the gate on the full markdown.
    ar_gate = check_text(markdown_ar, language=Language.AR)
    en_gate = check_text(markdown_en, language=Language.EN)
    forbidden = sorted(set(
        ar_gate.forbidden_tokens_found + en_gate.forbidden_tokens_found
    ))
    if forbidden:
        return {
            "schema_version": 1,
            "generated_at": datetime.now(UTC).isoformat(),
            "customer_handle": customer_handle,
            "period_label": period_label,
            "decision": PublishingDecision.BLOCKED.value,
            "approval_status": ApprovalStatus.BLOCKED.value,
            "audience": "invalid",
            "events": rendered_dicts,
            "summary_ar": summary_ar,
            "summary_en": summary_en,
            "markdown_ar": markdown_ar,
            "markdown_en": markdown_en,
            "forbidden_tokens_found": forbidden,
            "notes": "pack-level safe-publishing gate blocked the assembled document",
        }

    all_consented = all(
        bool(e.get("consent_for_publication")) for e in events
    )
    audience = "public_with_consent" if all_consented else "internal_only"

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "customer_handle": customer_handle,
        "period_label": period_label,
        "decision": PublishingDecision.ALLOWED_DRAFT.value,
        "approval_status": ApprovalStatus.APPROVAL_REQUIRED.value,
        "audience": audience,
        "events": rendered_dicts,
        "summary_ar": summary_ar,
        "summary_en": summary_en,
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "forbidden_tokens_found": [],
        "notes": (
            "internal-only pack — do NOT share externally without "
            "written customer consent on every included event."
            if audience == "internal_only"
            else "all events consented — founder approval still required before external publication."
        ),
    }


def boundaries() -> dict[str, Any]:
    """Documentation endpoint for the engine's safety boundaries."""
    return {
        "required_fields": list(REQUIRED_FIELDS),
        "default_audience": "internal_only",
        "default_approval_status": ApprovalStatus.APPROVAL_REQUIRED.value,
        "default_risk_level": RiskLevel.LOW.value,
        "service_bundle_default": ServiceBundle.PROOF_PACK.value if hasattr(ServiceBundle, "PROOF_PACK") else ServiceBundle.UNKNOWN.value,
        "rules": {
            "customer_name_anonymized_unless_consent": True,
            "rejected_if_forbidden_vocabulary": True,
            "always_approval_required_before_external_publish": True,
            "no_invented_metrics": True,
        },
    }
