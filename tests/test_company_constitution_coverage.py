"""Tests for Company Constitution coverage verifier (Stage B).

Covers happy path and each fail-closed rule using temporary mutated registry files,
never modifying the canonical registry. Reuses existing loader and verifier.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "config/company/company_constitution_registry.yaml"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.company_constitution import REQUIRED_DOMAINS, gap_report, load_registry, summary, validate_registry
from scripts.ops.verify_company_constitution_coverage import L5_SENSITIVE_DOMAINS, verify_registry


def _load_canonical() -> dict:
    return yaml.safe_load(DEFAULT_REGISTRY.read_text(encoding="utf-8"))


def _write_mutated(tmp_path: Path, mutator) -> Path:
    data = _load_canonical()
    mutated = copy.deepcopy(data)
    mutator(mutated)
    out = tmp_path / "mutated.yaml"
    out.write_text(yaml.safe_dump(mutated, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out


# --- original Stage B happy-path / coverage tests (kept for compatibility) ---

def test_registry_covers_exact_required_domains_without_fake_complete() -> None:
    registry = load_registry()
    assert set(registry["domains"]) == set(REQUIRED_DOMAINS)
    assert validate_registry(registry) == []
    report = summary(registry)
    assert report["is_valid"] is True
    assert report["by_state"]["IMPLEMENTED"] < report["total_domains"]
    assert gap_report(registry)["is_complete"] is False


def test_l5_sensitive_domains_are_action_bound() -> None:
    registry = load_registry()
    for domain, entry in registry["domains"].items():
        if entry.get("action_bound_l5_gate"):
            assert entry["autonomy_ceiling"] != "L5"


def test_loader_fails_closed_when_required_evidence_is_missing() -> None:
    registry = copy.deepcopy(load_registry())
    registry["domains"]["REVENUE"]["evidence_refs"] = []
    errors = validate_registry(registry)
    assert errors
    assert any("REVENUE" in error for error in errors)


def test_deep_verifier_passes_canonical_registry() -> None:
    receipt = verify_registry()
    assert receipt["verdict"] == "PASS"
    assert receipt["domains_checked"] == len(REQUIRED_DOMAINS)


# --- extended fail-closed coverage (mutated temp files) ---

def test_happy_path_passes():
    receipt = verify_registry(DEFAULT_REGISTRY)
    assert receipt["verdict"] == "PASS", receipt["failures"]


def test_missing_required_domain_fails(tmp_path):
    def mutator(d):
        d["domains"].pop("REVENUE")
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("missing_domains" in f or "REVENUE" in f for f in receipt["failures"])


def test_duplicate_primary_authority_without_marker_fails(tmp_path):
    def mutator(d):
        d["domains"]["BRAND"]["primary_authority"] = d["domains"]["REVENUE"]["primary_authority"]
        d["domains"]["BRAND"].pop("shared_authority", None)
        d["domains"]["REVENUE"].pop("shared_authority", None)
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("duplicate_primary_authority" in f for f in receipt["failures"])


def test_duplicate_primary_authority_with_marker_still_fails(tmp_path):
    def mutator(d):
        d["domains"]["BRAND"]["primary_authority"] = d["domains"]["REVENUE"]["primary_authority"]
        d["domains"]["BRAND"]["shared_authority"] = True
        d["domains"]["REVENUE"]["shared_authority"] = True
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("duplicate_primary_authority" in f for f in receipt["failures"])


def test_loader_rejects_duplicate_primary_authority_directly() -> None:
    registry = copy.deepcopy(load_registry())
    registry["domains"]["BRAND"]["primary_authority"] = registry["domains"]["REVENUE"]["primary_authority"]
    registry["domains"]["BRAND"]["shared_authority"] = True
    registry["domains"]["REVENUE"]["shared_authority"] = True
    errors = validate_registry(registry)
    assert any("duplicate_primary_authority" in error for error in errors)


def test_loader_rejects_missing_local_path_directly() -> None:
    registry = copy.deepcopy(load_registry())
    registry["domains"]["REVENUE"]["authority_paths"].append("docs/nonexistent/LOADER_MUST_FAIL.md")
    errors = validate_registry(registry)
    assert any("missing local path" in error and "LOADER_MUST_FAIL" in error for error in errors)


def test_invalid_state_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["state"] = "INVALID_STATE"
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("invalid state" in f.lower() or "INVALID_STATE" in f for f in receipt["failures"])


def test_invalid_autonomy_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["autonomy_ceiling"] = "L9"
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("autonomy" in f.lower() for f in receipt["failures"])


def test_missing_evidence_refs_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["evidence_refs"] = []
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("evidence_refs" in f for f in receipt["failures"])


def test_missing_receipt_requirements_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["receipt_requirements"] = []
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("receipt_requirements" in f for f in receipt["failures"])


def test_nonexistent_local_path_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["authority_paths"].append("nonexistent/path/that/does/not/exist.py")
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("missing local path" in f for f in receipt["failures"])


def test_nonexistent_evidence_ref_path_fails(tmp_path):
    def mutator(d):
        d["domains"]["REVENUE"]["evidence_refs"].append("docs/nonexistent/FAKE_DOC.md")
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("missing local path" in f and "FAKE_DOC" in f for f in receipt["failures"])


def test_l5_sensitive_missing_gate_fails(tmp_path):
    target = next(iter(sorted(L5_SENSITIVE_DOMAINS)))
    def mutator(d):
        d["domains"][target]["action_bound_l5_gate"] = False
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("L5-sensitive" in f for f in receipt["failures"])


@pytest.mark.parametrize("forbidden", ["railway", "vercel", ".github/workflows", "github actions"])
def test_forbidden_production_runtime_authority_fails(tmp_path, forbidden):
    def mutator(d):
        d["domains"]["REVENUE"]["authority_paths"].append(f"deploy/{forbidden}/production")
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("forbidden production" in f.lower() for f in receipt["failures"])


def test_forbidden_production_not_flagged_when_not_active(tmp_path):
    def mutator(d):
        # PEOPLE is NOT_PROVEN, not active, so even existing railway doc should not trigger forbidden when in PEOPLE
        d["domains"]["PEOPLE"]["authority_paths"] = ["docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md"]
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "PASS", receipt["failures"]


def test_extra_domain_fails(tmp_path):
    def mutator(d):
        d["domains"]["FAKE_DOMAIN"] = {
            "primary_authority": "x",
            "state": "IMPLEMENTED",
            "autonomy_ceiling": "L3",
            "authority_paths": ["dealix/company_constitution.py"],
            "evidence_inputs": ["dealix/company_constitution.py"],
            "verifier_paths": ["dealix/company_constitution.py"],
            "receipt_requirements": ["a"],
            "evidence_refs": ["docs/company/DEALIX_CONSTITUTION.md"],
            "action_bound_l5_gate": False,
        }
    p = _write_mutated(tmp_path, mutator)
    receipt = verify_registry(p)
    assert receipt["verdict"] == "FAIL"
    assert any("extra_domains" in f or "FAKE_DOMAIN" in f for f in receipt["failures"])
