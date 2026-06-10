"""Phase E sample-artifact contract.

Guards `docs/proof-events/SCHEMA.example.json` so a future careless edit
cannot break the founder's copy-paste-ready ProofEvent template.

Hard rules enforced here:
  1. The sample file exists and is valid JSON.
  2. The JSON parses cleanly into a `ProofEvent` Pydantic model.
  3. The sample contains zero forbidden marketing tokens
     (نضمن / guaranteed / blast / scrape) anywhere in its text.
  4. `consent_for_publication` stays `false` so the example
     never accidentally leaks as a publishable artifact.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.proof_ledger.schemas import ProofEvent

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = REPO_ROOT / "docs" / "proof-events" / "SCHEMA.example.json"

FORBIDDEN_TOKENS = ("نضمن", "guaranteed", "blast", "scrape")


@pytest.fixture(scope="module")
def sample_text() -> str:
    assert SAMPLE_PATH.exists(), f"Missing sample at {SAMPLE_PATH}"
    return SAMPLE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def sample_data(sample_text: str) -> dict:
    return json.loads(sample_text)


def test_sample_file_exists_and_is_valid_json(sample_data: dict) -> None:
    """Rule 1: the example file is present and parses as JSON."""
    assert isinstance(sample_data, dict), "Sample must be a JSON object"
    assert sample_data.get("event_type"), "Sample must declare event_type"


def test_sample_round_trips_through_proof_event_model(sample_data: dict) -> None:
    """Rule 2: the JSON must validate as a ProofEvent and round-trip."""
    event = ProofEvent.model_validate(sample_data)
    # Round-trip check — re-serialize and re-load to catch silent
    # field-coercion drift (e.g. enum aliasing or extras=forbid).
    redumped = json.loads(event.model_dump_json())
    revalidated = ProofEvent.model_validate(redumped)
    assert revalidated.id == event.id
    assert revalidated.event_type == event.event_type


def test_sample_contains_no_forbidden_marketing_tokens(sample_text: str) -> None:
    """Rule 3: forbidden tokens must never appear in the sample."""
    lowered = sample_text.lower()
    for token in FORBIDDEN_TOKENS:
        # Arabic token is non-ASCII; check raw text. English tokens
        # are case-folded for safety.
        if token.isascii():
            assert token not in lowered, (
                f"Sample contains forbidden marketing token: {token!r}"
            )
        else:
            assert token not in sample_text, (
                f"Sample contains forbidden Arabic marketing token: {token!r}"
            )


def test_sample_consent_for_publication_is_false(sample_data: dict) -> None:
    """Rule 4: the sample stays internal-only by default."""
    assert sample_data.get("consent_for_publication") is False, (
        "Sample must keep consent_for_publication=false to stay internal."
    )
    # Also check the parsed model agrees — guards against type drift.
    event = ProofEvent.model_validate(sample_data)
    assert event.consent_for_publication is False
    assert event.approval_status == "approval_required"
