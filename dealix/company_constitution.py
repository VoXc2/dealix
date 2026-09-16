"""Company Constitution Registry loader — Company Machine authority map.

Reuses existing Company Machine authorities (dealix_operating_constitution,
control_kernel, omega, arm_registry) and surfaces a single registry over 33
domains. No new domain systems are created; this module only maps and
validates existing repo paths.

Allowed states: IMPLEMENTED, PARTIAL, HOLD_EXTERNAL, NOT_PROVEN, NOT_APPLICABLE
Autonomy ceiling: L0..L5
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY_PATH = REPO_ROOT / "config" / "company" / "company_constitution_registry.yaml"

REQUIRED_DOMAINS: tuple[str, ...] = (
    "COMMAND",
    "STRATEGY",
    "REVENUE",
    "MARKETING",
    "BRAND",
    "DISTRIBUTION",
    "CLIENT",
    "CUSTOMER_SUCCESS",
    "SUPPORT",
    "DELIVERY",
    "PRODUCT",
    "ENGINEERING",
    "PLATFORM",
    "AI",
    "DATA",
    "SECURITY",
    "PRIVACY",
    "FINANCE",
    "TAX",
    "LEGAL",
    "PEOPLE",
    "PROCUREMENT",
    "PARTNER",
    "B2G",
    "GOVERNANCE",
    "PROOF",
    "RISK",
    "CONTINUITY",
    "QUALITY",
    "KNOWLEDGE",
    "ACADEMY",
    "LEARNING",
    "VENTURE",
)

ALLOWED_STATES: frozenset[str] = frozenset(
    {"IMPLEMENTED", "PARTIAL", "HOLD_EXTERNAL", "NOT_PROVEN", "NOT_APPLICABLE"}
)

ALLOWED_AUTONOMY: frozenset[str] = frozenset({"L0", "L1", "L2", "L3", "L4", "L5"})

REQUIRED_FIELDS: tuple[str, ...] = (
    "primary_authority",
    "authority_paths",
    "evidence_inputs",
    "verifier_paths",
    "autonomy_ceiling",
    "receipt_requirements",
    "state",
    "evidence_refs",
)

# action_bound_l5_gate is required where applicable; validate if present must be bool
OPTIONAL_FIELDS: tuple[str, ...] = ("action_bound_l5_gate", "description")

NON_FILE_PREFIXES: tuple[str, ...] = (
    "runtime:", "receipt:", "company_brain:", "ledger:", "external:", "http://", "https://",
)


def _validate_local_ref(domain: str, field: str, value: str, errors: list[str]) -> None:
    raw = value.strip()
    if not raw or raw.startswith(NON_FILE_PREFIXES):
        return
    candidate = Path(raw)
    if candidate.is_absolute():
        errors.append(f"{domain}: absolute local path not allowed {field}:{raw}")
        return
    resolved = (REPO_ROOT / candidate).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError:
        errors.append(f"{domain}: local path escapes repo {field}:{raw}")
        return
    if not resolved.exists():
        errors.append(f"{domain}: missing local path {field}:{raw}")


def _load_raw(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"registry YAML must be a mapping, got {type(data).__name__}")
    return data


@lru_cache(maxsize=4)
def load_registry(path: str | Path | None = None) -> dict[str, Any]:
    """Parse YAML using existing dependency (pyyaml) and return raw mapping."""
    target = Path(path) if path is not None else DEFAULT_REGISTRY_PATH
    if not target.exists():
        raise FileNotFoundError(f"constitution registry not found: {target}")
    data = _load_raw(target)
    # basic top-level sanity without hardcoding provider/sha/counts
    if "domains" not in data or not isinstance(data["domains"], dict):
        raise ValueError("registry missing 'domains' mapping")
    return data


def validate_registry(data: dict[str, Any] | None = None) -> list[str]:
    """Validate required domains, fields, states and autonomy ceilings.

    Returns a list of error strings; empty list means valid.
    Never performs production/DB/DNS/secrets/provider/external effects.
    """
    errors: list[str] = []
    if data is None:
        try:
            data = load_registry()
        except Exception as exc:  # noqa: BLE001 - surface as validation error
            return [f"load_failed: {exc}"]

    domains = data.get("domains")
    if not isinstance(domains, dict):
        errors.append("domains must be a mapping")
        return errors

    # exactly 33 required domains
    actual = set(domains.keys())
    expected = set(REQUIRED_DOMAINS)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"missing_domains: {missing}")
    if extra:
        errors.append(f"extra_domains: {extra}")
    if len(actual) != len(REQUIRED_DOMAINS):
        errors.append(f"domain_count_mismatch: expected {len(REQUIRED_DOMAINS)} got {len(actual)}")

    primary_authorities: dict[str, list[str]] = {}

    for domain in REQUIRED_DOMAINS:
        entry = domains.get(domain)
        if entry is None:
            continue
        if not isinstance(entry, dict):
            errors.append(f"{domain}: entry must be a mapping")
            continue
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{domain}: missing required field '{field}'")
        # type checks for list fields
        for list_field in ("authority_paths", "evidence_inputs", "verifier_paths", "receipt_requirements", "evidence_refs"):
            if list_field in entry and not isinstance(entry[list_field], list):
                errors.append(f"{domain}: '{list_field}' must be a list")
            elif list_field in entry and isinstance(entry[list_field], list) and len(entry[list_field]) == 0:
                errors.append(f"{domain}: '{list_field}' must be non-empty")

        if "primary_authority" in entry and not isinstance(entry["primary_authority"], str):
            errors.append(f"{domain}: primary_authority must be a string")
        elif "primary_authority" in entry and not str(entry["primary_authority"]).strip():
            errors.append(f"{domain}: primary_authority must be non-empty")
        else:
            primary = str(entry.get("primary_authority", "")).strip()
            if primary:
                primary_authorities.setdefault(primary, []).append(domain)
                _validate_local_ref(domain, "primary_authority", primary, errors)

        state = entry.get("state")
        if state is not None and state not in ALLOWED_STATES:
            errors.append(f"{domain}: invalid state '{state}' not in {sorted(ALLOWED_STATES)}")

        autonomy = entry.get("autonomy_ceiling")
        if autonomy is not None and autonomy not in ALLOWED_AUTONOMY:
            errors.append(f"{domain}: invalid autonomy_ceiling '{autonomy}' not in {sorted(ALLOWED_AUTONOMY)}")

        if "action_bound_l5_gate" in entry and not isinstance(entry["action_bound_l5_gate"], bool):
            errors.append(f"{domain}: action_bound_l5_gate must be boolean")

        # Ensure path-bearing references are strings and resolve inside the canonical repo.
        for pf in ("authority_paths", "evidence_inputs", "verifier_paths", "evidence_refs"):
            vals = entry.get(pf)
            if isinstance(vals, list):
                for idx, val in enumerate(vals):
                    if not isinstance(val, str) or not val.strip():
                        errors.append(f"{domain}: {pf}[{idx}] must be non-empty string")
                        continue
                    _validate_local_ref(domain, pf, val, errors)

    for primary, owners in sorted(primary_authorities.items()):
        if len(owners) > 1:
            errors.append(f"duplicate_primary_authority:{primary} -> {sorted(owners)}")

    # top-level schema sanity
    if data.get("schema") != "dealix.company_constitution_registry.v1":
        errors.append("schema must be 'dealix.company_constitution_registry.v1'")
    if "schema_version" not in data:
        errors.append("schema_version is required")
    return errors


def summary(data: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return counts per state and autonomy, plus domain list."""
    if data is None:
        data = load_registry()
    domains = data.get("domains", {}) if isinstance(data.get("domains"), dict) else {}
    by_state: dict[str, int] = {s: 0 for s in sorted(ALLOWED_STATES)}
    by_autonomy: dict[str, int] = {a: 0 for a in sorted(ALLOWED_AUTONOMY)}
    l5_gated = 0
    for entry in domains.values():
        if not isinstance(entry, dict):
            continue
        st = entry.get("state")
        if st in by_state:
            by_state[st] += 1
        au = entry.get("autonomy_ceiling")
        if au in by_autonomy:
            by_autonomy[au] += 1
        if entry.get("action_bound_l5_gate") is True:
            l5_gated += 1
    return {
        "total_domains": len(domains),
        "required_domains": len(REQUIRED_DOMAINS),
        "by_state": by_state,
        "by_autonomy": by_autonomy,
        "l5_gated_domains": l5_gated,
        "domains": sorted(domains.keys()),
        "validation_errors": validate_registry(data),
        "is_valid": len(validate_registry(data)) == 0,
    }


def gap_report(data: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return gaps: domains not IMPLEMENTED and their state/autonomy."""
    if data is None:
        data = load_registry()
    domains = data.get("domains", {}) if isinstance(data.get("domains"), dict) else {}
    gaps: list[dict[str, Any]] = []
    implemented: list[str] = []
    for name in REQUIRED_DOMAINS:
        entry = domains.get(name)
        if not isinstance(entry, dict):
            gaps.append({"domain": name, "state": "MISSING", "autonomy_ceiling": None, "primary_authority": None})
            continue
        state = entry.get("state")
        if state == "IMPLEMENTED":
            implemented.append(name)
        else:
            gaps.append(
                {
                    "domain": name,
                    "state": state,
                    "autonomy_ceiling": entry.get("autonomy_ceiling"),
                    "primary_authority": entry.get("primary_authority"),
                    "action_bound_l5_gate": entry.get("action_bound_l5_gate"),
                }
            )
    return {
        "total": len(REQUIRED_DOMAINS),
        "implemented": len(implemented),
        "gap_count": len(gaps),
        "implemented_domains": sorted(implemented),
        "gaps": sorted(gaps, key=lambda x: x["domain"]),
        "is_complete": len(gaps) == 0,
    }


__all__ = [
    "REQUIRED_DOMAINS",
    "ALLOWED_STATES",
    "ALLOWED_AUTONOMY",
    "REQUIRED_FIELDS",
    "DEFAULT_REGISTRY_PATH",
    "load_registry",
    "validate_registry",
    "summary",
    "gap_report",
]
