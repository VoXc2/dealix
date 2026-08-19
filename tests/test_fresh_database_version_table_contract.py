"""Regression contract for Dealix's long Alembic revision identifiers."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = (ROOT / "scripts" / "ops" / "bootstrap_fresh_database.py").read_text(
    encoding="utf-8"
)
VERSIONS = ROOT / "db" / "migrations" / "versions"


def test_repo_contains_revision_ids_longer_than_alembic_default() -> None:
    revision_ids: list[str] = []
    for path in VERSIONS.glob("*.py"):
        text = path.read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("revision") and "=" in stripped:
                value = stripped.split("=", 1)[1].strip().strip('"\'')
                if value and value != "None":
                    revision_ids.append(value)
                break
    assert revision_ids
    assert max(map(len, revision_ids)) > 32


def test_fresh_bootstrap_precreates_wide_standard_version_table() -> None:
    assert 'ALEMBIC_VERSION_LENGTH = 255' in BOOTSTRAP
    assert '"alembic_version"' in BOOTSTRAP
    assert '"version_num"' in BOOTSTRAP
    assert "String(ALEMBIC_VERSION_LENGTH)" in BOOTSTRAP
    assert "_ensure_wide_alembic_version_table(connection)" in BOOTSTRAP
    assert BOOTSTRAP.index("_ensure_wide_alembic_version_table(connection)") < BOOTSTRAP.index(
        'migration.stamp(script, "heads")'
    )
