#!/usr/bin/env python3
"""Build the Dealix President Approval Packet without inventing L5 authority.

The packet is a review artifact only. It never executes an action.

Hard laws:
- no hard-coded historical PR chain;
- no relationship/event evidence is promoted into an external send by itself;
- no deploy/DNS/DB/secret/provider/payment/tender action is synthesized from stale state;
- every non-merge L5 item must be supplied as an explicit current action manifest;
- every action receives ACTION_HASH = sha256(action_type|target|environment|payload)[:16];
- changing the exact payload invalidates prior approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
FOUNDER_OS = Path("/opt/dealix/company-os/founder-os")

REQUIRED_FIELDS = (
    "action_type",
    "target",
    "environment",
    "why_now",
    "economic_upside",
    "risk",
    "exact_mutation",
    "rollback",
    "evidence",
    "decision",
    "action_hash",
)

REQUEST_FIELDS = (
    "action_type",
    "target",
    "environment",
    "why_now",
    "economic_upside",
    "risk",
    "exact_mutation",
    "rollback",
    "evidence",
    "payload",
)

L5_ACTION_TYPES = frozenset(
    {
        "MERGE_PROTECTED_MAIN",
        "DEPLOY_RELEASE",
        "EXTERNAL_SEND",
        "PUBLIC_PUBLISH",
        "SPEND",
        "PAYMENT",
        "REFUND",
        "BINDING_QUOTE",
        "CONTRACT_SUBMIT",
        "TENDER_SUBMIT",
        "PRODUCTION_MUTATION",
        "DNS_MUTATION",
        "DB_MUTATION",
        "SECRET_MUTATION",
        "PROVIDER_MUTATION",
    }
)


def action_hash(action_type: str, target: str, environment: str, payload: str) -> str:
    material = "|".join([action_type, target, environment, payload])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _run(cmd: list[str], timeout: int = 20) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def git_rev(ref: str) -> str:
    return _run(["git", "-C", str(REPO_ROOT), "rev-parse", ref], timeout=10).strip() or "UNKNOWN"


def pr_head(number: int) -> str:
    """Return the exact current PR head plus URL, or UNKNOWN when it cannot be resolved."""
    if not shutil.which("gh"):
        return "UNKNOWN"
    raw = _run(["gh", "pr", "view", str(number), "--json", "headRefOid,url,state,isDraft"], timeout=30)
    if not raw:
        return "UNKNOWN"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return "UNKNOWN"
    sha = str(payload.get("headRefOid") or "").strip()
    url = str(payload.get("url") or "").strip()
    state = str(payload.get("state") or "UNKNOWN").strip()
    draft = bool(payload.get("isDraft"))
    if not sha:
        return "UNKNOWN"
    return f"{sha}|{url}|{state}|draft={str(draft).lower()}"


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return []
    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        values = line.split("\t")
        rows.append({header[i]: (values[i] if i < len(values) else "") for i in range(len(header))})
    return rows


def collect_evidence(founder_os: Path = FOUNDER_OS) -> dict[str, Any]:
    """Collect context only. Context never becomes executable approval authority automatically."""
    truth_path = founder_os / "current" / "LATEST_TRUTH.json"
    truth: dict[str, Any] = {}
    if truth_path.exists():
        try:
            truth = json.loads(truth_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            truth = {}
    economic = truth.get("economic_truth", {})
    return {
        "relationships": read_tsv(founder_os / "tables" / "SCOPED_RELATIONSHIPS.tsv"),
        "events": read_tsv(founder_os / "tables" / "EVENT_INTERACTIONS.tsv"),
        "verified_revenue_sar": economic.get("verified_revenue_sar", "UNKNOWN"),
        "verified_paid_pilots": economic.get("verified_paid_pilots", "UNKNOWN"),
        "real_contacts": economic.get("real_contacts", "UNKNOWN"),
    }


def evidence_for(entity_token: str, evidence: dict[str, Any]) -> list[str]:
    """Render relationship/event context without granting send/contract authority."""
    refs: list[str] = []
    for row in evidence.get("relationships", []):
        if entity_token.lower() in " ".join(str(value) for value in row.values()).lower():
            refs.append(
                f"relationship {row.get('relationship_id', 'UNKNOWN')} "
                f"({row.get('evidence_type', 'UNKNOWN')}, {row.get('observed_at', 'UNKNOWN')}, "
                f"{row.get('commercial_truth', 'UNKNOWN')})"
            )
    for row in evidence.get("events", []):
        if entity_token.lower() in " ".join(str(value) for value in row.values()).lower():
            refs.append(f"event {row.get('event', 'UNKNOWN')} ({row.get('evidence', 'UNKNOWN')})")
    return refs or ["NO_DIRECT_EVIDENCE_FOUND"]


def read_action_manifest(path: Path) -> list[dict[str, Any]]:
    """Read explicitly requested current L5 actions from JSON.

    Accepted shapes:
      [item, ...]
      {"items": [item, ...]}

    The manifest is authority input, not execution. Exact payload is hashed and
    removed from the emitted packet.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("items")
    if not isinstance(payload, list):
        raise ValueError("action manifest must be a list or an object with an items list")
    if not all(isinstance(item, dict) for item in payload):
        raise ValueError("every action manifest item must be an object")
    return payload


def _normalize_requested_action(item: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUEST_FIELDS if field not in item]
    if missing:
        raise ValueError(f"requested action missing fields: {missing}")

    action_type = str(item["action_type"]).strip()
    if action_type not in L5_ACTION_TYPES:
        raise ValueError(f"unsupported L5 action_type: {action_type}")

    target = str(item["target"]).strip()
    environment = str(item["environment"]).strip()
    payload = str(item["payload"])
    evidence = item["evidence"]
    if not target or not environment or not payload:
        raise ValueError("requested action target/environment/payload must be non-empty")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(ref, str) and ref.strip() for ref in evidence):
        raise ValueError("requested action evidence must be a non-empty list of evidence references")
    if action_type == "EXTERNAL_SEND" and any(ref == "NO_DIRECT_EVIDENCE_FOUND" for ref in evidence):
        raise ValueError("external send cannot be promoted without direct evidence")

    normalized = {
        "action_type": action_type,
        "target": target,
        "environment": environment,
        "why_now": str(item["why_now"]).strip(),
        "economic_upside": str(item["economic_upside"]).strip(),
        "risk": str(item["risk"]).strip(),
        "exact_mutation": str(item["exact_mutation"]).strip(),
        "rollback": str(item["rollback"]).strip(),
        "evidence": evidence,
        "decision": "PENDING_FOUNDER",
        "action_hash": action_hash(action_type, target, environment, payload),
    }
    for field in REQUIRED_FIELDS:
        if field not in normalized:
            raise ValueError(f"approval item missing field: {field}")
    return normalized


def build_items(
    main_sha: str,
    chain: dict[int, str],
    evidence: dict[str, Any],
    deployed_sha: str = "UNKNOWN",
    requested_actions: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build only explicitly grounded approval candidates.

    Relationship/event/economic context is intentionally *not* sufficient to
    create an EXTERNAL_SEND, deploy, DNS, payment, tender or other L5 item.
    `deployed_sha` is retained for API compatibility/context only; it does not
    mint deployment authority.
    """
    del evidence, deployed_sha  # context only; never auto-promote into authority
    items: list[dict[str, Any]] = []

    if chain:
        pr_lines: list[str] = []
        for number, value in sorted(chain.items()):
            parts = value.split("|")
            sha = parts[0].strip() if parts else ""
            if not sha or sha == "UNKNOWN":
                raise ValueError(f"PR #{number} has no exact current head")
            pr_lines.append(f"#{number}:{sha}")
        payload = "+".join(pr_lines)
        items.append(
            _normalize_requested_action(
                {
                    "action_type": "MERGE_PROTECTED_MAIN",
                    "target": "github.com/Dealix-sa/dealix main",
                    "environment": "repository",
                    "why_now": "Caller explicitly requested an exact current PR set for President review.",
                    "economic_upside": "Integrates accepted source value only if each listed head remains current and independently accepted.",
                    "risk": "medium",
                    "exact_mutation": f"serially integrate exact heads {payload}; re-resolve main and every PR immediately before each merge",
                    "rollback": f"revert the resulting merge/squash commit(s); pre-action main was {main_sha}",
                    "evidence": [f"pre_action_main={main_sha}", *pr_lines],
                    "payload": payload,
                }
            )
        )

    for item in requested_actions or []:
        items.append(_normalize_requested_action(item))

    return items


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# PRESIDENT APPROVAL PACKET",
        "",
        f"Generated: {packet['generated_at']}",
        f"Main SHA: {packet['main_sha']}",
        f"Verified revenue (SAR): {packet['evidence_summary'].get('verified_revenue_sar', 'UNKNOWN')}",
        f"Verified paid pilots: {packet['evidence_summary'].get('verified_paid_pilots', 'UNKNOWN')}",
        "",
        "Fail-closed packet: no action appears unless supplied as an exact current action or explicit PR head set.",
        "Every item is independent; approval matches one ACTION_HASH only. Payload changes require a new hash.",
        "",
    ]
    if not packet["items"]:
        lines.extend(["No current L5 action candidates were explicitly supplied.", ""])
    for index, item in enumerate(packet["items"], start=1):
        lines.extend(
            [
                f"## {index}. {item['action_type']} — {item['target']}",
                f"- WHY NOW: {item['why_now']}",
                f"- ECONOMIC UPSIDE: {item['economic_upside']}",
                f"- RISK: {item['risk']}",
                f"- EXACT MUTATION: {item['exact_mutation']}",
                f"- ROLLBACK: {item['rollback']}",
                f"- EVIDENCE: {'; '.join(item['evidence'])}",
                f"- DECISION: {item['decision']}",
                f"- ACTION_HASH: {item['action_hash']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_packet(
    main_sha: str,
    chain: dict[int, str],
    evidence: dict[str, Any],
    deployed_sha: str = "UNKNOWN",
    requested_actions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "main_sha": main_sha,
        "items": build_items(main_sha, chain, evidence, deployed_sha, requested_actions),
        "evidence_summary": {
            "verified_revenue_sar": evidence.get("verified_revenue_sar", "UNKNOWN"),
            "verified_paid_pilots": evidence.get("verified_paid_pilots", "UNKNOWN"),
            "real_contacts": evidence.get("real_contacts", "UNKNOWN"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the fail-closed President Approval Packet (read-only)")
    parser.add_argument("--write", action="store_true", help=f"write packet into {FOUNDER_OS / 'queues'}")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    parser.add_argument("--deployed-sha", default="UNKNOWN", help="context only; never creates deploy authority")
    parser.add_argument("--pr", action="append", type=int, default=[], help="explicit current PR number to include; repeatable")
    parser.add_argument("--action-file", type=Path, help="JSON file of exact current L5 action manifests")
    args = parser.parse_args()

    main_sha = git_rev("origin/main")
    chain: dict[int, str] = {}
    for number in args.pr:
        value = pr_head(number)
        if value == "UNKNOWN":
            parser.error(f"cannot resolve exact current head for PR #{number}; refusing partial approval packet")
        chain[number] = value

    requested_actions = read_action_manifest(args.action_file) if args.action_file else []
    evidence = collect_evidence()
    packet = build_packet(main_sha, chain, evidence, args.deployed_sha, requested_actions)
    rendered = json.dumps(packet, indent=2, ensure_ascii=False) if args.json else render_markdown(packet)
    print(rendered)

    if args.write:
        queues = FOUNDER_OS / "queues"
        queues.mkdir(parents=True, exist_ok=True)
        (queues / "PRESIDENT_APPROVAL_PACKET.md").write_text(render_markdown(packet), encoding="utf-8")
        (queues / "PRESIDENT_APPROVAL_PACKET.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {queues / 'PRESIDENT_APPROVAL_PACKET.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
