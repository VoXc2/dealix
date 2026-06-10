"""Proof Pack Ledger — append-only ledger of all Proof Packs generated across
engagements.

Storage: JSON file at data/proof_packs/ledger.json (directory created on first
write). All operations are synchronous and path-safe.

Publishable packs: proof_level >= L2, approved_by_founder=True,
customer_consented=True.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

ProofPackLevel = Literal["L0", "L1", "L2", "L3", "L4"]

_PROOF_LEVEL_RANK: dict[str, int] = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
    "L4": 4,
}

_DEFAULT_LEDGER_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "proof_packs" / "ledger.json"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ProofPackEntry(BaseModel):
    """A single Proof Pack record in the ledger."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(..., min_length=1, description="Unique identifier for this Proof Pack.")
    account_id: str = Field(..., min_length=1, description="Client / account identifier.")
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )
    proof_level: ProofPackLevel = Field(
        ..., description="Evidence tier: L0 (internal) through L4 (client-confirmed)."
    )
    evidence_items: list[str] = Field(
        default_factory=list,
        description="Short descriptions of each evidence artefact.",
    )
    approved_by_founder: bool = Field(
        default=False, description="Founder has reviewed and approved this pack."
    )
    customer_consented: bool = Field(
        default=False, description="Client has explicitly consented to publication."
    )
    published: bool = Field(
        default=False,
        description="Whether this pack has been shared externally (case-study eligible).",
    )


# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------


class ProofPackLedger:
    """Append-only ledger backed by a JSON file.

    Thread-safety note: this implementation uses file-level reads and writes
    without advisory locks — suitable for single-process usage.  For
    concurrent / multi-worker deployments, migrate to a database backend.
    """

    def __init__(self, ledger_path: Path | None = None) -> None:
        self._path: Path = ledger_path or _DEFAULT_LEDGER_PATH

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[dict]:
        if not self._path.exists():
            return []
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, records: list[dict]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def append(self, entry: ProofPackEntry) -> ProofPackEntry:
        """Append a new Proof Pack entry to the ledger. Returns the entry."""
        records = self._load()
        records.append(entry.model_dump())
        self._save(records)
        return entry

    def get_by_account(self, account_id: str) -> list[ProofPackEntry]:
        """Return all Proof Pack entries for a given account_id."""
        records = self._load()
        return [
            ProofPackEntry(**r)
            for r in records
            if r.get("account_id") == account_id
        ]

    def get_all(self) -> list[ProofPackEntry]:
        """Return every entry in the ledger."""
        return [ProofPackEntry(**r) for r in self._load()]

    def get_publishable(self) -> list[ProofPackEntry]:
        """Return entries that are L2+, founder-approved, and customer-consented."""
        return [
            e
            for e in self.get_all()
            if (
                _PROOF_LEVEL_RANK.get(e.proof_level, 0) >= _PROOF_LEVEL_RANK["L2"]
                and e.approved_by_founder
                and e.customer_consented
            )
        ]

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_markdown(self, account_id: str | None = None) -> str:
        """Export ledger (or a single account's packs) as PDF-ready markdown."""
        entries = self.get_by_account(account_id) if account_id else self.get_all()
        if not entries:
            return "# Proof Pack Ledger\n\n_No entries found._\n"

        lines: list[str] = ["# Proof Pack Ledger\n"]
        if account_id:
            lines[0] = f"# Proof Pack Ledger — Account: {account_id}\n"

        for entry in entries:
            lines.append(f"## Pack `{entry.pack_id}`\n")
            lines.append(f"- **Account:** {entry.account_id}")
            lines.append(f"- **Created:** {entry.created_at}")
            lines.append(f"- **Proof Level:** {entry.proof_level}")
            lines.append(f"- **Approved by Founder:** {'Yes' if entry.approved_by_founder else 'No'}")
            lines.append(f"- **Customer Consented:** {'Yes' if entry.customer_consented else 'No'}")
            lines.append(f"- **Published:** {'Yes' if entry.published else 'No'}")
            if entry.evidence_items:
                lines.append("\n### Evidence Items\n")
                for item in entry.evidence_items:
                    lines.append(f"- {item}")
            lines.append("")  # blank line between entries

        return "\n".join(lines)
