#!/usr/bin/env python3
"""Canonical Dealix self-operating company cycle.

This is an internal, evidence-first Company OS runner. It may research, score,
prioritize, draft, log proof gaps, and prepare approval packets. It never sends,
publishes, charges, merges, deploys, or mutates production.

Usage:
    python scripts/commercial/run_self_operating_company_os.py --mode draft-only --limit 50
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass

try:
    from dealix.commercial.universal_diagnostic_factory import (
        DiagnosticDepth,
        UniversalDiagnosticFactory,
    )
except Exception:
    UniversalDiagnosticFactory = None
    DiagnosticDepth = None
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "reports" / "self_operating_company_os"
DATA_ROOT = ROOT / "data" / "self_operating_company_os"

CANONICAL_COMMERCIAL_PATH = [
    "REAL_INTERACTION",
    "VERIFIED_RELATIONSHIP",
    "QUALIFIED_PROBLEM",
    "FREE_MINI_DIAGNOSTIC",
    "QUALIFIED_DISCOVERY",
    "CUSTOMER_SPECIFIC_QUOTE",
    "30_DAY_REVENUE_COMMAND_PILOT",
    "PAYMENT_EVIDENCE",
    "DELIVERY_EVIDENCE",
    "CUSTOMER_VALIDATED_PROOF",
    "EXPAND_OR_REDESIGN",
]

CANONICAL_ENTRY_OFFER = "Free Mini Diagnostic"
CANONICAL_PILOT = "30-Day Revenue Command Pilot"

FORBIDDEN_ENV_FLAGS = {
    "DEALIX_EXTERNAL_SEND": "1",
    "DEALIX_EMAIL_LIVE_SEND": "1",
    "DEALIX_WHATSAPP_OUTBOUND": "1",
    "DEALIX_PUBLIC_PUBLISH": "1",
    "DEALIX_PAID_SPEND": "1",
    "DEALIX_PAYMENT_EXECUTION": "1",
    "DEALIX_PRODUCTION_MUTATION": "1",
    "DEALIX_DNS_MUTATION": "1",
    "DEALIX_DB_MUTATION": "1",
    "DEALIX_SECRET_MUTATION": "1",
    "EXTERNAL_SEND_ENABLED": "true",
    "AUTO_WHATSAPP_ENABLED": "true",
    "AUTO_LINKEDIN_ENABLED": "true",
    "AUTO_PAYMENT_CAPTURE_ENABLED": "true",
    "AUTO_MERGE_ENABLED": "true",
    "PRODUCTION_MUTATION_ENABLED": "true",
}

REAL_RELATIONSHIP_STATES = {
    "REAL_INTERACTION",
    "VERIFIED_RELATIONSHIP",
    "INBOUND",
}
PURPOSE_CONSENT_STATES = {
    "PURPOSE_SPECIFIC",
    "INBOUND_REQUEST",
}
SUPPRESSED_STATES = {"SUPPRESSED", "OPTED_OUT", "WITHDRAWN"}

PLAYBOOKS = [
    {
        "name": "production_and_trust",
        "priority": 100,
        "goal": "Close current Production Trust and release-parity evidence before public scale.",
        "safe_actions": [
            "reconcile current main and production evidence",
            "classify exact-head trust blockers without weakening gates",
            "prepare rollback-aware public-truth closure evidence",
        ],
    },
    {
        "name": "market_signal_intake",
        "priority": 95,
        "goal": "Turn official and first-party signals into evidence-backed research attention.",
        "safe_actions": [
            "ingest source-bound market signals",
            "deduplicate companies and evidence references",
            "create research hypotheses without promoting relationship or consent",
        ],
    },
    {
        "name": "relationship_and_revenue",
        "priority": 90,
        "goal": "Move only real interactions through the canonical commercial path.",
        "safe_actions": [
            "qualify evidenced interactions",
            "prepare Free Mini Diagnostic drafts",
            "prepare discovery and customer-specific quote inputs",
        ],
    },
    {
        "name": "delivery_and_proof",
        "priority": 85,
        "goal": "Prepare governed 30-day delivery and customer-validated Proof Packs.",
        "safe_actions": [
            "validate scope baseline and data-boundary evidence",
            "prepare delivery work queues and acceptance criteria",
            "assemble proof gaps without inventing customer outcomes",
        ],
    },
    {
        "name": "content_and_distribution",
        "priority": 75,
        "goal": "Turn evidence into brand-safe drafts that support the commercial wedge.",
        "safe_actions": [
            "prepare founder insight drafts from verified evidence",
            "prepare Dealix Page and website content drafts",
            "prepare proof-safe repurposing packs",
        ],
    },
    {
        "name": "learning_loop",
        "priority": 70,
        "goal": "Improve priorities and playbooks from verified outcomes and failures.",
        "safe_actions": [
            "classify failed or stale actions",
            "extract repeated objections and delivery friction",
            "recommend the next bounded internal improvement",
        ],
    },
]


@dataclass
class ActionItem:
    id: str
    playbook: str
    action: str
    owner: str
    status: str
    approval_required: bool
    risk_level: str


@dataclass
class TargetCard:
    id: str
    company_name: str
    segment: str
    source: str
    evidence_refs: list[str]
    relationship_state: str
    consent_state: str
    suppression_state: str
    commercial_stage: str
    pain_hypothesis: str
    score: int
    next_action: str
    approval_status: str


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def date_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def ensure_dirs() -> None:
    for path in [
        OUT_ROOT / "daily",
        OUT_ROOT / "actions",
        OUT_ROOT / "approvals",
        OUT_ROOT / "targets",
        OUT_ROOT / "proof",
        OUT_ROOT / "content",
        DATA_ROOT,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def env_tripwire() -> list[str]:
    violations: list[str] = []
    for key, bad_value in FORBIDDEN_ENV_FLAGS.items():
        if os.getenv(key, "").strip().lower() == bad_value.lower():
            violations.append(f"{key}={bad_value}")
    return violations


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def load_targets() -> list[dict[str, Any]]:
    """Load only real/evidence-bearing inputs; never synthesize commercial targets."""
    path = DATA_ROOT / "targets.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def score_target(target: dict[str, Any]) -> int:
    fit = int(target.get("fit_score", 50))
    urgency = int(target.get("urgency_score", 50))
    evidence = int(target.get("evidence_score", 50))
    access = int(target.get("access_score", 25))
    risk = int(target.get("risk_score", 30))
    score = round(
        (fit * 0.30)
        + (urgency * 0.25)
        + (evidence * 0.25)
        + (access * 0.20)
        - (risk * 0.15)
    )
    return max(0, min(100, score))


def _dispatch_eligible(target: dict[str, Any]) -> bool:
    relationship = str(target.get("relationship_state", "RESEARCH")).upper()
    consent = str(target.get("consent_state", "NONE")).upper()
    suppression = str(target.get("suppression_state", "CLEAR")).upper()
    if suppression in SUPPRESSED_STATES:
        return False
    return relationship in REAL_RELATIONSHIP_STATES or consent in PURPOSE_CONSENT_STATES


def _next_action(target: dict[str, Any]) -> str:
    evidence_refs = _string_list(target.get("evidence_refs"))
    source = str(target.get("source", "")).strip()
    stage = str(target.get("commercial_stage", "RESEARCH")).upper()

    if not source or not evidence_refs:
        return "BLOCKED: add source and evidence references before commercial progression"
    if stage == "RESEARCH":
        return "capture a real interaction or purpose-specific consent; no outbound promotion"
    if stage in {"REAL_INTERACTION", "VERIFIED_RELATIONSHIP", "QUALIFIED_PROBLEM"}:
        return f"prepare {CANONICAL_ENTRY_OFFER} draft and evidence gaps"
    if stage == "FREE_MINI_DIAGNOSTIC":
        return "prepare qualified discovery agenda and baseline questions"
    if stage == "QUALIFIED_DISCOVERY":
        return "prepare customer-specific quote draft; no global price authority"
    if stage == "CUSTOMER_SPECIFIC_QUOTE":
        return "wait for approved customer acceptance and payment/start-condition evidence"
    if stage in {"VERIFIED_PAYMENT", "PAYMENT_EVIDENCE"}:
        return f"handoff authorized scope to dealix-delivery for {CANONICAL_PILOT}"
    if stage in {"DELIVERY", "DELIVERY_EVIDENCE"}:
        return "continue governed delivery and assemble customer evidence gaps"
    if stage in {"CUSTOMER_VALIDATED_PROOF", "PERMISSIONED_PROOF"}:
        return "prepare STOP / EXPAND / REDESIGN decision; no automatic upsell"
    return "review stage against canonical commercial path"


def build_target_cards(limit: int) -> list[TargetCard]:
    cards: list[TargetCard] = []
    for idx, target in enumerate(load_targets()[:limit], start=1):
        evidence_refs = _string_list(target.get("evidence_refs"))
        source = str(target.get("source", "")).strip()
        relationship = str(target.get("relationship_state", "RESEARCH")).upper()
        consent = str(target.get("consent_state", "NONE")).upper()
        suppression = str(target.get("suppression_state", "CLEAR")).upper()
        stage = str(target.get("commercial_stage", "RESEARCH")).upper()
        evidence_ready = bool(source and evidence_refs)
        dispatch_ready = evidence_ready and _dispatch_eligible(target)
        cards.append(
            TargetCard(
                id=f"TGT-{idx:04d}",
                company_name=str(target.get("company_name", "Unknown company")),
                segment=str(target.get("segment", "unknown")),
                source=source or "UNKNOWN_NOT_EVIDENCE_BACKED",
                evidence_refs=evidence_refs,
                relationship_state=relationship,
                consent_state=consent,
                suppression_state=suppression,
                commercial_stage=stage,
                pain_hypothesis=str(target.get("pain_hypothesis", "UNKNOWN_NOT_EVIDENCE_BACKED")),
                score=score_target(target) if evidence_ready else 0,
                next_action=_next_action(target),
                approval_status=(
                    "pending_action_bound_approval"
                    if dispatch_ready
                    else "internal_only_not_dispatch_eligible"
                ),
            )
        )
    return sorted(cards, key=lambda card: card.score, reverse=True)


def build_actions() -> list[ActionItem]:
    actions: list[ActionItem] = []
    counter = 1
    for playbook in sorted(PLAYBOOKS, key=lambda item: item["priority"], reverse=True):
        for action in playbook["safe_actions"]:
            actions.append(
                ActionItem(
                    id=f"ACT-{counter:04d}",
                    playbook=playbook["name"],
                    action=action,
                    owner="Dealix Company OS",
                    status="queued_internal",
                    approval_required=False,
                    risk_level="low",
                )
            )
            counter += 1
    return actions


def _draft_for(card: TargetCard) -> str:
    return (
        f"السلام عليكم [الاسم]، معك مؤسس Dealix. لاحظت سياقًا مرتبطًا بـ {card.company_name} "
        f"وأبغى أتأكد من فرضية واحدة بدل ما أفترض: {card.pain_hypothesis}. "
        "Dealix نبدأ فيه بـ Free Mini Diagnostic لتحديد أين يضيع القرار أو المتابعة، "
        "وما الدليل المتاح، وهل يوجد Pilot صغير قابل للقياس خلال 30 يوم. "
        "إذا مناسب، أرسل لك التشخيص المختصر ونقرر بعدها هل يستحق Discovery أو لا."
    )


def build_approval_queue(cards: list[TargetCard]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for card in cards:
        if card.approval_status != "pending_action_bound_approval":
            continue
        queue.append(
            {
                "target_id": card.id,
                "company_name": card.company_name,
                "action_type": "relationship_governed_follow_up_draft",
                "commercial_stage": card.commercial_stage,
                "relationship_state": card.relationship_state,
                "consent_state": card.consent_state,
                "suppression_state": card.suppression_state,
                "evidence_refs": card.evidence_refs,
                "draft_text": _draft_for(card),
                "risk_flags": [
                    "external_action_requires_action_bound_approval",
                    "sender_health_required",
                    "suppression_recheck_required",
                    "provider_receipt_required",
                    "no_auto_send",
                ],
                "status": "pending_action_bound_approval",
            }
        )
    return queue


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_content_queue(cards: list[TargetCard]) -> Path:
    today = date_stamp()
    path = OUT_ROOT / "content" / f"{today}.md"
    lines = [
        f"# Dealix evidence-backed content queue — {today}",
        "",
        "All outputs are internal drafts until the matching publish authority exists.",
        "",
        "- Founder draft: why Revenue + Proof + Command is an operating wedge, not an agent demo.",
        "- Proof draft: what separates activity, delivery, payment, value and publication permission.",
        "- Market draft: why a real interaction is more valuable than a scraped contact list.",
        "",
        "## Evidence-derived angles",
    ]
    for card in cards[:5]:
        if card.evidence_refs:
            lines.append(
                f"- {card.company_name}: {card.pain_hypothesis} "
                f"(stage={card.commercial_stage}; evidence={len(card.evidence_refs)})"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_daily_report(
    cards: list[TargetCard],
    actions: list[ActionItem],
    approvals: list[dict[str, Any]],
    tripwire: list[str],
) -> Path:
    today = date_stamp()
    path = OUT_ROOT / "daily" / f"{today}.md"
    lines = [
        f"# Dealix Self-Operating Company OS — {today}",
        "",
        "## Verdict",
        "SAFE_INTERNAL_AUTONOMY" if not tripwire else "HALTED_BY_ENV_TRIPWIRE",
        "",
        "## Canonical commercial path",
        " -> ".join(CANONICAL_COMMERCIAL_PATH),
        "",
        "## Top evidence-backed targets",
    ]
    if not cards:
        lines.append("- No evidence-backed targets loaded; synthetic targets are intentionally disabled.")
    for card in cards[:10]:
        lines.append(
            f"- **{card.id} — {card.company_name}** | score={card.score} | "
            f"stage={card.commercial_stage} | next={card.next_action}"
        )
    lines.extend(["", "## Top internal actions"])
    for action in actions[:12]:
        lines.append(f"- **{action.id}** [{action.playbook}] {action.action}")
    lines.extend(["", "## Approval-ready relationship actions"])
    if not approvals:
        lines.append("- None. Research/public contact data cannot create send authority.")
    for item in approvals[:10]:
        lines.append(f"- **{item['target_id']}** {item['action_type']} — {item['status']}")
    lines.extend(
        [
            "",
            "## Current executive focus",
            "1. Production Trust: current exact-head acceptance + current-main Web/API release parity.",
            "2. Revenue/Customer: real interaction -> qualified problem -> Diagnostic -> customer-specific quote -> verified payment.",
            "3. Company/Scale: Deep-WIP <= 3; partner/B2G only where eligibility, non-overlap, margin, and proof route are evidenced.",
            "4. Delivery/Proof: predefine acceptance and a customer-validated Proof Pack for paid work.",
            "5. Learning: convert root causes into bounded regression and evidence rules.",
            "",
            "## Truth firewall",
            "- Research != relationship.",
            "- Public contact != consent.",
            "- Draft != sent.",
            "- Quote != invoice.",
            "- Invoice != payment.",
            "- Activity != delivery.",
            "- Synthetic/demo != customer proof.",
            "- Customer outcome != publication permission.",
        ]
    )
    if tripwire:
        lines.extend(["", "## Tripwire violations", *[f"- {item}" for item in tripwire]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def verify_outputs() -> dict[str, Any]:
    today = date_stamp()
    required = [
        OUT_ROOT / "daily" / f"{today}.md",
        OUT_ROOT / "actions" / f"{today}.json",
        OUT_ROOT / "approvals" / f"{today}.json",
        OUT_ROOT / "targets" / f"{today}.json",
        OUT_ROOT / "proof" / f"{today}.json",
        OUT_ROOT / "content" / f"{today}.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    return {"ok": not missing, "missing": missing}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    ensure_dirs()
    today = date_stamp()
    tripwire = env_tripwire()
    cards = build_target_cards(args.limit)
    actions = build_actions()
    approvals = build_approval_queue(cards)

    proof_log = {
        "generated_at": utc_stamp(),
        "mode": args.mode,
        "source_sha": os.getenv("DEALIX_SOURCE_SHA", "UNKNOWN_NOT_EVIDENCE_BACKED"),
        "tripwire_violations": tripwire,
        "truth_firewall": [
            "research_is_not_relationship",
            "public_contact_is_not_consent",
            "draft_is_not_sent",
            "invoice_is_not_payment",
            "synthetic_is_not_customer_proof",
        ],
        "commercial_path": CANONICAL_COMMERCIAL_PATH,
        "safe_actions_count": len(actions),
        "evidence_backed_target_count": len(cards),
        "approval_ready_count": len(approvals),
    }

    # Universal Diagnostic Factory enrichment — D1 rapid per target (evidence-first, never fails cycle)
    try:
        if UniversalDiagnosticFactory and DiagnosticDepth:
            factory = UniversalDiagnosticFactory()
            for card in cards:
                sector = getattr(card, "sector", "technology_saas_si") or "technology_saas_si"
                buyer = getattr(card, "buyer_role", "ceo") or "ceo"
                problem = getattr(card, "problem", "revenue_leakage") or "revenue_leakage"
                families = factory.compose(sector, "sme", buyer, problem, DiagnosticDepth.D1_RAPID)
                if hasattr(card, "__dict__"):
                    card.__dict__["diagnostic_families"] = [f.family_id for f in families[:5]]
    except Exception as exc:
        print(f"DIAGNOSTIC_ENRICHMENT=SKIPPED reason={type(exc).__name__}:{exc}")

    write_json(OUT_ROOT / "targets" / f"{today}.json", [asdict(card) for card in cards])
    write_json(OUT_ROOT / "actions" / f"{today}.json", [asdict(action) for action in actions])
    write_json(OUT_ROOT / "approvals" / f"{today}.json", approvals)
    write_json(OUT_ROOT / "proof" / f"{today}.json", proof_log)
    write_content_queue(cards)
    report = write_daily_report(cards, actions, approvals, tripwire)
    verification = verify_outputs()

    summary = {
        "ok": verification["ok"] and not tripwire,
        "mode": args.mode,
        "daily_report": str(report.relative_to(ROOT)),
        "targets": len(cards),
        "actions": len(actions),
        "approvals": len(approvals),
        "missing": verification["missing"],
        "tripwire_violations": tripwire,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
