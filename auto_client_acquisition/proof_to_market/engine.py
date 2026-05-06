"""Proof-to-Market engine. Pure-local. NEVER fabricates."""
from __future__ import annotations


def select_publishable_proofs(events: list[dict]) -> list[dict]:
    """Filter proofs that are SAFE to publish externally:
    customer_approved=true AND signed_publish_permission=true."""
    return [e for e in events
            if e.get("customer_approved") is True
            and e.get("signed_publish_permission") is True
            and e.get("audience") != "internal_only"]


def approval_gate_check(event: dict) -> dict:
    """Returns allow/block decision with reason."""
    if not event:
        return {"allow": False, "reason_ar": "لا حدث", "reason_en": "no event"}
    if not event.get("customer_approved"):
        return {"allow": False,
                "reason_ar": "لا موافقة من العميل",
                "reason_en": "customer not approved"}
    if not event.get("signed_publish_permission"):
        return {"allow": False,
                "reason_ar": "لا توقيع نشر — internal_only فقط",
                "reason_en": "no signed publish permission — internal_only only"}
    if event.get("audience") == "internal_only":
        return {"allow": False,
                "reason_ar": "audience=internal_only",
                "reason_en": "audience=internal_only"}
    return {"allow": True,
            "reason_ar": "موافق عليه للنشر الخارجي",
            "reason_en": "approved for external publish"}


def proof_to_snippet(event: dict) -> dict:
    """Compose a publish-safe snippet from a proof event. Only runs
    if approval_gate_check returns allow=True."""
    decision = approval_gate_check(event)
    if not decision["allow"]:
        return {"blocked": True, **decision, "action_mode": "blocked"}
    action = event.get("action_taken", "delivery")
    return {
        "blocked": False,
        "snippet_ar": (
            f"خلال أسبوع: {action}. تم بموافقة وتوقيع العميل. "
            "تفاصيل أكثر بإذن إضافي."
        ),
        "snippet_en": (
            f"In one week: {action}. Done with signed customer "
            "permission. More details on additional approval."
        ),
        "audience": "public_allowed",
        "action_mode": "approval_required",  # founder still approves the publish
    }


def case_study_candidate(events: list[dict], min_events: int = 3) -> dict:
    """A customer becomes a case-study candidate when ≥ min_events real
    proof events exist + all signed for publish."""
    if not events:
        return {"candidate": False, "reason": "no_events"}
    publishable = select_publishable_proofs(events)
    if len(publishable) < min_events:
        return {
            "candidate": False,
            "publishable_count": len(publishable),
            "needed": min_events,
            "reason": "insufficient_signed_events",
        }
    return {
        "candidate": True,
        "publishable_count": len(publishable),
        "first_3_events": publishable[:3],
        "next_action_ar": "اعتمد قصة الحالة + أرسل للعميل النهائي للموافقة",
        "next_action_en": "Approve case-study draft + send to customer for final sign-off",
        "action_mode": "approval_required",
    }


def sector_learning_summary(events: list[dict]) -> dict:
    """What did proof events teach us per sector?"""
    if not events:
        return {"insufficient_data": True,
                "next_ar": "لا أحداث بعد", "next_en": "no events yet"}
    by_sector: dict[str, int] = {}
    for e in events:
        sec = e.get("sector_hint", "unknown")
        by_sector[sec] = by_sector.get(sec, 0) + 1
    top_sector = max(by_sector.items(), key=lambda kv: kv[1])
    return {
        "insufficient_data": False,
        "by_sector": by_sector,
        "top_sector": top_sector[0],
        "top_sector_count": top_sector[1],
        "next_action_ar": f"ضاعف التركيز على {top_sector[0]} وقطاعات مماثلة",
        "next_action_en": f"Double-down on {top_sector[0]} and similar sectors",
        "action_mode": "suggest_only",
    }
