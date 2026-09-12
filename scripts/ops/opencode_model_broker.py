#!/usr/bin/env python3
"""DEALIX_OPENCODE_MODEL_BROKER — identity-stable, no-secret free selector.

Reconciles the runtime free-model selector into repo source. It:

* runs ``opencode models --refresh`` as the canonical ``dealix`` identity so the
  live catalog is complete (root sees a smaller/empty catalog and can hit
  ``PermissionDenied`` on ``/root/opencode.jsonc``);
* stores model *availability* only — never credentials, auth files, or tokens;
* selects the first healthy explicitly-free model with a bounded, tool-free probe;
* never promotes a merely-known non-free model into the free selector.

Included subscription models such as the ``opencode-go/*`` namespace are routed
by ``go_resource_broker.py``. This module remains deliberately free-only.

All subprocesses are passed the exact argv built here; the tool never starts a
network listener. State is written under the runtime opencode control dir so the
existing systemd selector keeps working.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

OPS_DIR = Path(__file__).resolve().parent
if str(OPS_DIR) not in sys.path:
    sys.path.insert(0, str(OPS_DIR))

from model_cost_policy import explicit_free_models, is_explicit_free_model

STATE_DIR = Path(os.environ.get("DEALIX_OPENCODE_STATE_DIR", "/opt/dealix/control/opencode/state"))
READONLY_DIR = Path(os.environ.get("DEALIX_OPENCODE_READONLY_DIR", "/opt/dealix/control/opencode/readonly"))
AVAILABILITY_FILE = "model-availability.json"
POOL_FILE = "free-model-pool"
SELECTED_FILE = "selected-free-model"

PROBE_PROMPT = "Return exactly FREE_SELECTOR_OK. Do not use tools or modify files."
PROBE_MARKER = "FREE_SELECTOR_OK"
REFRESH_MARKER = "Models cache refreshed"

PREFERRED_FREE = (
    "opencode/deepseek-v4-flash-free",
    "opencode/north-mini-code-free",
    "opencode/mimo-v2.5-free",
    "opencode/nemotron-3-ultra-free",
    "opencode/nemotron-3.5-lightning-free",
    "opencode/ling-3.0-flash-fin-free",
    "opencode/muse-spark-1.3-contributor-free",
    "opencode/muse-spark-1.2-contributor-free",
)

_OPENCODE_BIN_CANDIDATES = (
    Path("/home/dealix/.opencode/bin/opencode"),
    Path("/usr/local/bin/opencode"),
    Path("/root/.opencode/bin/opencode"),
)
_CANONICAL_DEALIX_USER = "dealix"


def resolve_canonical_owner() -> str | None:
    if os.geteuid() == 0:
        try:
            import pwd

            pwd.getpwnam(_CANONICAL_DEALIX_USER)
            return _CANONICAL_DEALIX_USER
        except (ImportError, KeyError):
            return None
    return None


def resolve_opencode_bin() -> str | None:
    if resolve_canonical_owner():
        for candidate in _OPENCODE_BIN_CANDIDATES:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
    found = shutil.which("opencode")
    if found:
        return found
    for candidate in _OPENCODE_BIN_CANDIDATES:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def build_opencode_command(binary: str, args: list[str]) -> list[str]:
    owner = resolve_canonical_owner()
    if owner and owner != getpass.getuser() and shutil.which("sudo"):
        return ["sudo", "-n", "-u", owner, "-H", binary, *args]
    return [binary, *args]


def write_state(path: Path, text: str, mode: int = 0o640) -> None:
    """Write a state file owned by the canonical identity (not the root caller)."""
    path.write_text(text, encoding="utf-8")
    owner = resolve_canonical_owner()
    if owner and os.geteuid() == 0:
        try:
            import pwd

            entry = pwd.getpwnam(owner)
            os.chown(path, entry.pw_uid, entry.pw_gid)
        except (ImportError, KeyError, OSError):
            pass
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def run_opencode(args: list[str], timeout: int = 60) -> tuple[int, str]:
    binary = resolve_opencode_bin()
    if not binary:
        return 127, ""
    cmd = build_opencode_command(binary, args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            cwd=str(READONLY_DIR) if READONLY_DIR.is_dir() else None,
        )
        return result.returncode, result.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 124, ""


def parse_catalog(output: str) -> list[str]:
    models: list[str] = []
    for raw in output.splitlines():
        line = raw.strip()
        if "/" in line and not line.startswith("Error"):
            models.append(line)
    return models


def refresh(state_dir: Path = STATE_DIR) -> dict[str, Any]:
    rc, output = run_opencode(["models", "--refresh"], timeout=90)
    models = parse_catalog(output)
    if not models:
        rc, output = run_opencode(["models"], timeout=60)
        models = parse_catalog(output)
    free_models = explicit_free_models(models)
    payload = {
        "schema": "dealix.opencode.model-availability.v2",
        "refreshed_at": datetime.now(UTC).isoformat(),
        "refresh_rc": rc,
        "refreshed_live": REFRESH_MARKER in output or bool(models),
        "count": len(models),
        "free_count": len(free_models),
        "models": models,
        "free_models": free_models,
        "blocked_non_free_count": len(models) - len(free_models),
        "auto_select_policy": "explicit_free_only",
        "credentials_stored": False,
    }
    state_dir.mkdir(parents=True, exist_ok=True)
    write_state(state_dir / AVAILABILITY_FILE, json.dumps(payload, indent=2, ensure_ascii=False))
    if free_models:
        write_state(state_dir / POOL_FILE, "\n".join(free_models) + "\n")
    return payload


def load_availability(state_dir: Path = STATE_DIR) -> dict[str, Any]:
    path = state_dir / AVAILABILITY_FILE
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "schema": "dealix.opencode.model-availability.v2",
        "models": [],
        "free_models": [],
        "auto_select_policy": "explicit_free_only",
    }


def candidate_order(availability: dict[str, Any], current: str | None) -> list[str]:
    models = list(availability.get("models") or [])
    declared_free = list(availability.get("free_models") or [])
    free = explicit_free_models([*declared_free, *models])
    ordered: list[str] = []
    if current and is_explicit_free_model(current):
        ordered.append(current)
    for model in PREFERRED_FREE:
        if model in free and model not in ordered:
            ordered.append(model)
    for model in free:
        if model not in ordered:
            ordered.append(model)
    return ordered


def _remove_unsafe_selection(selected_path: Path, current: str | None) -> bool:
    """Delete legacy/non-free selection state before any autonomous consumer can read it."""
    if not current or is_explicit_free_model(current):
        return False
    try:
        selected_path.unlink(missing_ok=True)
    except OSError:
        return False
    return True


def select(state_dir: Path = STATE_DIR, dry_run: bool = False) -> dict[str, Any]:
    availability = load_availability(state_dir)
    selected_path = state_dir / SELECTED_FILE
    current = selected_path.read_text(encoding="utf-8").strip() if selected_path.is_file() else None
    stale_selection_removed = False if dry_run else _remove_unsafe_selection(selected_path, current)
    candidates = candidate_order(availability, current)
    if dry_run:
        return {
            "dry_run": True,
            "candidates": candidates[:10],
            "selected": None,
            "auto_select_policy": "explicit_free_only",
        }
    for model in candidates:
        rc, output = run_opencode(["run", "-m", model, PROBE_PROMPT], timeout=45)
        if rc == 0 and PROBE_MARKER in output:
            write_state(selected_path, model + "\n")
            return {
                "selected": model,
                "probe_rc": rc,
                "tested": candidates.index(model) + 1,
                "stale_selection_removed": stale_selection_removed,
                "auto_select_policy": "explicit_free_only",
            }
    return {
        "selected": None,
        "probe_rc": None,
        "tested": len(candidates),
        "stale_selection_removed": stale_selection_removed,
        "auto_select_policy": "explicit_free_only",
    }


def status(state_dir: Path = STATE_DIR) -> dict[str, Any]:
    availability = load_availability(state_dir)
    selected_path = state_dir / SELECTED_FILE
    selected = selected_path.read_text(encoding="utf-8").strip() if selected_path.is_file() else None
    return {
        "opencode_bin": resolve_opencode_bin() or "UNKNOWN",
        "owner": resolve_canonical_owner() or getpass.getuser(),
        "availability_count": availability.get("count", len(availability.get("models") or [])),
        "availability_refreshed_at": availability.get("refreshed_at"),
        "free_models": explicit_free_models(availability.get("free_models") or []),
        "selected": selected if is_explicit_free_model(selected) else None,
        "stale_non_free_selection_blocked": bool(selected and not is_explicit_free_model(selected)),
        "auto_select_policy": "explicit_free_only",
    }


def render_status(payload: dict[str, Any]) -> str:
    lines = [
        "OPENCODE_MODEL_BROKER=ACTIVE",
        f"OPENCODE_BIN={payload['opencode_bin']}",
        f"OWNER={payload['owner']}",
        f"AVAILABILITY_COUNT={payload['availability_count']}",
        f"AVAILABILITY_REFRESHED_AT={payload['availability_refreshed_at']}",
        f"FREE_MODELS={payload['free_models']}",
        f"SELECTED={payload['selected']}",
        f"STALE_NON_FREE_SELECTION_BLOCKED={payload['stale_non_free_selection_blocked']}",
        f"AUTO_SELECT_POLICY={payload['auto_select_policy']}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix OpenCode free-model broker (identity-stable, no secrets)")
    parser.add_argument("command", nargs="?", choices=("status", "refresh", "select"), default="status")
    parser.add_argument("--state-dir", type=Path, default=STATE_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.command == "refresh":
        payload = refresh(args.state_dir)
        print(
            json.dumps(payload, indent=2, ensure_ascii=False)
            if args.json
            else f"REFRESHED count={payload['count']} free={payload['free_count']} blocked_non_free={payload['blocked_non_free_count']} rc={payload['refresh_rc']}"
        )
        return 0 if payload["count"] else 1
    if args.command == "select":
        payload = select(args.state_dir, dry_run=args.dry_run)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if (payload.get("dry_run") or payload.get("selected")) else 1
    payload = status(args.state_dir)
    print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else render_status(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())