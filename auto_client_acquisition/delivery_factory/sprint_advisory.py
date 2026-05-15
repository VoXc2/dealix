"""Optional AI advisory layer for the delivery Sprint.

Pure helpers that enrich deterministic Sprint steps with LLM suggestions.
The deterministic output ALWAYS stays the record of truth — these helpers
only ATTACH an ``advisory`` sub-object; they never reorder ranks or replace
deterministic text.

Doctrine:
- Every advisory item is flagged ``advisory_draft`` + ``awaiting=founder_approval``.
- Outreach drafts are governance-checked by the Sprint (step 5); the ranking
  rationale is self-checked here via ``policy_check_draft``.
- On any router failure / cost block, the helper returns an
  ``advisory_unavailable`` object — never a fabricated draft, never a silent
  ``None`` (Article 8).
"""

from __future__ import annotations

from typing import Any

# Cap the number of accounts we draft outreach for, to bound LLM cost.
_MAX_ADVISORY_ACCOUNTS = 5

_OK_STATUSES = ("ok_cloud", "ok_local")


def _outreach_prompt(account: dict[str, Any], language: str) -> str:
    name = account.get("company_name", "?")
    sector = account.get("sector", "") or "B2B"
    if language == "ar":
        return (
            f"اكتب رسالة افتتاحية قصيرة واحترافية لحساب '{name}' في قطاع "
            f"'{sector}' بالسوق السعودي. ركّز على القيمة، اترك القرار للعميل، "
            "ولا تستخدم أي وعود أو ضمانات بنتائج مبيعات."
        )
    return (
        f"Write a short, professional opening outreach note for the account "
        f"'{name}' in the '{sector}' sector of the Saudi B2B market. "
        "Value-led, decision left to the customer, no guarantees of sales outcomes."
    )


def advisory_ranking_rationale(top_accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """AI rationale for the deterministic top-N ranking. Does NOT re-rank.

    Returns an advisory dict; ``status`` is ``advisory_draft`` on success,
    ``advisory_blocked`` if governance blocks the rationale, or
    ``advisory_unavailable`` if the router could not produce a response.
    """
    from auto_client_acquisition.governance_os.policy_check import policy_check_draft
    from auto_client_acquisition.intelligence.dealix_model_router import route_task

    if not top_accounts:
        return {
            "status": "advisory_unavailable",
            "awaiting": "founder_approval",
            "reason": "no_accounts",
        }

    lines = [
        f"{a.get('rank', '?')}. {a.get('company_name', '?')} — "
        f"score {a.get('score', '?')} "
        f"({', '.join(a.get('reasons', [])) or 'n/a'})"
        for a in top_accounts
    ]
    prompt = (
        "أنت محلل نمو في Dealix. فيما يلي ترتيب حتمي لأفضل الحسابات وفق قواعد "
        "ثابتة. اكتب فقرة قصيرة (٣-٥ جمل) تشرح منطق هذا الترتيب وأين تتركز "
        "الفرصة — دون إعادة ترتيب ودون أي وعود أو ضمانات بنتائج.\n\n" + "\n".join(lines)
    )
    decision = route_task("company_brain_summarize", prompt=prompt, language="ar")
    if decision.status not in _OK_STATUSES:
        return {
            "status": "advisory_unavailable",
            "awaiting": "founder_approval",
            "reason": decision.status,
            "router_reasons": list(decision.fallback_reasons),
        }

    gov = policy_check_draft(decision.text)
    return {
        "status": "advisory_draft" if gov.allowed else "advisory_blocked",
        "awaiting": "founder_approval",
        "rationale": decision.text if gov.allowed else "",
        "router_status": decision.status,
        "backend_used": decision.backend_used,
        "confidence": {
            "level": decision.confidence.level,
            "score": decision.confidence.score,
        },
        "governance": {
            "decision": gov.verdict.value,
            "allowed": gov.allowed,
            "reasons": list(gov.issues),
        },
        "estimated_cost_usd": decision.estimated_cost_usd,
    }


def advisory_outreach_drafts(top_accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """Real AR + EN outreach drafts for the top accounts (advisory only).

    Governance is applied later by the Sprint (step 5); each draft carries
    ``governance=None`` / ``surfaced=None`` until then. Deterministic
    outlines in ``step4_draft_pack`` are unaffected.
    """
    from auto_client_acquisition.intelligence.dealix_model_router import route_task

    if not top_accounts:
        return {
            "status": "advisory_unavailable",
            "awaiting": "founder_approval",
            "reason": "no_accounts",
            "drafts": [],
        }

    drafts: list[dict[str, Any]] = []
    any_ok = False
    for acc in top_accounts[:_MAX_ADVISORY_ACCOUNTS]:
        ar = route_task("draft_message_arabic", prompt=_outreach_prompt(acc, "ar"), language="ar")
        en = route_task("draft_message_english", prompt=_outreach_prompt(acc, "en"), language="en")
        ar_ok = ar.status in _OK_STATUSES
        en_ok = en.status in _OK_STATUSES
        any_ok = any_ok or ar_ok or en_ok
        drafts.append(
            {
                "account": acc.get("company_name", "?"),
                "draft_ar": ar.text if ar_ok else "",
                "draft_en": en.text if en_ok else "",
                "router_status_ar": ar.status,
                "router_status_en": en.status,
                "confidence_ar": {"level": ar.confidence.level, "score": ar.confidence.score},
                "confidence_en": {"level": en.confidence.level, "score": en.confidence.score},
                "estimated_cost_usd": round(ar.estimated_cost_usd + en.estimated_cost_usd, 6),
                # Filled in by the Sprint after the step-5 governance review.
                "governance": None,
                "surfaced": None,
            }
        )

    return {
        "status": "advisory_draft" if any_ok else "advisory_unavailable",
        "awaiting": "founder_approval",
        "drafts": drafts,
        "accounts_drafted": len(drafts),
    }


__all__ = ["advisory_outreach_drafts", "advisory_ranking_rationale"]
