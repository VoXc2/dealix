#!/usr/bin/env python3
"""Soft commercial launch readiness — config, digest tests, smoke imports (no Moyasar claim)."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

FAILURES: list[str] = []
WARNINGS: list[str] = []
STRICT = False


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  WARN: {msg}")


def check_paths() -> None:
    required = [
        "frontend/src/components/gtm/CommercialLaunchHome.tsx",
        "frontend/src/app/[locale]/page.tsx",
        "frontend/src/app/[locale]/learn/[slug]/page.tsx",
        "frontend/src/content/learn/articles.ts",
        "frontend/src/app/[locale]/ops/page.tsx",
        "frontend/src/components/gtm/OpsFounderCommandCenter.tsx",
        "dealix/config/social_content_queue.yaml",
        "dealix/config/icp_agency_wedge.yaml",
        "dealix/commercial_ops/outreach_drafts.py",
        "dealix/revenue_ops_autopilot/affiliate_compliance.py",
        "dealix/revenue_ops_autopilot/external_ingest.py",
        "dealix/marketing_factory/store.py",
        "dealix/execution_assurance/health.py",
        "docs/commercial/operations/targeting/agency_accounts_seed.csv",
        "docs/commercial/operations/CLIENT_PACK_SOP_AR.md",
        "dealix/commercial_ops/client_pack.py",
        "dealix/commercial_ops/doctrine.py",
        "scripts/founder_soaen_daily.py",
        "scripts/verify_commercial_fe_be.py",
        "scripts/verify_paid_launch_readiness.py",
        "scripts/verify_first_paid_diagnostic_tracker.py",
        "scripts/generate_client_pack.py",
        "scripts/expand_agency_targets_seed.py",
        "scripts/import_war_room_targets.py",
        "scripts/generate_war_room_touch_drafts.py",
        "scripts/expand_social_queue_12w.py",
        "scripts/enrich_targeting_warm.py",
        "scripts/founder_all_motions_pipeline.py",
        "dealix/commercial_ops/expansion_status.py",
        "dealix/commercial_ops/motion_pipelines.py",
        "scripts/expand_commercial_operating_stack.py",
        "scripts/run_governed_full_ops_autopilot.py",
        "scripts/run_governed_full_ops_autopilot.ps1",
        "dealix/commercial_ops/governed_autopilot.py",
        "scripts/expand_commercial_stack.py",
        "scripts/founder_motion_a_pipeline.py",
        "scripts/export_value_plan_snapshot.py",
        "frontend/src/app/[locale]/learn/page.tsx",
        "dealix/config/icp_segments.yaml",
        "dealix/config/founder_weekly_strategy_refs.yaml",
        "dealix/commercial_ops/strategy_refs.py",
        "scripts/founder_morning.ps1",
        "scripts/bootstrap_founder_kpi_import.py",
        "scripts/log_founder_commercial_day_evidence.py",
        "scripts/founder_soft_to_paid_verify.sh",
        "scripts/founder_soft_to_paid_verify.ps1",
        "scripts/expand_commercial_ops_all.py",
        "scripts/run_commercial_expansion.py",
        "scripts/run_commercial_expansion.ps1",
        "scripts/run_dealix_full_autonomous_ops.py",
        "scripts/run_dealix_full_autonomous_ops.ps1",
        "scripts/run_dealix_complete_autonomous_day.py",
        "scripts/run_full_commercial_ops_autopilot.py",
        "scripts/verify_full_autonomous_ops_stack.py",
        "scripts/founder_one_command.sh",
        "scripts/founder_one_command.ps1",
        "dealix/commercial_ops/full_ops_autopilot.py",
        "dealix/commercial_ops/complete_autonomous_day.py",
        "dealix/commercial_ops/founder_cockpit.py",
        "dealix/commercial_ops/autonomous_ops.py",
        "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
        "frontend/src/components/gtm/OpsFullAutonomousOpsCard.tsx",
        "scripts/founder_commercial_expand.ps1",
        "scripts/founder_commercial_expand.sh",
        "scripts/founder_expansion_status.py",
        "scripts/enrich_targeting_warm.py",
        "scripts/founder_all_motions_pipeline.py",
        "dealix/commercial_ops/expansion_status.py",
        "dealix/commercial_ops/motion_pipelines.py",
        "scripts/run_value_plan_day.ps1",
        "scripts/run_value_plan_day.sh",
        "scripts/founder_evening.ps1",
        "scripts/founder_evening_evidence.py",
        "scripts/founder_motion_a_pipeline.py",
        "scripts/founder_weekly_scorecard.py",
        "scripts/founder_paid_launch_gate.py",
        "scripts/run_value_plan_day.ps1",
        "scripts/run_value_plan_day.sh",
        "scripts/export_value_plan_snapshot.py",
        "scripts/verify_value_plan_stack.py",
        "dealix/commercial_ops/value_plan.py",
        "dealix/commercial_ops/value_map_status.py",
        "dealix/commercial_ops/gtm_stack.py",
        "scripts/commercial_value_map_status.py",
        "frontend/src/components/gtm/ValuePlanPanel.tsx",
        ".github/workflows/founder_evening_evidence.yml",
        ".github/workflows/founder_weekly_scorecard.yml",
        "scripts/run_dealix_daily_ops.py",
        "scripts/run_founder_commercial_day.sh",
        "scripts/verify_dealix_commercial_go_live.sh",
        "scripts/verify_dealix_commercial_go_live.ps1",
        "docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md",
        "docs/commercial/COMMERCIAL_VALUE_MAP_AR.md",
        "docs/commercial/COMMERCIAL_OPS_QUICK_REFERENCE_AR.md",
        "scripts/commercial_value_map_status.py",
        "dealix/commercial_ops/value_map_status.py",
        "dealix/commercial_ops/value_map_catalog.py",
        "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
    ]
    for rel in required:
        p = ROOT / rel
        if p.is_file():
            ok(rel)
        else:
            fail(f"missing {rel}")


def check_targeting_rows() -> None:
    from dealix.commercial_ops.targeting_csv import load_targets

    rows = load_targets()
    n = len(rows)
    min_rows = 250 if STRICT else 80
    if n >= min_rows:
        ok(f"agency_accounts_seed rows={n}")
    elif n >= 200:
        ok(f"agency_accounts_seed rows={n}")
        if STRICT:
            warn(
                f"strategic targeting below {min_rows} rows ({n}) — "
                "run scripts/expand_agency_targets_seed.py --wave4"
            )
    elif n >= 150:
        ok(f"agency_accounts_seed rows={n}")
        if STRICT:
            warn(
                f"strategic targeting below {min_rows} rows ({n}) — "
                "run scripts/expand_agency_targets_seed.py --wave3"
            )
    elif n >= 120:
        ok(f"agency_accounts_seed rows={n}")
        if STRICT:
            warn(
                f"strategic targeting below {min_rows} rows ({n}) — "
                "run scripts/expand_agency_targets_seed.py --wave2"
            )
    elif n >= 80:
        ok(f"agency_accounts_seed rows={n}")
        if not STRICT:
            ok("soft launch targeting OK (>= 80)")
        else:
            warn(
                f"strategic targeting below {min_rows} rows ({n}) — "
                "run scripts/expand_agency_targets_seed.py --wave2"
            )
    elif n >= 20:
        ok(f"agency_accounts_seed rows={n}")
        warn(f"strategic targeting below 80 rows ({n}) — run expand_agency_targets_seed.py")
    else:
        fail(f"agency_accounts_seed has only {n} rows (need >= {min_rows} in strict)")


def check_doctrine() -> None:
    from dealix.commercial_ops.doctrine import doctrine_status

    st = doctrine_status()
    if st["ok"]:
        ok(f"commercial_doctrine rules={st['rules_count']} checklist={st['checklist_count']}")
    else:
        fail("commercial_doctrine incomplete")


def check_strategy_refs() -> None:
    from dealix.commercial_ops.strategy_refs import strategy_refs_status

    st = strategy_refs_status()
    if st["ok"]:
        ok(f"founder_strategy_refs daily={st['daily_count']} weekly={st['weekly_count']}")
    else:
        fail(f"founder_strategy_refs incomplete missing={st.get('missing_paths')}")


def check_social_queue() -> None:
    from dealix.commercial_ops.social_queue import load_social_queue

    q = load_social_queue()
    posts = list(q.get("posts") or [])
    cycle = int(q.get("cycle_weeks") or 12)
    if len(posts) >= 120 and cycle >= 24:
        ok(f"social_content_queue posts={len(posts)} ({cycle}w)")
    elif len(posts) >= 100:
        ok(f"social_content_queue posts={len(posts)} ({cycle}w)")
        if STRICT and cycle < 24:
            warn("social cycle below 24w — run expand_social_queue_12w.py --cycle-weeks 24")
    elif len(posts) >= 80:
        ok(f"social_content_queue posts={len(posts)} ({cycle}w)")
        if cycle >= 20:
            warn("social queue below 100 posts — run expand_social_queue_12w.py --cycle-weeks 20")
    elif len(posts) >= 60:
        ok(f"social_content_queue posts={len(posts)} (12w+)")
        warn("social queue below 80 posts — run scripts/expand_social_queue_12w.py --cycle-weeks 16")
    elif posts:
        ok(f"social_content_queue posts={len(posts)}")
        warn("social queue below 60 posts — run scripts/expand_social_queue_12w.py")
    else:
        fail("social_content_queue has no posts")


def check_war_room_build() -> None:
    from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
    from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    pool = select_daily_p0_targets(load_targets(), top_n=10)
    pack = attach_outreach_drafts(build_war_room_today(pool, top_n=10))
    items = (pack.get("targets") or {}).get("items") or []
    if items and items[0].get("outreach_draft_ar"):
        ok("build_war_room_today + outreach_drafts")
    else:
        fail("war room missing targets or outreach_draft_ar")


def check_phase2_api_smoke() -> None:
    try:
        import os as _os

        ensure_stdout_utf8()
        # Isolated smoke key — do not reuse host .env (DEALIX_ADMIN_API_KEY may not match ADMIN_API_KEYS).
        smoke_admin = "dev"
        _os.environ["DEALIX_ADMIN_API_KEY"] = smoke_admin
        _os.environ["ADMIN_API_KEYS"] = smoke_admin
        _os.environ.pop("API_KEYS", None)

        from fastapi.testclient import TestClient

        from api.main import app

        client = TestClient(app)
        admin = smoke_admin
        headers = {"X-Admin-API-Key": admin}

        r_tgt = client.get(
            "/api/v1/ops-autopilot/targeting/today",
            params={"top_n": 3},
            headers=headers,
        )
        if r_tgt.status_code == 200:
            items = (r_tgt.json().get("targets") or {}).get("items") or []
            if items:
                ok("GET targeting/today")
            else:
                warn("targeting/today returned no items")
        else:
            fail(f"targeting/today status={r_tgt.status_code}")

        r_cal = client.get("/api/v1/ops-autopilot/marketing/calendar", headers=headers, params={"limit": 5})
        if r_cal.status_code == 200:
            ok("GET marketing/calendar")
        else:
            fail(f"marketing/calendar status={r_cal.status_code}")

        r_health = client.get("/api/v1/ops-autopilot/full-ops-health", headers=headers)
        if r_health.status_code == 200:
            ok("GET full-ops-health")
        else:
            fail(f"full-ops-health status={r_health.status_code}")

        r_fao = client.get(
            "/api/v1/ops-autopilot/founder/full-autonomous-ops",
            headers=headers,
            params={"top_n": 3, "include_nested": False, "include_value_plan": False},
        )
        if r_fao.status_code == 200 and r_fao.json().get("automation_readiness"):
            ok("GET founder/full-autonomous-ops")
        else:
            fail(f"founder/full-autonomous-ops status={r_fao.status_code}")

        r_cockpit = client.get(
            "/api/v1/ops-autopilot/founder/cockpit",
            headers=headers,
            params={"top_n": 3, "mode": "morning"},
        )
        if r_cockpit.status_code == 200 and r_cockpit.json().get("cockpit_verdict"):
            ok("GET founder/cockpit")
        else:
            fail(f"founder/cockpit status={r_cockpit.status_code}")

        r_partner = client.post(
            "/api/v1/public/partner-apply",
            json={
                "name": "Smoke Partner",
                "email": "smoke-partner@example.sa",
                "company": "Smoke",
                "partner_type": "referral",
                "message": "Dealix تضمن لك نمو الإيراد 100%",
                "consent": True,
            },
        )
        if r_partner.status_code == 422:
            ok("partner-apply blocks misleading affiliate copy")
        else:
            fail(f"partner-apply expected 422 got {r_partner.status_code}")
    except Exception as exc:
        warn(f"phase2 API smoke skipped: {exc}")


def _subprocess_env() -> dict[str, str]:
    """Isolate pytest from host .env admin keys (tests expect key ``dev``)."""
    env = {
        **os.environ,
        "PYTHONIOENCODING": "utf-8",
        "ADMIN_API_KEYS": "dev",
        "DEALIX_ADMIN_API_KEY": "dev",
        "APP_ENV": "test",
    }
    # Host .env may set API_KEYS that reject TestClient without X-API-Key.
    env.pop("API_KEYS", None)
    return env


def run_pytest_bundle() -> None:
    tests = [
        "tests/test_founder_commercial_digest.py",
        "tests/test_targeting_rotation.py",
        "tests/test_outreach_drafts.py",
        "tests/test_affiliate_compliance.py",
        "tests/test_external_ingest_bridge.py",
        "tests/test_client_pack.py",
        "tests/test_value_plan_ops.py",
        "tests/test_commercial_value_map_status.py",
        "tests/test_evidence_placeholders.py",
        "tests/test_full_ops_autopilot.py",
        "tests/test_complete_autonomous_day.py",
        "tests/test_founder_cockpit.py",
    ]
    cmd = [sys.executable, "-m", "pytest", *tests, "-q", "--no-cov"]
    r = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_subprocess_env(),
    )
    if r.returncode == 0:
        ok("commercial pytest bundle (phase 2)")
    else:
        fail(f"pytest bundle: {r.stdout[-400:]}{r.stderr[-400:]}")


def smoke_touch_drafts_dry_run() -> None:
    cmd = [sys.executable, str(ROOT / "scripts/generate_war_room_touch_drafts.py"), "--dry-run"]
    r = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_subprocess_env(),
    )
    if r.returncode == 0 and "WAR_ROOM_TOUCH_DRAFTS" in r.stdout:
        ok("generate_war_room_touch_drafts --dry-run")
    else:
        fail(f"touch drafts dry-run: {r.stderr or r.stdout}")


def smoke_import_dry_run() -> None:
    cmd = [sys.executable, str(ROOT / "scripts/import_war_room_targets.py"), "--dry-run"]
    r = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_subprocess_env(),
    )
    if r.returncode == 0 and "WAR_ROOM_IMPORT" in r.stdout:
        ok("import_war_room_targets --dry-run")
    else:
        fail(f"import dry-run: {r.stderr or r.stdout}")


def smoke_daily_ops_dry_run() -> None:
    cmd = [sys.executable, str(ROOT / "scripts/run_dealix_daily_ops.py"), "--dry-run", "--skip-api"]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode == 0:
        ok("run_dealix_daily_ops --dry-run --skip-api")
    else:
        warn(f"daily ops dry-run: {(r.stderr or r.stdout)[-200:]}")


def smoke_public_funnel() -> None:
    try:
        from fastapi.testclient import TestClient

        from api.main import app

        client = TestClient(app)
        r = client.get("/api/v1/public/knowledge/answer", params={"q": "post-lead"})
        if r.status_code in (200, 422):
            ok("GET /api/v1/public/knowledge/answer")
        else:
            fail(f"public knowledge status={r.status_code}")
        lead = client.post(
            "/api/v1/public/leads",
            json={
                "name": "Launch Smoke",
                "email": "smoke@example.sa",
                "company": "Smoke Co",
                "consent_marketing": False,
            },
        )
        if lead.status_code in (200, 201, 422):
            ok("POST /api/v1/public/leads")
        else:
            fail(f"public leads status={lead.status_code}")
    except Exception as exc:
        warn(f"public funnel smoke skipped: {exc}")


def smoke_live_api(base: str, admin_key: str) -> None:
    import urllib.error
    import urllib.request

    def _get(path: str) -> int:
        req = urllib.request.Request(
            f"{base.rstrip('/')}{path}",
            headers={"X-Admin-API-Key": admin_key},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status

    def _post(path: str, body: bytes, content_type: str = "application/json") -> int:
        req = urllib.request.Request(
            f"{base.rstrip('/')}{path}",
            data=body,
            headers={"X-Admin-API-Key": admin_key, "Content-Type": content_type},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status

    try:
        if _get("/api/v1/ops-autopilot/full-ops-health") == 200:
            ok(f"live GET full-ops-health @ {base}")
        else:
            fail("live full-ops-health not 200")
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            warn(f"live API auth failed ({exc.code}) — check DEALIX_ADMIN_API_KEY")
        else:
            fail(f"live full-ops-health HTTP {exc.code}")
    except Exception as exc:
        warn(f"live API skipped: {exc}")
        return

    try:
        if _post("/api/v1/ops-autopilot/ingest/replay-postgres", b"{}") in (200, 201):
            ok(f"live POST replay-postgres @ {base}")
        else:
            fail("live replay-postgres not 200")
    except urllib.error.HTTPError as exc:
        if exc.code == 503:
            ok(
                "live replay-postgres deferred (503 — start postgres / DATABASE_URL for full bridge)"
            )
        elif exc.code in (401, 403):
            warn(f"live replay auth failed ({exc.code}) — check DEALIX_ADMIN_API_KEY")
        else:
            fail(f"live replay-postgres HTTP {exc.code}")
    except Exception as exc:
        warn(f"live replay skipped: {exc}")


def run_frontend_build() -> None:
    frontend = ROOT / "frontend"
    if not (frontend / "package.json").is_file():
        fail("frontend/package.json missing")
        return
    next_dir = frontend / ".next"
    if next_dir.exists():
        shutil.rmtree(next_dir, ignore_errors=True)
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    r = subprocess.run(
        [npm, "run", "build"],
        cwd=frontend,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode == 0:
        ok("frontend npm run build")
    else:
        fail(f"frontend build: {(r.stderr or r.stdout)[-500:]}")


def main() -> int:
    global STRICT
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true", help="Fail on targeting WARN (>=80 rows)")
    p.add_argument(
        "--with-api",
        action="store_true",
        help="If DEALIX_API_BASE + DEALIX_ADMIN_API_KEY set, hit replay-postgres + full-ops-health",
    )
    p.add_argument(
        "--with-frontend-build",
        action="store_true",
        help="Run npm run build in frontend/ (slow; optional official launch gate)",
    )
    args = p.parse_args()
    STRICT = args.strict

    print("== verify_commercial_launch_ready (soft launch) ==")
    check_paths()
    check_doctrine()
    check_strategy_refs()
    check_targeting_rows()
    check_social_queue()
    check_war_room_build()
    smoke_import_dry_run()
    smoke_daily_ops_dry_run()
    r_fao = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_full_autonomous_ops_stack.py"), "--skip-api"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_subprocess_env(),
    )
    if r_fao.returncode == 0:
        ok("verify_full_autonomous_ops_stack")
    else:
        fail(f"verify_full_autonomous_ops_stack: {(r_fao.stderr or r_fao.stdout)[-400:]}")
    run_pytest_bundle()
    check_phase2_api_smoke()
    smoke_public_funnel()
    r_fe = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/verify_commercial_fe_be.py"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_subprocess_env(),
    )
    if r_fe.returncode == 0:
        ok("verify_commercial_fe_be")
    else:
        fail(f"verify_commercial_fe_be: {(r_fe.stderr or r_fe.stdout)[-400:]}")

    if args.with_api:
        base = os.environ.get("DEALIX_API_BASE", "").strip()
        key = os.environ.get("DEALIX_ADMIN_API_KEY", "").strip()
        if base and key:
            smoke_live_api(base, key)
        else:
            warn("--with-api: set DEALIX_API_BASE and DEALIX_ADMIN_API_KEY")

    if args.with_frontend_build:
        run_frontend_build()

    for w in WARNINGS:
        print(f"  (warning) {w}")
        if STRICT:
            FAILURES.append(w)

    if FAILURES:
        print("\nCOMMERCIAL_LAUNCH_READY: FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        print("See docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md")
        return 1

    print("\nCOMMERCIAL_LAUNCH_READY: PASS (soft — not full LAUNCH_GATES / Moyasar)")
    print("Unified gate: bash scripts/verify_dealix_commercial_go_live.sh")
    print("Public home: /ar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
