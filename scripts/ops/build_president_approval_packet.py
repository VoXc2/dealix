#!/usr/bin/env python3
"""Build ONE consolidated President Approval Packet for L5 actions (read-only).

Every L5 item carries the approval contract fingerprint
ACTION_HASH = sha256(action_type|target|environment|payload)[0:16]
per docs/ops/APPROVAL_FINGERPRINT_CONTRACT.md. Payload changes invalidate the hash.
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
    if not shutil.which("gh"):
        return "UNKNOWN"
    raw = _run(["gh", "pr", "view", str(number), "--json", "headRefOid,url"], timeout=30)
    if not raw:
        return "UNKNOWN"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return "UNKNOWN"
    return f"{payload.get('headRefOid', 'UNKNOWN')}|{payload.get('url', '')}"


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
    refs: list[str] = []
    for row in evidence.get("relationships", []):
        if entity_token.lower() in " ".join(row.values()).lower():
            refs.append(
                f"relationship {row.get('relationship_id', 'UNKNOWN')} "
                f"({row.get('evidence_type', 'UNKNOWN')}, {row.get('observed_at', 'UNKNOWN')}, "
                f"{row.get('commercial_truth', 'UNKNOWN')})"
            )
    for row in evidence.get("events", []):
        if entity_token.lower() in " ".join(row.values()).lower():
            refs.append(f"event {row.get('event', 'UNKNOWN')} ({row.get('evidence', 'UNKNOWN')})")
    return refs or ["NO_DIRECT_EVIDENCE_FOUND"]


def build_items(main_sha: str, chain: dict[int, str], evidence: dict[str, Any], deployed_sha: str = "UNKNOWN") -> list[dict[str, Any]]:
    pr_lines = [f"#{number}:{value.split('|')[0]}" for number, value in sorted(chain.items())]
    chain_payload = "+".join(pr_lines) or "UNKNOWN"
    tip_sha = chain[max(chain)].split("|")[0] if chain else "UNKNOWN"
    raw_items = [
        {
            "action_type": "MERGE_PROTECTED_MAIN",
            "target": "github.com/Dealix-sa/dealix main",
            "environment": "production",
            "why_now": "PR chain #1700-#1705 is locally verified and stacked; main has not absorbed the truth/diagnostic/ops/sector/market fixes.",
            "economic_upside": "Unblocks release parity and the free diagnostic product; no direct cash movement.",
            "risk": "medium",
            "exact_mutation": f"merge {chain_payload} into main (fast-forward if possible)",
            "rollback": f"revert the merge commit; main stays at {main_sha}",
            "evidence": pr_lines or ["PR_CHAIN_UNKNOWN"],
            "payload": chain_payload,
        },
        {
            "action_type": "DEPLOY_RELEASE",
            "target": "api.dealix.me + dealix.me",
            "environment": "production",
            "why_now": "API_RELEASE_PARITY=FAIL: deployed build is behind the accepted release tip, so production truth cannot be claimed.",
            "economic_upside": "Unlocks trustworthy production surface for paid diagnostics and delivery.",
            "risk": "high",
            "exact_mutation": f"deploy post-merge main via the approved Railway/Runner path; after fast-forward merge of the #1705 chain, origin/main is expected to equal {tip_sha} — verify the exact SHA at deploy time",
            "rollback": f"redeploy previous release SHA {deployed_sha}",
            "evidence": [f"current_main={main_sha}", f"accepted_tip={tip_sha}", f"deployed={deployed_sha}", "sentinel: HTTP_WEB=200 HTTP_API=200"],
            "payload": tip_sha,
        },
        {
            "action_type": "FIX_TLS_SAN",
            "target": "www.dealix.me",
            "environment": "production",
            "why_now": "www.dealix.me is a DNS-only CNAME to the Railway edge (apex is Cloudflare-proxied); TLS fails because the origin presents *.up.railway.app, which does not cover www, while Cloudflare's existing edge cert (CN=dealix.me, SAN *.dealix.me) already covers it.",
            "economic_upside": "Removes a trust warning on the public funnel.",
            "risk": "low",
            "exact_mutation": "Cloudflare zone dealix.me: set the `www` CNAME (target e2adtsx4.up.railway.app) to Proxied, then add one redirect rule www.dealix.me/* -> https://dealix.me/$1 (301). No certificate purchase; no Railway change.",
            "rollback": "set the www CNAME back to DNS-only and remove the redirect rule",
            "evidence": [
                "www.dealix.me CNAME -> e2adtsx4.up.railway.app (DNS-only); apex dealix.me is Cloudflare-proxied",
                "curl -k https://www.dealix.me/ -> HTTP 200 (Railway routes Host correctly; only TLS termination is missing)",
                "apex edge cert CN=dealix.me SAN dealix.me,*.dealix.me (Cloudflare/GTS) — already covers www",
            ],
            "payload": "www cloudflare proxy + 301 redirect",
        },
        {
            "action_type": "EXTERNAL_SEND",
            "target": "iMini / Jannie",
            "environment": "founder_income_lane",
            "why_now": "Two-way negotiation exists; counter send of 150 USD is drafted and waiting.",
            "economic_upside": "Founder income lane only; NOT Dealix company revenue.",
            "risk": "medium",
            "exact_mutation": "send the founder-approved counter offer from the founder Gmail account",
            "rollback": "no automated rollback; commercial conversation state unchanged if rejected",
            "evidence": evidence_for("imini", evidence),
            "payload": "counter_send_150_usd",
        },
        {
            "action_type": "EXTERNAL_SEND",
            "target": "NASEEJ FOR TECHNOLOGY (NELC prime)",
            "environment": "production",
            "why_now": "Partner path prepared; one two-way partner conversation is the next evidence gate.",
            "economic_upside": "B2G partner lane; no verified revenue yet.",
            "risk": "medium",
            "exact_mutation": "send the prepared NELC/NASEEJ partner approach draft",
            "rollback": "no automated rollback; relationship state unchanged if no reply",
            "evidence": evidence_for("naseej", evidence) + evidence_for("nelc", evidence),
            "payload": "naseej_partner_approach",
        },
        {
            "action_type": "EXTERNAL_SEND",
            "target": "KARIZMA / Eman Louzon",
            "environment": "production",
            "why_now": "Observed inbound LEAP connection request; no two-way exchange verified yet.",
            "economic_upside": "Event relationship lane; no verified revenue yet.",
            "risk": "low",
            "exact_mutation": "founder reviews and responds inside the LEAP app (not automated)",
            "rollback": "not applicable (manual app action)",
            "evidence": evidence_for("karizma", evidence),
            "payload": "karizma_leap_review",
        },
        {
            "action_type": "EXTERNAL_SEND",
            "target": "Linnk Arabia + Leap29 Saudi",
            "environment": "production",
            "why_now": "Outbound sent with no reply proven; bounded follow-ups keep the thread honest.",
            "economic_upside": "Warm follow-up lane; no verified revenue yet.",
            "risk": "low",
            "exact_mutation": "send one bounded follow-up draft per company after founder approval",
            "rollback": "no automated rollback; stop on any opt-out",
            "evidence": evidence_for("linnk", evidence) + evidence_for("leap29", evidence),
            "payload": "bounded_followups_linnk_leap29",
        },
    ]
    items: list[dict[str, Any]] = []
    for item in raw_items:
        item["decision"] = "PENDING_FOUNDER"
        item["action_hash"] = action_hash(item["action_type"], item["target"], item["environment"], item["payload"])
        item.pop("payload", None)
        missing = [field for field in REQUIRED_FIELDS if field not in item]
        if missing:
            raise ValueError(f"approval item missing fields: {missing}")
        items.append(item)
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
        "One packet. Each item is independent; approval matches one ACTION_HASH only.",
        "",
    ]
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


def build_packet(main_sha: str, chain: dict[int, str], evidence: dict[str, Any], deployed_sha: str = "UNKNOWN") -> dict[str, Any]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "main_sha": main_sha,
        "items": build_items(main_sha, chain, evidence, deployed_sha),
        "evidence_summary": {
            "verified_revenue_sar": evidence.get("verified_revenue_sar", "UNKNOWN"),
            "verified_paid_pilots": evidence.get("verified_paid_pilots", "UNKNOWN"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the consolidated President Approval Packet (read-only)")
    parser.add_argument("--write", action="store_true", help=f"write packet into {FOUNDER_OS / 'queues'}")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    parser.add_argument("--deployed-sha", default="UNKNOWN", help="currently deployed release SHA for rollback")
    args = parser.parse_args()

    main_sha = git_rev("origin/main")
    chain = {}
    for number in (1700, 1701, 1702, 1703, 1704, 1705):
        value = pr_head(number)
        if value != "UNKNOWN":
            chain[number] = value
    evidence = collect_evidence()
    packet = build_packet(main_sha, chain, evidence, args.deployed_sha)
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
