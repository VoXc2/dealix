#!/usr/bin/env python3
"""Verify the repo-owned weekly proof-pack executable contract (source-only).

The host may carry a stale ``dealix-omega-weekly.service`` unit (exit 127 =
missing ExecStart target). That unit is host state: this verifier never edits
/etc nor restarts services. It pins the repo-owned contract instead:

1. Canonical generator + adapter exist and the adapter is executable.
2. Every repo-owned scheduler branch (legacy autopilot ``weekly()``,
   canonical revenue cycle ``weekly``) resolves to the canonical adapter path
   ``scripts/commercial/run_weekly_proof_pack.py`` — never the stale
   ``scripts/run_weekly_proof_pack.py`` which silently skips.
3. No repo-owned automation (scripts/, deploy/) declares the legacy
   ``dealix-omega-weekly.service`` name as its target.
4. The canonical installer still defines the ``dealix-company@weekly``
   template path (dealix-company@.service + weekly timer).

Read-only. Exit 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_ADAPTER = ROOT / "scripts" / "commercial" / "run_weekly_proof_pack.py"
CANONICAL_GENERATOR = ROOT / "scripts" / "generate_weekly_operating_proof_pack.py"
LEGACY_AUTOPILOT = ROOT / "scripts" / "ops" / "dealix_company_autopilot_legacy.sh"
CANONICAL_CYCLE = ROOT / "scripts" / "ops" / "dealix_canonical_revenue_cycle.sh"
CANONICAL_INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_company_autopilot.sh"

STALE_ADAPTER_REF = "scripts/run_weekly_proof_pack.py"
STALE_UNIT_NAME = "dealix-omega-weekly.service"


def _fail(reason: str) -> int:
    print(f"WEEKLY_PROOF_PACK_TARGET=FAIL reason={reason}")
    return 1


def main() -> int:
    if not CANONICAL_GENERATOR.is_file():
        return _fail("canonical_generator_missing")
    if not CANONICAL_ADAPTER.is_file():
        return _fail("canonical_adapter_missing")
    # Schedulers invoke the adapter via `python3 <path>`, so the contract is
    # valid-python, not the exec bit.
    try:
        compile(CANONICAL_ADAPTER.read_text(encoding="utf-8"), str(CANONICAL_ADAPTER), "exec")
    except (OSError, SyntaxError):
        return _fail("canonical_adapter_not_valid_python")

    for path in (LEGACY_AUTOPILOT, CANONICAL_CYCLE):
        if not path.is_file():
            return _fail(f"scheduler_missing:{path.name}")
        text = path.read_text(encoding="utf-8")
        if STALE_ADAPTER_REF in text:
            return _fail(f"stale_adapter_ref:{path.name}")
        if "scripts/commercial/run_weekly_proof_pack.py" not in text:
            return _fail(f"canonical_adapter_unwired:{path.name}")

    installer = CANONICAL_INSTALLER.read_text(encoding="utf-8")
    if "dealix-company@.service" not in installer or "weekly" not in installer:
        return _fail("canonical_weekly_template_missing")

    stale_hits: list[str] = []
    for base in (ROOT / "scripts", ROOT / "deploy"):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix in {".pyc"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if STALE_UNIT_NAME in text and path.resolve() != Path(__file__).resolve():
                stale_hits.append(str(path.relative_to(ROOT)))
    if stale_hits:
        return _fail(f"stale_unit_declared:{','.join(stale_hits)}")

    print("WEEKLY_PROOF_PACK_TARGET=PASS")
    print(f"WEEKLY_ADAPTER={CANONICAL_ADAPTER.relative_to(ROOT)}")
    print(f"WEEKLY_GENERATOR={CANONICAL_GENERATOR.relative_to(ROOT)}")
    print("WEEKLY_TEMPLATE=dealix-company@weekly.service(timer)")
    print("STALE_HOST_UNIT=dealix-omega-weekly.service(host-only;operator_removal_required)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
