"""Stability test: re-rendering the trust badges produces byte-identical
output on identical state. This is what makes the CI drift gate work
(`git diff --exit-code -- landing/assets/badges/*.svg`).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_trust_badges.py"
_spec = importlib.util.spec_from_file_location("render_trust_badges_mod", _SCRIPT)
renderer = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(renderer)


def _read(dirpath: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(dirpath.glob("*.svg"))}


def test_render_is_byte_stable(tmp_path):
    out1 = tmp_path / "round1"
    out2 = tmp_path / "round2"
    renderer.render(out1)
    renderer.render(out2)
    a = _read(out1)
    b = _read(out2)
    assert set(a.keys()) == set(b.keys())
    for name in a:
        assert a[name] == b[name], f"badge {name} drifted between identical runs"


def test_render_produces_five_badges(tmp_path):
    out = tmp_path / "out"
    written = renderer.render(out)
    names = set(written.keys())
    assert names == {
        "doctrine-status.svg",
        "verifier-score.svg",
        "ceo-complete.svg",
        "partner-outreach.svg",
        "invoice-sent.svg",
    }


def test_render_handles_missing_report(tmp_path, monkeypatch):
    """If verifier-report.json is missing, badges still render (FAIL / 0)."""
    monkeypatch.setattr(renderer, "REPORT_PATH", tmp_path / "absent.json")
    out = tmp_path / "out"
    renderer.render(out)
    assert (out / "doctrine-status.svg").exists()
    text = (out / "doctrine-status.svg").read_text()
    assert "FAIL" in text
