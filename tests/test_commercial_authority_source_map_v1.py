from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_commercial_authority_source_map_v1.py"


def test_commercial_authority_source_map_matches_live_repository() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "COMMERCIAL_AUTHORITY_SOURCE_MAP_V1_PASS" in completed.stdout
    assert "closure_verdict=BLOCKED_RETIRED_RUNTIME_AUTHORITY" in completed.stdout
    assert "unresolved_count=5" in completed.stdout
    assert completed.stderr == ""
