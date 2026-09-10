#!/usr/bin/env python3
"""Canonical master-prompt-bound entrypoint for the Dealix Founder Command Room."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_master_prompt_binding_v1.py"
COMMAND_ROOM = ROOT / "scripts" / "commercial" / "run_dealix_command_room_v1.py"


def main() -> int:
    if not BINDING.is_file() or not VERIFY.is_file() or not COMMAND_ROOM.is_file():
        print("MASTER_COMPANY_CYCLE=BLOCKED_REQUIRED_FILE_MISSING", file=sys.stderr)
        return 2

    verify = subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=False)
    if verify.returncode != 0:
        print("MASTER_COMPANY_CYCLE=BLOCKED_MASTER_PROMPT_INVALID", file=sys.stderr)
        return int(verify.returncode or 1)

    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    prompt = ROOT / str(binding["prompt_ref"])
    meta_control = ROOT / str(binding["meta_control_ref"])
    digest = hashlib.sha256(prompt.read_bytes()).hexdigest()
    meta_digest = hashlib.sha256(meta_control.read_bytes()).hexdigest()

    env = dict(os.environ)
    env[str(binding["prompt_env"])] = str(prompt)
    env[str(binding["prompt_sha_env"])] = digest
    env[str(binding["meta_control_env"])] = str(meta_control)
    env[str(binding["meta_control_sha_env"])] = meta_digest
    env["DEALIX_MASTER_PROMPT_BOUND"] = "1"
    env["DEALIX_META_CONTROL_BOUND"] = "1"
    env["DEALIX_UNIVERSAL_L5"] = "0"
    env["DEALIX_EXTERNAL_SEND"] = "0"
    env["EMAIL_LIVE_SEND"] = "0"
    env["WHATSAPP_ALLOW_LIVE_SEND"] = "0"
    env["PUBLIC_PUBLISH"] = "0"
    env["PAYMENT_EXECUTION"] = "0"
    env["PRODUCTION_MUTATION"] = "0"

    command = [sys.executable, str(COMMAND_ROOM), *sys.argv[1:]]
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    print(f"MASTER_COMPANY_CYCLE_RC={result.returncode}")
    print(f"MASTER_PROMPT_SHA256={digest}")
    print(f"META_CONTROL_SHA256={meta_digest}")
    print("MASTER_PROMPT_BOUND=true")
    print("META_CONTROL_BOUND=true")
    print("UNIVERSAL_L5=false")
    print("MATERIAL_EXTERNAL_EFFECTS=DISABLED_BY_ENTRYPOINT")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
