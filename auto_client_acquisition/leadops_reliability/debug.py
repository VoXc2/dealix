"""LeadOps debug — diagnoses why no leads are flowing."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def diagnose() -> dict[str, Any]:
    """Returns a list of detected issues. Empty list = healthy."""
    issues = safe_call(name="diagnose", fn=_run_all_checks, fallback=[])
    if not isinstance(issues, list):
        issues = []
    return {
        "issues_count": len(issues),
        "issues": issues,
        "is_healthy": len(issues) == 0,
    }


def _run_all_checks() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_check_no_sources())
    issues.extend(_check_manual_board_empty())
    issues.extend(_check_provider_keys())
    issues.extend(_check_all_blocked_or_low_score())
    issues.extend(_check_approval_queue_health())
    return issues


def _check_no_sources() -> list[dict[str, Any]]:
    """Are any leads coming in at all?"""
    from auto_client_acquisition.leadops_spine import list_records
    records = list_records(limit=10)
    if not records:
        return [{
            "id": "no_sources_connected",
            "severity": "high",
            "reason_ar": "لا توجد leads في القائمة. هل تمّ توصيل أي مصدر؟",
            "reason_en": "No leads in the queue. Has any source been connected?",
            "fix_ar": "أضف lead يدوي عبر POST /api/v1/leadops/run أو ارفع CSV.",
            "fix_en": "Add a manual lead via POST /api/v1/leadops/run or upload a CSV.",
        }]
    return []


def _check_manual_board_empty() -> list[dict[str, Any]]:
    """Specifically: are manual-source leads totally absent?"""
    from auto_client_acquisition.leadops_spine import list_records
    records = list_records(limit=200)
    manual = [r for r in records if r.source == "manual"]
    warm_intro = [r for r in records if r.source == "warm_intro"]
    if not manual and not warm_intro:
        return [{
            "id": "manual_board_empty",
            "severity": "medium",
            "reason_ar": "لا توجد leads يدويّة أو warm_intro — الأقوى عادةً.",
            "reason_en": "No manual or warm_intro leads — usually the highest-converting.",
            "fix_ar": "ابدأ بـ ٥ warm intros من شبكتك الشخصية.",
            "fix_en": "Start with 5 warm intros from your personal network.",
        }]
    return []


def _check_provider_keys() -> list[dict[str, Any]]:
    """Provider API keys missing?"""
    from auto_client_acquisition.leadops_reliability.source_health import (
        source_health,
    )
    health = source_health()
    blockers = [s for s in health["sources"] if s.get("blocker")]
    if blockers:
        return [{
            "id": "provider_keys_missing",
            "severity": "low",
            "reason_ar": f"{len(blockers)} مصدر يحتاج مفاتيح API.",
            "reason_en": f"{len(blockers)} source(s) need API keys.",
            "fix_ar": "أضف المفاتيح الناقصة في env. (Manual + warm_intro يعملان دون مفاتيح.)",
            "fix_en": "Add missing keys in env. Manual + warm_intro work without keys.",
        }]
    return []


def _check_all_blocked_or_low_score() -> list[dict[str, Any]]:
    """Are all leads getting blocked or low-scored?"""
    from auto_client_acquisition.leadops_spine import list_records
    records = list_records(limit=100)
    if not records:
        return []
    blocked = sum(1 for r in records if r.compliance_status == "blocked")
    low_fit = sum(
        1 for r in records
        if isinstance(r.score, dict) and r.score.get("fit", 0) < 0.4
    )
    out: list[dict[str, Any]] = []
    if blocked == len(records):
        out.append({
            "id": "all_leads_blocked_by_compliance",
            "severity": "critical",
            "reason_ar": "جميع leads محجوبة بقواعد الامتثال — راجع البلوك ليست.",
            "reason_en": "All leads blocked by compliance rules — review the block list.",
            "fix_ar": "افحص data/compliance/blocked_customers.json",
            "fix_en": "Inspect data/compliance/blocked_customers.json",
        })
    if low_fit == len(records) and len(records) >= 5:
        out.append({
            "id": "all_leads_low_score",
            "severity": "high",
            "reason_ar": "جميع leads بدرجة منخفضة — راجع جودة البيانات أو تعريف الـ ICP.",
            "reason_en": "All leads scoring low — review data quality or ICP definition.",
            "fix_ar": "تأكد من أن كل lead فيه email + sector + region.",
            "fix_en": "Ensure every lead has email + sector + region.",
        })
    return out


def _check_approval_queue_health() -> list[dict[str, Any]]:
    """Drafts created but no approval queue?"""
    from auto_client_acquisition.leadops_spine import list_records
    records = list_records(limit=100)
    if not records:
        return []
    with_drafts = [r for r in records if r.draft_id is not None]
    with_approvals = [r for r in records if r.approval_id is not None]
    if with_drafts and not with_approvals:
        return [{
            "id": "approval_queue_missing",
            "severity": "medium",
            "reason_ar": "drafts منشأة لكن approval_id مفقود — قد لا تكون متصلة بمركز القرارات.",
            "reason_en": "drafts created but approval_id missing — may not be wired to approval center.",
            "fix_ar": "تحقق من approval_center module + GET /api/v1/approvals/pending",
            "fix_en": "Verify approval_center wiring + GET /api/v1/approvals/pending",
        }]
    return []
