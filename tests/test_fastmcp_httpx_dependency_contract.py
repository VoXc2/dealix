from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_requirements_httpx_floor_matches_fastmcp_contract() -> None:
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert re.search(r"^httpx>=0\.28\.1,<1$", text, flags=re.MULTILINE)
    assert re.search(r"^fastmcp>=2\.14\.0,<3$", text, flags=re.MULTILINE)
    assert re.search(r"^uvicorn\[standard\]>=0\.35\.0,<0\.36$", text, flags=re.MULTILINE)


def test_pyproject_runtime_and_dev_httpx_floors_match() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    runtime = set(data["project"]["dependencies"])
    dev = set(data["project"]["optional-dependencies"]["dev"])
    assert "httpx>=0.28.1" in runtime
    assert "httpx>=0.28.1" in dev
    assert "uvicorn[standard]>=0.35.0" in runtime
    assert not any(value.startswith("httpx>=0.27") for value in runtime | dev)
