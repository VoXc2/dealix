#!/usr/bin/env python3
"""Dealix Launch Engine — one command runs the whole local machine.

This is the single entry point the founder (or a cron) runs to make the
*system itself* produce the full daily launch package — comprehensively,
end to end — and to print an honest launch-readiness verdict.

It does TWO things:

  1. GENERATORS — runs every local (no-prod-API) producer and collects
     their output into a single dated bundle at `data/daily_ops/<date>/`:
       • Founder daily brief        (scripts/dealix_founder_daily_brief.py)
       • Daily call sheet           (scripts/dealix_call_sheet.py)
       • Warm-list outreach drafts  (scripts/warm_list_outreach.py)
       • Content drafts             (scripts/dealix_content_factory_daily.py)

  2. READINESS AUDIT — offline checks that don't need a deployed URL:
       • Doctrine guard tests pass (the 8 non-negotiable guards)
       • Core OS modules import
       • Frontend build artifact + /custom-ai route present
       • No-overclaim register parses
       • Launch docs present
       • Warm list populated (else: founder action needed)

Everything is written to `data/daily_ops/<date>/INDEX.md` with a final
bilingual verdict: READY / NEEDS-FOUNDER / BLOCKED.

Doctrine: this NEVER sends anything externally and NEVER charges anyone.
Every produced message is a draft for founder approval. No scraping, no
cold automation. Degrades gracefully when credentials/inputs are missing.

Usage:
    python scripts/dealix_launch_engine.py
    python scripts/dealix_launch_engine.py --csv data/warm_list.csv
    python scripts/dealix_launch_engine.py --skip-tests   # faster, no pytest
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable
DISCLAIMER = "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

# Offline doctrine guards (must pass for a credible launch).
DOCTRINE_TESTS = [
    "tests/test_no_source_passport_no_ai.py",
    "tests/test_pii_external_requires_approval.py",
    "tests/test_no_cold_whatsapp.py",
    "tests/test_no_linkedin_automation.py",
    "tests/test_no_scraping_engine.py",
    "tests/test_no_guaranteed_claims.py",
    "tests/test_output_requires_governance_status.py",
    "tests/test_proof_pack_required.py",
]

# Canonical OS modules — the spine of the operating system.
CORE_MODULES = [
    "auto_client_acquisition.data_os",
    "auto_client_acquisition.governance_os",
    "auto_client_acquisition.proof_os",
    "auto_client_acquisition.value_os",
    "auto_client_acquisition.capital_os",
    "auto_client_acquisition.adoption_os",
    "auto_client_acquisition.friction_log",
    "auto_client_acquisition.sales_os.qualification",
    "auto_client_acquisition.icp_scorer",
    "auto_client_acquisition.lead_inbox",
]

LAUNCH_DOCS = [
    "docs/LAUNCH_MASTER_PLAN.md",
    "docs/brand/VISUAL_IDENTITY.md",
    "sales/playbook/WARM_LIST_CALL_SCRIPTS.md",
    "sales/playbook/OBJECTION_BANK.md",
    "dealix/registers/no_overclaim.yaml",
]

PASS, WARN, FAIL = "✅ PASS", "🟡 NEEDS-FOUNDER", "🔴 FAIL"


def _run(argv: list[str], timeout: int = 240) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            argv, cwd=str(REPO), capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, p.stdout, p.stderr
    except Exception as e:  # pragma: no cover - environment dependent
        return 1, "", str(e)


def _warm_csv(explicit: str | None) -> Path:
    """Prefer the founder's real warm list; fall back to the template so the
    engine always has something to run against."""
    if explicit:
        p = Path(explicit)
        return p if p.is_absolute() else REPO / p
    real = REPO / "data" / "warm_list.csv"
    if real.exists() and _csv_rows(real) > 0:
        return real
    return REPO / "data" / "warm_list.csv.template"


def _csv_rows(path: Path) -> int:
    """Count non-empty data rows (excluding the header)."""
    if not path.exists():
        return 0
    try:
        import csv

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return sum(
                1
                for r in reader
                if (r.get("name") or "").strip() or (r.get("company") or "").strip()
            )
    except Exception:
        return 0


# ─────────────────────────── generators ───────────────────────────


def run_generators(bundle: Path, warm_csv: Path) -> list[dict]:
    results: list[dict] = []

    # 1) Founder daily brief — prints markdown to stdout; capture it.
    rc, out, err = _run([PY, "scripts/dealix_founder_daily_brief.py"])
    if rc == 0 and out.strip():
        (bundle / "01_founder_brief.md").write_text(out, encoding="utf-8")
        results.append({"name": "Founder daily brief", "status": PASS, "file": "01_founder_brief.md"})
    else:
        results.append({"name": "Founder daily brief", "status": FAIL, "detail": (err or out)[:200]})

    # 2) Daily call sheet — writes its own file via --out.
    rc, out, err = _run(
        [PY, "scripts/dealix_call_sheet.py", "--csv", str(warm_csv), "--out", str(bundle / "02_call_sheet.md")]
    )
    if rc == 0:
        results.append({"name": "Daily call sheet", "status": PASS, "file": "02_call_sheet.md", "note": out.strip().splitlines()[0] if out.strip() else ""})
    else:
        results.append({"name": "Daily call sheet", "status": FAIL, "detail": (err or out)[:200]})

    # 3) Warm-list outreach drafts.
    rc, out, err = _run(
        [PY, "scripts/warm_list_outreach.py", "--csv", str(warm_csv), "--out", str(bundle / "03_warm_outreach_drafts.md")]
    )
    if rc == 0:
        results.append({"name": "Warm-list outreach drafts", "status": PASS, "file": "03_warm_outreach_drafts.md"})
    else:
        results.append({"name": "Warm-list outreach drafts", "status": FAIL, "detail": (err or out)[:200]})

    # 4) Content drafts — pass an explicit runtime out-dir and read back from
    # it. Never mutates the tracked reports/company_os/daily/ fixture; the
    # bundle copy below is the launch-engine-owned artifact.
    content_out = bundle / "content_factory"
    rc, out, err = _run(
        [PY, "scripts/dealix_content_factory_daily.py", "--out-dir", str(content_out)]
    )
    src = content_out / "CONTENT_DRAFTS_TODAY.md"
    if rc == 0 and src.exists():
        shutil.copyfile(src, bundle / "04_content_drafts.md")
        results.append({"name": "Content drafts", "status": PASS, "file": "04_content_drafts.md"})
    else:
        results.append({"name": "Content drafts", "status": FAIL, "detail": (err or out)[:200]})

    return results


# ─────────────────────────── readiness audit ───────────────────────────


def run_audit(skip_tests: bool, warm_csv: Path) -> list[dict]:
    checks: list[dict] = []

    # Doctrine guards.
    if skip_tests:
        checks.append({"name": "Doctrine guards (8)", "status": WARN, "detail": "skipped (--skip-tests)"})
    else:
        rc, out, err = _run([PY, "-m", "pytest", *DOCTRINE_TESTS, "-q"], timeout=300)
        if rc == 0:
            tail = [ln for ln in out.strip().splitlines() if "passed" in ln]
            checks.append({"name": "Doctrine guards (8)", "status": PASS, "detail": tail[-1] if tail else "passed", "hard": True})
        elif "No module named pytest" in (err + out):
            checks.append({"name": "Doctrine guards (8)", "status": WARN, "detail": "pytest not installed — run `pip install pytest`"})
        else:
            checks.append({"name": "Doctrine guards (8)", "status": FAIL, "detail": (out or err)[-200:], "hard": True})

    # Core OS module imports.
    failed = []
    for mod in CORE_MODULES:
        rc, _, err = _run([PY, "-c", f"import {mod}"], timeout=60)
        if rc != 0:
            failed.append(mod)
    if failed:
        checks.append({"name": "Core OS modules import", "status": FAIL, "detail": "failed: " + ", ".join(failed), "hard": True})
    else:
        checks.append({"name": "Core OS modules import", "status": PASS, "detail": f"{len(CORE_MODULES)} modules", "hard": True})

    # Frontend build artifact + /custom-ai route.
    next_built = (REPO / "frontend" / ".next").exists()
    custom_route = (REPO / "frontend" / "src" / "app" / "[locale]" / "custom-ai" / "page.tsx").exists()
    if custom_route and next_built:
        checks.append({"name": "Frontend build + /custom-ai route", "status": PASS, "detail": ".next present, route present"})
    elif custom_route:
        checks.append({"name": "Frontend build + /custom-ai route", "status": WARN, "detail": "route present; run `cd frontend && npm run build`"})
    else:
        checks.append({"name": "Frontend build + /custom-ai route", "status": FAIL, "detail": "custom-ai route missing"})

    # No-overclaim register parses.
    reg = REPO / "dealix" / "registers" / "no_overclaim.yaml"
    try:
        import yaml  # type: ignore

        yaml.safe_load(reg.read_text(encoding="utf-8"))
        checks.append({"name": "No-overclaim register", "status": PASS, "detail": "parses"})
    except Exception as e:
        status = WARN if not reg.exists() else FAIL
        checks.append({"name": "No-overclaim register", "status": status, "detail": str(e)[:120]})

    # Launch docs present.
    missing = [d for d in LAUNCH_DOCS if not (REPO / d).exists()]
    if missing:
        checks.append({"name": "Launch docs", "status": FAIL, "detail": "missing: " + ", ".join(missing)})
    else:
        checks.append({"name": "Launch docs", "status": PASS, "detail": f"{len(LAUNCH_DOCS)} present"})

    # Warm list populated (gates the "able to call" capability).
    rows = _csv_rows(REPO / "data" / "warm_list.csv")
    if rows >= 1:
        checks.append({"name": "Warm contacts loaded", "status": PASS, "detail": f"{rows} contact(s)"})
    else:
        checks.append({
            "name": "Warm contacts loaded",
            "status": WARN,
            "detail": "0 in data/warm_list.csv — founder must fill it (copy data/warm_list.csv.template)",
        })

    return checks


# ─────────────────────────── reporting ───────────────────────────


def _verdict(checks: list[dict]) -> tuple[str, str]:
    hard_fail = any(c.get("hard") and c["status"] == FAIL for c in checks)
    any_fail = any(c["status"] == FAIL for c in checks)
    any_warn = any(c["status"] == WARN for c in checks)
    if hard_fail or any_fail:
        return ("🔴 BLOCKED", "عائق يمنع الإطلاق — صحّح الفحوصات الحمراء. / A blocker prevents launch — fix the red checks.")
    if any_warn:
        return ("🟡 NEEDS-FOUNDER", "النظام جاهز تقنياً — تبقّى إجراء من المؤسس (الأصفر). / System is technically ready — founder action remains (yellow).")
    return ("🟢 READY", "كل الفحوصات خضراء — جاهز للإطلاق. / All checks green — ready to launch.")


def render_index(bundle: Path, today: str, generators: list[dict], checks: list[dict]) -> str:
    verdict, verdict_msg = _verdict(checks)
    L: list[str] = []
    L.append(f"# 🚀 Dealix Launch Engine — Daily Package · {today}")
    L.append("")
    L.append("**حزمة التشغيل اليومية الكاملة + تدقيق الجاهزية.** _Full daily ops package + readiness audit._")
    L.append("لا إرسال خارجي · لا شحن مالي · كل رسالة مسودة باعتماد المؤسس. / No external send · no charge · every message is a founder-approved draft.")
    L.append("")
    L.append(f"## الحكم / Verdict: {verdict}")
    L.append("")
    L.append(verdict_msg)
    L.append("")

    L.append("## 1. المخرجات المُولّدة / Generated artifacts")
    L.append("")
    L.append("| Artifact | Status | File |")
    L.append("|---|---|---|")
    for g in generators:
        f = g.get("file", "—")
        link = f"[`{f}`]({f})" if f != "—" else "—"
        L.append(f"| {g['name']} | {g['status']} | {link} |")
    L.append("")

    L.append("## 2. تدقيق الجاهزية / Readiness audit")
    L.append("")
    L.append("| Check | Status | Detail |")
    L.append("|---|---|---|")
    for c in checks:
        L.append(f"| {c['name']} | {c['status']} | {c.get('detail','')} |")
    L.append("")

    L.append("## 3. خطوات المؤسس / Founder next steps")
    L.append("")
    founder_items = [c for c in checks if c["status"] == WARN]
    if founder_items:
        for c in founder_items:
            L.append(f"- **{c['name']}** — {c.get('detail','')}")
    else:
        L.append("- لا يوجد — كل شيء أخضر. / None — everything is green.")
    L.append("")
    L.append("بعد تعبئة قائمة الجهات: `python scripts/dealix_launch_engine.py` يوميًا. / After filling the warm list, run the engine daily.")
    L.append("")
    L.append(DISCLAIMER)
    L.append("")
    return "\n".join(L)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full Dealix local launch machine + readiness audit.")
    parser.add_argument("--csv", default=None, help="warm-list CSV (defaults to data/warm_list.csv, else the template)")
    parser.add_argument("--skip-tests", action="store_true", help="skip the doctrine guard pytest run")
    parser.add_argument("--out", default=None, help="bundle dir (default data/daily_ops/<date>/)")
    args = parser.parse_args()

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    bundle = Path(args.out) if args.out else (REPO / "data" / "daily_ops" / today)
    if not bundle.is_absolute():
        bundle = REPO / bundle
    bundle.mkdir(parents=True, exist_ok=True)
    warm_csv = _warm_csv(args.csv)

    print("═" * 60)
    print(f"  🚀  DEALIX LAUNCH ENGINE · {today}")
    print(f"      bundle: {bundle}")
    print(f"      warm list: {warm_csv.name}")
    print("═" * 60)

    generators = run_generators(bundle, warm_csv)
    checks = run_audit(args.skip_tests, warm_csv)

    index = render_index(bundle, today, generators, checks)
    (bundle / "INDEX.md").write_text(index, encoding="utf-8")

    print("\n── Generators ──")
    for g in generators:
        print(f"  {g['status']}  {g['name']}")
    print("\n── Readiness audit ──")
    for c in checks:
        print(f"  {c['status']}  {c['name']} — {c.get('detail','')}")

    verdict, verdict_msg = _verdict(checks)
    print("\n" + "═" * 60)
    print(f"  VERDICT: {verdict}")
    print(f"  {verdict_msg}")
    print(f"  📦 {bundle / 'INDEX.md'}")
    print("═" * 60)

    # Hard failures (doctrine / imports) → non-zero exit for CI/cron.
    hard_fail = any(c.get("hard") and c["status"] == FAIL for c in checks)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
