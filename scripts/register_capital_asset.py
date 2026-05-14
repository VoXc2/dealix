#!/usr/bin/env python3
"""Register a Capital Asset in the public index.

Honest-marker discipline: every entry includes git_author + entry_id +
created_at. The file the verifier and the public API both read is
`data/capital_asset_index.json`.

Doctrine: a capital asset must be registered BEFORE the invoice that
references it (see docs/ops/FIRST_INVOICE_UNLOCK.md step 1).

Usage:
    python scripts/register_capital_asset.py \\
        --type PROOF_EXAMPLE \\
        --title "Sample title" \\
        --description "What it is, how it was produced." \\
        --evidence "Path to evidence file or reference."

The script validates the entry via the existing
auto_client_acquisition/capital_os/capital_ledger.py:capital_ledger_event_valid()
contract before writing.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "capital_asset_index.json"

sys.path.insert(0, str(REPO_ROOT))
from auto_client_acquisition.capital_os.asset_types import CapitalAssetType  # noqa: E402
from auto_client_acquisition.capital_os.capital_ledger import (  # noqa: E402
    CapitalLedgerEvent,
    capital_ledger_event_valid,
)


def _git_author() -> str:
    try:
        out = subprocess.run(
            ["git", "config", "user.email"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _load_index() -> dict:
    if not INDEX_PATH.exists():
        return {
            "index_id": "CAPITAL-ASSET-INDEX-001",
            "updated_at": datetime.now(timezone.utc).date().isoformat(),
            "entries": [],
        }
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(f"capital_asset_index.json is invalid JSON: {INDEX_PATH}")


def _write_index(data: dict) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def register(
    asset_type: str,
    title: str,
    description: str,
    evidence: str,
    project_id: str = "internal",
    client_id: str = "internal",
) -> dict:
    # Validate enum.
    try:
        kind = CapitalAssetType(asset_type.lower())
    except ValueError as e:
        valid = ", ".join(t.value for t in CapitalAssetType)
        raise SystemExit(
            f"unknown asset_type {asset_type!r}. Valid values: {valid}"
        ) from e

    entry_id = uuid.uuid4().hex
    event = CapitalLedgerEvent(
        capital_event_id=entry_id,
        project_id=project_id.strip(),
        client_id=client_id.strip(),
        asset_type=kind.value,
        title=title.strip(),
        description=description.strip(),
        evidence=evidence.strip(),
    )
    if not capital_ledger_event_valid(event):
        raise SystemExit(
            "capital ledger event invalid — every field must be non-empty"
        )

    now = datetime.now(timezone.utc).isoformat()
    record = {
        "entry_id": entry_id,
        "asset_type": event.asset_type,
        "title": event.title,
        "description": event.description,
        "evidence": event.evidence,
        "project_id": event.project_id,
        "client_id": event.client_id,
        "created_at": now,
        "git_author": _git_author(),
    }

    data = _load_index()
    entries = list(data.get("entries") or [])
    entries.append(record)
    data["entries"] = entries
    data["updated_at"] = now[:10]
    _write_index(data)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="register a capital asset")
    parser.add_argument(
        "--type", required=True,
        help="CapitalAssetType value (e.g., PROOF_EXAMPLE, SCORING_RULE)",
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--project-id", default="internal")
    parser.add_argument("--client-id", default="internal")
    args = parser.parse_args(argv)

    rec = register(
        asset_type=args.type,
        title=args.title,
        description=args.description,
        evidence=args.evidence,
        project_id=args.project_id,
        client_id=args.client_id,
    )
    print(f"registered capital asset: {rec['entry_id']} ({rec['asset_type']})")
    print(f"  title: {rec['title']}")
    print(f"  index: data/capital_asset_index.json (now {sum(1 for _ in _load_index()['entries'])} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
