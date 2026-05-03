#!/usr/bin/env python3
"""
Dealix Founder CLI — daily companion in one command.

Replaces 6 separate API calls + spreadsheets with a single 30-second
terminal view every morning.

Commands:
    dealix today                    Founder daily summary (CEO brief + KPIs + incidents)
    dealix standup                  60-second daily standup: today's queue + stale + wins
    dealix prospects add            Add a prospect (interactive)
    dealix prospects list           List prospects (--status / --due-hours filters)
    dealix prospects advance <id>   Move prospect status forward (auto-emits RWU)
    dealix funnel                   Show prospects funnel (count + expected SAR per stage)
    dealix invoice <amount> <cust>  Create a payment-link invoice (Moyasar or manual fallback)
    dealix smoke                    Run staging_smoke against $DEALIX_BASE_URL
    dealix seed                     Run seed_commercial_demo against current DB
    dealix proof <customer_id>      Fetch and pretty-print a customer's Proof Pack
    dealix outreach pick [N]        Pick next N (default 5) outreach messages
    dealix run-window <window>      Trigger one daily-ops window (morning/midday/closing/scorecard)
    dealix gates                    Print all 8 live-action gates + their status
    dealix activate-payments        Print exact env-var changes to flip Moyasar live charge
    dealix first-customer-flow      End-to-end demo: prospect→pilot→invoice→Proof Pack
    dealix approvals                List + interactively approve/reject pending actions
    dealix workspace <cus_id>       Print customer workspace
    dealix brain <cus_id>           Print Company Brain (12 fields + proof_summary)
    dealix learning weekly          Show this week's learning report
    dealix forecast [days]          Phase 5: 30-day MRR projection (default horizon=30)
    dealix benchmarks [sector]      Phase 5: sector-aggregated KPIs
    dealix smart-launch             🚀 9 AM founder ritual — primes today's day
    dealix verify                   Run full_acceptance.sh + 6-layer audit
    dealix help                     Show this text

Configuration:
    DEALIX_BASE_URL                 Required for all commands except 'help'/'outreach pick'
                                    (default: http://127.0.0.1:8000)

Examples:
    DEALIX_BASE_URL=https://app.dealix.me dealix today
    DEALIX_BASE_URL=http://localhost:8000 dealix smoke
    dealix outreach pick 5

Install (optional):
    chmod +x scripts/dealix_cli.py
    sudo ln -s "$(pwd)/scripts/dealix_cli.py" /usr/local/bin/dealix
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


# ── ANSI helpers ─────────────────────────────────────────────────


def _is_tty() -> bool:
    return sys.stdout.isatty()


def _c(text: str, color: str) -> str:
    if not _is_tty():
        return text
    codes = {"red": 31, "green": 32, "yellow": 33, "blue": 34, "magenta": 35, "cyan": 36, "bold": 1, "dim": 2, "reset": 0}
    c = codes.get(color, 0)
    return f"\033[{c}m{text}\033[0m"


def _hdr(text: str) -> str:
    bar = "═" * 60
    return f"\n{_c(bar, 'cyan')}\n  {_c(text, 'bold')}\n{_c(bar, 'cyan')}"


def _kv(k: str, v: Any, *, color: str = "reset") -> str:
    return f"  {_c(k, 'dim'):24s}  {_c(str(v), color)}"


# ── HTTP fetch ───────────────────────────────────────────────────


def _base_url() -> str:
    return os.environ.get("DEALIX_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def _fetch(path: str, *, method: str = "GET", json_body: Any = None) -> dict[str, Any] | None:
    """Lightweight stdlib HTTP — avoid extra deps for the CLI."""
    import json
    import urllib.error
    import urllib.request

    url = _base_url() + path
    data = None
    headers = {"Accept": "application/json"}
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        try:
            return {"_status": exc.code, "_body": (json.loads(body) if body else None)}
        except Exception:
            return {"_status": exc.code, "_body": body}
    except Exception as exc:  # noqa: BLE001
        return {"_error": str(exc)}


# ── Commands ─────────────────────────────────────────────────────


def cmd_today(_args) -> int:
    data = _fetch("/api/v1/founder/today?days=7")
    if not data or "_error" in data:
        print(_c(f"✗ failed to reach {_base_url()}: {data}", "red"))
        return 1

    print(_hdr(f"DEALIX · TODAY · {data.get('as_of', '')[:16]}"))

    # CEO brief summary
    ceo = data.get("ceo_brief") or {}
    decisions = ceo.get("top_decisions") or []
    print(f"\n{_c('🟢 CEO BRIEF', 'green')}")
    print(_kv("today's decisions", len(decisions)))
    for i, d in enumerate(decisions[:3], 1):
        title = d.get("title_ar") or d.get("title") or "(no title)"
        print(f"    {_c(str(i) + '.', 'bold')}  {title}")

    # KPIs
    k = data.get("kpis") or {}
    invariant_ok = k.get("no_unsafe_action_executed_invariant", True)
    print(f"\n{_c('📊 KPIs (7-day window)', 'green')}")
    print(_kv("active subscriptions", k.get("active_paying_subscriptions", 0)))
    print(_kv("current MRR (SAR)", f"{k.get('current_mrr_sar', 0):,.2f}", color="green"))
    print(_kv("annual run rate", f"{k.get('annual_run_rate_sar', 0):,.0f} SAR"))
    print(_kv("proof events emitted", k.get("proof_events_emitted", 0)))
    print(_kv("unsafe blocked", k.get("unsafe_actions_blocked", 0)))
    print(_kv(
        "unsafe-execution invariant",
        "✓ holds" if invariant_ok else "✗ VIOLATED",
        color="green" if invariant_ok else "red",
    ))

    # Quality
    q = data.get("quality") or {}
    print(f"\n{_c('✨ Quality', 'green')}")
    print(_kv("draft acceptance rate", f"{q.get('draft_acceptance_rate', 0) * 100:.1f}%"))
    print(_kv("override rate", f"{q.get('override_rate', 0) * 100:.1f}%"))
    print(_kv("complaint rate", f"{q.get('complaint_rate', 0) * 100:.1f}%"))

    # Cost
    c = data.get("cost") or {}
    print(f"\n{_c('💸 AI Cost (7-day)', 'green')}")
    print(_kv("total (SAR)", f"{c.get('total_sar', 0):,.2f}"))
    print(_kv("agent runs", c.get("run_count", 0)))
    print(_kv("avg latency", f"{c.get('avg_latency_ms', 0):,.0f} ms"))
    print(_kv("error rate", f"{c.get('error_rate', 0) * 100:.1f}%"))

    # Incidents
    incs = data.get("open_incidents") or []
    if incs:
        print(f"\n{_c('⚠ Open Incidents', 'red')}")
        for inc in incs:
            print(f"  {_c(inc['priority'], 'red')}  {inc['ticket_id']} · {inc['subject']} · {inc['age_hours']}h")
    else:
        print(f"\n{_c('✓ No open P0/P1 incidents', 'green')}")

    # Recent ops
    ops = data.get("recent_daily_ops") or []
    if ops:
        print(f"\n{_c('🕐 Recent Daily-Ops Runs', 'green')}")
        for r in ops[:4]:
            t = (r.get("started_at") or "")[11:16]
            print(f"    {t}  {r.get('window', ''):12s}  decisions={r.get('decisions', 0)}  "
                  f"refusals={r.get('risks_blocked', 0)}")

    # Gates
    pol = (data.get("policy") or {}).get("live_action_gates") or {}
    flipped = [k for k, v in pol.items() if v]
    print(f"\n{_c('🛡 Live-Action Gates', 'green')}")
    print(_kv("8 gates", "all FALSE ✓" if not flipped else f"⚠ FLIPPED: {flipped}",
              color="green" if not flipped else "red"))

    # Next actions
    actions = data.get("next_morning_actions_ar") or []
    if actions:
        print(f"\n{_c('🎯 Next Morning Actions', 'green')}")
        for i, a in enumerate(actions, 1):
            print(f"    {i}. {a}")

    print(_c("\n" + "═" * 60, "cyan"))
    return 0


def cmd_smoke(_args) -> int:
    base = _base_url()
    print(_c(f"→ smoking {base}", "blue"))
    try:
        from scripts.staging_smoke import render, run_smoke
    except ImportError as exc:
        print(_c(f"✗ {exc}", "red"))
        return 2
    report = run_smoke(base)
    print(render(report))
    return 0 if report.passed else 1


def cmd_seed(_args) -> int:
    print(_c(f"→ seeding (DATABASE_URL={os.environ.get('DATABASE_URL', '<not set>')[:50]})", "blue"))
    from scripts.seed_commercial_demo import main as seed_main
    return seed_main()


def cmd_proof(args) -> int:
    cid = args.customer_id
    if not cid:
        print(_c("✗ customer_id required", "red"))
        return 2
    data = _fetch(f"/api/v1/proof-ledger/customer/{cid}/pack")
    if not data or "_error" in data:
        print(_c(f"✗ failed: {data}", "red"))
        return 1
    pack = data.get("pack") or {}
    totals = pack.get("totals") or {}
    print(_hdr(f"PROOF PACK · {cid}"))
    print(_kv("event count", data.get("event_count", 0)))
    print(_kv("created units", totals.get("created_units", 0)))
    print(_kv("protected units", totals.get("protected_units", 0)))
    print(_kv("approvals collected", totals.get("approvals_collected", 0)))
    print(_kv("pending approvals", totals.get("pending_approvals", 0)))
    print(_kv("revenue impact (SAR)",
              f"{totals.get('estimated_revenue_impact_sar', 0):,.2f}",
              color="green"))
    print(f"\n{_c('Next recommended action:', 'cyan')}")
    print(f"  {pack.get('next_recommended_action_ar', '—')}")
    return 0


def cmd_outreach(args) -> int:
    n = int(getattr(args, "n", None) or 5)
    msgs_path = REPO / "docs" / "READY_OUTREACH_MESSAGES.md"
    if not msgs_path.exists():
        print(_c(f"✗ {msgs_path} missing", "red"))
        return 2
    text = msgs_path.read_text(encoding="utf-8")
    # Find all "### Msg NN — ..." headers
    headers = re.findall(r"^### (Msg \d{2}.*)$", text, re.MULTILINE)
    if not headers:
        print(_c("✗ no Msg headers found", "red"))
        return 2

    # Stateful pick: rotate based on a tiny pointer file in /tmp
    state = Path("/tmp/dealix_outreach.cursor")
    cursor = 0
    if state.exists():
        try:
            cursor = int(state.read_text().strip()) % len(headers)
        except Exception:
            cursor = 0
    picked = []
    for i in range(n):
        picked.append(headers[(cursor + i) % len(headers)])
    state.write_text(str((cursor + n) % len(headers)))

    print(_hdr(f"OUTREACH · next {n} (cursor={cursor}/{len(headers)})"))
    for i, h in enumerate(picked, 1):
        print(f"  {i}. {_c(h, 'bold')}")
    print(_c(f"\n📂 open docs/READY_OUTREACH_MESSAGES.md → copy each → edit [الاسم] → send manually.", "dim"))
    return 0


def cmd_run_window(args) -> int:
    win = args.window
    valid = {"morning", "midday", "closing", "scorecard"}
    if win not in valid:
        print(_c(f"✗ window must be one of {valid}", "red"))
        return 2
    data = _fetch("/api/v1/daily-ops/run", method="POST", json_body={"window": win})
    if not data or "_error" in data:
        print(_c(f"✗ failed: {data}", "red"))
        return 1
    print(_c(f"✓ {win}: run_id={data.get('run_id', '?')} · "
             f"decisions={data.get('decisions_total', 0)} · "
             f"refusals={data.get('risks_blocked_total', 0)}", "green"))
    return 0


def cmd_gates(_args) -> int:
    data = _fetch("/api/v1/founder/today")
    if not data or "_error" in data:
        # Fallback: read from local settings
        try:
            from core.config.settings import Settings
            s = Settings()
            gates = {
                g: bool(getattr(s, g, False))
                for g in (
                    "whatsapp_allow_live_send", "gmail_allow_live_send",
                    "moyasar_allow_live_charge", "linkedin_allow_auto_dm",
                    "resend_allow_live_send", "whatsapp_allow_internal_send",
                    "whatsapp_allow_customer_send", "calls_allow_live_dial",
                )
            }
        except Exception as exc:
            print(_c(f"✗ {exc}", "red"))
            return 1
    else:
        gates = (data.get("policy") or {}).get("live_action_gates") or {}
    print(_hdr("LIVE-ACTION GATES (8)"))
    for k, v in gates.items():
        flag = _c("FALSE ✓", "green") if not v else _c("TRUE ⚠", "red")
        print(f"  {k:36s}  {flag}")
    if all(not v for v in gates.values()):
        print(_c("\n✓ All 8 gates FALSE — invariant holds.", "green"))
    else:
        print(_c("\n⚠ Some gates flipped — verify intent + commit history.", "red"))
    return 0


# ── Standup / prospects / invoice / activate-payments ────────────


def cmd_standup(_args) -> int:
    """60-second morning routine — today's queue + stale + wins + funnel."""
    data = _fetch("/api/v1/prospects/standup")
    if not data or "_error" in data:
        print(_c("✗ Could not reach /api/v1/prospects/standup", "red"))
        print(_c(f"  base_url={_base_url()}", "dim"))
        return 1

    print(_hdr("DAILY STANDUP — " + str(data.get("as_of", ""))[:10]))

    funnel = data.get("funnel") or {}
    if funnel:
        ladder = ("identified", "messaged", "replied", "meeting", "pilot",
                  "closed_won", "closed_lost")
        line = "  ".join(f"{s}:{funnel.get(s, 0)}" for s in ladder)
        print(_c("  Funnel: ", "dim") + line)

    due = data.get("due_today") or []
    print(_kv("due today", len(due), color="yellow" if due else "green"))
    for p in due[:10]:
        nm = (p.get("name") or "")[:30]
        co = (p.get("company") or "")[:25]
        nx = (p.get("next_step_ar") or "")[:50]
        print(f"    {_c('→', 'cyan')} {nm:30s}  {co:25s}  {_c(nx, 'dim')}")

    stale = data.get("stale_messaged") or []
    if stale:
        print(_kv("stale (no reply >3d)", len(stale), color="yellow"))
        for p in stale[:5]:
            print(f"    {_c('⏳', 'yellow')} {(p.get('name') or '')[:30]:30s}  {(p.get('company') or '')[:25]:25s}")

    wins = data.get("wins_yesterday") or []
    if wins:
        print(_kv("WINS yesterday", len(wins), color="green"))
        for p in wins:
            print(f"    {_c('🏆', 'green')} {(p.get('name') or '')[:30]:30s}  +{p.get('expected_value_sar', 0):.0f} SAR")

    advice = data.get("advice_ar") or ""
    if advice:
        print(_c("\n  💡 " + advice, "magenta"))
    return 0


def cmd_prospects(args) -> int:
    sub = (args.subcmd or "list").lower()
    if sub == "add":
        print("اسم الشخص: ", end="", flush=True); name = sys.stdin.readline().strip()
        print("اسم الشركة: ", end="", flush=True); co = sys.stdin.readline().strip()
        print("LinkedIn URL: ", end="", flush=True); li = sys.stdin.readline().strip()
        print("القيمة المتوقعة (SAR، Enter = 499): ", end="", flush=True)
        vraw = sys.stdin.readline().strip()
        try:
            v = float(vraw) if vraw else 499.0
        except ValueError:
            v = 499.0
        print("نوع العلاقة (cold/warm_1st_degree/warm_2nd_degree/referral): ", end="", flush=True)
        rel = sys.stdin.readline().strip() or "warm_1st_degree"
        body = {
            "name": name, "company": co, "linkedin_url": li,
            "expected_value_sar": v, "relationship_type": rel,
            "next_step_ar": "أرسل warm-intro DM",
        }
        out = _fetch("/api/v1/prospects", method="POST", json_body=body)
        if not out or "_error" in out:
            print(_c("✗ failed to create prospect", "red")); return 1
        print(_c(f"✓ created {out.get('id')} — status={out.get('status')}", "green"))
        return 0

    if sub == "list":
        qs = []
        if getattr(args, "status", None):
            qs.append(f"status={args.status}")
        if getattr(args, "due_hours", None):
            qs.append(f"due_by_hours={args.due_hours}")
        path = "/api/v1/prospects" + ("?" + "&".join(qs) if qs else "")
        out = _fetch(path)
        if not out:
            print(_c("✗ failed", "red")); return 1
        rows = out.get("prospects") or []
        print(_hdr(f"PROSPECTS ({out.get('count', 0)})"))
        for p in rows[:30]:
            print(f"  {p.get('id')}  {p.get('status', ''):14s}  {(p.get('name') or '')[:24]:24s}  {(p.get('company') or '')[:24]:24s}  {p.get('expected_value_sar', 0):>6.0f} SAR")
        return 0

    if sub == "advance":
        pid = getattr(args, "prospect_id", None)
        if not pid:
            print(_c("✗ usage: dealix prospects advance <id> [target_status]", "red"))
            return 2
        body: dict[str, Any] = {}
        target = getattr(args, "target", None)
        if target:
            body["target_status"] = target
        out = _fetch(f"/api/v1/prospects/{pid}/advance", method="POST", json_body=body)
        if not out:
            print(_c("✗ failed", "red")); return 1
        rwu = out.get("rwu_emitted") or "—"
        print(_c(f"✓ {pid}: {out.get('from')} → {out.get('to')}  (RWU: {rwu})", "green"))
        return 0

    print(_c(f"unknown prospects subcommand: {sub}", "red"))
    print("  usage: dealix prospects [add|list|advance]")
    return 2


def cmd_funnel(_args) -> int:
    out = _fetch("/api/v1/prospects/funnel")
    if not out:
        print(_c("✗ failed", "red")); return 1
    f = out.get("funnel") or {}
    print(_hdr("PROSPECTS FUNNEL"))
    total_sar = 0.0
    for stage in ("identified", "messaged", "replied", "meeting", "pilot",
                  "closed_won", "closed_lost"):
        d = f.get(stage) or {"count": 0, "expected_value_sar": 0.0}
        sar = d.get("expected_value_sar", 0.0)
        if stage not in ("closed_lost",):
            total_sar += sar
        print(f"  {stage:14s}  count={d.get('count', 0):>3}   expected={sar:>8.0f} SAR")
    print(_c(f"\n  Pipeline value (excl. closed_lost): {total_sar:.0f} SAR", "cyan"))
    return 0


def cmd_invoice(args) -> int:
    body = {
        "amount_sar": float(args.amount),
        "customer_id": args.customer,
        "description_ar": getattr(args, "description", None) or "Pilot Dealix — 7 أيام",
    }
    out = _fetch("/api/v1/payments/invoice", method="POST", json_body=body)
    if not out:
        print(_c("✗ failed to create invoice", "red")); return 1
    print(_hdr("INVOICE CREATED"))
    print(_kv("invoice_id", out.get("invoice_id")))
    print(_kv("amount", f"{out.get('amount_sar', 0):.2f} SAR"))
    print(_kv("mode", out.get("mode"), color="yellow" if out.get("mode") == "manual" else "green"))
    print(_kv("status", out.get("status")))
    print(_c(f"\n  📲 {out.get('instruction_ar', '')}\n", "cyan"))
    print(_c(f"  URL → {out.get('url')}", "bold"))
    return 0


def cmd_first_customer_flow(_args) -> int:
    """End-to-end demo flow — proves the pipeline works from lead to Proof Pack.

    Creates one synthetic prospect, walks them through every stage, generates
    an invoice, confirms payment, and prints the Proof Pack URL. Useful for:
      - Onboarding a new founder/operator
      - Verifying production after deploy
      - Demoing to investors / customers
    """
    import json as _json
    print(_hdr("FIRST-CUSTOMER FLOW — E2E DEMO"))

    # 1. Create prospect
    print(_c("\n[1/8] Creating demo prospect…", "cyan"))
    p = _fetch("/api/v1/prospects", method="POST", json_body={
        "name": "عميل تجريبي",
        "company": "شركة Demo Co",
        "linkedin_url": "https://linkedin.com/in/demo",
        "relationship_type": "warm_1st_degree",
        "expected_value_sar": 499.0,
        "next_step_ar": "warm-intro DM",
    })
    if not p or "id" not in p:
        print(_c("  ✗ failed to create prospect", "red")); return 1
    pid = p["id"]
    print(_c(f"  ✓ prospect_id={pid}", "green"))

    # 2-6. Advance through each stage
    stages = [("messaged", "draft_created"), ("replied", "opportunity_created"),
              ("meeting", "meeting_drafted"), ("pilot", "approval_collected")]
    for i, (target, expected_rwu) in enumerate(stages, start=2):
        print(_c(f"\n[{i}/8] Advancing to '{target}' (expect RWU: {expected_rwu})…", "cyan"))
        a = _fetch(f"/api/v1/prospects/{pid}/advance", method="POST",
                   json_body={"target_status": target})
        if not a or "to" not in a:
            print(_c(f"  ✗ failed: {a}", "red")); return 1
        rwu = a.get("rwu_emitted") or "—"
        print(_c(f"  ✓ {a['from']} → {a['to']}  (RWU: {rwu})", "green"))

    # 7. Invoice 499 SAR
    print(_c(f"\n[6/8] Creating Moyasar invoice 499 SAR…", "cyan"))
    inv = _fetch("/api/v1/payments/invoice", method="POST", json_body={
        "amount_sar": 499.0, "customer_id": pid,
        "description_ar": "Pilot Dealix - 7 أيام (demo)",
    })
    if not inv or "invoice_id" not in inv:
        print(_c("  ✗ failed to create invoice", "red")); return 1
    print(_c(f"  ✓ invoice_id={inv['invoice_id']}  mode={inv.get('mode')}", "green"))
    print(_c(f"  → URL: {inv.get('url')}", "dim"))

    # 8. Confirm paid
    print(_c(f"\n[7/8] Confirming payment received…", "cyan"))
    cf = _fetch("/api/v1/payments/confirm", method="POST", json_body={"invoice_id": inv["invoice_id"]})
    if not cf or cf.get("status") != "paid":
        print(_c(f"  ✗ failed: {cf}", "red")); return 1
    print(_c(f"  ✓ paid_at={cf.get('paid_at')}", "green"))

    # 9. Close won → auto-creates customer
    print(_c(f"\n[8/8] Closing won → auto-creating CustomerRecord…", "cyan"))
    close = _fetch(f"/api/v1/prospects/{pid}/advance", method="POST",
                   json_body={"target_status": "closed_won"})
    if not close:
        print(_c("  ✗ close failed", "red")); return 1
    print(_c(f"  ✓ {close.get('from')} → closed_won  (RWU: {close.get('rwu_emitted')})", "green"))

    # Read Proof Pack
    print(_c("\n[Proof Pack JSON]", "bold"))
    pack = _fetch(f"/api/v1/proof-ledger/customer/{pid}/pack")
    if pack and "pack" in pack:
        totals = pack["pack"].get("totals") or {}
        print(_kv("created units", totals.get("created_units", 0), color="green"))
        print(_kv("revenue impact (SAR)", totals.get("estimated_revenue_impact_sar", 0), color="green"))
        print(_kv("event count", pack.get("event_count", 0)))

    print(_c(f"\n  ✅ FLOW COMPLETE", "green"))
    print(_c(f"  Open Proof Pack HTML: {_base_url()}/api/v1/proof-ledger/customer/{pid}/pack.html", "cyan"))
    print(_c(f"  This was a demo prospect — clean it up: DELETE /prospects/{pid} (TODO)\n", "dim"))
    return 0


def cmd_approvals(_args) -> int:
    """List pending actions + interactively approve/reject."""
    print(_hdr("APPROVAL QUEUE"))
    out = _fetch("/api/v1/actions/pending")
    if not out:
        print(_c("✗ failed to fetch pending actions", "red"))
        return 1
    items = out.get("items") or []
    if not items:
        print(_c("  ✓ inbox zero — no pending approvals", "green"))
        return 0
    print(_kv("pending", len(items), color="yellow"))
    for i, item in enumerate(items, start=1):
        print(_c(f"\n[{i}/{len(items)}] {item.get('label_ar') or item.get('unit_type')}", "bold"))
        print(f"  customer: {item.get('customer_id') or '—'}")
        print(f"  age:      {item.get('age_hours', 0):.1f}h   risk: {item.get('risk_level')}")
        if item.get("revenue_impact_sar"):
            print(f"  revenue:  {item['revenue_impact_sar']:.0f} SAR")
        if item.get("meta", {}).get("draft_text"):
            preview = str(item["meta"]["draft_text"])[:120]
            print(f"  draft:    {_c(preview, 'dim')}")
        print("  [a]pprove  [r]eject  [s]kip  [q]uit")
        try:
            choice = sys.stdin.readline().strip().lower() or "s"
        except (KeyboardInterrupt, EOFError):
            print()
            return 0
        eid = item.get("event_id")
        if choice == "a":
            r = _fetch(f"/api/v1/actions/{eid}/approve", method="POST", json_body={"actor": "founder_cli"})
            print(_c(f"  ✓ approved → {r.get('status') if r else '?'}", "green"))
        elif choice == "r":
            print("  reason: ", end="", flush=True)
            reason = sys.stdin.readline().strip() or "rejected_via_cli"
            r = _fetch(f"/api/v1/actions/{eid}/reject", method="POST", json_body={"actor": "founder_cli", "reason": reason})
            print(_c(f"  ✗ rejected → {r.get('status') if r else '?'}", "yellow"))
        elif choice == "q":
            return 0
        else:
            print(_c("  ↩ skipped", "dim"))
    return 0


def cmd_workspace(args) -> int:
    cid = getattr(args, "customer_id", None)
    if not cid:
        print(_c("✗ usage: dealix workspace <customer_id>", "red"))
        return 2
    out = _fetch(f"/api/v1/companies/{cid}/workspace")
    if not out:
        print(_c("✗ failed", "red")); return 1
    print(_hdr(f"WORKSPACE — {out.get('company_name') or cid}"))
    sprint = out.get("current_sprint")
    if sprint:
        print(_kv("sprint", f"{sprint.get('service_id')} (day {sprint.get('day')}/{sprint.get('sla_days', 7)})"))
    print(_kv("opportunities", out.get("opportunities_count", 0)))
    print(_kv("drafts", out.get("drafts_count", 0)))
    print(_kv("open decisions", len(out.get("open_decisions") or []), color="yellow" if out.get("open_decisions") else "green"))
    print(_kv("meetings", len(out.get("meetings") or [])))
    print(_kv("invoices", len(out.get("invoices") or [])))
    print(_kv("proof packs", len(out.get("proof_packs") or [])))
    print(_kv("risks blocked", len(out.get("risks_blocked") or [])))
    return 0


def cmd_brain(args) -> int:
    cid = getattr(args, "customer_id", None)
    if not cid:
        print(_c("✗ usage: dealix brain <customer_id>", "red"))
        return 2
    out = _fetch(f"/api/v1/companies/{cid}/brain")
    if not out:
        print(_c("✗ failed", "red")); return 1
    print(_hdr(f"COMPANY BRAIN — {out.get('company_name') or cid}"))
    for k in ("plan", "sector", "city", "offer_ar", "ideal_customer_ar",
              "average_deal_value_sar", "tone_ar", "current_service_id", "churn_risk"):
        if k in out and out[k] not in (None, "", []):
            print(_kv(k, out[k]))
    print(_kv("approved channels", ", ".join(out.get("approved_channels") or [])))
    print(_kv("blocked channels", ", ".join(out.get("blocked_channels") or []), color="yellow"))
    print(_kv("forbidden claims", ", ".join(out.get("forbidden_claims") or []), color="red"))
    ps = out.get("proof_summary") or {}
    print(_kv("proof events", ps.get("events_total", 0)))
    print(_kv("approvals pending", ps.get("approvals_pending", 0),
              color="yellow" if ps.get("approvals_pending") else "green"))
    print(_kv("revenue impact (SAR)", f"{ps.get('estimated_revenue_impact_sar', 0):.0f}", color="green"))
    return 0


def cmd_learning(args) -> int:
    sub = (getattr(args, "subcmd", None) or "weekly").lower()
    if sub != "weekly":
        print(_c(f"unknown learning subcommand: {sub} (only 'weekly' supported)", "red"))
        return 2
    out = _fetch("/api/v1/learning/weekly?days=7")
    if not out:
        print(_c("✗ failed", "red")); return 1
    print(_hdr("WEEKLY LEARNING (last 7 days)"))
    print(_kv("bottleneck", out.get("bottleneck_ar") or "—", color="yellow"))
    print(_kv("next experiment", out.get("next_experiment_ar") or "—", color="green"))
    print(_kv("high-risk blocked", out.get("high_risk_blocked", 0)))
    print(_kv("pending approvals", out.get("pending_approvals", 0), color="yellow"))
    by_unit = out.get("totals_by_unit") or {}
    if by_unit:
        print(_c("\nRWUs this week:", "bold"))
        for k, v in sorted(by_unit.items(), key=lambda x: -x[1])[:8]:
            print(f"  {k:30s}  {v}")
    return 0


def cmd_verify(_args) -> int:
    """Run full_acceptance.sh + 6-layer audit. Wraps the existing script."""
    import subprocess
    print(_hdr("DEALIX VERIFY — 6-layer acceptance"))
    script = REPO / "scripts" / "full_acceptance.sh"
    if not script.exists():
        print(_c("✗ scripts/full_acceptance.sh missing", "red"))
        return 1
    rc = subprocess.call(["bash", str(script)])
    return rc


def cmd_forecast(args) -> int:
    """Phase 5 — 30-day MRR projection."""
    days = getattr(args, "days", 30) or 30
    out = _fetch(f"/api/v1/intelligence/forecast?horizon_days={days}")
    if not out:
        print(_c("✗ failed", "red")); return 1
    print(_hdr(f"FORECAST — horizon {days} days"))
    print(_kv("pipeline (count)", out.get("pipeline_count", 0)))
    print(_kv("pipeline value (SAR)", f"{out.get('pipeline_value_sar', 0):,.0f}"))
    print(_kv("close rate", f"{out.get('expected_close_rate', 0):.2%}", color="cyan"))
    print(_kv("confidence", out.get("expected_close_rate_confidence_ar", "—")))
    print(_kv("projected revenue (SAR)", f"{out.get('projected_revenue_sar', 0):,.0f}", color="green"))
    print(_kv("current MRR (SAR)", f"{out.get('current_mrr_sar', 0):,.0f}"))
    print(_kv("current ARR (SAR)", f"{out.get('current_arr_sar', 0):,.0f}"))
    print(_kv("projected MRR @ horizon", f"{out.get('projected_mrr_at_horizon_sar', 0):,.0f}", color="green"))
    print(_kv("projected ARR @ horizon", f"{out.get('projected_arr_at_horizon_sar', 0):,.0f}", color="green"))
    if out.get("note_ar"):
        print(_c(f"\n  ℹ {out['note_ar']}", "dim"))
    return 0


def cmd_benchmarks(args) -> int:
    sector = getattr(args, "sector", None)
    qs = f"?sector={sector}" if sector else ""
    out = _fetch(f"/api/v1/intelligence/benchmarks{qs}")
    if not out:
        print(_c("✗ failed", "red")); return 1
    print(_hdr(f"BENCHMARKS{(' — ' + sector) if sector else ''}"))
    print(_kv("total customers", out.get("total_customers", 0)))
    print(_kv("sectors analyzed", out.get("sectors_analyzed", 0)))
    if out.get("empty_ar"):
        print(_c(f"\n  {out['empty_ar']}", "yellow"))
        return 0
    for sec in (out.get("sectors") or [])[:8]:
        print(_c(f"\n  ── {sec['sector']} ({sec['sample_quality_ar']}) ──", "bold"))
        print(_kv("  customers", sec.get("customers_count", 0)))
        print(_kv("  avg proof events/customer", sec.get("avg_proof_events_per_customer", 0)))
        atc = sec.get("avg_pilot_days_to_close")
        print(_kv("  avg days to close", f"{atc:.1f}" if atc else "—"))
        for rwu in sec.get("top_rwus", []):
            print(f"    • {rwu['unit_type']:30s} ×{rwu['count']}")
    return 0


def cmd_smart_launch(_args) -> int:
    """🚀 Founder daily ritual — primes the day in one shot.

    Calls /api/v1/founder/digest, prints standup queue + LLM intros +
    best channel + active sprints + approvals + LLM provider status.
    """
    print(_hdr("🚀 SMART LAUNCH — صباح الخير"))
    out = _fetch("/api/v1/founder/digest")
    if not out:
        print(_c("✗ تعذّر الوصول إلى /api/v1/founder/digest", "red"))
        print(_c(f"  base_url={_base_url()}", "dim"))
        return 1

    # ── LLM provider status ──
    llm = out.get("llm") or {}
    providers = llm.get("available_providers") or []
    if providers:
        print(_kv("🧠 LLM providers", ", ".join(providers), color="green"))
    else:
        print(_kv("🧠 LLM providers", "none — fallback path active", color="yellow"))
    print()

    # ── Today's queue ──
    standup = out.get("standup") or {}
    due = standup.get("due_today") or []
    stale = standup.get("stale_messaged") or []
    print(_c("📋 STANDUP", "bold"))
    print(_kv("due today", len(due), color="yellow" if due else "green"))
    for p in due[:6]:
        print(f"   → {(p.get('name') or '')[:24]:24s}  {(p.get('company') or '')[:24]:24s}  {(p.get('next_step_ar') or '')[:40]}")
    if stale:
        print(_kv("stale (>3d)", len(stale), color="yellow"))
    print()

    # ── 3 LLM intros ──
    intros = out.get("intros") or []
    if intros:
        print(_c("✍️  LINKEDIN INTROS (نسخ + الصق + خصّص)", "bold"))
        for i, intro in enumerate(intros, 1):
            llm_tag = "🧠 LLM" if intro.get("llm_used") else "📝 fallback"
            print(_c(f"\n  [{i}] {intro.get('company') or '—'}  ({llm_tag})", "cyan"))
            for line in (intro.get("draft_ar") or "").split("\n")[:6]:
                print(f"      {line}")
        print()

    # ── Best channel ──
    bc = out.get("best_channel")
    if bc:
        print(_c("📡 BEST CHANNEL TODAY", "bold"))
        print(_kv("channel", bc.get("channel", "—"), color="green"))
        print(_kv("score", bc.get("score", 0)))
        print(_kv("reason", (bc.get("reason_ar") or "")[:80]))
        print()

    # ── Active sprints ──
    sprints = out.get("active_sprints") or []
    print(_c("🏃 ACTIVE SPRINTS", "bold"))
    if sprints:
        for s in sprints[:5]:
            print(f"   • {s.get('sprint_id', '')}  customer={s.get('customer_id', '')}  day={s.get('current_day', 0)}/7  status={s.get('status', '')}")
    else:
        print(_c("   (no active sprints — start one with: dealix first-customer-flow)", "dim"))
    print()

    # ── Approvals ──
    appr = out.get("approvals") or {}
    cnt = appr.get("count", 0)
    print(_c("✋ APPROVALS PENDING", "bold"))
    print(_kv("count", cnt, color="yellow" if cnt else "green"))
    for it in (appr.get("top_oldest") or [])[:3]:
        print(f"   • {(it.get('label_ar') or it.get('unit_type'))[:50]:50s}  age={it.get('age_hours', 0):.1f}h")
    print()

    # ── Gates ──
    gates = out.get("live_action_gates") or {}
    all_false = all(not v for v in gates.values()) if gates else True
    if gates:
        flag = _c("8/8 FALSE ✓", "green") if all_false else _c("⚠ check gates!", "red")
        print(_kv("🛡️  Live-action gates", flag))

    # ── Advice ──
    advice = out.get("advice_ar")
    if advice:
        print(_c(f"\n💡 {advice}", "magenta"))

    return 0


def cmd_activate_payments(_args) -> int:
    """Print exact env changes to flip Moyasar live charge — no auto-flip for safety."""
    state = _fetch("/api/v1/payments/state")
    print(_hdr("ACTIVATE LIVE PAYMENTS"))
    if state:
        gates = state.get("gates") or {}
        live = gates.get("live_charge", False)
        ready = state.get("ready_to_flip_live_charge", False)
        secret = state.get("moyasar_secret_configured", False)
        print(_kv("MOYASAR_ALLOW_LIVE_CHARGE", "TRUE ✓" if live else "FALSE", color="green" if live else "yellow"))
        print(_kv("MOYASAR_SECRET_KEY", "configured ✓" if secret else "MISSING", color="green" if secret else "red"))
        print(_kv("ready to flip?", "YES" if ready else "NO — set secret first", color="green" if ready else "red"))

    print(_c("\nSteps:", "bold"))
    print("  1. Complete Moyasar merchant onboarding (KYB + DPA): https://moyasar.com")
    print("  2. railway variables set MOYASAR_SECRET_KEY=sk_live_xxx --service web")
    print("  3. railway variables set MOYASAR_ALLOW_LIVE_CHARGE=true --service web")
    print("  4. After redeploy: dealix invoice 1 cus_demo  (test 1 SAR charge)")
    print("  5. See: docs/MOYASAR_LIVE_CUTOVER.md\n")
    print(_c("⚠ Until done, /api/v1/payments/charge returns 403 — invoices via /invoice work fine.", "yellow"))
    return 0


# ── Main ─────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dealix", description="Dealix Founder CLI")
    sub = parser.add_subparsers(dest="cmd", required=False)

    sub.add_parser("today",   help="Founder daily summary")
    sub.add_parser("standup", help="60s morning standup queue + funnel")
    sub.add_parser("smoke",   help="Smoke test the API")
    sub.add_parser("seed",    help="Seed demo commercial data")
    sub.add_parser("funnel",  help="Show prospects funnel")
    sub.add_parser("activate-payments", help="Print Moyasar live-charge activation steps")
    sub.add_parser("first-customer-flow", help="End-to-end demo: prospect→pilot→invoice→Proof Pack")
    sub.add_parser("approvals", help="Interactive approval queue")
    sub.add_parser("smart-launch", help="🚀 9 AM founder ritual — primes today's day")
    sub.add_parser("verify", help="Run full_acceptance.sh + 6-layer audit")

    p_fc = sub.add_parser("forecast", help="Phase 5 — 30-day MRR projection")
    p_fc.add_argument("days", nargs="?", type=int, default=30)

    p_bm = sub.add_parser("benchmarks", help="Phase 5 — sector-aggregated KPIs")
    p_bm.add_argument("sector", nargs="?", default=None)

    p_ws = sub.add_parser("workspace", help="Print customer workspace")
    p_ws.add_argument("customer_id")

    p_brain = sub.add_parser("brain", help="Print Company Brain")
    p_brain.add_argument("customer_id")

    p_learn = sub.add_parser("learning", help="Show learning report (weekly only for now)")
    p_learn.add_argument("subcmd", nargs="?", default="weekly")

    p_proof = sub.add_parser("proof", help="Fetch a customer's Proof Pack")
    p_proof.add_argument("customer_id")

    p_out = sub.add_parser("outreach", help="Pick next outreach messages")
    p_out.add_argument("subcmd", nargs="?", default="pick")
    p_out.add_argument("n", nargs="?", type=int, default=5)

    p_pros = sub.add_parser("prospects", help="Manage prospects (add/list/advance)")
    p_pros.add_argument("subcmd", nargs="?", default="list")
    p_pros.add_argument("prospect_id", nargs="?")
    p_pros.add_argument("target", nargs="?")
    p_pros.add_argument("--status")
    p_pros.add_argument("--due-hours", type=int, dest="due_hours")

    p_inv = sub.add_parser("invoice", help="Create a payment-link invoice")
    p_inv.add_argument("amount", type=float)
    p_inv.add_argument("customer")
    p_inv.add_argument("description", nargs="?")

    p_run = sub.add_parser("run-window", help="Trigger a daily-ops window")
    p_run.add_argument("window")

    sub.add_parser("gates",  help="Print live-action gates")
    sub.add_parser("help",   help="Show help")

    args = parser.parse_args(argv)
    cmd = args.cmd or "help"

    handlers = {
        "today":              cmd_today,
        "standup":            cmd_standup,
        "smoke":              cmd_smoke,
        "seed":               cmd_seed,
        "proof":              cmd_proof,
        "outreach":           cmd_outreach,
        "prospects":          cmd_prospects,
        "funnel":             cmd_funnel,
        "invoice":            cmd_invoice,
        "activate-payments":  cmd_activate_payments,
        "first-customer-flow": cmd_first_customer_flow,
        "approvals":          cmd_approvals,
        "workspace":          cmd_workspace,
        "brain":              cmd_brain,
        "learning":           cmd_learning,
        "forecast":           cmd_forecast,
        "benchmarks":         cmd_benchmarks,
        "smart-launch":       cmd_smart_launch,
        "verify":             cmd_verify,
        "run-window":         cmd_run_window,
        "gates":              cmd_gates,
        "help":               lambda _a: (parser.print_help(), 0)[1],
    }
    handler = handlers.get(cmd)
    if handler is None:
        parser.print_help()
        return 2
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
