#!/usr/bin/env python3
"""Audit Dealix Omega V3 agent governance without creating a second registry.

The lightweight audit keeps GitHub's existing stdlib-only workflow usable while
verifying that repository guidance points to the canonical Agentic Holding source.
When the full application environment is available it also calls
``dealix.agentic_holding.runtime.build_current_registry()`` and records the real
registry receipt. Sovereign acceptance on device V MUST run the dynamic mode;
source-only mode is governance lint, not runtime proof.

Outputs:
  - reports/agents/agent_team_audit.json
  - reports/agents/agent_team_audit.md
  - stdout: DEALIX_AGENT_TEAM_AUDIT=PASS|FAIL
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

AGENT_DIRS: tuple[str, ...] = (
    ".claude/agents",
    ".codex/agents",
    ".cursor/rules",
    "core/agents",
    "dealix/agentic_holding",
    "autonomous_growth/agents",
    "auto_client_acquisition",
    "mcp_server",
    "prompts",
)

REQUIRED_DOCS: tuple[str, ...] = (
    "AGENTS.md",
    "docs/agents/README.md",
    "docs/agents/AGENT_TEAM_REGISTRY.md",
    "docs/agents/AGENT_OUTPUT_CONTRACT.md",
    "docs/agents/AGENT_PERMISSION_MATRIX.md",
    "docs/agents/AGENT_DAILY_RUNBOOK.md",
    "docs/agents/AGENT_SECURITY_POLICY.md",
    "docs/agents/TOKEN_BUDGET_POLICY.md",
    "docs/agents/PR_TRIAGE_POLICY.md",
)

RECOMMENDED_DOCS: tuple[str, ...] = (
    "docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md",
    "docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md",
)

CLAUDE_AGENT_DIR = ".claude/agents"
CODEX_AGENT_DIR = ".codex/agents"
REQUIRED_CLAUDE_FRONTMATTER: tuple[str, ...] = ("name", "description", "tools")
MIN_DOCTRINE_GUARD_TESTS = 5

LEGACY_FIXED_FIVE_MARKERS: tuple[str, ...] = (
    "the 5 real sub-agents",
    "5 real sub-agents",
    "canonical sub-agents (the real roster)",
)

CURRENT_AUTHORITY_MARKERS: tuple[str, ...] = (
    "agentic holding",
    "resourcegovernor",
    "session factory",
)


def _exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def _read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8-sig")


def _count_files(rel: str) -> int:
    path = ROOT / rel
    if not path.exists():
        return 0
    if path.is_file():
        return 1
    return sum(1 for child in path.rglob("*") if child.is_file())


def _frontmatter_block(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return None


def _agent_names(rel: str, pattern: str) -> list[str]:
    directory = ROOT / rel
    if not directory.exists():
        return []
    return sorted(path.stem for path in directory.glob(pattern))


def _check_frontmatter() -> dict[str, dict[str, object]]:
    directory = ROOT / CLAUDE_AGENT_DIR
    result: dict[str, dict[str, object]] = {}
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.md")):
        block = _frontmatter_block(path.read_text(encoding="utf-8"))
        if block is None:
            result[path.stem] = {"ok": False, "missing": list(REQUIRED_CLAUDE_FRONTMATTER)}
            continue
        present = {
            line.split(":", 1)[0].strip()
            for line in block.splitlines()
            if ":" in line and not line.startswith((" ", "\t"))
        }
        missing = [key for key in REQUIRED_CLAUDE_FRONTMATTER if key not in present]
        result[path.stem] = {"ok": not missing, "missing": missing}
    return result


def _doctrine_guard_tests() -> list[str]:
    tests_dir = ROOT / "tests"
    if not tests_dir.exists():
        return []
    return sorted(path.name for path in tests_dir.glob("test_no_*.py"))


def _source_authority_status() -> dict[str, Any]:
    runtime = _read("dealix/agentic_holding/runtime.py")
    arm_registry = _read("dealix/commercial/arm_registry.py")
    sector_factory = _read("dealix/commercial/sector_company_factory.py")
    required_runtime = (
        "def build_current_registry",
        "class AgentHierarchyRegistry",
        "orphan_failures",
        "unmapped_arms",
        "ResourceSnapshot",
    )
    runtime_ok = all(marker in runtime for marker in required_runtime)
    arm_ok = "get_active_arms" in arm_registry and "CapabilityArm" in arm_registry
    sector_ok = "SectorCompanyFactory" in sector_factory
    return {
        "ok": runtime_ok and arm_ok and sector_ok,
        "runtime_markers_ok": runtime_ok,
        "arm_registry_markers_ok": arm_ok,
        "sector_factory_markers_ok": sector_ok,
        "authority": "dealix.agentic_holding.runtime.build_current_registry",
    }


def _dynamic_registry_status() -> dict[str, Any]:
    """Use the canonical runtime when dependencies are available.

    The hosted agent-team audit intentionally installs no third-party packages.
    Missing optional runtime dependencies therefore produce SOURCE_ONLY mode, not
    a fake dynamic PASS. Device-V acceptance must require mode=DYNAMIC.
    """
    try:
        from dealix.agentic_holding.runtime import build_current_registry

        receipt = build_current_registry().receipt()
    except Exception as exc:  # noqa: BLE001 - report exact dependency/runtime blocker
        source = _source_authority_status()
        return {
            "mode": "SOURCE_ONLY",
            "ok": source["ok"],
            "runtime_receipt_proven": False,
            "reason": f"dynamic_registry_unavailable:{type(exc).__name__}",
            "source_authority": source,
            "required_sovereign_command": "python scripts/audit_agent_team.py --strict --require-dynamic-registry",
        }

    orphan_failures = list(receipt.get("orphan_failures") or [])
    unmapped_arms = list(receipt.get("unmapped_arms") or [])
    return {
        "mode": "DYNAMIC",
        "ok": not orphan_failures and not unmapped_arms,
        "runtime_receipt_proven": True,
        "receipt": receipt,
        "required_sovereign_command": "python scripts/audit_agent_team.py --strict --require-dynamic-registry",
    }


def _governance_authority_status() -> dict[str, Any]:
    targets = {
        "AGENTS.md": _read("AGENTS.md"),
        "docs/agents/README.md": _read("docs/agents/README.md"),
        "docs/agents/AGENT_TEAM_REGISTRY.md": _read("docs/agents/AGENT_TEAM_REGISTRY.md"),
    }
    legacy_hits: dict[str, list[str]] = {}
    missing_markers: dict[str, list[str]] = {}
    for path, text in targets.items():
        lowered = text.lower()
        hits = [marker for marker in LEGACY_FIXED_FIVE_MARKERS if marker in lowered]
        if hits:
            legacy_hits[path] = hits
        missing = [marker for marker in CURRENT_AUTHORITY_MARKERS if marker not in lowered]
        if missing:
            missing_markers[path] = missing

    root = targets["AGENTS.md"].lower()
    old_test_rule = "run/tests commands only when explicitly requested by the user" in root
    current_commercial_ok = (
        "diagnostic" in root
        and "qualified discovery" in root
        and "customer-specific" in root
    )
    provider_neutral_model_ok = (
        "provider-neutral" in root
        and "no silent paid spill" in root
        and "legacy default mints authority" in root
    )

    return {
        "ok": not legacy_hits and not missing_markers and not old_test_rule and current_commercial_ok and provider_neutral_model_ok,
        "fixed_five_authority_hits": legacy_hits,
        "missing_current_authority_markers": missing_markers,
        "obsolete_explicit-test-only_rule_present": old_test_rule,
        "current_commercial_law_present": current_commercial_ok,
        "provider_neutral_model_authority_present": provider_neutral_model_ok,
    }


def build_report(*, require_dynamic_registry: bool = False) -> dict[str, Any]:
    gaps: list[str] = []
    warnings: list[str] = []

    surfaces: dict[str, dict[str, object]] = {}
    for rel in AGENT_DIRS:
        count = _count_files(rel)
        surfaces[rel] = {"exists": _exists(rel), "files": count}
        if count == 0:
            gaps.append(f"Missing or empty agent surface: {rel}")

    required_docs = {doc: _exists(doc) for doc in REQUIRED_DOCS}
    for doc, ok in required_docs.items():
        if not ok:
            gaps.append(f"Missing required governance doc: {doc}")

    recommended_docs = {doc: _exists(doc) for doc in RECOMMENDED_DOCS}
    for doc, ok in recommended_docs.items():
        if not ok:
            warnings.append(f"Missing recommended doc: {doc}")

    claude_agents = _agent_names(CLAUDE_AGENT_DIR, "*.md")
    codex_agents = _agent_names(CODEX_AGENT_DIR, "*.toml")
    claude_only = sorted(set(claude_agents) - set(codex_agents))
    codex_only = sorted(set(codex_agents) - set(claude_agents))
    parity_in_sync = not claude_only and not codex_only
    if claude_only:
        warnings.append(f"Claude compatibility agents without Codex mirror: {', '.join(claude_only)}")
    if codex_only:
        warnings.append(f"Codex compatibility agents without Claude mirror: {', '.join(codex_only)}")

    frontmatter = _check_frontmatter()
    for name, info in frontmatter.items():
        if not info["ok"]:
            missing = ", ".join(info["missing"])  # type: ignore[arg-type]
            gaps.append(f"Claude compatibility agent '{name}' missing frontmatter: {missing}")

    doctrine_tests = _doctrine_guard_tests()
    doctrine_ok = len(doctrine_tests) >= MIN_DOCTRINE_GUARD_TESTS
    if not doctrine_ok:
        gaps.append(f"Only {len(doctrine_tests)} doctrine guard tests found (expected >= {MIN_DOCTRINE_GUARD_TESTS})")

    governance = _governance_authority_status()
    if not governance["ok"]:
        gaps.append("Root/docs agent guidance still conflicts with Omega V3 registry authority")

    registry = _dynamic_registry_status()
    if not registry["ok"]:
        gaps.append("Canonical Agentic Holding registry/source authority failed validation")
    if registry["mode"] != "DYNAMIC":
        warnings.append("Dynamic Agentic Holding receipt not proven in this environment; sovereign V acceptance is still required")
    if require_dynamic_registry and registry["mode"] != "DYNAMIC":
        gaps.append("Dynamic Agentic Holding registry receipt required but unavailable")

    verdict = "FAIL" if gaps else "PASS"
    return {
        "schema": "dealix.agent_team_audit/v2",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "verdict": verdict,
        "canonical_architecture": "Dealix Holding -> Company Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> ResourceGovernor-bounded runtime workers",
        "fixed_five_authority": False,
        "legacy_five": "compatibility_aliases_only",
        "agent_surfaces": surfaces,
        "compatibility_agent_files": {
            "claude": claude_agents,
            "codex": codex_agents,
            "in_sync": parity_in_sync,
            "claude_only": claude_only,
            "codex_only": codex_only,
        },
        "agent_frontmatter": frontmatter,
        "required_docs": required_docs,
        "recommended_docs": recommended_docs,
        "governance_authority": governance,
        "agentic_holding_registry": registry,
        "doctrine_guard_tests": {"count": len(doctrine_tests), "ok": doctrine_ok, "tests": doctrine_tests},
        "gaps": gaps,
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    registry = report["agentic_holding_registry"]
    governance = report["governance_authority"]
    compat = report["compatibility_agent_files"]
    lines = [
        "# Dealix Agent Governance Audit",
        "",
        f"- Verdict: **{report['verdict']}**",
        f"- Generated: `{report['generated_at_utc']}`",
        f"- Registry mode: **{registry['mode']}**",
        f"- Fixed-five authority: **{report['fixed_five_authority']}**",
        "",
        "## Omega V3 authority",
        f"- Governance guidance: {'PASS' if governance['ok'] else 'FAIL'}",
        f"- Agentic Holding registry/source: {'PASS' if registry['ok'] else 'FAIL'}",
        f"- Dynamic runtime receipt proven: {registry['runtime_receipt_proven']}",
        "",
        "## Compatibility surfaces",
        f"- Claude files: {len(compat['claude'])}",
        f"- Codex files: {len(compat['codex'])}",
        f"- File parity: {'in sync' if compat['in_sync'] else 'out of sync'}",
        "- These counts are compatibility hygiene, not logical-fleet architecture.",
        "",
        "## Gaps",
    ]
    lines.extend([f"- ❌ {gap}" for gap in report["gaps"]] or ["- None"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- ⚠ {warning}" for warning in report["warnings"]] or ["- None"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Dealix Omega V3 agent governance.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 when verdict is FAIL.")
    parser.add_argument("--json-only", action="store_true")
    parser.add_argument(
        "--require-dynamic-registry",
        action="store_true",
        help="Require build_current_registry() to execute and produce an orphan-free receipt (sovereign acceptance).",
    )
    args = parser.parse_args(argv)

    report = build_report(require_dynamic_registry=args.require_dynamic_registry)
    out_dir = ROOT / "reports" / "agents"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "agent_team_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "agent_team_audit.md").write_text(render_markdown(report), encoding="utf-8")

    if args.json_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for gap in report["gaps"]:
            print(f"GAP: {gap}", file=sys.stderr)
        for warning in report["warnings"]:
            print(f"WARN: {warning}", file=sys.stderr)
        print(f"DEALIX_AGENT_TEAM_AUDIT={report['verdict']}")
        print(f"AGENTIC_HOLDING_REGISTRY_MODE={report['agentic_holding_registry']['mode']}")

    if args.strict and report["verdict"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
