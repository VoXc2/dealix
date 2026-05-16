#!/usr/bin/env python3
"""Founder one-command status terminal.

Prints a 30-line bilingual snapshot of the system: service activation
counts, reliability matrix, top 3 actions today, weekly scorecard,
review-pending decisions, live-gate status, founder decision pack
queue. Read-only — never mutates anything.

Usage:
    python scripts/dealix_status.py
    python scripts/dealix_status.py --json   # machine-readable

Exit code is always 0; this is diagnostics, not a CI gate. The
terminal output is bilingual (Arabic primary line + English label).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Make the repo importable when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO_ROOT = Path(__file__).resolve().parents[1]


def _safe(fn, default):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001
        return {"_error": f"{type(exc).__name__}: {exc}", "_default": default}


def _service_counts() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import (  # noqa: WPS433
        service_activation_matrix,
    )
    return service_activation_matrix.counts()


def _health_matrix() -> dict[str, Any]:
    from auto_client_acquisition.reliability_os import build_health_matrix
    return build_health_matrix()


def _daily_loop() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    return daily_growth_loop.build_today()


def _weekly_scorecard() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard
    return weekly_growth_scorecard.build_scorecard()


def _review_pending_count() -> int:
    """Count REVIEW_PENDING entries in the forbidden-claims allowlist."""
    test_file = REPO_ROOT / "tests" / "test_landing_forbidden_claims.py"
    if not test_file.exists():
        return -1
    txt = test_file.read_text(encoding="utf-8")
    # Count only allowlist reason assignments, not comments/assertions.
    return len(re.findall(r':\s*"REVIEW_PENDING"', txt))


def _open_founder_decisions() -> int:
    """Count unchecked ☐ items in the Decision Pack."""
    pack = REPO_ROOT / "docs" / "EXECUTIVE_DECISION_PACK.md"
    if not pack.exists():
        return -1
    txt = pack.read_text(encoding="utf-8")
    # Count "Options:" lines and check whether any ☑ appears for that
    # decision. Simpler proxy: count "☐" minus "☑" — in the v1 pack
    # all 10 decisions are unchecked.
    unchecked = txt.count("☐")
    checked = txt.count("☑")
    # Each decision has 3 options (3 ☐) but only one is meant to be
    # picked. Approximate "open" = decisions with zero ☑.
    decisions_total = 10
    decisions_signed = checked  # heuristic: any tick on a decision row
    return max(0, decisions_total - min(decisions_signed, decisions_total))


def _live_gate_status() -> dict[str, str]:
    """Status of the four live-action gates. All should be BLOCKED."""
    out: dict[str, str] = {}

    # 1. Live charge — finance_os
    try:
        from auto_client_acquisition.finance_os import is_live_charge_allowed
        live = is_live_charge_allowed()
        out["live_charge"] = "BLOCKED" if not live.get("allowed") else "ALLOWED"
    except Exception as exc:  # noqa: BLE001
        out["live_charge"] = f"UNKNOWN ({type(exc).__name__})"

    # 2. WhatsApp live send — settings flag
    try:
        from core.config.settings import get_settings
        settings = get_settings()
        flag = getattr(settings, "whatsapp_allow_live_send", False)
        out["whatsapp_live_send"] = "BLOCKED" if not flag else "ALLOWED"
    except Exception as exc:  # noqa: BLE001
        out["whatsapp_live_send"] = f"UNKNOWN ({type(exc).__name__})"

    # 3. Email live send — no flag exists, so always BLOCKED
    out["email_live_send"] = "BLOCKED (no flag exists by design)"

    # 4. LinkedIn automation / scraping — agent_governance forbids
    try:
        from auto_client_acquisition.agent_governance import (
            FORBIDDEN_TOOLS,
            ToolCategory,
        )
        forbidden_ok = (
            ToolCategory.LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS
            and ToolCategory.SCRAPE_WEB in FORBIDDEN_TOOLS
        )
        out["linkedin_and_scraping"] = (
            "BLOCKED" if forbidden_ok else "MISCONFIGURED"
        )
    except Exception as exc:  # noqa: BLE001
        out["linkedin_and_scraping"] = f"UNKNOWN ({type(exc).__name__})"

    return out


def _build_status_payload() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "services": _safe(_service_counts, default={}),
        "reliability": _safe(_health_matrix, default={}),
        "daily_loop": _safe(_daily_loop, default={}),
        "weekly_scorecard": _safe(_weekly_scorecard, default={}),
        "review_pending_count": _review_pending_count(),
        "open_founder_decisions": _open_founder_decisions(),
        "live_gates": _live_gate_status(),
    }


# ─────────────────────────── rendering ────────────────────────────


def _line(prefix: str, value: str) -> str:
    return f"{prefix:<28} │ {value}"


def render_text(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("═══════════════════════════════════════════════════════════════")
    lines.append(" Dealix — Founder Status / حالة المنصّة")
    lines.append(f" generated_at: {payload['generated_at']}")
    lines.append("═══════════════════════════════════════════════════════════════")

    # Services
    lines.append("")
    lines.append(" خدمات التفعيل / Service Activation")
    lines.append("───────────────────────────────────────────────────────────────")
    svc = payload["services"] if isinstance(payload["services"], dict) else {}
    if "_error" in svc:
        lines.append(_line("services", f"ERROR — {svc['_error']}"))
    else:
        for k in ("total", "live", "pilot", "partial", "target"):
            lines.append(_line(f"  {k}", str(svc.get(k, "—"))))

    # Reliability
    lines.append("")
    lines.append(" حالة المنظومة / Reliability OS")
    lines.append("───────────────────────────────────────────────────────────────")
    rel = payload["reliability"] if isinstance(payload["reliability"], dict) else {}
    if "_error" in rel:
        lines.append(_line("reliability", f"ERROR — {rel['_error']}"))
    else:
        lines.append(_line("  overall", str(rel.get("overall_status", "—"))))
        for sub in rel.get("subsystems", [])[:9]:
            lines.append(_line(
                f"  {sub.get('name', '?')}",
                str(sub.get("status", "?")),
            ))

    # Daily loop
    lines.append("")
    lines.append(" أبرز قرارات اليوم / Top decisions today")
    lines.append("───────────────────────────────────────────────────────────────")
    loop = payload["daily_loop"] if isinstance(payload["daily_loop"], dict) else {}
    if "_error" in loop:
        lines.append(_line("daily_loop", f"ERROR — {loop['_error']}"))
    else:
        decisions = loop.get("decisions") or []
        if not decisions:
            lines.append(_line("  decisions", "(no items today)"))
        for i, d in enumerate(decisions[:3], 1):
            title = (
                d.get("title_ar")
                or d.get("title")
                or d.get("title_en")
                or str(d)[:60]
            )
            lines.append(_line(f"  #{i}", str(title)[:60]))

    # Weekly scorecard
    lines.append("")
    lines.append(" نتيجة الأسبوع / Weekly scorecard")
    lines.append("───────────────────────────────────────────────────────────────")
    sc = (
        payload["weekly_scorecard"]
        if isinstance(payload["weekly_scorecard"], dict)
        else {}
    )
    if "_error" in sc:
        lines.append(_line("scorecard", f"ERROR — {sc['_error']}"))
    else:
        for k in (
            "perimeter_pass_rate",
            "services_close_to_promotion",
            "review_pending_items",
            "advisory_seo_gap",
        ):
            if k in sc:
                lines.append(_line(f"  {k}", str(sc[k])))

    # Live gates
    lines.append("")
    lines.append(" بوابات التشغيل الحيّ / Live-action gates")
    lines.append("───────────────────────────────────────────────────────────────")
    for k, v in payload.get("live_gates", {}).items():
        lines.append(_line(f"  {k}", str(v)))

    # Founder queue
    lines.append("")
    lines.append(" قرارات المؤسس / Founder decisions queue")
    lines.append("───────────────────────────────────────────────────────────────")
    lines.append(_line(
        "  review_pending (forbidden-claims)",
        str(payload.get("review_pending_count", "—")),
    ))
    lines.append(_line(
        "  open_decisions (B1-B5 + S1-S5)",
        str(payload.get("open_founder_decisions", "—")),
    ))

    lines.append("")
    lines.append("═══════════════════════════════════════════════════════════════")
    lines.append(" دلائلx — لا إرسال حيّ، لا scraping، لا cold outreach.")
    lines.append(" Dealix — no live sends, no scraping, no cold outreach.")
    lines.append("═══════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix founder status terminal.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of the text dashboard",
    )
    args = parser.parse_args(argv)

    payload = _build_status_payload()
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
