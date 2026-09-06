from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "ops" / "verify_autonomous_company_machine_v2.py"
CONTRACT = ROOT / "data" / "ops" / "dealix_autonomous_company_machine_v2.json"


def _load_verifier():
    spec = importlib.util.spec_from_file_location("verify_autonomous_company_machine_v2", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stale_source_and_wip_metadata_do_not_false_fail_exact_source(tmp_path, monkeypatch) -> None:
    verifier = _load_verifier()
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    data["source_main_sha"] = "1" * 40
    data["active_wip"] = {
        "p0": "MERGED:#1329",
        "p1": "MERGED:#1335_SUPERSEDES_#1330",
    }
    contract = tmp_path / "contract.json"
    contract.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(verifier, "CONTRACT", contract)

    current_source = "2" * 40
    errors, metadata = verifier.verify(current_source)

    assert errors == []
    assert metadata["contract_source_sha"] == "1" * 40
    assert metadata["source_metadata"] == "SUPERSEDED"
    assert metadata["active_wip_metadata"] == "NON_AUTHORITATIVE_HISTORICAL_PROVENANCE"


def test_current_contract_source_is_classified_current(tmp_path, monkeypatch) -> None:
    verifier = _load_verifier()
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    current_source = "a" * 40
    data["source_main_sha"] = current_source
    contract = tmp_path / "contract.json"
    contract.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(verifier, "CONTRACT", contract)

    errors, metadata = verifier.verify(current_source)

    assert errors == []
    assert metadata["source_metadata"] == "CURRENT"


def test_explicit_source_sha_validation() -> None:
    verifier = _load_verifier()
    assert verifier.resolve_source_sha("b" * 40) == "b" * 40

    try:
        verifier.resolve_source_sha("not-a-sha")
    except ValueError as exc:
        assert str(exc) == "invalid_source_sha"
    else:
        raise AssertionError("invalid source SHA must fail closed")


def test_active_wip_shape_is_still_validated(tmp_path, monkeypatch) -> None:
    verifier = _load_verifier()
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    data["active_wip"] = ["not", "an", "object"]
    contract = tmp_path / "contract.json"
    contract.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(verifier, "CONTRACT", contract)

    errors, _ = verifier.verify("c" * 40)

    assert "active_wip_metadata_not_object" in errors
