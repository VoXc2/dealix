"""Founder v5 — aggregate read-only dashboard.

Composes one bilingual snapshot across the 12 v5 layers + the
self-growth perimeter so the founder can see the full state of the
business in one HTTP call instead of 12. Read-only; never mutates
state; never sends a message; never charges anything.

Designed to be safe to call from a phone. Bilingual fields where
human-facing.

v6 additions: ``first_3_customers`` slot board summary,
``pending_approvals`` count + first 3 cards, ``unsafe_blocks`` sanity
check on FORBIDDEN_TOOLS, and ``next_founder_action`` (extracted from
the daily growth loop top decision).
"""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _safe(fn, *, default: Any) -> Any:
    """Run fn(); on any error, return a typed error blob.

    The dashboard MUST stay reachable even if one layer is mid-deploy
    or has a probe failure — so each section is wrapped.
    """
    try:
        return fn()
    except BaseException as exc:
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_message": str(exc)[:200],
            "_default": default,
        }


def _service_counts() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import (
        service_activation_matrix,
    )
    return service_activation_matrix.counts()


def _reliability() -> dict[str, Any]:
    from auto_client_acquisition.reliability_os import build_health_matrix
    matrix = build_health_matrix()
    # Trim to the founder-relevant fields — overall + status counts +
    # a one-line status per subsystem. Full matrix still lives at
    # /api/v1/reliability/health-matrix for deep inspection.
    subs = [
        {"name": s.get("name"), "status": s.get("status")}
        for s in matrix.get("subsystems") or []
    ]
    return {
        "overall_status": matrix.get("overall_status"),
        "counts": matrix.get("counts"),
        "subsystems": subs,
    }


def _live_gates() -> dict[str, Any]:
    """All live-action gates. Every value should be `BLOCKED` on a
    healthy production deploy. The dashboard surfaces this so the
    founder catches misconfiguration immediately."""
    out: dict[str, str] = {}

    # 1. Live charge — finance_os
    try:
        from auto_client_acquisition.finance_os import is_live_charge_allowed
        live = is_live_charge_allowed()
        out["live_charge"] = (
            "BLOCKED" if not live.get("allowed") else "ALLOWED"
        )
    except BaseException as exc:
        out["live_charge"] = f"UNKNOWN ({type(exc).__name__})"

    # 2. WhatsApp live send — settings flag
    try:
        from core.config.settings import get_settings
        flag = getattr(get_settings(), "whatsapp_allow_live_send", False)
        out["whatsapp_live_send"] = "BLOCKED" if not flag else "ALLOWED"
    except BaseException as exc:
        out["whatsapp_live_send"] = f"UNKNOWN ({type(exc).__name__})"

    # 3. Email live send — no flag exists, so always BLOCKED
    out["email_live_send"] = "BLOCKED (no flag exists by design)"

    # 4. LinkedIn / scraping — agent_governance forbids
    try:
        from auto_client_acquisition.agent_governance import (
            FORBIDDEN_TOOLS,
            ToolCategory,
        )
        ok = (
            ToolCategory.LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS
            and ToolCategory.SCRAPE_WEB in FORBIDDEN_TOOLS
        )
        out["linkedin_and_scraping"] = "BLOCKED" if ok else "MISCONFIGURED"
    except BaseException as exc:
        out["linkedin_and_scraping"] = f"UNKNOWN ({type(exc).__name__})"

    return out


def _daily_loop_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today()
    decisions = loop.get("decisions") or []
    return {
        "decisions_count": len(decisions),
        "top_3_decisions": decisions[:3],
        "open_loops": loop.get("decline_or_open_loops", []),
    }


def _weekly_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard
    return weekly_growth_scorecard.build_scorecard()


def _ceo_brief_top() -> dict[str, Any]:
    from auto_client_acquisition.role_command_os import (
        RoleName,
        build_role_brief,
    )
    brief = build_role_brief(RoleName.CEO)
    return {
        "summary_ar": brief.summary_ar,
        "summary_en": brief.summary_en,
        "top_decisions": [d.model_dump() for d in brief.top_decisions[:3]],
        "next_action_ar": brief.next_action_ar,
        "next_action_en": brief.next_action_en,
    }


def _first_3_customers() -> dict[str, Any]:
    """Surface the 3-slot loop board from the local markdown file.

    Reads ``docs/FIRST_3_CUSTOMER_LOOP_BOARD.md`` and reports per-slot
    state markers. Real customer names are NEVER pulled — the doc itself
    only contains placeholders (Slot-A / Slot-B / Slot-C) per PDPL.
    """
    repo_root = Path(__file__).resolve().parents[2]
    board = repo_root / "docs" / "FIRST_3_CUSTOMER_LOOP_BOARD.md"
    if not board.exists():
        return {"slots": [], "status_counts": {}, "source_missing": True}

    text = board.read_text(encoding="utf-8")

    # Each slot row in the board markdown is `| **A** | Slot-A | ...`.
    # Walk the table rows in order and extract the columns we expose.
    slots: list[dict[str, Any]] = []
    diagnostic_counts: dict[str, int] = {}
    pilot_counts: dict[str, int] = {}
    proof_counts: dict[str, int] = {}
    for slot_letter in ("A", "B", "C"):
        marker = f"| **{slot_letter}** |"
        idx = text.find(marker)
        if idx == -1:
            continue
        line_end = text.find("\n", idx)
        row = text[idx:line_end if line_end != -1 else None]
        cells = [c.strip() for c in row.split("|")]
        row_cells: list[str] = list(cells)

        # cells[1]=slot, cells[2]=company placeholder, ... col mapping:
        # 1 slot, 2 company, 3 source, 4 consent, 5 segment, 6 problem,
        # 7 diagnostic_status, 8 pilot_status, 9 proof_status, 10 next, 11 owner
        def _col(i: int, _row: list[str] = row_cells) -> str:
            return _row[i] if i < len(_row) else ""

        diag = _col(7)
        pilot = _col(8)
        proof = _col(9)
        slots.append({
            "slot": slot_letter,
            "placeholder": _col(2),
            "segment": _col(5),
            "diagnostic_status": diag,
            "pilot_status": pilot,
            "proof_status": proof,
        })
        diagnostic_counts[diag] = diagnostic_counts.get(diag, 0) + 1
        pilot_counts[pilot] = pilot_counts.get(pilot, 0) + 1
        proof_counts[proof] = proof_counts.get(proof, 0) + 1

    return {
        "slots": slots,
        "status_counts": {
            "diagnostic": diagnostic_counts,
            "pilot": pilot_counts,
            "proof": proof_counts,
        },
        "source": "docs/FIRST_3_CUSTOMER_LOOP_BOARD.md",
    }


def _pending_approvals() -> dict[str, Any]:
    """Count pending approvals and surface the first 3 as bilingual cards."""
    from auto_client_acquisition.approval_center import (
        list_pending,
        render_approval_card,
    )
    pending = list_pending()
    cards = [render_approval_card(p) for p in pending[:3]]
    return {
        "count": len(pending),
        "first_3": cards,
    }


def _unsafe_blocks() -> dict[str, Any]:
    """Sanity check: FORBIDDEN_TOOLS must contain at least the 5 v6
    perimeter tools. Surfacing the names lets the founder catch a
    deploy-time flip from `forbidden` to `allowed`.
    """
    from auto_client_acquisition.agent_governance import FORBIDDEN_TOOLS
    names = sorted(t.value for t in FORBIDDEN_TOOLS)
    return {
        "count": len(names),
        "names": names,
    }


def _next_founder_action() -> str:
    """Extract just the title of the top decision from build_today().

    Returns ``"no_action_today"`` when the daily loop has no decisions.
    """
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today()
    decisions = loop.get("decisions") or []
    if not decisions:
        return "no_action_today"
    top = decisions[0]
    if isinstance(top, dict):
        title = (
            top.get("title_ar")
            or top.get("title_en")
            or top.get("title")
            or top.get("name_ar")
            or top.get("name_en")
        )
        if title:
            return str(title)
    elif isinstance(top, str):
        return top
    return "no_action_today"


def _governance_risk_payload() -> dict[str, Any]:
    from api.routers.governance_risk_dashboard import build_risk_dashboard_payload

    return build_risk_dashboard_payload()


def _service_sessions_summary() -> dict[str, Any]:
    from collections import Counter

    from auto_client_acquisition.service_sessions import list_sessions

    recs = list_sessions(limit=200)
    by_status = Counter(s.status for s in recs)
    return {
        "sampled": len(recs),
        "status_counts": dict(by_status),
    }


@router.get("/operating-scorecard")
async def operating_scorecard() -> dict[str, Any]:
    """Weekly-style operating snapshot — read-only; composes governance + sessions."""
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "governance_risk": _safe(_governance_risk_payload, default={}),
        "service_sessions": _safe(_service_sessions_summary, default={}),
        "readiness_endpoints": {
            "service_readiness_get": "/api/v1/commercial/service-readiness/{service_id}",
            "readiness_gates_post": "/api/v1/commercial/readiness-gates/check",
        },
        "revenue_placeholders": {
            "mrr_sar": None,
            "note_ar": "الإيراد المؤكد يحتاج ربط دفتر مدفوعات؛ لا أرقام وهمية.",
            "note_en": "Confirmed revenue requires a payment ledger; no fake revenue.",
        },
        "docs": {
            "north_star": "docs/commercial/NORTH_STAR_METRICS_AR.md",
            "capability_verification": "docs/company/CAPABILITY_VERIFICATION_AR.md",
        },
        "read_only": True,
    }


@router.get("/status")
async def status() -> dict:
    return {
        "module": "founder",
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
        "endpoints": ["/dashboard", "/operating-scorecard"],
    }


@router.get("/dashboard")
async def dashboard() -> dict:
    """Single bilingual snapshot of the entire v5 stack (cached 60s).

    Read-only. Never sends, never charges, never writes. Safe to
    call from a phone. Composes 6+ heavy aggregations behind a
    minute-bucket cache so the second call within 60s returns in
    <50ms. Degraded sections produce an explicit ``degraded=true``
    marker rather than a 5xx.
    """
    from auto_client_acquisition.founder_v10 import (
        build_dashboard_payload,
        cached_dashboard_payload,
    )
    return cached_dashboard_payload(build_dashboard_payload)


@router.get("/leads")
async def leads(
    limit: int = 200,
    status: str | None = None,
) -> dict[str, Any]:
    """Lead-inbox feed for the founder. Lists every demo / pilot
    inquiry persisted by the public form, newest first.

    Read-only. Backed by `auto_client_acquisition.lead_inbox` — a
    JSON-Lines file at $DEALIX_LEAD_INBOX_PATH (default
    `var/lead-inbox.jsonl`, gitignored).

    Server-side this endpoint is unauthenticated, but the matching
    landing page (/founder-leads.html) is gated by the access-tier
    JS overlay so the public never reaches it casually. Real auth
    comes when first paying customer ships per Article 13.
    """
    from auto_client_acquisition import lead_inbox
    return {
        "schema_version": 1,
        "leads": lead_inbox.list_leads(limit=limit, status=status),
        "stats": lead_inbox.stats(),
        "hard_gates": {
            "no_live_send_to_leads": True,
            "no_cold_outreach": True,
            "manual_follow_up_only": True,
        },
        "next_action_ar": "افتح /founder-leads.html وابدأ بالـ leads الجديدة",
        "next_action_en": "Open /founder-leads.html and start with the 'new' leads.",
    }


@router.post("/leads/{lead_id}/status")
async def update_lead_status(
    lead_id: str,
    body: dict[str, Any],
) -> dict[str, Any]:
    """Update the status of a single lead (new / contacted /
    qualified / converted / lost). Append-only — original record
    stays intact, status changes are appended to the audit log."""
    from auto_client_acquisition import lead_inbox
    new_status = str(body.get("status") or "").strip()
    try:
        rec = lead_inbox.update_status(lead_id, new_status)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if rec is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="lead_inbox_empty")
    return {"ok": True, "change": rec}
