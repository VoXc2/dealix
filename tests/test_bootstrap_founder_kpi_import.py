"""Bootstrap founder KPI import from example."""

from __future__ import annotations

from pathlib import Path

from scripts.bootstrap_founder_kpi_import import EXAMPLE, TARGET, bootstrap


def test_bootstrap_creates_from_example(tmp_path: Path, monkeypatch) -> None:
    example = tmp_path / "example.yaml"
    target = tmp_path / "import.yaml"
    example.write_text(
        "version: 1\nentries:\n  measured_customer_value_sar:\n"
        "    value_numeric: 0.0\n    source_ref: crm:test:not_synced_yet\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("scripts.bootstrap_founder_kpi_import.EXAMPLE", example)
    monkeypatch.setattr("scripts.bootstrap_founder_kpi_import.TARGET", target)

    first = bootstrap()
    assert first["created"] is True
    assert target.is_file()

    second = bootstrap()
    assert second["created"] is False


def test_example_and_target_paths_exist_in_repo() -> None:
    assert EXAMPLE.is_file()
    # import may exist locally (gitignored)
    assert EXAMPLE.read_text(encoding="utf-8")
