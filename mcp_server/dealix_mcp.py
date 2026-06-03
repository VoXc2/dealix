"""
Dealix MCP Server — Model Context Protocol interface for Dealix business operations.

Exposes key Dealix capabilities as MCP tools so any MCP client
(Claude Desktop, Claude Code, etc.) can interact directly with the platform.

Run as STDIO server (Claude Desktop / Claude Code):
    python mcp_server/dealix_mcp.py

Run as HTTP server:
    python mcp_server/dealix_mcp.py --transport http --port 8001

Or via FastMCP CLI:
    fastmcp run mcp_server/dealix_mcp.py

Environment variables:
    DEALIX_API_BASE    — FastAPI base URL (default: http://localhost:8000)
    DEALIX_ADMIN_API_KEY — admin key for protected endpoints
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Add repo root to path so dealix.* imports work
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from fastmcp import FastMCP

mcp = FastMCP(
    name="Dealix Business OS",
    instructions=(
        "Dealix is a Saudi B2B Revenue Intelligence platform. "
        "These tools give you direct access to the founder's war room, "
        "KPI snapshots, commercial operations, and business status. "
        "ALL write actions require explicit founder approval — never send "
        "outreach or commit to customers without human confirmation."
    ),
)

# ── helpers ────────────────────────────────────────────────────────────────


def _api_base() -> str:
    return os.getenv("DEALIX_API_BASE", "http://localhost:8000")


def _admin_key() -> str | None:
    return os.getenv("DEALIX_ADMIN_API_KEY")


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str, indent=2)


def _load_yaml_file(path: Path) -> dict[str, Any]:
    try:
        import yaml
        if not path.exists():
            return {}
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _load_json_file(path: Path) -> Any:
    try:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ── read tools ─────────────────────────────────────────────────────────────


@mcp.tool
def get_war_room_today() -> str:
    """
    Returns today's War Room snapshot: top 10 P0 leads with their outreach status,
    pain hypothesis, next action, and urgency. Read-only — requires no approval.
    """
    try:
        from dealix.commercial_ops.targeting_csv import build_war_room_today
        from dealix.commercial_ops.paths import REPO_ROOT

        leads = build_war_room_today(top_n=10)
        result = {
            "date": datetime.now(UTC).date().isoformat(),
            "p0_leads": leads,
            "count": len(leads),
            "note_ar": "War Room — قراءة فقط. أي إرسال يحتاج موافقة صريحة.",
        }
        return _safe_json(result)
    except Exception as exc:
        return _safe_json({"error": str(exc), "hint": "Run 'bash scripts/run_founder_commercial_day.sh' first"})


@mcp.tool
def get_kpi_snapshot() -> str:
    """
    Returns the current KPI snapshot across platform + commercial dimensions.
    Commercial KPIs show 'pending' until the founder imports real CRM numbers.
    Never invents values — reads from kpi_baselines.yaml and kpi_founder_commercial_import.yaml only.
    """
    try:
        from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
        status = load_kpi_commercial_status()
        return _safe_json(status)
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_business_now() -> str:
    """
    Returns the 8-pillar Business NOW snapshot: commercial, GTM, delivery, product,
    compliance, finance, team, platform. Reads from repo truth — no invented CRM numbers.
    """
    try:
        from dealix.business_now.snapshot_builder import build_snapshot
        snap = build_snapshot()
        return _safe_json(snap)
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_commercial_strategy() -> str:
    """
    Returns the commercial strategy snapshot: offer ladder (Diagnostic → Sprint 499 →
    Data Pack 1500 → Managed Ops 2999-4999 → Custom AI 5K-25K), GTM motion, focus override.
    """
    try:
        from dealix.business_now.commercial_strategy import build_commercial_strategy_snapshot
        snap = build_commercial_strategy_snapshot()
        return _safe_json(snap)
    except Exception:
        # Fallback: read from cache
        cache_path = _REPO / "dealix" / "transformation" / "business_now_cache.yaml"
        data = _load_yaml_file(cache_path)
        strategy = data.get("commercial_strategy") or data.get("commercial") or {}
        return _safe_json({"commercial_strategy": strategy, "source": "cache"})


@mcp.tool
def get_doctrine_rules() -> str:
    """
    Returns the 11 non-negotiable doctrine rules: no cold WhatsApp, no LinkedIn automation,
    no invented KPIs, proof before upsell, etc. Always check before taking any action.
    """
    try:
        from dealix.commercial_ops.doctrine import NON_NEGOTIABLE_RULES, SOAEN_CHECKLIST_AR
        return _safe_json({
            "non_negotiables": NON_NEGOTIABLE_RULES,
            "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
            "critical": "All external actions require founder approval. No cold outreach.",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_founder_cockpit(mode: str = "morning") -> str:
    """
    Returns the founder's operational cockpit for the day.

    Args:
        mode: One of 'morning', 'evening', 'weekly', 'full'. Default: 'morning'.
    """
    valid_modes = ("morning", "evening", "weekly", "full")
    if mode not in valid_modes:
        mode = "morning"
    try:
        from dealix.commercial_ops.founder_cockpit import build_founder_cockpit
        cockpit = build_founder_cockpit(strongest_ops_mode=mode)
        return _safe_json(cockpit)
    except Exception as exc:
        return _safe_json({"error": str(exc), "mode": mode})


@mcp.tool
def get_expansion_status(abm_top_n: int = 10) -> str:
    """
    Returns GTM expansion status: targeting pool size, ABM wave readiness,
    social queue depth, motion distribution (A/B/C/D).

    Args:
        abm_top_n: Number of top ABM accounts to include (default: 10, max: 30).
    """
    abm_top_n = max(1, min(abm_top_n, 30))
    try:
        from dealix.commercial_ops.expansion_status import build_expansion_status
        snap = build_expansion_status(abm_top_n=abm_top_n)
        return _safe_json(snap)
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_outreach_drafts(n: int = 5) -> str:
    """
    Returns pending outreach drafts waiting for founder approval.
    These are warm intros only — NO cold WhatsApp, NO LinkedIn automation.
    Each draft must be manually approved and sent by the founder.

    Args:
        n: Number of drafts to return (default: 5, max: 20).
    """
    n = max(1, min(n, 20))
    try:
        from dealix.commercial_ops.outreach_drafts import load_outreach_drafts
        drafts = load_outreach_drafts()
        return _safe_json({
            "drafts": drafts[:n],
            "total": len(drafts),
            "approval_required": True,
            "note": "Drafts only — founder must send manually after approval.",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_evidence_summary() -> str:
    """
    Returns commercial evidence summary: number of events by tier
    (estimated / observed / verified / client_confirmed).
    Used to gauge proof pack readiness.
    """
    try:
        from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
        rows = load_evidence_rows()
        counts = count_evidence_events(rows, exclude_placeholders=True)
        return _safe_json({"evidence_counts": counts, "total_rows": len(rows)})
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_commercial_digest() -> str:
    """
    Returns the daily commercial digest: evidence, KPIs, social draft, P0 targets,
    and benchmarks. This is the founder's primary morning brief.
    """
    try:
        from dealix.commercial_ops.digest import build_commercial_digest
        digest = build_commercial_digest()
        # Truncate large nested objects for readability
        for key in ("gtm_stack", "value_plan", "benchmark"):
            digest.pop(key, None)
        return _safe_json(digest)
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_ceo_master_plan_status() -> str:
    """
    Returns the CEO 90-day master plan status: 138 tasks across 30/60/90-day milestones,
    completion percentage, and current phase focus.
    """
    try:
        from dealix.commercial_ops.ceo_master_plan import build_ceo_master_plan_status
        status = build_ceo_master_plan_status()
        return _safe_json(status)
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_platform_kpi_baselines() -> str:
    """
    Returns platform KPI baselines: p99 latency, uptime target, token cost,
    Alembic head status. Never includes invented commercial numbers.
    """
    baselines_path = _REPO / "dealix" / "transformation" / "kpi_baselines.yaml"
    data = _load_yaml_file(baselines_path)
    return _safe_json(data or {"note": "kpi_baselines.yaml not found"})


@mcp.tool
def get_todo_registry() -> str:
    """
    Returns the current task registry with pending, in-progress, and done items.
    Shows what needs to be done across all business dimensions.
    """
    todo_path = _REPO / "dealix" / "transformation" / "todo_registry.yaml"
    data = _load_yaml_file(todo_path)
    return _safe_json(data or {"note": "todo_registry.yaml not found"})


@mcp.tool
def get_risk_register() -> str:
    """
    Returns the current risk register: open risks by severity, owner, and mitigation status.
    """
    risk_path = _REPO / "dealix" / "transformation" / "risk_register.yaml"
    data = _load_yaml_file(risk_path)
    return _safe_json(data or {"note": "risk_register.yaml not found"})


@mcp.tool
def get_targeting_pool(top_n: int = 20, motion: str = "all") -> str:
    """
    Returns the active targeting pool from agency_accounts_seed.csv.
    Read-only — returns warm accounts only, no scraping or cold data.

    Args:
        top_n: Number of accounts to return (default: 20, max: 50).
        motion: Filter by motion A/B/C/D or 'all' (default: 'all').
    """
    top_n = max(1, min(top_n, 50))
    try:
        from dealix.commercial_ops.targeting_csv import load_targets
        targets = load_targets()
        if motion != "all":
            targets = [t for t in targets if (t.get("motion") or "A").upper() == motion.upper()]
        return _safe_json({
            "accounts": targets[:top_n],
            "total_pool": len(targets),
            "motion_filter": motion,
            "source": "agency_accounts_seed.csv (warm list only)",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_social_content_queue(weeks: int = 4) -> str:
    """
    Returns pending social content (LinkedIn posts) from the queue.
    Posts need founder approval before publishing — never auto-posts.

    Args:
        weeks: Number of weeks of content to preview (default: 4, max: 12).
    """
    weeks = max(1, min(weeks, 12))
    try:
        from dealix.commercial_ops.social_queue import load_social_queue
        queue = load_social_queue()
        posts = list(queue.get("posts") or [])[:weeks * 3]
        return _safe_json({
            "posts": posts,
            "total_queued": len(list(queue.get("posts") or [])),
            "cycle_weeks": queue.get("cycle_weeks"),
            "approval_required": True,
            "soaen_check": "Each post needs Source + Owner + Approval + Evidence + Next Action",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_company_policy() -> str:
    """
    Returns the current company policy: auto_send_enabled (always false),
    external_outreach_enabled (always false), approval_required (always true).
    """
    try:
        from dealix.company_brain.policy import CompanyPolicy
        policy = CompanyPolicy.from_env()
        return _safe_json({
            "auto_send_enabled": policy.auto_send_enabled,
            "external_outreach_enabled": policy.external_outreach_enabled,
            "approval_required": policy.approval_required,
            "safe": not policy.auto_send_enabled and not policy.external_outreach_enabled and policy.approval_required,
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def get_war_room_lead_stages() -> str:
    """
    Returns the complete War Room funnel stages and outreach status transitions.
    Shows allowed stage progressions and which events are critical tracking points.
    """
    try:
        from dealix.revenue_ops_autopilot.war_room import OUTREACH_ORDER, CRITICAL_OUTREACH_EVENTS
        return _safe_json({
            "outreach_order": list(OUTREACH_ORDER),
            "critical_events": CRITICAL_OUTREACH_EVENTS,
            "note": "Transitions: not_contacted → message_drafted → approved_to_send → sent_manual → ... → paid",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


# ── write/action tools (all require explicit approval) ────────────────────


@mcp.tool
def draft_warm_intro(
    company_name: str,
    contact_role: str,
    pain_point_ar: str,
    channel: str = "linkedin",
) -> str:
    """
    Generates a warm intro message draft for founder review.
    DOES NOT SEND — creates a draft only. Founder must approve and send manually.
    Only warm contacts are eligible — no cold outreach.

    Args:
        company_name: Target company name (Arabic or English).
        contact_role: Contact's role (e.g. 'مدير تسويق', 'CEO').
        pain_point_ar: Specific pain point in Arabic (max 200 chars).
        channel: 'linkedin' or 'email' (never WhatsApp cold).
    """
    if channel not in ("linkedin", "email"):
        return _safe_json({"error": "channel must be 'linkedin' or 'email'. No cold WhatsApp."})
    if len(pain_point_ar) > 200:
        pain_point_ar = pain_point_ar[:200]

    try:
        from dealix.commercial.warm_intro_generator import generate_warm_intro
        draft = generate_warm_intro(
            company_name=company_name,
            contact_role=contact_role,
            pain_point=pain_point_ar,
            channel=channel,
        )
        return _safe_json({
            "draft": draft,
            "status": "draft_only",
            "approval_required": True,
            "next_step": "Founder reviews and sends manually via /ops/approvals",
            "note": "لا إرسال تلقائي — مسودة للمراجعة فقط",
        })
    except Exception as exc:
        return _safe_json({"error": str(exc)})


@mcp.tool
def run_diagnostic_report(
    company_name: str,
    industry: str,
    data_maturity: str = "low",
    crm_in_use: bool = False,
) -> str:
    """
    Runs a Dealix diagnostic report for a prospect. Returns estimated gaps and
    opportunity areas. Does NOT send anything — for founder review only.

    Args:
        company_name: Prospect company name.
        industry: Industry sector (e.g. 'real_estate', 'retail', 'logistics').
        data_maturity: 'low', 'medium', or 'high'.
        crm_in_use: Whether they have a CRM.
    """
    valid_maturity = ("low", "medium", "high")
    if data_maturity not in valid_maturity:
        data_maturity = "low"

    try:
        from dealix.commercial.diagnostic_engine import run_diagnostic
        result = run_diagnostic(
            company_name=company_name,
            industry=industry,
            data_maturity=data_maturity,
            crm_in_use=crm_in_use,
        )
        return _safe_json({
            **result,
            "approval_required": False,
            "note": "Diagnostic is read-only analysis — no data sent to client yet.",
        })
    except Exception as exc:
        return _safe_json({
            "company": company_name,
            "industry": industry,
            "data_maturity": data_maturity,
            "crm_in_use": crm_in_use,
            "estimated_gaps": [
                "بيانات العملاء غير موحّدة",
                "لا توجد نقاط تسجيل للعملاء المحتملين",
                "تقارير يدوية بدلاً من لوحة KPI تلقائية",
            ],
            "recommended_offer": "Sprint 499 SAR — Revenue Intelligence Sprint (7 days)",
            "error": str(exc),
            "fallback": True,
        })


# ── resource: business overview ────────────────────────────────────────────


@mcp.resource("dealix://business/overview")
def business_overview() -> str:
    """Current Dealix business overview — offers, pricing, and GTM focus."""
    return """# Dealix — Saudi B2B Revenue Intelligence Platform

## Offer Ladder (5 rungs)
1. **Free Diagnostic** — 10-minute risk score + gaps report
2. **Revenue Intelligence Sprint** — 499 SAR, 7 days, full data analysis
3. **Data Pack** — 1,500 SAR, clean data + scoring model
4. **Managed RevOps** — 2,999–4,999 SAR/month, ongoing ops
5. **Custom AI** — 5,000–25,000 SAR, bespoke AI workflows

## GTM Focus (Saudi B2B)
- Primary: agencies (marketing/digital/PR) with 5–50 employees
- Pain: manual pipelines, no CRM discipline, lost leads
- PDPL compliant — warm outreach only, consent-first

## Non-Negotiables
- No cold WhatsApp, no LinkedIn automation
- No invented KPIs or revenue claims
- Proof before upsell, evidence before growth
- All external actions: founder approval required

## Key Metrics (live from kpi_baselines.yaml)
Run `get_kpi_snapshot()` for current values.
"""


@mcp.resource("dealix://doctrine/non-negotiables")
def doctrine_resource() -> str:
    """The 11 Dealix doctrine rules — always consult before any action."""
    try:
        from dealix.commercial_ops.doctrine import NON_NEGOTIABLE_RULES
        lines = [f"- **{r['id']}**: {r['ar']}" for r in NON_NEGOTIABLE_RULES]
        return "# Dealix Non-Negotiables\n\n" + "\n".join(lines)
    except Exception:
        return "# Dealix Non-Negotiables\n\nLoad error — run get_doctrine_rules() tool instead."


# ── prompt templates ────────────────────────────────────────────────────────


@mcp.prompt
def morning_briefing() -> str:
    """Generate a structured morning briefing prompt for the founder."""
    return """You are the Dealix Company Brain helping the founder start the day.

Use the following tools in order:
1. get_doctrine_rules() — confirm rules are active
2. get_company_policy() — verify safe mode
3. get_war_room_today() — see today's P0 leads
4. get_commercial_digest() — get full morning brief
5. get_kpi_snapshot() — check current metrics
6. get_social_content_queue(weeks=1) — see today's content

Then provide a structured Arabic summary:
- 3 most important P0 leads and their next action
- Evidence count by tier
- One content draft ready for review
- Any blocking issues

Remember: Draft only, no sending, founder approves everything."""


@mcp.prompt
def lead_analysis(company_name: str, context: str = "") -> str:
    """Generate a lead analysis prompt for a specific company."""
    return f"""Analyze this prospect for Dealix outreach qualification:

Company: {company_name}
Context: {context or "No additional context provided"}

Steps:
1. get_doctrine_rules() — check non-negotiables apply
2. get_targeting_pool() — see if they're in the warm pool
3. run_diagnostic_report(company_name="{company_name}", industry="unknown") — generate diagnostic
4. draft_warm_intro(company_name="{company_name}", ...) — create draft if qualified

Qualification criteria:
- Saudi B2B company
- 5–200 employees
- Digital/marketing/ops team exists
- Warm connection or inbound signal preferred

Output: qualification verdict (A/B/C/D) + recommended offer + draft message for approval."""


# ── entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dealix MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP transport")
    parser.add_argument("--port", type=int, default=8001, help="Port for HTTP transport")
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run()
    elif args.transport in ("http", "sse"):
        mcp.run(transport=args.transport, host=args.host, port=args.port)
