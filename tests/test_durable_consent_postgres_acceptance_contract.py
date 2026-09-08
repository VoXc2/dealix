from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPT = ROOT / "scripts" / "ops" / "accept_durable_consent_postgres_v1.sh"
RUNNER = ROOT / "scripts" / "ops" / "run_durable_consent_postgres_acceptance_v1.sh"
BOOTSTRAP = ROOT / "scripts" / "ops" / "bootstrap_fresh_database.py"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_postgres_acceptance_uses_repository_fresh_database_bootstrap() -> None:
    for path in (ACCEPT, RUNNER):
        text = _text(path)
        assert "bootstrap_fresh_database.py" in text, path
        assert "--confirm-empty-bootstrap" in text, path
        assert "DEALIX_ALLOW_FRESH_DB_BOOTSTRAP" in text, path


def test_postgres_acceptance_does_not_replay_historical_roots_on_empty_db() -> None:
    forbidden = (
        "-m alembic upgrade head",
        "-m alembic -c \"$ROOT/alembic.ini\" upgrade head",
    )
    for path in (ACCEPT, RUNNER):
        text = _text(path)
        for token in forbidden:
            assert token not in text, f"{path}: historical empty-db replay returned: {token}"


def test_fresh_bootstrap_explains_and_guards_the_historical_root_contract() -> None:
    text = _text(BOOTSTRAP)
    normalized = " ".join(text.split())
    assert "Historical Alembic roots predate a formal baseline" in normalized
    assert "refusing fresh bootstrap on non-empty database" in text
    assert "build_fresh_schema_metadata()" in text
    assert "metadata.create_all(connection)" in text
    assert 'migration.stamp(script, "heads")' in text
    assert "compare_metadata(compare_context, metadata)" in text


def test_acceptance_remains_fail_closed_for_material_authority() -> None:
    required = (
        "DEALIX_EXTERNAL_SEND=0",
        "DEALIX_EMAIL_LIVE_SEND=0",
        "DEALIX_WHATSAPP_OUTBOUND=0",
        "DEALIX_PUBLIC_PUBLISH=0",
        "DEALIX_PAID_SPEND=0",
        "DEALIX_PAYMENT_EXECUTION=0",
        "DEALIX_PRODUCTION_MUTATION=0",
        "DEALIX_DNS_MUTATION=0",
        "DEALIX_DB_MUTATION=0",
        "DEALIX_SECRET_MUTATION=0",
        "DEALIX_IDENTITY_MUTATION=0",
    )
    for path in (ACCEPT, RUNNER):
        text = _text(path)
        for token in required:
            assert token in text, f"{path}: missing fail-closed authority flag {token}"
