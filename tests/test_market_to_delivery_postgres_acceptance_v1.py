from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "commercial" / "verify_market_to_delivery_postgres_v1.py"
RUNNER = ROOT / "scripts" / "commercial" / "run_market_to_delivery_postgres_acceptance_v1.sh"


def load_module():
    spec = importlib.util.spec_from_file_location("mtd_postgres_acceptance", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_url_guard_accepts_only_named_loopback_ephemeral_postgres():
    module = load_module()
    safe = module.validated_test_url(
        "postgresql+asyncpg://u:p@127.0.0.1:55432/dealix_mtd_acceptance_fixture"
    )
    assert safe.host == "127.0.0.1"
    assert safe.database.startswith(module.DB_PREFIX)

    for unsafe in (
        "postgresql+asyncpg://u:p@db.internal:5432/dealix_mtd_acceptance_fixture",
        "postgresql+asyncpg://u:p@127.0.0.1:5432/dealix",
        "sqlite+aiosqlite:///tmp/dealix_mtd_acceptance_fixture.db",
    ):
        with pytest.raises(SystemExit):
            module.validated_test_url(unsafe)


def test_runner_is_loopback_ephemeral_and_no_implicit_image_pull():
    text = RUNNER.read_text(encoding="utf-8")
    assert '-p "127.0.0.1:${PORT}:5432"' in text
    assert 'VOLUME="dealix-mtd-pg-vol-' in text
    assert "docker restart" in text
    assert "docker volume rm -f" in text
    assert "DEALIX_ALLOW_TEST_IMAGE_PULL" in text
    assert '"${DEALIX_ALLOW_TEST_IMAGE_PULL:-0}" != "1"' in text
    assert "production_db=false" in text
    assert "customer_effects=false" in text


def test_verifier_has_two_restart_phases_and_truth_guards():
    text = VERIFIER.read_text(encoding="utf-8")
    assert 'choices=["setup-race", "replay-after-restart"]' in text
    assert "MTD_POSTGRES_CONCURRENT_IDEMPOTENCY=PASS" in text
    assert "MTD_POSTGRES_RESTART_REPLAY=PASS" in text
    assert "market_to_delivery_request_id_payload_conflict" in text
    assert "RELATIONSHIP_AUTHORITY_DRIFT" in text
    assert "CONSENT_AUTHORITY_DRIFT" in text
    assert "OPPORTUNITY_AUTHORITY_DRIFT" in text
    assert "EXTERNAL_EFFECT_DRIFT" in text
