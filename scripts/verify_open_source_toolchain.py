#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TOOL_DIR = ROOT / "tooling" / "oss"
RADAR = ROOT / "dealix" / "registers" / "oss_capability_radar_2026_09.json"
MISE = Path(os.environ.get("MISE_BIN", str(Path.home() / ".local/bin/mise")))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"OPEN_SOURCE_TOOLCHAIN_VERIFY=FAIL reason={message}")


def command_ok(command: list[str]) -> bool:
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-installed", action="store_true")
    args = parser.parse_args()

    radar = json.loads(RADAR.read_text())
    require(radar["counts"]["total"] >= 100, "radar_too_small")
    require(radar["counts"]["strict_oss"] >= 50, "fewer_than_50_strict_oss")
    require(radar["counts"]["review_required"] == 0, "unreviewed_license")
    require(radar["counts"]["archived"] == 0, "archived_repository_in_current_radar")

    mise_cfg = tomllib.loads((TOOL_DIR / "mise.toml").read_text())
    mise_lock = tomllib.loads((TOOL_DIR / "mise.lock").read_text())
    uv_specs = [line.strip() for line in (TOOL_DIR / "uv-tools.txt").read_text().splitlines() if line.strip() and not line.startswith("#")]
    require(len(mise_cfg.get("tools", {})) >= 45, "mise_profile_too_small")
    require(len(mise_lock.get("tools", {})) == len(mise_cfg.get("tools", {})), "mise_lock_mismatch")
    require(len(uv_specs) >= 8, "uv_tool_profile_too_small")

    bootstrap = (ROOT / "scripts" / "bootstrap_open_source_toolchain.sh").read_text().lower()
    forbidden = ("docker compose up", "systemctl enable", "systemctl start", "railway up", "railway deploy", "cloudflared tunnel route dns")
    require(not any(token in bootstrap for token in forbidden), "bootstrap_contains_runtime_or_production_mutation")

    if args.check_installed:
        require(MISE.exists(), "mise_missing")
        critical_mise = ("actionlint", "gitleaks", "trivy", "osv-scanner", "syft", "cosign", "shellcheck", "hadolint", "hurl", "k6")
        for tool in critical_mise:
            version_args = ["version"] if tool == "cosign" else ["--version"]
            require(command_ok([str(MISE), "-C", str(TOOL_DIR), "exec", "--", tool, *version_args]), f"missing_or_broken_{tool}")
        critical_path = ("semgrep", "yamllint", "pip-audit", "cyclonedx-py", "schemathesis", "markitdown", "mcp", "pgcli")
        for tool in critical_path:
            require(shutil.which(tool) is not None, f"missing_{tool}")

    counts = radar["counts"]
    print("OSS_RADAR_TOTAL=" + str(counts["total"]))
    print("STRICT_OSS=" + str(counts["strict_oss"]))
    print("OPEN_CORE_MIXED=" + str(counts["open_core_mixed"]))
    print("SOURCE_AVAILABLE_NON_OSI=" + str(counts["source_available_non_osi"]))
    print("MISE_LOCKED_TOOLS=" + str(len(mise_cfg["tools"])))
    print("UV_ISOLATED_TOOLS=" + str(len(uv_specs)))
    print("OPEN_SOURCE_TOOLCHAIN_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
