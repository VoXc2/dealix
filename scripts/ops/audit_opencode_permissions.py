#!/usr/bin/env python3
"""DEALIX_OPENCODE_PERMISSIONS_AUDIT — prove the auto-execution boundary.

Goal: zero routine founder permission prompts *without* surrendering the hard
material boundary. OpenCode v1 auto-approves every permission that is not
explicitly denied when started with ``--auto``. So the safety of auto mode is
exactly the completeness of the explicit deny set.

This is a deterministic (zero-token) auditor. It:

* resolves the effective OpenCode config (``opencode debug config``) or reads
  the project/user JSON directly;
* detects the config family (v1 ``permission`` object) and refuses to guess if
  the schema is unknown;
* asserts that every required hard-material responsibilty has at least one
  explicit ``deny`` rule;
* asserts safe L0-L4 capabilities remain ``allow``;
* never prints credentials and never invokes a model.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_CONFIG = REPO_ROOT / "opencode.json"
USER_CONFIG = Path("/home/dealix/.config/opencode/opencode.json")

# Each requirement maps to distinctive substrings; at least one ``deny`` rule
# must contain every listed phrase (case-insensitive).
REQUIRED_HARD_DENIES: dict[str, tuple[str, ...]] = {
    "protected_main_push": ("main",),
    "force_push": ("--force", "push -f"),
    "pull_request_merge": ("gh pr merge", "gh merge"),
    "production_deploy": ("railway up", "railway redeploy", "wrangler deploy", "vercel"),
    "secret_read": ("secret", ".env", "printenv", "environ"),
    "destructive_rm": ("rm -rf",),
    "dns_mutation": ("route53", "gcloud dns", "domain"),
    "db_migration": ("alembic upgrade", "alembic downgrade"),
}

# Requirements expressed as "any of these substrings" (OR) rather than all.
REQUIRED_ANY_DENIES: dict[str, tuple[str, ...]] = {
    "cloudflare_dns": ("cloudflare",),
}

REQUIRED_SAFE_ALLOWS = ("edit", "read", "glob", "grep")


def detect_version(text: str) -> tuple[int, int, int] | None:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", text or "")
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def schema_family(config: dict[str, Any]) -> str:
    if "permission" in config and isinstance(config["permission"], dict):
        return "v1"
    if "permissions" in config:
        return "v2-unknown"
    return "unknown"


def classify(config: dict[str, Any]) -> dict[str, list[str]]:
    permission = config.get("permission") or {}
    bash = permission.get("bash") if isinstance(permission.get("bash"), dict) else {}
    denies: list[str] = []
    asks: list[str] = []
    allows: list[str] = []
    for pattern, action in bash.items():
        bucket = {"deny": denies, "ask": asks, "allow": allows}.get(str(action))
        if bucket is not None:
            bucket.append(str(pattern))
    return {"deny": denies, "ask": asks, "allow": allows}


def _contains_any(haystack: list[str], needles: tuple[str, ...]) -> bool:
    joined = " ".join(haystack).lower()
    return any(needle.lower() in joined for needle in needles)


def audit_config(config: dict[str, Any], version: str = "") -> dict[str, Any]:
    if "permission" not in config and ("bash" in config or "edit" in config):
        config = {"permission": config}
    family = schema_family(config)
    rules = classify(config)
    denies = rules["deny"]
    denies_lower = [item.lower() for item in denies]

    missing_hard: list[str] = []
    for name, needles in REQUIRED_HARD_DENIES.items():
        if not all(needle.lower() in " ".join(denies_lower) for needle in needles):
            missing_hard.append(name)
    for name, needles in REQUIRED_ANY_DENIES.items():
        if not _contains_any(denies_lower, needles):
            missing_hard.append(name)

    permission = config.get("permission") or {}
    safe_allows = {key: permission.get(key) == "allow" for key in REQUIRED_SAFE_ALLOWS}
    bash_default_allow = permission.get("bash", {}).get("*") == "allow" if isinstance(permission.get("bash"), dict) else False

    parsed_version = detect_version(version)
    version_ok = parsed_version is not None and parsed_version[0] == 1
    known_schema = family == "v1"

    # Under ``--auto`` any rule that is not an explicit deny is auto-approved.
    # Residual ``ask`` rules are therefore holes in the autonomous boundary.
    residual_asks = sorted(rules["ask"])

    verdict = "PASS"
    if not known_schema or not version_ok:
        verdict = "FAIL"
    if missing_hard:
        verdict = "FAIL"
    if residual_asks:
        verdict = "FAIL"
    if not all(safe_allows.values()) or not bash_default_allow:
        verdict = "FAIL"

    return {
        "schema": "dealix.opencode_permissions_audit.v1",
        "opencode_version": version or "UNKNOWN",
        "schema_family": family,
        "version_supported": version_ok,
        "deny_count": len(denies),
        "ask_count": len(rules["ask"]),
        "allow_count": len(rules["allow"]),
        "missing_hard_denies": missing_hard,
        "residual_ask_rules": residual_asks,
        "safe_allows": safe_allows,
        "bash_default_allow": bash_default_allow,
        "hard_material_actions_fail_closed": not missing_hard,
        "auto_mode_safe": verdict == "PASS",
        "verdict": verdict,
        "secrets_printed": False,
    }


def harden_config(config: dict[str, Any]) -> dict[str, Any]:
    """Return a copy where every material ``ask`` rule is closed to ``deny``.

    ``--auto`` auto-approves anything not explicitly denied, so an ``ask`` rule
    is a silent hole in the autonomous boundary. Fail closed instead.
    """
    hardened = json.loads(json.dumps(config))
    permission = hardened.setdefault("permission", {})
    bash = permission.get("bash")
    if isinstance(bash, dict):
        for pattern, action in list(bash.items()):
            if str(action) == "ask":
                bash[pattern] = "deny"
    return hardened


def render(payload: dict[str, Any]) -> str:
    lines = [
        f"OPENCODE_PERMISSIONS_AUDIT={payload['verdict']}",
        f"OPENCODE_VERSION={payload['opencode_version']}",
        f"SCHEMA_FAMILY={payload['schema_family']}",
        f"VERSION_SUPPORTED={payload['version_supported']}",
        f"DENY_RULES={payload['deny_count']} ASK_RULES={payload['ask_count']}",
        f"MISSING_HARD_DENIES={payload['missing_hard_denies'] or 'none'}",
        f"RESIDUAL_ASK_RULES={payload['residual_ask_rules'] or 'none'}",
        f"SAFE_ALLOWS={payload['safe_allows']}",
        f"BASH_DEFAULT_ALLOW={payload['bash_default_allow']}",
        f"HARD_MATERIAL_FAIL_CLOSED={payload['hard_material_actions_fail_closed']}",
        f"AUTO_MODE_SAFE={payload['auto_mode_safe']}",
    ]
    return "\n".join(lines)


def resolve_config_from_opencode(binary: str) -> dict[str, Any] | None:
    try:
        result = subprocess.run(
            [binary, "debug", "config"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            cwd=str(REPO_ROOT),
        )
        return json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def load_config_file(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"//.*", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def resolve_config() -> dict[str, Any]:
    binary = shutil.which("opencode")
    if binary:
        resolved = resolve_config_from_opencode(binary)
        if resolved:
            return resolved
    for candidate in (PROJECT_CONFIG, USER_CONFIG):
        loaded = load_config_file(candidate)
        if loaded:
            return loaded
    return {}


def opencode_version() -> str:
    binary = shutil.which("opencode")
    if not binary:
        return ""
    try:
        result = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=20, check=False)
        return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the OpenCode permission boundary (deterministic, no model)")
    parser.add_argument("--config", type=Path, help="read a specific config JSON instead of discovering")
    parser.add_argument("--emit-hardened", action="store_true", help="print a config with every ask rule closed to deny")
    parser.add_argument("--emit-permission", action="store_true", help="print only the hardened permission object")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.config:
        config = load_config_file(args.config) or {}
    else:
        config = resolve_config()
    if args.emit_permission:
        print(json.dumps(harden_config(config).get("permission", {}), indent=2, ensure_ascii=False))
        return 0
    if args.emit_hardened:
        print(json.dumps(harden_config(config), indent=2, ensure_ascii=False))
        return 0
    payload = audit_config(config, version=opencode_version())
    print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else render(payload))
    return 0 if payload["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
