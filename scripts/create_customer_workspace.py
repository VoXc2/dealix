#!/usr/bin/env python3
"""Create a governed customer-specific delivery workspace.

Copies the canonical customer workspace into ``customers/<slug>/`` by default.
Callers that need isolated verification may pass ``output_root`` so synthetic
state never touches the repository customer directory. The file names are kept
stable for repository compatibility, while current commercial authority is:

real interaction -> Free Mini Diagnostic -> Qualified Discovery ->
customer-specific Quote/scope/duration -> governed delivery -> payment/start
evidence -> delivery -> customer-validated Proof -> STOP/EXPAND/REDESIGN.

No customer-facing send, price authority, payment, production mutation, or
external effect occurs here.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO / "customers" / "_template"
CUSTOMERS_DIR = REPO / "customers"

PILOT_WORKSPACE_FILES = (
    "00_intake.md",
    "01_company_intelligence.md",
    "02_diagnostic_summary.md",
    "03_command_sprint_scope.md",  # compatibility filename; content is customer-specific delivery scope
    "04_revenue_map.md",
    "05_proof_register.md",
    "06_approval_register.md",
    "07_next_action_board.md",
    "08_executive_command_brief.md",
    "09_delivery_log.md",
    "10_proof_pack.md",
    "11_upsell_recommendation.md",  # compatibility filename; content is outcome review
)

# Compatibility alias for historical importers. Not commercial authority.
COMMAND_SPRINT_FILES = PILOT_WORKSPACE_FILES


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "customer"


def create_workspace(
    name: str,
    force: bool = False,
    *,
    output_root: Path | None = None,
) -> tuple[Path, list[str]]:
    """Create the workspace; return (path, list of file names written).

    ``output_root`` is intentionally keyword-only. Production/operator callers
    keep the historical ``customers/<slug>/`` default, while verification can
    use a temporary directory without mutating the source worktree.
    """
    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(f"Template directory missing: {TEMPLATE_DIR}")

    slug = slugify(name)
    root = output_root if output_root is not None else CUSTOMERS_DIR
    target = root / slug

    if target.exists() and not force:
        print("CUSTOMER_WORKSPACE_EXISTS")
        raise FileExistsError(
            f"Customer folder already exists: {target} (use --force to overwrite)"
        )

    target.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for fname in PILOT_WORKSPACE_FILES:
        src = TEMPLATE_DIR / fname
        if not src.is_file():
            raise FileNotFoundError(f"Template file missing: {src}")
        content = src.read_text(encoding="utf-8").replace("<<COMPANY_NAME>>", name)
        (target / fname).write_text(content, encoding="utf-8")
        written.append(fname)
    return target, written


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(
        description="Create a governed customer-specific delivery workspace"
    )
    parser.add_argument("--name", required=True, help="Customer / company name")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing customer folder (default: refuse)",
    )
    args = parser.parse_args(argv)

    try:
        target, written = create_workspace(args.name, force=args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    rel = target.relative_to(REPO)
    print(f"Created governed customer delivery workspace: {rel}")
    for fname in written:
        print(f"  + {fname}")
    print("CUSTOMER_WORKSPACE_CREATED")
    print(f"CUSTOMER_WORKSPACE_FILES={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
