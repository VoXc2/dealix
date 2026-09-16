from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _active_requirement_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def test_main_api_does_not_install_optional_fastmcp_runtime() -> None:
    requirements = _active_requirement_lines(ROOT / "requirements.txt")
    assert not any(line.lower().startswith("fastmcp") for line in requirements)


def test_mcp_server_keeps_fastmcp_in_its_isolated_dependency_plane() -> None:
    requirements = _active_requirement_lines(ROOT / "mcp_server" / "requirements-mcp.txt")
    assert "fastmcp>=3.4.7,<4" in requirements


def test_runtime_image_contract_is_fail_fast_and_prunes_build_tooling() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "RUN set -eux;" in dockerfile
    assert "python -m pip uninstall -y pip setuptools wheel" in dockerfile
    assert "libpcre2-8-0" in dockerfile
    assert "2>/dev/null || true" not in dockerfile
