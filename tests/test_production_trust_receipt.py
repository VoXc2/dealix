"""Production Trust receipt regressions (Omega V3 SRE, source-only).

Pins the source-level contracts repaired for Production Trust:
- runtime report outputs honor DEALIX_RUNTIME_REPORTS_ROOT and their in-repo
  fallbacks stay gitignored so autonomous runs cannot dirty Source Sync;
- Web release identity exposes an immutable git SHA (never HTTP-200-only);
- the weekly proof-pack scheduler target resolves to a real repo executable;
- backup/rollback verification scripts stay fail-closed and testable.

No merge, deploy, DNS/DB/secret mutation, outbound, or spend.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_REPORT_DIRS = [
    "reports/president_portfolio_command/",
    "reports/strategy_execution_orchestrator/",
    "reports/self_operating_company_os/",
    "reports/company_os/",
]

# Representative runtime-generated output paths. These must stay invisible to
# `git status --porcelain` so scheduled runs cannot poison Source Sync.
RUNTIME_OUTPUT_PATHS = [
    "reports/president_portfolio_command/2026-09-13/president_command.json",
    "reports/strategy_execution_orchestrator/2026-09-13T00:00:00Z/strategy_execution_plan.json",
    "reports/self_operating_company_os/daily/2026-09-13.md",
    "reports/company_os/weekly/OPERATING_PROOF_2026-09-13.md",
]


def _load_fresh(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_runtime_report_dirs_are_gitignored() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for entry in RUNTIME_REPORT_DIRS:
        assert entry in gitignore
    for output in RUNTIME_OUTPUT_PATHS:
        proc = subprocess.run(
            ["git", "check-ignore", output],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, f"{output} must be git-ignored"


def test_president_portfolio_out_root_honors_control_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path))
    module = _load_fresh(
        "dealix_president_portfolio_receipt",
        "scripts/commercial/run_president_portfolio_command_v1.py",
    )
    assert module.OUT_ROOT == tmp_path / "president_portfolio_command"


def test_president_portfolio_out_root_default_stays_in_repo(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_RUNTIME_REPORTS_ROOT", raising=False)
    module = _load_fresh(
        "dealix_president_portfolio_default",
        "scripts/commercial/run_president_portfolio_command_v1.py",
    )
    assert module.OUT_ROOT == ROOT / "reports" / "president_portfolio_command"


def test_strategy_orchestrator_out_root_honors_control_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path))
    module = _load_fresh(
        "dealix_strategy_orchestrator_receipt",
        "scripts/commercial/run_strategy_execution_orchestrator_v1.py",
    )
    assert module.OUT_ROOT == tmp_path / "strategy_execution_orchestrator"
    assert module._display_path(tmp_path / "x.json") == str(tmp_path / "x.json")


def test_self_operating_os_out_root_honors_control_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path))
    module = _load_fresh(
        "dealix_self_os_receipt",
        "scripts/commercial/run_self_operating_company_os.py",
    )
    assert module.OUT_ROOT == tmp_path / "self_operating_company_os"


def test_weekly_proof_pack_out_honors_control_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path))
    module = _load_fresh(
        "dealix_weekly_proof_receipt",
        "scripts/commercial/run_weekly_proof_pack.py",
    )
    out = module._default_out("2026-09-13")
    assert out == tmp_path / "company_os" / "weekly" / "OPERATING_PROOF_2026-09-13.md"


def test_frontend_healthz_exposes_immutable_sha() -> None:
    source = (ROOT / "frontend" / "src" / "app" / "healthz" / "route.ts").read_text(
        encoding="utf-8"
    )
    assert "git_sha" in source
    assert "NEXT_PUBLIC_GIT_SHA" in source
    assert "VERCEL_GIT_COMMIT_SHA" in source
    assert "force-dynamic" in source
    assert "no-store" in source
    assert "force-static" not in source


def test_apps_web_healthz_prefers_immutable_sha() -> None:
    source = (ROOT / "apps" / "web" / "app" / "healthz" / "route.ts").read_text(
        encoding="utf-8"
    )
    assert "git_sha" in source
    ordered = [
        "DEALIX_RELEASE_SHA",
        "RAILWAY_GIT_COMMIT_SHA",
        "VERCEL_GIT_COMMIT_SHA",
        "NEXT_PUBLIC_GIT_SHA",
        "process.env.GIT_SHA",
    ]
    positions = [source.index(item) for item in ordered]
    assert positions == sorted(positions)


def test_selfhost_verifier_tracks_current_release_identity_chain() -> None:
    source = (ROOT / "scripts" / "ops" / "verify_selfhosted_production_plane.py").read_text(
        encoding="utf-8"
    )
    for item in (
        "DEALIX_RELEASE_SHA",
        "RAILWAY_GIT_COMMIT_SHA",
        "VERCEL_GIT_COMMIT_SHA",
        "NEXT_PUBLIC_GIT_SHA",
        "process.env.GIT_SHA",
    ):
        assert item in source


def test_frontend_dockerfile_bakes_git_sha() -> None:
    source = (ROOT / "frontend" / "Dockerfile").read_text(encoding="utf-8")
    assert "NEXT_PUBLIC_GIT_SHA" in source


def test_apps_web_dockerfile_passes_git_sha() -> None:
    source = (ROOT / "apps" / "web" / "Dockerfile").read_text(encoding="utf-8")
    assert "ARG GIT_SHA" in source


def test_root_recovery_allows_canonical_weekly_only() -> None:
    source = (ROOT / "scripts" / "ops" / "dealix-root-service-recover.sh").read_text(
        encoding="utf-8"
    )
    assert '"dealix-company@weekly.service"' in source
    assert '"dealix-company-weekly.timer"' in source
    assert '"dealix-omega-weekly.service"' not in source
    assert '"dealix-omega-weekly.timer"' not in source


def test_weekly_proof_pack_target_verifier_passes() -> None:
    verifier = _load_fresh(
        "dealix_weekly_target_receipt",
        "scripts/ops/verify_weekly_proof_pack_target.py",
    )
    assert verifier.main() == 0


def test_weekly_scheduler_branches_resolve_to_canonical_adapter() -> None:
    canonical = "scripts/commercial/run_weekly_proof_pack.py"
    assert (ROOT / canonical).is_file()
    for relative in (
        "scripts/ops/dealix_company_autopilot_legacy.sh",
        "scripts/ops/dealix_canonical_revenue_cycle.sh",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert canonical in text
        assert "scripts/run_weekly_proof_pack.py" not in text.replace(
            "scripts/commercial/run_weekly_proof_pack.py", ""
        )


def test_verify_backup_fail_closed_without_bucket(monkeypatch) -> None:
    monkeypatch.delenv("BACKUP_S3_BUCKET", raising=False)
    module = _load_fresh("dealix_verify_backup_receipt", "scripts/verify_backup.py")
    code, findings = module._verify(verbose=False, json_mode=False)
    assert code == 2
    assert "BACKUP_S3_BUCKET" in str(findings.get("error", ""))


def test_server_backup_verifies_archive_integrity() -> None:
    source = (ROOT / "scripts" / "server_backup.sh").read_text(encoding="utf-8")
    assert "sha256sum" in source
    assert "tar -tzf" in source


def test_rollback_drill_record_and_dry_run(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-q", "--allow-empty", "-m", "init"],
        check=True,
    )
    script = ROOT / "scripts" / "ops" / "rollback_drill.sh"
    env = {
        "APP_DIR": str(repo),
        "LOG_FILE": str(tmp_path / "drill.log"),
        "LAST_GOOD_FILE": str(repo / ".last_good_sha"),
        "PATH": "/usr/bin:/bin:/usr/local/bin",
    }
    record = subprocess.run(["bash", str(script), "--record-last-good"], env=env, check=False)
    assert record.returncode == 0
    expected = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert (repo / ".last_good_sha").read_text(encoding="utf-8").strip() == expected
    dry = subprocess.run(["bash", str(script), "--dry-run"], env=env, check=False)
    assert dry.returncode == 0
