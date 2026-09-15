#!/usr/bin/env python3
"""Verify the source-managed Dealix internal Company Machine schedule."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "scripts/ops/runtime_templates/autonomous_company"
DEFAULT_RUNTIME = Path("/opt/dealix/control/autonomous-company/bin")
FILES = ("dealix-company-cycle", "dealix-company-dispatch.core-v6")
REQUIRED_SCHEDULE = (
    "run_due 1130 45 content_morning content business",
    "run_due 1330 45 delivery_midday delivery business",
    "run_due 1630 45 content_afternoon content business",
)
REQUIRED_CYCLE = (
    "  content)",
    "scripts/dealix_content_factory_daily.py",
    "  delivery)",
    "ACTIVE_CLIENT_WORKSPACES=",
    "scripts/verify_delivery_os.py",
)
FORBIDDEN_TRUE = (
    "EMAIL_LIVE_SEND=true",
    "WHATSAPP_OUTBOUND=true",
    "PUBLIC_PUBLISH=true",
    "PAYMENT_EXECUTION=true",
    "PRODUCTION_MUTATION=true",
)
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(runtime: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for name in FILES:
        src = TEMPLATES / name
        dst = runtime / name
        if not src.is_file():
            errors.append(f"missing template: {src}")
            continue
        if not dst.is_file():
            errors.append(f"missing runtime file: {dst}")
            continue
        if sha256(src) != sha256(dst):
            errors.append(f"runtime drift: {name}")

    dispatch = (runtime / "dealix-company-dispatch.core-v6")
    cycle = (runtime / "dealix-company-cycle")
    if dispatch.is_file():
        text = dispatch.read_text(encoding="utf-8")
        for token in REQUIRED_SCHEDULE:
            if token not in text:
                errors.append(f"missing schedule token: {token}")
    if cycle.is_file():
        text = cycle.read_text(encoding="utf-8")
        for token in REQUIRED_CYCLE:
            if token not in text:
                errors.append(f"missing cycle token: {token}")
        for token in FORBIDDEN_TRUE:
            if token in text:
                errors.append(f"unsafe live flag: {token}")
    return not errors, errors
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME)
    args = parser.parse_args()
    ok, errors = evaluate(args.runtime_root)
    print(f"SOURCE_MANAGED_COMPANY_SCHEDULE={'PASS' if ok else 'FAIL'}")
    print("CONTENT_CYCLES=11:30,16:30 Asia/Riyadh Sun-Thu")
    print("DELIVERY_CYCLE=13:30 Asia/Riyadh Sun-Thu")
    print("EXTERNAL_ACTION_AUTHORITY=FALSE")
    for error in errors:
        print(f"ERROR={error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
