from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_iac_source_is_present_and_provider_safe() -> None:
    text = (ROOT / ".railway" / "railway.ts").read_text(encoding="utf-8")
    assert 'project("Dealix"' in text
    assert 'service("dealix"' in text
    assert 'service("web"' in text
    assert 'postgres("Postgres"' in text
    assert text.count('checkSuites: true') == 2
    assert 'checkSuites: false' not in text
    for path in (
        "/api/**", "/app/**", "/db/**", "/dealix/**",
        "/alembic/**", "/alembic.ini",
    ):
        assert path in text
    assert "railway config apply" not in text


def test_migration_runbook_is_explicitly_non_applying() -> None:
    text = (ROOT / ".railway" / "README.md").read_text(encoding="utf-8")
    assert "2026-12-01" in text
    assert "Never run `railway config apply`" in text
    assert "exact action-bound" in text
    assert "Do not set `checkSuites: false`" in text
    assert "disable Railway GitHub autodeploy" in text
    assert "explicit accepted commit SHA" in text
