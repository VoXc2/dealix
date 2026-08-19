"""Production trust smoke workflows must fail truthfully and remain runnable."""

from __future__ import annotations

import json
from types import SimpleNamespace

import scripts.production_smoke_auth as smoke_auth
from scripts.dealix_smoke_test import APIKeyCandidate


def _clear_key_envs(monkeypatch) -> None:
    for name in (*smoke_auth._SINGLE_KEY_ENVS, *smoke_auth._BUNDLE_KEY_ENVS):
        monkeypatch.delenv(name, raising=False)


def test_candidates_preserve_precedence_and_deduplicate(monkeypatch) -> None:
    _clear_key_envs(monkeypatch)
    monkeypatch.setenv("DEALIX_SMOKE_API_KEY", "stale")
    monkeypatch.setenv("DEALIX_API_KEY", "shared")
    monkeypatch.setenv("API_KEYS", "shared,valid-two")

    candidates = smoke_auth.configured_api_key_candidates()

    assert [(row.source, row.value) for row in candidates] == [
        ("DEALIX_SMOKE_API_KEY", "stale"),
        ("DEALIX_API_KEY", "shared"),
        ("API_KEYS", "valid-two"),
    ]


def test_selector_falls_back_after_rejected_dedicated_key(monkeypatch) -> None:
    candidates = [
        APIKeyCandidate(value="stale", source="DEALIX_SMOKE_API_KEY"),
        APIKeyCandidate(value="valid", source="API_KEYS"),
    ]
    seen: list[str] = []

    def fake_request(base_url, check, timeout, api_key=""):
        del base_url, check, timeout
        seen.append(api_key)
        return SimpleNamespace(status=401 if api_key == "stale" else 200)

    monkeypatch.setattr(smoke_auth, "_do_request", fake_request)
    selected = smoke_auth.select_api_key_candidate("https://api.example", 1.0, candidates)

    assert selected.candidate.source == "API_KEYS"
    assert selected.candidate.value == "valid"
    assert selected.configured_count == 2
    assert selected.tried_count == 2
    assert selected.all_rejected is False
    assert seen == ["stale", "valid"]


def test_selector_reports_all_rejected_without_logging_values(monkeypatch) -> None:
    candidates = [
        APIKeyCandidate(value="secret-one", source="DEALIX_SMOKE_API_KEY"),
        APIKeyCandidate(value="secret-two", source="DEALIX_API_KEY"),
    ]

    monkeypatch.setattr(
        smoke_auth,
        "_do_request",
        lambda base_url, check, timeout, api_key="": SimpleNamespace(status=401),
    )
    selected = smoke_auth.select_api_key_candidate("https://api.example", 1.0, candidates)

    assert selected.all_rejected is True
    assert selected.configured_count == 2
    assert selected.tried_count == 2
    assert selected.candidate.source == "DEALIX_SMOKE_API_KEY"


def test_all_rejected_marker_does_not_claim_canonical_smoke_ran(
    monkeypatch,
    capsys,
) -> None:
    secret = "secret-that-must-not-be-logged"
    selection = smoke_auth.AuthSelection(
        candidate=APIKeyCandidate(value=secret, source="DEALIX_SMOKE_API_KEY"),
        configured_count=1,
        tried_count=1,
        all_rejected=True,
    )
    monkeypatch.setattr(smoke_auth, "configured_api_key_candidates", lambda: [selection.candidate])
    monkeypatch.setattr(
        smoke_auth,
        "select_api_key_candidate",
        lambda base_url, timeout, candidates: selection,
    )
    monkeypatch.setattr(
        smoke_auth,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not run")),
    )

    rc = smoke_auth.main(["--base-url", "https://api.example", "--json"])
    output = capsys.readouterr().out
    marker = json.loads(output)

    assert rc == 3
    assert marker["canonical_smoke_executed"] is False
    assert marker["authenticated_details_logged"] is False
    assert marker["result_source"] == "process_exit_code"
    assert secret not in output


def test_success_marker_claims_canonical_smoke_only_after_run(
    monkeypatch,
    capsys,
) -> None:
    secret = "valid-secret-that-must-not-be-logged"
    selection = smoke_auth.AuthSelection(
        candidate=APIKeyCandidate(value=secret, source="API_KEYS"),
        configured_count=1,
        tried_count=1,
        all_rejected=False,
    )
    monkeypatch.setattr(smoke_auth, "configured_api_key_candidates", lambda: [selection.candidate])
    monkeypatch.setattr(
        smoke_auth,
        "select_api_key_candidate",
        lambda base_url, timeout, candidates: selection,
    )
    monkeypatch.setattr(
        smoke_auth,
        "run",
        lambda *args, **kwargs: {
            "results": [{"status": 200}],
            "total": 1,
            "failed_required": 0,
        },
    )

    rc = smoke_auth.main(["--base-url", "https://api.example", "--json"])
    output = capsys.readouterr().out
    marker = json.loads(output)

    assert rc == 0
    assert marker["canonical_smoke_executed"] is True
    assert marker["authenticated_details_logged"] is False
    assert marker["result_source"] == "process_exit_code"
    assert secret not in output


def test_workflow_uses_auth_fallback_wrapper() -> None:
    workflow = smoke_auth.ROOT / ".github" / "workflows" / "production-smoke.yml"
    text = workflow.read_text(encoding="utf-8")
    assert "python scripts/production_smoke_auth.py" in text
    assert "DEALIX_SMOKE_API_KEY" in text
    assert "DEALIX_API_KEY" in text
    assert "API_KEYS" in text


def test_production_api_trust_workflow_installs_project_dependencies() -> None:
    workflow = (
        smoke_auth.ROOT
        / ".github"
        / "workflows"
        / "production_api_trust_smoke.yml"
    )
    text = workflow.read_text(encoding="utf-8")

    assert "pip install -r requirements.txt" in text
    assert "pip install -e ." in text
    assert "pytest tests/test_railway_production_config.py" in text
    assert "timeout-minutes: 20" in text
