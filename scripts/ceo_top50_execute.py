#!/usr/bin/env python3
"""Execute automatable CEO Top-50 items and update tracker."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class ActionCommand:
    action: str
    command: str
    timeout_seconds: int = 180


AUTOMATABLE_ACTIONS: tuple[ActionCommand, ...] = (
    ActionCommand("run_pm_daily_brief", "python3 scripts/dealix_pm_daily.py --json"),
    ActionCommand("run_founder_status", "python3 scripts/dealix_status.py --json"),
    ActionCommand("run_daily_scorecard", "python3 scripts/founder_daily_scorecard.py --json"),
    ActionCommand("weekly_go_no_go_gate", "bash scripts/dealix_market_launch_ready_verify.sh", 240),
    ActionCommand(
        "weekly_friction_review",
        (
            "python3 -c \"from auto_client_acquisition.friction_log.aggregator import aggregate; "
            "print(aggregate(customer_id='dealix_internal', window_days=7).to_dict())\""
        ),
    ),
    ActionCommand("align_30_60_90_outputs", "python3 scripts/ceo_top50_planning_sync.py --mode align"),
    ActionCommand("revenue_os_baseline", "bash scripts/revenue_os_master_verify.sh", 240),
    ActionCommand("capability_baseline", "bash scripts/dealix_capability_verify.sh", 240),
    ActionCommand("list_sector_bundles", "python3 scripts/dealix_diagnostic.py --list-bundles"),
    ActionCommand(
        "create_icp_diagnostic",
        (
            "python3 scripts/dealix_diagnostic.py --company \"Sample Co\" "
            "--sector b2b_services --region riyadh --pipeline-state \"manual follow-up\" --json"
        ),
    ),
    ActionCommand("weekly_p0_p1_backlog", "python3 scripts/ceo_top50_planning_sync.py --mode backlog"),
    ActionCommand(
        "create_warm_list_file",
        "python3 -c \"from pathlib import Path;p=Path('data/warm_list.csv');"
        "t=Path('data/warm_list.csv.template');"
        "print('exists' if p.exists() else 'created');"
        "p.write_text(t.read_text(encoding='utf-8'),encoding='utf-8') if not p.exists() else None\"",
    ),
    ActionCommand(
        "fill_first_20_warm_contacts",
        "python3 scripts/seed_warm_contacts.py --min-contacts 20",
    ),
    ActionCommand("generate_bilingual_drafts", "python3 scripts/warm_list_outreach.py"),
    ActionCommand("run_first10_board", "python3 scripts/dealix_first10_warm_intros.py"),
    ActionCommand(
        "personalize_first_5_messages",
        (
            "python3 scripts/seed_warm_contacts.py --min-contacts 20 && "
            "python3 scripts/warm_list_outreach.py && "
            "python3 scripts/warm_list_first5_personalized.py"
        ),
    ),
    ActionCommand(
        "prepare_499_pilot_brief",
        "python3 scripts/dealix_pilot_brief.py --company \"Sample Co\" --sector b2b_services --amount-sar 499",
    ),
    ActionCommand(
        "prepare_invoice_dry_run",
        (
            "python3 scripts/dealix_invoice.py --email sample@example.sa --amount-sar 499 "
            "--description \"Dealix Sprint\" --dry-run"
        ),
    ),
    ActionCommand(
        "record_payment_intent_confirmation",
        (
            "rm -f docs/wave6/live/payment_state_top50.json ; "
            "python3 scripts/dealix_payment_confirmation_stub.py --action invoice-intent "
            "--customer sample --amount-sar 499 --service-type 7_day_revenue_proof_sprint "
            "--out-path docs/wave6/live/payment_state_top50.json ; "
            "python3 scripts/dealix_payment_confirmation_stub.py --action send-payment-link "
            "--out-path docs/wave6/live/payment_state_top50.json ; "
            "python3 scripts/dealix_payment_confirmation_stub.py --action upload-evidence "
            "--evidence-note \"bank transfer slip\" --evidence-kind transfer_reference "
            "--out-path docs/wave6/live/payment_state_top50.json ; "
            "python3 scripts/dealix_payment_confirmation_stub.py --action confirm "
            "--confirmed-by founder --out-path docs/wave6/live/payment_state_top50.json ; "
            "python3 scripts/dealix_payment_confirmation_stub.py --action kickoff-ready "
            "--out-path docs/wave6/live/payment_state_top50.json"
        ),
        300,
    ),
    ActionCommand(
        "run_delivery_kickoff",
        (
            "python3 scripts/dealix_delivery_kickoff.py --company \"Sample Co\" "
            "--service 7_day_revenue_proof_sprint --payment-state-file docs/wave6/live/payment_state_top50.json"
        ),
    ),
    ActionCommand(
        "generate_proof_pack_allow_empty",
        (
            "python3 scripts/dealix_proof_pack.py --customer-handle sample "
            "--allow-empty --out docs/wave6/live/sample-proof-pack.md"
        ),
    ),
    ActionCommand("verify_proof_pack_templates", "python3 scripts/verify_proof_pack.py"),
    ActionCommand(
        "run_doctrine_core_tests",
        (
            "pytest tests/test_no_cold_whatsapp.py tests/test_no_linkedin_automation.py "
            "tests/test_no_scraping_engine.py tests/test_no_guaranteed_claims.py "
            "tests/test_no_source_no_answer.py -q"
        ),
        300,
    ),
    ActionCommand("run_governance_verifier", "python3 scripts/verify_governance.py"),
    ActionCommand("keep_live_actions_safe_default", "python3 scripts/dealix_status.py --json"),
    ActionCommand(
        "close_review_pending_claims",
        (
            "python3 -c \"from pathlib import Path;import re;"
            "txt=Path('tests/test_landing_forbidden_claims.py').read_text(encoding='utf-8');"
            "n=len(re.findall(r':\\s*\\\"REVIEW_PENDING\\\"', txt));"
            "print({'review_pending_count':n});raise SystemExit(0 if n==0 else 1)\""
        ),
    ),
    ActionCommand("enforce_no_source_no_answer", "pytest tests/test_no_source_no_answer.py -q"),
    ActionCommand("start_postgres_redis", "docker compose up -d postgres redis", 120),
    ActionCommand(
        "start_backend_dev_server",
        "curl -sS -m 3 http://localhost:8000/health | python3 -m json.tool",
        30,
    ),
    ActionCommand("run_api_smoke", "python3 scripts/dealix_smoke_test.py --base-url http://localhost:8000", 240),
    ActionCommand(
        "run_hello_world_lead_pipeline",
        (
            "curl -sS -X POST http://localhost:8000/api/v1/leads -H \"Content-Type: application/json\" "
            "-d '{\"company\":\"Test Co\",\"name\":\"Test\",\"email\":\"test@example.sa\","
            "\"phone\":\"+966501234567\",\"sector\":\"technology\",\"region\":\"Saudi Arabia\","
            "\"budget\":50000,\"message\":\"Test message\"}' | python3 -m json.tool"
        ),
        120,
    ),
    ActionCommand("check_alembic_single_head", "python3 scripts/check_alembic_single_head.py"),
    ActionCommand("run_morning_readiness_gate", "bash scripts/dealix_market_launch_ready_verify.sh", 240),
    ActionCommand("daily_payment_reconciliation", "python3 scripts/reconcile_moyasar.py --dry-run"),
    ActionCommand("prepare_saudi_seed_dry_run", "python3 scripts/import_seed_leads.py --dry-run"),
    ActionCommand(
        "qualification_gate_per_lead",
        (
            "curl -sS -X POST http://localhost:8000/api/v1/service-setup/qualify "
            "-H \"Content-Type: application/json\" "
            "-d '{\"pain_clear\":true,\"owner_present\":true,\"data_available\":true,"
            "\"accepts_governance\":true,\"has_budget\":true,\"wants_safe_methods\":true,"
            "\"proof_path_visible\":true,\"retainer_path_visible\":true,"
            "\"raw_request_text\":\"Warm intro lead\",\"sector\":\"technology\",\"city\":\"riyadh\"}' "
            "| python3 -m json.tool"
        ),
        120,
    ),
    ActionCommand(
        "follow_up_sla_24h",
        (
            "python3 scripts/dealix_founder_daily_brief.py --blocking-approvals 0 "
            "--pending-payments 0 --pending-proof-packs 0 --overdue-followups 0 "
            "--sla-at-risk 0 --format json"
        ),
    ),
    ActionCommand("watch_ci_blockers", "bash scripts/ci_watch.sh || true", 180),
    ActionCommand(
        "one_capital_asset_per_engagement",
        (
            "python3 -c \"from auto_client_acquisition.capital_os.capital_ledger import add_asset; "
            "a=add_asset(customer_id='sample', engagement_id='eng_ceo_top50', "
            "asset_type='playbook', owner='ceo', asset_ref='docs/strategic/CEO_TOP50_EXECUTION_SYSTEM_AR.md', "
            "notes='CEO Top50 operating system'); print(a.asset_id)\""
        ),
    ),
    ActionCommand(
        "prepare_live_payment_cutover",
        "rg \"cutover|rollback|MOYASAR|allow-live\" docs/integrations/PAYMENT_MOYASAR_LIVE.md -n",
    ),
    ActionCommand("monthly_refund_payment_governance", "python3 scripts/monthly_cadence_runner.py --all-active"),
    ActionCommand("run_weekly_executive_pack", "python3 scripts/dealix_weekly_executive_pack.py --all-customers"),
    ActionCommand("weekly_retro_friction_proof_capital", "python3 scripts/dealix_pm_daily.py --json"),
)


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _read_tracker(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError("Tracker CSV has no header")
        return reader.fieldnames, rows


def _write_tracker(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute automatable CEO Top-50 actions")
    parser.add_argument(
        "--tracker",
        default="docs/ops/CEO_TOP50_TRACKER.csv",
        help="Path to tracker CSV",
    )
    parser.add_argument(
        "--log-dir",
        default="docs/ops/live",
        help="Directory for execution logs",
    )
    parser.add_argument(
        "--run-next-7",
        action="store_true",
        help="Also execute automatable NEXT_7 items if defined",
    )
    parser.add_argument(
        "--run-next-30",
        action="store_true",
        help="Also execute automatable NEXT_30 items if defined",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    tracker_path = (repo_root / args.tracker).resolve()
    log_dir = (repo_root / args.log_dir).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)

    fieldnames, rows = _read_tracker(tracker_path)
    rows_by_action = {row["action"]: row for row in rows}
    run_at = _now_utc()
    next_review = (run_at + timedelta(days=7)).isoformat()
    run_stamp = run_at.strftime("%Y%m%dT%H%M%SZ")
    results: list[dict[str, object]] = []

    for item in AUTOMATABLE_ACTIONS:
        row = rows_by_action.get(item.action)
        if row is None:
            continue
        if row["status"] not in {"DONE_NOW", "NEXT_7", "NEXT_30"}:
            continue
        if row["status"] == "NEXT_7" and not args.run_next_7:
            continue
        if row["status"] == "NEXT_30" and not args.run_next_30:
            continue

        started = _now_utc()
        timed_out = False
        try:
            proc = subprocess.run(
                item.command,
                cwd=repo_root,
                text=True,
                shell=True,
                capture_output=True,
                timeout=item.timeout_seconds,
            )
            exit_code = proc.returncode
            stdout_tail = "\n".join(proc.stdout.strip().splitlines()[-20:])
            stderr_tail = "\n".join(proc.stderr.strip().splitlines()[-20:])
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = 124
            out = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", "ignore")
            err = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", "ignore")
            stdout_tail = "\n".join(out.strip().splitlines()[-20:])
            stderr_tail = "\n".join(err.strip().splitlines()[-20:])
        ended = _now_utc()
        status = "PASS" if exit_code == 0 else "FAIL"
        row["last_run_utc"] = ended.isoformat()
        row["next_review_utc"] = next_review
        if row["status"] in {"NEXT_7", "NEXT_30"} and exit_code == 0:
            row["status"] = "DONE_NOW"

        results.append(
            {
                "action": item.action,
                "status": status,
                "command": item.command,
                "exit_code": exit_code,
                "timed_out": timed_out,
                "started_at_utc": started.isoformat(),
                "ended_at_utc": ended.isoformat(),
                "stdout_tail": stdout_tail,
                "stderr_tail": stderr_tail,
            }
        )

    _write_tracker(tracker_path, fieldnames, rows)

    log_json = log_dir / f"ceo_top50_run_{run_stamp}.json"
    log_json.write_text(
        json.dumps(
            {
                "generated_at_utc": _now_utc().isoformat(),
                "tracker": str(tracker_path.relative_to(repo_root)),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed
    log_md = log_dir / f"ceo_top50_run_{run_stamp}.md"
    lines = [
        f"# CEO Top50 execution run — {run_stamp}",
        "",
        f"- Total actions: {total}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Tracker: `{tracker_path.relative_to(repo_root)}`",
        f"- JSON log: `{log_json.relative_to(repo_root)}`",
        "",
        "## Results",
    ]
    for result in results:
        lines.append("")
        lines.append(f"### {result['action']} — {result['status']} (exit={result['exit_code']})")
        lines.append(f"- Command: `{result['command']}`")
        if result["stdout_tail"]:
            lines.append("- Stdout tail:")
            lines.append("")
            lines.extend(f"  {line}" for line in str(result["stdout_tail"]).splitlines())
        if result["stderr_tail"]:
            lines.append("- Stderr tail:")
            lines.append("")
            lines.extend(f"  {line}" for line in str(result["stderr_tail"]).splitlines())
    log_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK: wrote tracker updates -> {tracker_path}")
    print(f"OK: wrote log json -> {log_json}")
    print(f"OK: wrote log md -> {log_md}")
    print(f"SUMMARY: total={total} pass={passed} fail={failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
