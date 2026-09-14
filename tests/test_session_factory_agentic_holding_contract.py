from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from dealix.agentic_holding.runtime import build_current_registry

ROOT = Path(__file__).resolve().parents[1]
FACTORY_SCRIPT = ROOT / "scripts/ops/session_factory.py"
WATCHDOG_SCRIPT = ROOT / "scripts/ops/session_factory_watchdog.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


factory = _load(FACTORY_SCRIPT, "session_factory_agentic_contract")
watchdog = _load(WATCHDOG_SCRIPT, "session_factory_watchdog_agentic_contract")


def _job(owner: str):
    return factory.make_job(
        owner_agent=owner,
        business_goal="agentic holding owner validation contract",
        job_class="LOCAL_AI",
        authority_level="L2",
        modifying=False,
        executor={"prompt": "bounded internal test"},
    )


def test_legacy_executor_alias_remains_compatible() -> None:
    job = _job("dealix-engineer")
    assert not [error for error in factory.validate_job(job) if "OWNER_AGENT" in error]


def test_real_dynamic_logical_agent_is_accepted() -> None:
    registry = build_current_registry()
    owner = "dealix.group.engineering"
    assert owner in registry.agents
    job = _job(owner)
    assert not [error for error in factory.validate_job(job) if "OWNER_AGENT" in error]


def test_orphan_dynamic_logical_agent_fails_closed() -> None:
    registry = build_current_registry()
    owner = "dealix.group.this-agent-does-not-exist"
    assert owner not in registry.agents
    job = _job(owner)
    errors = factory.validate_job(job)
    assert any("OWNER_AGENT" in error for error in errors), errors


def test_runtime_worker_capacity_is_not_globally_capped_at_legacy_three() -> None:
    resources = {
        "cpu_count": 8,
        "load1": 0.1,
        "load5": 0.1,
        "load15": 0.1,
        "mem_total_mb": 16384,
        "mem_available_mb": 12288,
        "disk_free_gb": 100.0,
    }
    capacity = factory.compute_max_concurrent_deep(resources)
    assert capacity > 3, (
        "Agentic Holding policy deprecates the legacy global DEEP_WIP_MAX=3 runtime cap; "
        f"roomy host capacity resolved to {capacity}"
    )


def test_watchdog_uses_governor_capacity_not_hardcoded_three(tmp_path: Path) -> None:
    state = tmp_path / "session_factory"
    jobs_dir = state / "jobs"
    jobs_dir.mkdir(parents=True)
    for index in range(4):
        (jobs_dir / f"J{index}.json").write_text(
            json.dumps(
                {
                    "JOB_ID": f"J{index}",
                    "STATUS": "RUNNING",
                    "MODIFYING": True,
                    "LEASE": {"present": True},
                    "CREATED_AT": "2026-09-13T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )
    (state / "RESOURCE_GOVERNOR_STATE.json").write_text(
        json.dumps(
            {
                "schema": "dealix.resource_governor.v1",
                "max_concurrent_deep": 8,
                "deep_wip_available": 4,
            }
        ),
        encoding="utf-8",
    )

    findings = watchdog.evaluate(state, now=1_800_000_000.0)
    capacity_findings = [finding for finding in findings if finding.get("kind") == "DEEP_WIP_EXCEEDED"]
    assert capacity_findings == [], capacity_findings


def test_hierarchical_owner_resolves_when_run_as_standalone_script(tmp_path: Path) -> None:
    """Reproduce the real standalone-scheduler condition (cron/systemd).

    The factory is invoked as a script from a neutral cwd with no PYTHONPATH.
    ``canonical_agent_ids`` must still resolve the canonical registry instead of
    failing closed to "registry unavailable" just because the repo root is not
    importable by default.
    """
    code = (
        "import importlib.util\n"
        f"spec = importlib.util.spec_from_file_location('sf_standalone', {str(FACTORY_SCRIPT)!r})\n"
        "m = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(m)\n"
        "ids = m.canonical_agent_ids()\n"
        "print('NONE' if ids is None else ('HAS' if 'dealix.group.engineering' in ids else 'MISS'))\n"
    )
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "HAS", (result.stdout, result.stderr)
