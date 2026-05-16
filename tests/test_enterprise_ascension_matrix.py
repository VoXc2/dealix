from __future__ import annotations

from pathlib import Path

import yaml

from scripts.verify_enterprise_ascension import (
    EXPECTED_AXES,
    MATRIX_PATH,
    load_matrix,
    validate_matrix,
)


def test_matrix_file_exists():
    assert MATRIX_PATH.exists()


def test_matrix_has_expected_axis_count():
    data = load_matrix()
    axes = data.get("axes") or []
    assert len(axes) == EXPECTED_AXES


def test_matrix_validates_cleanly():
    data = load_matrix()
    errors, summary = validate_matrix(data, repo_root=Path(__file__).resolve().parents[1])
    assert not errors, f"validation errors: {errors}"
    assert summary.total == EXPECTED_AXES
    assert summary.live >= 1


def test_matrix_yaml_loadable():
    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        parsed = yaml.safe_load(f)
    assert isinstance(parsed, dict)
