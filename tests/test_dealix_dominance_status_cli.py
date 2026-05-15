"""Tests for scripts/dealix_dominance_status.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_dominance_status.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_dominance_status  # type: ignore[import-not-found]

        return dealix_dominance_status
    finally:
        sys.path.pop(0)


def test_script_exists_and_has_shebang() -> None:
    assert SCRIPT.exists()
    text = SCRIPT.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env python3")


def test_json_payload_shape() -> None:
    mod = _import_module()
    payload = mod._build_payload()
    assert payload["schema_version"] == 1
    assert payload["dominance_layers"] == 10
    assert payload["dominance_gates"] == ["A", "B", "C", "D"]
    assert payload["snapshot"]["missing_layer_contracts"] == []


def test_text_render_contains_core_sections() -> None:
    mod = _import_module()
    rendered = mod.render_text(mod._build_payload())
    assert "Dominance Status" in rendered
    assert "Gate readiness" in rendered
    assert "Layer contract view" in rendered


def test_main_json_mode_returns_zero(capsys) -> None:
    mod = _import_module()
    rc = mod.main(["--json"])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["dominance_layers"] == 10


def test_main_text_mode_returns_zero(capsys) -> None:
    mod = _import_module()
    rc = mod.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Dominance Status" in out
