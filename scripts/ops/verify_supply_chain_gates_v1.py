#!/usr/bin/env python3
"""Omega5 supply-chain presence-aware source gate (no installs, no signing).

Reuses the existing isolated-lab contract
(``config/oss/supply_chain_lab_v1.json``), the SBOM policy
(``docs/ops/SBOM_AND_SUPPLY_CHAIN_POLICY.md``), the local SBOM
generator (``scripts/generate_sbom.py``), and CI scan surfaces
(Trivy/SBOM workflows + ``.trivyignore.yaml``).

Fail-closed rules:
- A missing scanner reports NOT_AVAILABLE/HOLD and the overall
  verdict is HOLD — never PASS.
- Cosign/signature verification counts only with explicit
  identity + digest evidence (env or receipt file); otherwise HOLD.
- This script never installs tools (no curl/network), never signs,
  pushes, mutates dependencies, or touches Production.

Exit codes: 0 = PASS (all required evidence present),
2 = HOLD (blocked, fail-closed), 1 = script/manifest error.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB_MANIFEST = ROOT / "config" / "oss" / "supply_chain_lab_v1.json"
LAB_BIN = Path(os.environ.get("DEALIX_SUPPLY_CHAIN_LAB_ROOT", "/opt/dealix/labs/supply-chain")) / "bin"

REQUIRED_TOOLS = ("osv-scanner", "trivy", "syft", "cosign")

HOLD = "HOLD"
AVAILABLE = "AVAILABLE"
NOT_AVAILABLE = "NOT_AVAILABLE"


def _which_candidates(name: str) -> str | None:
    """Return isolated-lab binary first, else PATH lookup. No installs."""
    lab_hit = LAB_BIN / name
    if lab_hit.is_file() and os.access(lab_hit, os.X_OK):
        return str(lab_hit)
    return shutil.which(name)


def _probe_version(binary: str) -> str:
    """Best-effort local --version probe (no network). Returns redacted one-liner."""
    for args in (["--version"], ["version"]):
        try:
            proc = subprocess.run(
                [binary, *args],
                capture_output=True,
                text=True,
                timeout=10,
            )
            out = (proc.stdout or proc.stderr or "").strip().splitlines()
            if out:
                return out[0][:160]
            if proc.returncode == 0:
                return "present_version_unknown"
        except Exception:
            continue
    return "present_version_unknown"


def _sbom_evidence() -> tuple[str, str]:
    """Check for locally generated SBOM evidence (no generation here)."""
    candidates = [
        ROOT / "docs" / "SBOM.json",
        ROOT / "docs" / "generated" / "dependency-inventory.json",
    ]
    for path in candidates:
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                lowered = text.lower()
                if "cyclonedx" in lowered or "spdx" in lowered or "components" in lowered:
                    return AVAILABLE, path.relative_to(ROOT).as_posix()
                return HOLD, f"{path.relative_to(ROOT).as_posix()}:unrecognized_format"
            except OSError:
                return HOLD, f"{path.relative_to(ROOT).as_posix()}:unreadable"
    gen = ROOT / "scripts" / "generate_sbom.py"
    if gen.is_file():
        return NOT_AVAILABLE, "sbom_generator_present_no_artifact"
    return NOT_AVAILABLE, "no_sbom_surface"


def _cosign_evidence() -> tuple[str, str]:
    """Cosign counts only with explicit identity + digest evidence."""
    identity = os.environ.get("COSIGN_IDENTITY", "").strip()
    digest_file = os.environ.get("COSIGN_DIGEST_FILE", "").strip()
    digest = os.environ.get("COSIGN_DIGEST", "").strip()
    binary = _which_candidates("cosign")
    if not binary:
        return NOT_AVAILABLE, "cosign_binary_missing"
    if identity and (digest or (digest_file and Path(digest_file).is_file())):
        return AVAILABLE, f"identity_present_digest_present_binary={binary}"
    return HOLD, "signing_requires_explicit_identity_and_digest"


def main() -> int:
    try:
        statuses: dict[str, str] = {}
        details: dict[str, str] = {}
        for tool in REQUIRED_TOOLS:
            if tool == "cosign":
                status, detail = _cosign_evidence()
            else:
                binary = _which_candidates(tool)
                if binary:
                    status, detail = AVAILABLE, f"{binary} :: {_probe_version(binary)}"
                else:
                    status, detail = NOT_AVAILABLE, "binary_not_found_no_install_attempted"
            statuses[tool] = status
            details[tool] = detail

        sbom_status, sbom_detail = _sbom_evidence()
        manifest_ok = LAB_MANIFEST.is_file()
        policy_ok = (ROOT / "docs" / "ops" / "SBOM_AND_SUPPLY_CHAIN_POLICY.md").is_file()
        trivyignore_ok = (ROOT / ".trivyignore.yaml").is_file()

        required_ok = all(statuses[t] == AVAILABLE for t in ("osv-scanner", "trivy", "syft"))
        signing_ok = statuses["cosign"] == AVAILABLE
        overall_pass = required_ok and signing_ok and sbom_status == AVAILABLE

        verdict = "PASS" if overall_pass else HOLD
        print(f"DEALIX_SUPPLY_CHAIN_GATES_V1={verdict}")
        for tool in REQUIRED_TOOLS:
            print(f"tool={tool} status={statuses[tool]} detail={details[tool]}")
        print(f"sbom={sbom_status} detail={sbom_detail}")
        print(f"lab_manifest={'present' if manifest_ok else 'missing'}")
        print(f"sbom_policy={'present' if policy_ok else 'missing'}")
        print(f"trivyignore={'present' if trivyignore_ok else 'missing'}")
        print("production_mutation=false")
        print("customer_effects=false")
        print("auto_install=false")
        print("auto_sign=false")
        if verdict == HOLD:
            print("action=resolve_missing_evidence_then_rerun")
            return 2
        print("action=none_required")
        return 0
    except Exception as exc:
        print(f"DEALIX_SUPPLY_CHAIN_GATES_V1=ERROR error={type(exc).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
