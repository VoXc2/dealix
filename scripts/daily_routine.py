#!/usr/bin/env python3
"""Continuous Commercial Routine — Wave 17.

ONE founder-morning command that composes every existing daily script
into a single 15-minute ritual. Reads on phone:

    python scripts/daily_routine.py             # full routine
    python scripts/daily_routine.py --quick     # skip drafts if today's exist
    python scripts/daily_routine.py --json      # machine output for cron logs

Sequence (idempotent — safe to re-run any number of times):
  1. Daily PM brief        → data/daily_brief/YYYY-MM-DD.md
  2. Warm-list drafts      → data/outreach/warm_list_drafts.md
  3. WhatsApp drafts       → data/outreach/whatsapp_drafts.md
  4. Renewal queue check   → in-memory list of SAR-committed renewals due ≤ 7d
  5. Lead-waiting check    → in-memory list of leads waiting > 24h

Emits a single consolidated `data/daily_routine/YYYY-MM-DD.md` with 5
numbered sections + 3 numbered next actions.

NEVER sends external messages. NEVER calls the LLM. Pure composition
over existing modules + scripts. Honors the 11 non-negotiables.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _today_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _run(name: str, cmd: list[str], skip_if_exists: Path | None = None) -> dict:
    """Run a sub-step. Returns {name, status, output_path, skipped}."""
    if skip_if_exists is not None and skip_if_exists.exists():
        return {
            "name": name,
            "status": "skipped",
            "output_path": str(skip_if_exists.relative_to(REPO_ROOT)),
            "reason": "already exists for today",
        }
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        return {
            "name": name,
            "status": "ok" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "stdout_tail": result.stdout.strip().splitlines()[-3:] if result.stdout else [],
            "stderr_tail": result.stderr.strip().splitlines()[-3:] if result.stderr else [],
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": name,
            "status": "error",
            "detail": f"{type(exc).__name__}: {exc}",
        }


def _renewals_due_next_7d() -> list[dict]:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        cutoff = datetime.now(timezone.utc) + timedelta(days=7)
        items: list[dict] = []
        for s in list_due(on_date=cutoff):
            items.append({
                "customer_id": getattr(s, "customer_id", ""),
                "plan": getattr(s, "plan", ""),
                "amount_sar": getattr(s, "amount_sar", 0),
                "cycle": getattr(s, "cycle_count", 0),
            })
        return items
    except Exception:
        return []


def _leads_waiting_over_24h() -> list[dict]:
    try:
        from auto_client_acquisition import lead_inbox
        if not hasattr(lead_inbox, "list_leads"):
            return []
        leads = lead_inbox.list_leads(limit=100)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        items: list[dict] = []
        for r in leads:
            try:
                created = datetime.fromisoformat(r.get("created_at", "") or "")
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if created < cutoff:
                items.append({
                    "id": r.get("id", ""),
                    "company": r.get("company", ""),
                    "sector": r.get("sector", ""),
                    "created_at": created.isoformat(),
                })
        return items
    except Exception:
        return []


def _emit_consolidated_brief(
    routine_id: str,
    sub_results: list[dict],
    renewals: list[dict],
    waiting_leads: list[dict],
) -> Path:
    out_dir = REPO_ROOT / "data" / "daily_routine"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{routine_id}.md"

    today = _today_iso()
    lines: list[str] = []
    lines.append(f"# Dealix Daily Routine — {today}")
    lines.append("")
    lines.append(
        f"_Generated {datetime.now(timezone.utc).isoformat()}._ "
        "Read on phone every morning. Five numbered sections, three numbered next actions."
    )
    lines.append("")

    # Section 1 — Sub-step results
    lines.append("## 1. Morning routine sub-steps · خطوات الروتين الصباحي")
    lines.append("")
    for r in sub_results:
        emoji = {"ok": "✅", "skipped": "🔵", "failed": "🔴", "error": "🔴"}.get(
            r.get("status", "?"), "⚪"
        )
        line = f"- {emoji} **{r['name']}** — `{r.get('status', '?')}`"
        if r.get("output_path"):
            line += f" → `{r['output_path']}`"
        if r.get("reason"):
            line += f" ({r['reason']})"
        lines.append(line)
    lines.append("")

    # Section 2 — Outreach drafts ready
    lines.append("## 2. Outreach drafts ready · مسوّدات للإرسال")
    lines.append("")
    drafts_warm = REPO_ROOT / "data" / "outreach" / "warm_list_drafts.md"
    drafts_wa = REPO_ROOT / "data" / "outreach" / "whatsapp_drafts.md"
    if drafts_warm.exists():
        lines.append(f"- Warm-list drafts: `{drafts_warm.relative_to(REPO_ROOT)}` (LinkedIn / email)")
    else:
        lines.append("- ⚠ Warm-list drafts NOT generated. Fill `data/warm_list.csv` then re-run.")
    if drafts_wa.exists():
        lines.append(f"- WhatsApp drafts: `{drafts_wa.relative_to(REPO_ROOT)}`")
    else:
        lines.append("- ⚠ WhatsApp drafts NOT generated.")
    lines.append("")
    lines.append(
        "_Pick the 5 highest-priority contacts flagged `accept` or "
        "`diagnostic_only`. Send via the channel they prefer. NEVER send "
        "to anyone flagged `reject` or with doctrine violations._"
    )
    lines.append("")

    # Section 3 — Leads waiting > 24h
    lines.append(f"## 3. Leads to reply · ردود مطلوبة ({len(waiting_leads)})")
    lines.append("")
    if waiting_leads:
        for lead in waiting_leads[:5]:
            lines.append(
                f"- **{lead.get('company', '?')}** ({lead.get('sector', '?')}) — "
                f"{lead.get('created_at', '?')[:10]} — open `/founder-leads.html?key=<admin>`"
            )
    else:
        lines.append("- 0 leads waiting > 24h. Continue outbound cadence.")
    lines.append("")

    # Section 4 — Renewal queue
    lines.append(f"## 4. Renewals due next 7d · تجديدات خلال أسبوع ({len(renewals)})")
    lines.append("")
    if renewals:
        sar_committed = sum(int(r.get("amount_sar", 0)) for r in renewals)
        lines.append(
            f"- **{sar_committed:,} SAR committed across {len(renewals)} retainers.** Confirm each:"
        )
        for r in renewals[:10]:
            lines.append(
                f"  - `{r.get('customer_id', '?')}` — {r.get('plan', '?')} — "
                f"{int(r.get('amount_sar', 0)):,} SAR (cycle {r.get('cycle', '?')})"
            )
    else:
        lines.append("- 0 retainers due. Focus on closing new ones.")
    lines.append("")

    # Section 5 — Daily brief reference
    lines.append("## 5. Full PM brief · التقرير الكامل")
    lines.append("")
    pm_brief = REPO_ROOT / "data" / "daily_brief" / f"{today}.md"
    if pm_brief.exists():
        lines.append(f"- Detailed: `{pm_brief.relative_to(REPO_ROOT)}` (friction log + capital review + recommendations)")
    else:
        lines.append("- ⚠ PM brief NOT generated. Run `python scripts/dealix_pm_daily.py`.")
    lines.append("")

    # Top 3 next actions
    lines.append("## Top 3 next actions · أهم 3 إجراءات")
    lines.append("")
    actions: list[str] = []
    if waiting_leads:
        actions.append(f"Reply to {len(waiting_leads)} lead(s) waiting > 24h (Section 3).")
    if renewals:
        sar = sum(int(r.get("amount_sar", 0)) for r in renewals)
        actions.append(f"Confirm {len(renewals)} retainer renewal(s) — {sar:,} SAR (Section 4).")
    if drafts_warm.exists() or drafts_wa.exists():
        actions.append("Send 5 outreach messages from today's drafts (Section 2).")
    if not actions:
        actions.append("Quiet day. Publish 1 LinkedIn post + reach out to 2 warm contacts.")
    fallbacks = [
        "Read `docs/THE_DEALIX_PROMISE.md` and pick one paragraph to share with one prospect.",
        "Open `data/anchor_partner_pipeline.json` and book one of the 3 anchor partner calls.",
    ]
    for fb in fallbacks:
        if len(actions) >= 3:
            break
        actions.append(fb)
    for i, a in enumerate(actions[:3], start=1):
        lines.append(f"{i}. {a}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quick", action="store_true",
        help="Skip warm-list / WhatsApp regen if today's drafts already exist.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout instead of human text.")
    args = parser.parse_args()

    today = _today_iso()
    py = sys.executable

    sub_results: list[dict] = []

    # 1. PM daily brief — always runs (cheap; refreshes counts)
    sub_results.append(_run(
        name="dealix_pm_daily",
        cmd=[py, str(REPO_ROOT / "scripts" / "dealix_pm_daily.py")],
    ))

    # 2. Warm-list outreach drafts (skip if --quick AND today's exist)
    warm_path = REPO_ROOT / "data" / "outreach" / "warm_list_drafts.md"
    sub_results.append(_run(
        name="warm_list_outreach",
        cmd=[py, str(REPO_ROOT / "scripts" / "warm_list_outreach.py")],
        skip_if_exists=warm_path if args.quick else None,
    ))

    # 3. WhatsApp drafts (same skip rule)
    wa_path = REPO_ROOT / "data" / "outreach" / "whatsapp_drafts.md"
    sub_results.append(_run(
        name="whatsapp_draft",
        cmd=[py, str(REPO_ROOT / "scripts" / "whatsapp_draft.py")],
        skip_if_exists=wa_path if args.quick else None,
    ))

    # 4 + 5. In-process queue reads (cheap)
    renewals = _renewals_due_next_7d()
    waiting_leads = _leads_waiting_over_24h()

    out_path = _emit_consolidated_brief(today, sub_results, renewals, waiting_leads)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "routine_date": today,
        "consolidated_brief": str(out_path.relative_to(REPO_ROOT)),
        "sub_steps": sub_results,
        "renewals_due_next_7d": len(renewals),
        "renewals_sar_committed": sum(int(r.get("amount_sar", 0)) for r in renewals),
        "leads_waiting_over_24h": len(waiting_leads),
        "is_estimate": False,
        "governance_decision": "allow",
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print(f"━━ Dealix Daily Routine — {today} ━━\n")
    for r in sub_results:
        emoji = {"ok": "✅", "skipped": "🔵", "failed": "🔴", "error": "🔴"}.get(
            r.get("status", "?"), "⚪"
        )
        print(f"  {emoji} {r['name']}: {r.get('status', '?')}")
    print()
    print(f"Renewals due next 7d: {len(renewals)} ({summary['renewals_sar_committed']:,} SAR)")
    print(f"Leads waiting > 24h: {len(waiting_leads)}")
    print()
    print(f"✓ Consolidated brief: {out_path.relative_to(REPO_ROOT)}")
    print()
    print("Next: open the brief on phone and complete the 3 numbered next actions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
