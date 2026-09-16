#!/usr/bin/env python3
"""Verify Company Constitution coverage over ONE Company Machine.

Loads the existing Stage A registry/loader (config/company/company_constitution_registry.yaml
+ dealix/company_constitution.py) and fail-closes on:
- missing required domains
- duplicate primary_authority (never allowed; shared reuse belongs in authority_paths)
- invalid state / autonomy
- missing/empty evidence_refs or receipt_requirements
- any local path in primary_authority/authority_paths/evidence_inputs/verifier_paths/evidence_refs that does not exist
- L5-sensitive domains lacking action_bound_l5_gate true
- active production authority refs reintroducing Railway/Vercel/GitHub Actions as production runtime authority

Prints concise PASS/FAIL and exits nonzero on failure. No production/DB/DNS/secrets/provider/send effects.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

# Ensure repo root is on sys.path for `dealix` package when run as script
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Reuse Stage A loader for canonical constants and parsing
try:
    from dealix.company_constitution import (
        ALLOWED_AUTONOMY,
        ALLOWED_STATES,
        REQUIRED_DOMAINS,
        DEFAULT_REGISTRY_PATH,
        REPO_ROOT as LOADER_REPO_ROOT,
        load_registry as loader_load_registry,
        validate_registry as loader_validate_registry,
    )
except Exception:  # fallback if loader not available during import
    ALLOWED_STATES = frozenset({"IMPLEMENTED", "PARTIAL", "HOLD_EXTERNAL", "NOT_PROVEN", "NOT_APPLICABLE"})
    ALLOWED_AUTONOMY = frozenset({"L0", "L1", "L2", "L3", "L4", "L5"})
    REQUIRED_DOMAINS = (
        "COMMAND","STRATEGY","REVENUE","MARKETING","BRAND","DISTRIBUTION","CLIENT","CUSTOMER_SUCCESS",
        "SUPPORT","DELIVERY","PRODUCT","ENGINEERING","PLATFORM","AI","DATA","SECURITY","PRIVACY",
        "FINANCE","TAX","LEGAL","PEOPLE","PROCUREMENT","PARTNER","B2G","GOVERNANCE","PROOF","RISK",
        "CONTINUITY","QUALITY","KNOWLEDGE","ACADEMY","LEARNING","VENTURE",
    )
    DEFAULT_REGISTRY_PATH = _REPO_ROOT / "config/company/company_constitution_registry.yaml"
    LOADER_REPO_ROOT = _REPO_ROOT

    def loader_validate_registry(data: dict[str, Any] | None = None) -> list[str]:  # type: ignore
        return []

    def loader_load_registry(path: str | Path | None = None) -> dict[str, Any]:  # type: ignore
        p = Path(path) if path is not None else Path(DEFAULT_REGISTRY_PATH)
        return yaml.safe_load(p.read_text(encoding="utf-8"))

# L5-sensitive domains that must have action_bound_l5_gate == true
L5_SENSITIVE_DOMAINS: frozenset[str] = frozenset({
    "COMMAND", "REVENUE", "MARKETING", "DISTRIBUTION", "CLIENT",
    "SECURITY", "PRIVACY", "TAX", "LEGAL", "PROCUREMENT",
    "PARTNER", "B2G", "GOVERNANCE", "VENTURE",
})

FORBIDDEN_PRODUCTION_SUBSTRINGS: tuple[str, ...] = (
    "railway",
    "vercel",
    ".github/workflows",
    "github actions",
)

ACTIVE_STATES_FOR_PRODUCTION_CHECK: frozenset[str] = frozenset({"IMPLEMENTED", "PARTIAL"})


def _repo_root_for(registry_path: Path) -> Path:
    # For canonical registry, registry lives at <repo>/config/company/...
    # For temporary mutated files (pytest tmp_path), use the loader's repo root
    # to ensure relative paths are checked against the real repo, not /tmp.
    try:
        candidate = registry_path.resolve()
        # If the file is inside the loader repo, derive from it; otherwise use loader root
        if str(candidate).startswith(str(Path(LOADER_REPO_ROOT).resolve())):
            return candidate.parents[2]
        return Path(LOADER_REPO_ROOT)
    except Exception:
        return Path(LOADER_REPO_ROOT)


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"registry YAML must be a mapping: {path}")
    return data


def verify_registry(registry_path: Path | None = None) -> dict[str, Any]:
    target = Path(registry_path) if registry_path is not None else Path(DEFAULT_REGISTRY_PATH)
    failures: list[str] = []

    if not target.is_file():
        return {"verdict": "FAIL", "failures": [f"missing_registry:{target}"], "registry": str(target)}

    try:
        data = _load_yaml(target)
    except Exception as exc:
        return {"verdict": "FAIL", "failures": [f"yaml_parse_failed:{exc}"], "registry": str(target)}

    # Base loader validation (required domains, fields, states, autonomy, schema)
    try:
        base_errors = loader_validate_registry(data)
        failures.extend(base_errors)
    except Exception as exc:
        failures.append(f"loader_validate_failed:{exc}")

    domains = data.get("domains") if isinstance(data.get("domains"), dict) else {}

    # Primary authority is unique by definition. Shared reuse belongs in authority_paths.
    if isinstance(domains, dict):
        auth_map: dict[str, list[str]] = defaultdict(list)
        for domain, entry in domains.items():
            if isinstance(entry, dict):
                pa = entry.get("primary_authority")
                if isinstance(pa, str) and pa.strip():
                    auth_map[pa.strip()].append(domain)
        for pa, dlist in auth_map.items():
            if len(dlist) > 1:
                failures.append(f"duplicate_primary_authority:{pa} -> {sorted(dlist)}")

    # Per-domain deep checks
    repo_root = _repo_root_for(target)
    if isinstance(domains, dict):
        for domain in REQUIRED_DOMAINS:
            entry = domains.get(domain)
            if not isinstance(entry, dict):
                continue

            # invalid state/autonomy already covered by base, but keep explicit for clarity
            state = entry.get("state")
            if state not in ALLOWED_STATES:
                # already reported, but ensure fail-closed if base missed
                if f"{domain}: invalid state" not in " ".join(failures):
                    failures.append(f"{domain}: invalid state '{state}'")

            autonomy = entry.get("autonomy_ceiling")
            if autonomy not in ALLOWED_AUTONOMY:
                if f"{domain}: invalid autonomy" not in " ".join(failures):
                    failures.append(f"{domain}: invalid autonomy_ceiling '{autonomy}'")

            # missing/empty evidence_refs or receipt_requirements
            for field in ("evidence_refs", "receipt_requirements"):
                vals = entry.get(field)
                if not isinstance(vals, list) or len(vals) == 0:
                    failures.append(f"{domain}: missing/empty {field}")
                else:
                    for idx, v in enumerate(vals):
                        if not isinstance(v, str) or not v.strip():
                            failures.append(f"{domain}: {field}[{idx}] must be non-empty string")

            # Local authority/evidence refs must resolve to real repo paths unless explicitly non-file.
            non_file_prefixes = ("runtime:", "receipt:", "company_brain:", "ledger:", "external:", "http://", "https://")
            path_values: list[tuple[str, str]] = []
            pa_value = entry.get("primary_authority")
            if isinstance(pa_value, str) and pa_value.strip():
                path_values.append(("primary_authority", pa_value.strip()))
            for field in ("authority_paths", "evidence_inputs", "verifier_paths", "evidence_refs"):
                vals = entry.get(field)
                if isinstance(vals, list):
                    path_values.extend((field, p.strip()) for p in vals if isinstance(p, str) and p.strip())
            for field, raw in path_values:
                if raw.startswith(non_file_prefixes):
                    continue
                candidate = Path(raw)
                if candidate.is_absolute():
                    failures.append(f"{domain}: absolute local path not allowed {field}:{raw}")
                    continue
                resolved = (repo_root / candidate).resolve()
                try:
                    resolved.relative_to(repo_root.resolve())
                except ValueError:
                    failures.append(f"{domain}: local path escapes repo {field}:{raw}")
                    continue
                if not resolved.exists():
                    failures.append(f"{domain}: missing local path {field}:{raw}")

            # L5-sensitive domains lacking action_bound_l5_gate true
            if domain in L5_SENSITIVE_DOMAINS:
                if entry.get("action_bound_l5_gate") is not True:
                    failures.append(f"{domain}: L5-sensitive requires action_bound_l5_gate true")

            # active production authority refs reintroducing Railway/Vercel/GitHub Actions
            if state in ACTIVE_STATES_FOR_PRODUCTION_CHECK:
                # check primary_authority and authority_paths only (evidence_refs may be docs)
                to_check: list[str] = []
                pa = entry.get("primary_authority")
                if isinstance(pa, str):
                    to_check.append(pa)
                for ap in entry.get("authority_paths", []) or []:
                    if isinstance(ap, str):
                        to_check.append(ap)
                for s in to_check:
                    low = s.lower()
                    for forbidden in FORBIDDEN_PRODUCTION_SUBSTRINGS:
                        if forbidden in low:
                            failures.append(f"{domain}: forbidden production runtime authority '{s}' contains '{forbidden}'")
                            break

    verdict = "FAIL" if failures else "PASS"
    return {
        "verdict": verdict,
        "failures": sorted(set(failures)),
        "registry": str(target),
        "domains_checked": len(domains) if isinstance(domains, dict) else 0,
        "required_domains": len(REQUIRED_DOMAINS),
        "l5_sensitive": sorted(L5_SENSITIVE_DOMAINS),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Company Constitution coverage")
    parser.add_argument("--registry", type=str, default=str(DEFAULT_REGISTRY_PATH), help="path to constitution registry YAML")
    args = parser.parse_args()
    receipt = verify_registry(Path(args.registry))
    # concise summary
    print(f"DEALIX_COMPANY_CONSTITUTION_COVERAGE: {receipt['verdict']} ({receipt['domains_checked']}/{receipt['required_domains']} domains)")
    if receipt["failures"]:
        print("Failures:")
        for f in receipt["failures"]:
            print(f"  - {f}")
    else:
        print("All coverage checks passed.")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
