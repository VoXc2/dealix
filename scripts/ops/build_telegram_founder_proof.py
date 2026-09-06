#!/usr/bin/env python3
"""Build a durable, tamper-evident Founder Proof envelope for Telegram projection.

This script NEVER sends to Telegram and NEVER executes L5 actions.
It renders one concise founder brief from explicit, local evidence references and
writes a private receipt under /opt/dealix/control/proof/telegram-founder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data/ops/telegram_proof_plane_v1.json"
DEFAULT_OUT = Path("/opt/dealix/control/proof/telegram-founder")
ALLOWED_TRUTH = {
    "VERIFIED",
    "EXECUTED",
    "HOLD",
    "DRAFT",
    "PLAN",
    "UNKNOWN_NOT_EVIDENCE_BACKED",
}
ALLOWED_STATUS = {"PASS", "WARN", "HOLD", "FAIL", "INFO"}
TRACE_RE = re.compile(r"^[0-9a-f]{32}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TOKEN_RE = re.compile(
    r"(?i)(authorization:\s*bearer\s+)[^\s]+|"
    r"\b(?:gh[opsu]_|github_pat_|sk-)[A-Za-z0-9_\-]{10,}\b|"
    r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*)\s*=\s*[^\s]+"
)


class ProofError(RuntimeError):
    pass


def now_rfc3339() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    """Restricted deterministic JSON encoding for the proof envelope hash."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def redact(value: str) -> str:
    value = value.replace("\x00", "")
    value = "".join(ch for ch in value if ch in "\n\t" or ord(ch) >= 32)

    def repl(match: re.Match[str]) -> str:
        if match.group(1):
            return f"{match.group(1)}[REDACTED]"
        if match.group(2):
            return f"{match.group(2)}=[REDACTED]"
        return "[REDACTED]"

    return TOKEN_RE.sub(repl, value)


def safe_text(value: str, *, limit: int = 800) -> str:
    return redact(value.strip())[:limit]


def validate_proof_root(path: Path) -> None:
    resolved = path.resolve(strict=False)
    allowed = Path("/opt/dealix/control/proof").resolve(strict=False)
    if resolved != allowed and allowed not in resolved.parents:
        raise ProofError("output root must remain under /opt/dealix/control/proof")
    if path.exists() and path.is_symlink():
        raise ProofError("output root cannot be a symlink")


def evidence_digest(path_text: str) -> dict[str, str]:
    path = Path(path_text)
    if not path.is_absolute():
        raise ProofError("evidence path must be absolute")
    resolved = path.resolve(strict=True)
    allowed = Path("/opt/dealix/control/proof").resolve(strict=True)
    if resolved != allowed and allowed not in resolved.parents:
        raise ProofError("evidence must remain under canonical proof root")
    if path.is_symlink() or not path.is_file():
        raise ProofError("evidence must be a regular non-symlink file")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o022:
        raise ProofError("evidence cannot be group/world writable")
    return {
        "path": str(resolved),
        "sha256": sha256_hex(path.read_bytes()),
    }


def read_previous_digest(out_root: Path) -> str | None:
    latest = out_root / "LATEST"
    if not latest.exists():
        return None
    if latest.is_symlink() or not latest.is_file():
        raise ProofError("LATEST pointer is unsafe")
    name = latest.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"proof_[0-9a-f]{16}\.json", name):
        raise ProofError("LATEST pointer is invalid")
    previous = out_root / name
    if previous.is_symlink() or not previous.is_file():
        raise ProofError("previous envelope is unsafe")
    payload = json.loads(previous.read_text(encoding="utf-8"))
    digest = str(payload.get("envelope_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ProofError("previous envelope digest invalid")
    previous_core = dict(payload)
    previous_core.pop("envelope_sha256", None)
    actual = sha256_hex(canonical_bytes(previous_core))
    if actual != digest:
        raise ProofError("previous envelope integrity check failed")
    return digest


def load_contract() -> dict[str, Any]:
    if not CONTRACT.is_file():
        raise ProofError("proof-plane contract missing")
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if payload.get("schema") != "dealix.telegram-proof-plane.v1":
        raise ProofError("proof-plane schema drift")
    return payload


def render_message(payload: dict[str, Any], max_chars: int) -> str:
    lines = [
        "DEALIX PRESIDENT PROOF",
        f"truth={payload['truth_class']} status={payload['status']}",
        f"proof={payload['proof_id']} trace={payload['trace_id'][:12]}",
        f"sha={payload['source_sha'][:12]} receipt={payload['envelope_sha256'][:16]}",
        "",
    ]
    for section in ("MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"):
        lines.append(section)
        items = payload["brief"][section]
        if not items:
            lines.append("- none")
        else:
            lines.extend(f"- {item}" for item in items)
        lines.append("")
    message = "\n".join(lines).strip()
    if len(message) > max_chars:
        raise ProofError(f"Telegram proof exceeds safe message limit ({len(message)}>{max_chars})")
    return message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--truth-class", required=True, choices=sorted(ALLOWED_TRUTH))
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUS))
    parser.add_argument("--subject", required=True)
    parser.add_argument("--trace-id", default=None)
    parser.add_argument("--money", action="append", default=[])
    parser.add_argument("--decision", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--approval", action="append", default=[])
    parser.add_argument("--next-action", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--output-root", default=str(DEFAULT_OUT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract = load_contract()
    if not SHA_RE.fullmatch(args.source_sha):
        raise ProofError("source SHA must be exact 40-character lowercase hex")
    trace_id = args.trace_id or uuid4().hex
    if not TRACE_RE.fullmatch(trace_id):
        raise ProofError("trace id must be 32 lowercase hex characters")

    out_root = Path(args.output_root)
    validate_proof_root(out_root)
    out_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(out_root, 0o700)

    evidence = [evidence_digest(item) for item in args.evidence]
    previous_digest = read_previous_digest(out_root)
    event_id = f"proof_{uuid4().hex[:16]}"

    core = {
        "specversion": "1.0",
        "id": event_id,
        "source": "dealix://company-machine/founder-proof",
        "type": "com.dealix.founder.proof.v1",
        "subject": safe_text(args.subject, limit=240),
        "time": now_rfc3339(),
        "datacontenttype": "application/json",
        "proof_id": event_id,
        "trace_id": trace_id,
        "source_sha": args.source_sha,
        "truth_class": args.truth_class,
        "status": args.status,
        "previous_envelope_sha256": previous_digest,
        "brief": {
            "MONEY": [safe_text(x) for x in args.money],
            "DECISIONS": [safe_text(x) for x in args.decision],
            "RISKS": [safe_text(x) for x in args.risk],
            "APPROVALS": [safe_text(x) for x in args.approval],
            "NEXT_ACTION": [safe_text(x) for x in args.next_action],
        },
        "evidence": evidence,
        "authority": {
            "customer_send": False,
            "public_publish": False,
            "payment_or_refund": False,
            "main_merge": False,
            "production_mutation": False,
            "dns_db_secret_mutation": False,
        },
    }
    envelope_digest = sha256_hex(canonical_bytes(core))
    envelope = {**core, "envelope_sha256": envelope_digest}
    message = render_message(envelope, int(contract["channel"]["message_max_chars"]))

    filename = f"{event_id}.json"
    envelope_path = out_root / filename
    message_path = out_root / f"{event_id}.telegram.txt"
    digest_path = out_root / f"{event_id}.sha256"

    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    message_path.write_text(message + "\n", encoding="utf-8")
    digest_path.write_text(f"{envelope_digest}  {filename}\n", encoding="utf-8")
    for path in (envelope_path, message_path, digest_path):
        os.chmod(path, 0o600)

    latest = out_root / "LATEST"
    temp = out_root / ".LATEST.tmp"
    temp.write_text(filename + "\n", encoding="utf-8")
    os.chmod(temp, 0o600)
    os.replace(temp, latest)
    os.chmod(latest, 0o600)

    print(message)
    print(f"\nPROOF_PATH={envelope_path}")
    print(f"PROOF_SHA256={envelope_digest}")
    print("TELEGRAM_SENT=false")
    print("L5_EXECUTED=false")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProofError as exc:
        print(f"DEALIX_TELEGRAM_PROOF=FAIL: {exc}")
        raise SystemExit(1)
