"""Shared utilities for Dealix launch checks and the dealix CLI.

Pure stdlib + PyYAML. No other third-party dependencies so the checks run
deterministically in CI. Every check imports from here so the contracts
(required fields, banned phrases, expected counts) live in exactly one place.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - yaml is a hard dependency, guarded for clarity
    yaml = None


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]


def rel(path: str | Path) -> Path:
    """Resolve a repo-relative path to an absolute Path."""
    return ROOT / Path(path)


# --------------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------------
def load_yaml(path: str | Path) -> Any:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required; install it with `pip install pyyaml`.")
    with open(rel(path), "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_json(path: str | Path) -> Any:
    with open(rel(path), "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_jsonl(path: str | Path) -> list[dict]:
    rows: list[dict] = []
    with open(rel(path), "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{i} invalid JSON line: {exc}") from exc
    return rows


# --------------------------------------------------------------------------
# Canonical references derived from generated data (single source of truth)
# --------------------------------------------------------------------------
def core_system_ids() -> list[str]:
    needs = load_yaml("data/business_need_intelligence/need_taxonomy_25.yaml")["needs"]
    return sorted({n["core_system"] for n in needs})


def core_system_names() -> dict[str, str]:
    gates = load_jsonl("data/delivery/acceptance_gates.jsonl")
    return {g["system_id"]: g["system"] for g in gates}


# --------------------------------------------------------------------------
# Contracts: required fields and expected counts
# --------------------------------------------------------------------------
# Core taxonomy sizes (the spec's "readiness conditions").
EXPECTED_CORE_SYSTEMS = 5
EXPECTED_BUSINESS_SYSTEMS = 40
EXPECTED_NEEDS = 25
EXPECTED_SECTORS = 20
EXPECTED_SPRINTS = 50

# Account Pack output contract — every nightly pack must carry these 27 keys.
ACCOUNT_PACK_FIELDS = [
    "company_name", "website", "sector", "city", "country",
    "signals_detected", "detected_business_needs", "primary_need",
    "recommended_core_system", "recommended_specialized_system",
    "sector_specific_sprint", "delivery_variant", "buyer_roles",
    "contact_confidence", "email_angle", "call_angle", "mini_proposal_title",
    "required_inputs", "acceptance_criteria", "cash_priority_score",
    "need_fit_score", "account_score", "final_account_score", "next_action",
    # provenance / policy fields
    "record_type", "source", "generated_at",
]

# Every internal business system (catalog) must carry these keys.
BUSINESS_SYSTEM_FIELDS = [
    "core_system_mapping", "entry_sprint", "starter_price", "deliverables",
    "required_inputs", "acceptance_criteria", "buyer_role", "email_angle",
    "upsell_path",
]

# Email draft contract.
EMAIL_DRAFT_FIELDS = [
    "draft_id", "company_name", "system", "evidence_level", "subject",
    "body", "approval_required",
]

# Mini proposal contract.
MINI_PROPOSAL_FIELDS = [
    "proposal_id", "company_name", "title", "price", "currency", "scope",
    "required_inputs", "acceptance_criteria", "approval_required", "status",
]

# Phrases that are never allowed in prospect-facing copy (no guaranteed claims).
GUARANTEE_BANNED = [
    "نضمن", "مضمون", "نتائج مضمونة", "نتائج مؤكدة", "نعدك بـ", "نعدكم",
    "guarantee", "guaranteed", "100%", "%100", "زيادة مؤكدة", "بدون أي مخاطرة",
    "نضاعف أرباحك", "أرباح مضمونة",
]

# Fake reply/forward prefixes that fabricate prior conversation in cold email.
FAKE_THREAD_PREFIXES = ["re:", "re :", "fwd:", "fw:", "رد:", "إعادة توجيه:"]

VALID_EVIDENCE_LEVELS = ["high", "medium", "low", "inferred"]
VALID_CONTACT_CONFIDENCE = ["high", "medium", "low", "unknown", "missing"]


# --------------------------------------------------------------------------
# Minimal JSON-Schema validator (draft-07 subset)
# --------------------------------------------------------------------------
def validate_instance(instance: Any, schema: dict, path: str = "$") -> list[str]:
    """Validate `instance` against a JSON-Schema subset.

    Supported keywords: type, required, properties, items, enum, minimum,
    maximum, minItems, additionalProperties(False only as a soft check skipped).
    Returns a list of human-readable error strings (empty == valid).
    """
    errors: list[str] = []
    if not isinstance(schema, dict):
        return errors

    expected = schema.get("type")
    if expected is not None and not _type_ok(instance, expected):
        errors.append(f"{path}: expected type {expected}, got {_jtype(instance)}")
        return errors  # further checks are meaningless on a type mismatch

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property '{key}'")
        props = schema.get("properties", {})
        for key, subschema in props.items():
            if key in instance:
                errors.extend(validate_instance(instance[key], subschema, f"{path}.{key}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items, got {len(instance)}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(instance):
                errors.extend(validate_instance(item, item_schema, f"{path}[{idx}]"))

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    return errors


def _jtype(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "null"
    return type(value).__name__


def _type_ok(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(_type_ok(value, e) for e in expected)
    actual = _jtype(value)
    if expected == "number":
        return actual in ("number", "integer")
    return actual == expected


# --------------------------------------------------------------------------
# Text scanning helpers
# --------------------------------------------------------------------------
def find_banned(text: str, banned: Iterable[str]) -> list[str]:
    low = (text or "").lower()
    hits = []
    for phrase in banned:
        if phrase.lower() in low:
            hits.append(phrase)
    return hits


# --------------------------------------------------------------------------
# Check result plumbing
# --------------------------------------------------------------------------
class CheckResult:
    def __init__(self, name: str):
        self.name = name
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)

    @property
    def passed(self) -> bool:
        return not self.errors

    def require(self, condition: bool, msg: str) -> bool:
        if not condition:
            self.error(msg)
        return condition


def run_check(result: CheckResult) -> int:
    """Print a check result and return an exit code (0 == pass)."""
    status = "PASS" if result.passed else "FAIL"
    print(f"[{status}] {result.name}")
    for msg in result.info:
        print(f"   - {msg}")
    for msg in result.warnings:
        print(f"   ! {msg}")
    for msg in result.errors:
        print(f"   x {msg}")
    return 0 if result.passed else 1


def main(check_fn) -> None:
    """Entry-point wrapper: run a check function returning a CheckResult."""
    result = check_fn()
    sys.exit(run_check(result))
