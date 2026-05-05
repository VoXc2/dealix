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
    except BaseException as exc:  # noqa: BLE001 — never crash the dashboard
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
    except BaseException as exc:  # noqa: BLE001
        out["live_charge"] = f"UNKNOWN ({type(exc).__name__})"

    # 2. WhatsApp live send — settings flag
    try:
        from core.config.settings import get_settings
        flag = getattr(get_settings(), "whatsapp_allow_live_send", False)
        out["whatsapp_live_send"] = "BLOCKED" if not flag else "ALLOWED"
    except BaseException as exc:  # noqa: BLE001
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
    except BaseException as exc:  # noqa: BLE001
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
        # cells[1]=slot, cells[2]=company placeholder, ... col mapping:
        # 1 slot, 2 company, 3 source, 4 consent, 5 segment, 6 problem,
        # 7 diagnostic_status, 8 pilot_status, 9 proof_status, 10 next, 11 owner
        def _col(i: int) -> str:
            return cells[i] if i < len(cells) else ""

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
        "endpoints": ["/dashboard"],
    }


@router.get("/dashboard")
async def dashboard() -> dict:
    """Single bilingual snapshot of the entire v5 stack.

    Read-only. Never sends, never charges, never writes. Safe to
    call from a phone. Composes:

      - service_activation_matrix.counts()
      - reliability_os.build_health_matrix() (trimmed)
      - finance_os.is_live_charge_allowed() + 3 other live gates
      - daily_growth_loop.build_today() (top 3 only)
      - weekly_growth_scorecard
      - role_command_os CEO brief (top 3 decisions only)
    """
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "لوحة المؤسس — Dealix",
        "title_en": "Founder Dashboard — Dealix",
        "services": _safe(_service_counts, default={}),
        "reliability": _safe(_reliability, default={}),
        "live_gates": _live_gates(),  # never errors — internally wrapped
        "daily_loop": _safe(_daily_loop_summary, default={}),
        "weekly_scorecard": _safe(_weekly_summary, default={}),
        "ceo_brief": _safe(_ceo_brief_top, default={}),
        "first_3_customers": _safe(_first_3_customers, default={}),
        "pending_approvals": _safe(_pending_approvals, default={"count": 0, "first_3": []}),
        "unsafe_blocks": _safe(_unsafe_blocks, default={"count": 0, "names": []}),
        "next_founder_action": _safe(_next_founder_action, default="no_action_today"),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }
