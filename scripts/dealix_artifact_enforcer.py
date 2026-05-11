#!/usr/bin/env python3
"""Wave 16 §C2 — Daily Artifact Enforcer CLI.

Surfaces every active service session that has gone 2+ days without a
daily artifact. The founder runs this each morning to know which
delivery sessions are stalled — preventing silent slippage.

Article 4: never auto-sends, never auto-closes a session. Only reports.
Article 8: Article 8 enforced upstream by ``orchestrator.tick()`` —
this CLI just surfaces what the orchestrator already detects.
Article 11: thin wrapper over `service_sessions.orchestrator` +
`service_sessions.store`. Zero new business logic.

Sandbox-safe: in-memory queries only. Output: 1 of 3 formats.

Usage:
    # Founder portfolio view (md):
    python3 scripts/dealix_artifact_enforcer.py

    # Per-customer scope:
    python3 scripts/dealix_artifact_enforcer.py --customer-handle acme-real-estate

    # JSON for piping into WhatsApp Decision Bot:
    python3 scripts/dealix_artifact_enforcer.py --format json

    # Strict mode: exit 1 if ANY overdue session found (cron-friendly)
    python3 scripts/dealix_artifact_enforcer.py --strict
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.service_sessions.orchestrator import (  # noqa: E402
    is_artifact_overdue,
)
from auto_client_acquisition.service_sessions.store import list_sessions  # noqa: E402


def find_overdue_sessions(customer_handle: str | None = None) -> list[dict]:
    """Return list of session dicts where artifact is overdue.

    Each dict has: session_id, customer_handle, service_type, started_at,
    last_artifact_day, days_since_last_artifact.
    """
    sessions = list_sessions(
        customer_handle=customer_handle,
        status="active",
    )
    out: list[dict] = []
    today = datetime.now(UTC).date()
    for s in sessions:
        if not is_artifact_overdue(s):
            continue
        # Compute days since last artifact (best-effort)
        if s.daily_artifacts:
            last_day = max(int(a.get("day_number", 0)) for a in s.daily_artifacts)
        else:
            last_day = 0
        started_at = getattr(s, "started_at", None)
        if started_at is not None:
            if hasattr(started_at, "tzinfo") and started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=UTC)
            days_since_start = (datetime.now(UTC) - started_at).days
        else:
            days_since_start = 0
        out.append({
            "session_id": s.session_id,
            "customer_handle": s.customer_handle,
            "service_type": s.service_type,
            "started_at": started_at.isoformat() if started_at else None,
            "last_artifact_day": last_day,
            "days_since_session_start": days_since_start,
        })
    return out


def render_md(overdue: list[dict], scope_label: str) -> str:
    """Bilingual markdown table — readable in terminal + WhatsApp paste."""
    if not overdue:
        return (
            f"# 🟢 Artifact Enforcer — {scope_label}\n\n"
            "**لا توجد جلسات متأخرة. كل التسليمات على المسار.**\n"
            "_No overdue sessions. All deliveries on track._\n"
        )
    lines = [
        f"# 🔴 Artifact Enforcer — {scope_label}",
        "",
        f"**عدد الجلسات المتأخرة: {len(overdue)}**",
        f"_{len(overdue)} overdue session(s) — daily artifact missing 2+ days._",
        "",
        "| Customer | Session | Service | Last Artifact Day | Days Since Start |",
        "|---|---|---|---:|---:|",
    ]
    for o in overdue:
        lines.append(
            f"| {o['customer_handle']} | "
            f"`{o['session_id']}` | "
            f"{o['service_type']} | "
            f"{o['last_artifact_day']} | "
            f"{o['days_since_session_start']} |"
        )
    lines.extend([
        "",
        "## Today's action",
        "",
        "🇸🇦 **سلِّم Daily Artifact لكل جلسة فوق + سجِّله عبر**:",
        "🇬🇧 **Deliver a daily artifact for each session above + record it via**:",
        "",
        "```python",
        "from auto_client_acquisition.service_sessions.orchestrator import record_artifact",
        "record_artifact(session_id='...', day_number=N, artifact_id='...', status='delivered')",
        "```",
        "",
        "_Article 4: never close a stale session without delivering real work. "
        "Article 8: don't backfill artifacts that didn't happen._",
    ])
    return "\n".join(lines)


def render_one_line(overdue: list[dict]) -> str:
    """Single-line summary for cron logs / WhatsApp."""
    if not overdue:
        return "[OK] artifact_enforcer: 0 overdue sessions"
    handles = ", ".join(sorted({o["customer_handle"] for o in overdue}))
    return f"[ALERT] artifact_enforcer: {len(overdue)} overdue · customers: {handles}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--customer-handle", default=None,
                   help="Per-customer view (None = founder portfolio).")
    p.add_argument("--format", choices=("md", "json", "one-line"), default="md")
    p.add_argument(
        "--strict", action="store_true",
        help="Exit 1 if any overdue session found (cron-friendly).",
    )
    args = p.parse_args()

    overdue = find_overdue_sessions(args.customer_handle)
    scope = args.customer_handle or "FOUNDER PORTFOLIO"

    if args.format == "json":
        print(json.dumps(
            {
                "scope": scope,
                "overdue_count": len(overdue),
                "is_estimate": True,  # Article 8
                "overdue_sessions": overdue,
                "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
            ensure_ascii=False, indent=2,
        ))
    elif args.format == "one-line":
        print(render_one_line(overdue))
    else:
        print(render_md(overdue, scope))

    if args.strict and overdue:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
