"""Service readiness matrix and sellability docs stay present."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from auto_client_acquisition.delivery_os.service_readiness import compute_service_readiness_score

REPO = Path(__file__).resolve().parents[1]


def test_flagship_services_officially_sellable() -> None:
    for sid in ("lead_intelligence_sprint", "support_desk_sprint"):
        out = compute_service_readiness_score(sid)
        assert out["sellable_officially"] is True


def test_verify_sellability_script_passes() -> None:
    r = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / "verify_sellability.py")],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr or r.stdout
