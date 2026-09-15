#!/usr/bin/env python3
"""Generate evidence-only Founder Intelligence without an LLM or network calls."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_CURRENT = Path("/opt/dealix/company-os/founder-os/current")
DEFAULT_GTM = Path("/opt/dealix/control/autonomous-company/gtm")
DEFAULT_REPO = Path("/opt/dealix/workspace/dealix")


def load_required(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"required evidence missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def age_hours(value: str | None, now: datetime) -> float | None:
    parsed = parse_time(value)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return max(0.0, (now - parsed.astimezone(now.tzinfo)).total_seconds() / 3600)


def first_ranked(repo: Path, today: str) -> dict[str, Any]:
    payload = load_optional(repo / "reports" / "probability_revenue_engine" / f"{today}.json", {})
    rows = payload.get("ranked_targets") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not rows:
        return {}
    return sorted((row for row in rows if isinstance(row, dict)), key=lambda row: row.get("rank", 9999))[0]


def build_markdown(*, truth: dict[str, Any], kpi: dict[str, Any], opportunity: dict[str, Any], approvals: list[dict[str, Any]], ranked: dict[str, Any], now: datetime, source_sha: str) -> str:
    economic = truth.get("economic_truth") or {}
    revenue = economic.get("verified_revenue_sar", kpi.get("verified_revenue_sar", 0))
    contacts = economic.get("real_contacts", 0)
    paid_markers = economic.get("paid_pilot_markers", 0)
    verified_pilots = economic.get("verified_paid_pilots", 0)
    relationships = kpi.get("real_relationships", 0)
    pressure = economic.get("generated_pipeline_pressure", "UNKNOWN")
    production_green = opportunity.get("production_green", "UNKNOWN")
    external_send = bool(opportunity.get("external_send_authorized", False))
    top_rows = opportunity.get("top") if isinstance(opportunity.get("top"), list) else []
    fallback_top = top_rows[0] if top_rows and isinstance(top_rows[0], dict) else {}
    top_name = ranked.get("company_name") or fallback_top.get("company") or "UNKNOWN"
    top_stage = ranked.get("commercial_stage") or fallback_top.get("stage") or "UNKNOWN"
    top_next = ranked.get("next_action") or fallback_top.get("next") or "UNKNOWN"
    top_score = ranked.get("evidence_priority", fallback_top.get("score", "UNKNOWN"))
    pending = [item for item in approvals if isinstance(item, dict) and item.get("status") != "EXECUTED"]
    truth_age = age_hours(truth.get("generated_at"), now)
    kpi_age = age_hours(kpi.get("generated_at"), now)
    stale = any(value is None or value > 48 for value in (truth_age, kpi_age))
    approval_lines = []
    for item in pending[:6]:
        approval_lines.append(
            f"- `{item.get('action', 'UNKNOWN')}` → **{item.get('target', 'UNKNOWN')}** | "
            f"status={item.get('status', 'UNKNOWN')} | authority={item.get('authority_required', 'UNKNOWN')}"
        )
    if not approval_lines:
        approval_lines = ["- No pending material approval item is present in the current approval queue."]
    safe_actions = []
    if stale:
        safe_actions.append("- Refresh `LATEST_TRUTH.json` and `ECONOMIC_KPI.json` from canonical internal evidence before using them for new economic claims.")
    if str(production_green).lower() != "true":
        safe_actions.append("- Reconcile source SHA → build identity → running Web/API SHA → health/critical routes → TLS → rollback evidence; do not treat HTTP 200 as release parity.")
    if top_name != "UNKNOWN":
        safe_actions.append(f"- Review and improve the existing **{top_name}** draft/qualification packet internally; keep every send/publish action held behind its exact L5 approval.")
    safe_actions.append("- Continue free diagnostic/discovery/quote preparation only where evidence supports the current commercial stage; do not promote research or markers into relationships, consent, payment, or revenue.")
    truth_age_text = "UNKNOWN" if truth_age is None else f"{truth_age:.1f}h"
    kpi_age_text = "UNKNOWN" if kpi_age is None else f"{kpi_age:.1f}h"
    return f"""# Hermes Founder Intelligence

Generated: {now.isoformat()}
Generator: deterministic_no_agent · external_effect=NONE · source_sha={source_sha}
Evidence freshness: LATEST_TRUTH={truth_age_text} · ECONOMIC_KPI={kpi_age_text}

## TRUTH

- Verified Dealix revenue: **{revenue} SAR**. Verified paid pilots: **{verified_pilots}**. Paid-pilot markers: **{paid_markers}**; markers are not payment evidence.
- Real contacts: **{contacts}**. Canonical economic KPI real relationships: **{relationships}**.
- Generated-pipeline pressure: **{pressure}**. Production Green evidence: **{production_green}**. External send authorized: **{str(external_send).lower()}**.
- Source freshness is **{'STALE' if stale else 'CURRENT'}** under the 48-hour Founder Intelligence threshold; stale evidence is never promoted to current fact without refresh.

## MONEY

- Verified revenue remains **{revenue} SAR** from the current canonical truth/KPI evidence. No quote, marker, prepared send, or pipeline stage is treated as payment.
- Top evidence-ranked commercial target is **{top_name}** at stage **{top_stage}** with evidence priority/score **{top_score}**; this does not by itself prove payment or revenue.

## REAL RELATIONSHIPS

- Canonical KPI reports **{relationships}** real relationships. Opportunity/approval records may show `REAL_INTERACTION`; interaction is not silently upgraded to a verified relationship, consent, or customer state.
- Current top opportunity summary contains **{len(top_rows)}** selected opportunity rows; they remain bounded by their recorded stage and evidence.

## TOP OPPORTUNITY

- **{top_name}** | stage={top_stage} | evidence_priority_or_score={top_score}.
- Recorded next action: `{top_next}`.
- If that action implies send/publish/spend/contract/deploy/DNS/DB/secret mutation, execution remains held for exact action-bound authority.

## APPROVAL NEEDED

{os.linesep.join(approval_lines)}

## BEST SAFE L0-L4 ACTION

{os.linesep.join(safe_actions)}

## LEARNING

- Revenue, payment, relationship, consent, and production truth are kept as separate evidence states; no synthetic promotion is allowed.
- Founder truth freshness is an operational dependency: LATEST_TRUTH age={truth_age_text}, ECONOMIC_KPI age={kpi_age_text}. A stale snapshot can guide refresh work but cannot establish new current commercial facts.
- The highest-value autonomous work is internal evidence reconciliation and customer-specific preparation; material external effects remain fail-closed until their exact approval event exists.
"""


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-dir", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--gtm-dir", type=Path, default=DEFAULT_GTM)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--now")
    parser.add_argument("--source-sha", default=os.environ.get("DEALIX_SOURCE_SHA", "UNKNOWN"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    now = parse_time(args.now) if args.now else datetime.now().astimezone()
    if now is None:
        raise SystemExit("invalid --now")
    truth = load_required(args.current_dir / "LATEST_TRUTH.json")
    kpi = load_required(args.current_dir / "ECONOMIC_KPI.json")
    opportunity = load_optional(args.gtm_dir / "state" / "opportunity-summary.json", {})
    approval_raw = load_optional(args.gtm_dir / "queues" / "material-approval-queue.json", [])
    approvals = approval_raw if isinstance(approval_raw, list) else []
    ranked = first_ranked(args.repo, now.date().isoformat())
    text = build_markdown(truth=truth, kpi=kpi, opportunity=opportunity, approvals=approvals, ranked=ranked, now=now, source_sha=args.source_sha)
    output = args.output or (args.current_dir / "HERMES_FOUNDER_INTELLIGENCE.md")
    if args.dry_run:
        print(text, end="")
        return 0
    atomic_write(output, text)
    print("FOUNDER_INTELLIGENCE=PASS")
    print(f"OUTPUT={output}")
    print("MODE=deterministic_no_agent")
    print("EXTERNAL_EFFECT=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
