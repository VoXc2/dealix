from __future__ import annotations

import subprocess
import sys

import scripts.ceo_production_trust_bundle as bundle


def _argv(*extra: str) -> list[str]:
    return ["ceo_production_trust_bundle.py", *extra]


def test_ceo_bundle_delegates_green_to_canonical_identity_gate(monkeypatch, capsys):
    seen: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout="PRODUCTION_GREEN=TRUE\nRAILWAY_PRODUCTION_IDENTITY_GATE_VERDICT=PASS\n",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        _argv(
            "--accepted-sha",
            "a" * 40,
            "--web-provider-receipt",
            "/tmp/web.json",
            "--api-provider-receipt",
            "/tmp/api.json",
        ),
    )

    assert bundle.main() == 0
    output = capsys.readouterr().out
    assert "CEO_PRODUCTION_TRUST_VERDICT=PASS" in output
    assert "railway_production_identity_gate.py" in " ".join(seen["cmd"])
    assert "--accepted-sha" in seen["cmd"]
    assert "--web-provider-receipt" in seen["cmd"]
    assert "--api-provider-receipt" in seen["cmd"]


def test_ceo_bundle_holds_without_provider_identity_evidence(monkeypatch, capsys):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            cmd,
            1,
            stdout="PRODUCTION_GREEN=FALSE\nRAILWAY_PRODUCTION_IDENTITY_GATE_VERDICT=HOLD\n",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", _argv())

    assert bundle.main() == 1
    output = capsys.readouterr().out
    assert "CEO_PRODUCTION_TRUST_VERDICT=HOLD" in output
    assert "capture fresh read-only Railway web/API provider receipts" in output
    assert "DNS dealix.me" not in output
