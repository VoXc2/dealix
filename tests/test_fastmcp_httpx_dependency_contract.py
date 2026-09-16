from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_api_runtime_keeps_httpx_uvicorn_and_isolates_fastmcp() -> None:
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    mcp_text = (ROOT / "mcp_server" / "requirements-mcp.txt").read_text(encoding="utf-8")
    assert re.search(r"^httpx>=0\.28\.1,<1$", text, flags=re.MULTILINE)
    assert not re.search(r"^fastmcp", text, flags=re.MULTILINE)
    assert re.search(r"^fastmcp>=3\.4\.7,<4$", mcp_text, flags=re.MULTILINE)
    assert re.search(r"^uvicorn\[standard\]>=0\.35\.0,<0\.36$", text, flags=re.MULTILINE)


def test_pyproject_runtime_and_dev_httpx_floors_match() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    runtime = set(data["project"]["dependencies"])
    dev = set(data["project"]["optional-dependencies"]["dev"])
    assert "httpx>=0.28.1" in runtime
    assert "httpx>=0.28.1" in dev
    assert "uvicorn[standard]>=0.35.0" in runtime
    assert not any(value.startswith("httpx>=0.27") for value in runtime | dev)
