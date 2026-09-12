"""Generate a truth-gated bilingual Dealix proposal draft.

This is the canonical legacy proposal CLI upgraded to obey the commercial truth
firewall. It does not send anything. A customer proposal draft is permitted only
after a qualified problem or an explicit customer request. Research/demo inputs
produce INTERNAL_HYPOTHESIS artifacts, never customer-specific factual proposals.

No fixed price authority lives here. Commercial structure remains a founder
approval placeholder until an action-bound price/terms approval exists.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
INDEX_PATH = REPO_ROOT / "business" / "_data" / "proposals.index.json"
EXPORT_DIR = REPO_ROOT / "business" / "proposals" / "generated"

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

CANONICAL_OFFERS = {
    "Saudi Opportunity Snapshot",
    "Revenue Proof Sprint",
    "Revenue Command Pilot",
    "Saudi Market Access Sprint",
    "AI Company OS Setup",
    "B2G Readiness Sprint",
    "Partner / Distributor Desk",
    "Revenue Command Room",
}

# Backward-compatible CLI aliases. They map into current canonical offer families;
# they do not retain legacy price authority.
LEGACY_OFFER_ALIASES = {
    "Revenue OS": "Revenue Command Pilot",
    "Command Center": "Revenue Command Room",
    "Delivery OS": "AI Company OS Setup",
    "Review & Reputation": "Revenue Proof Sprint",
    "Custom Enterprise": "AI Company OS Setup",
    "Managed Retainer": "AI Company OS Setup",
}

PROPOSAL_READY_STATES = {
    "QUALIFIED_PROBLEM",
    "DISCOVERY_READY",
    "PROPOSAL_READY",
    "DECISION_PENDING",
}

DEMO_ACCOUNT = {
    "id": "demo-test",
    "name": "Demo Test Account",
    "segment": "B2B Services",
    "city": "Riyadh",
    "visibleSignal": "Manual follow-up, scattered tools",
    "weaknessHypothesis": "Revenue leakage from slow response",
}


def _copy(lang: str, ar: str, en: str) -> str:
    return ar if lang == "ar" else en


def canonical_offer(value: str) -> str:
    offer = LEGACY_OFFER_ALIASES.get(value, value)
    if offer not in CANONICAL_OFFERS:
        raise ValueError(f"offer is not canonical: {value}")
    return offer


def load_account(account_id: str, mode: str) -> dict | None:
    if LEADS_PATH.exists():
        data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
        match = next((a for a in data.get("accounts", []) if a.get("id") == account_id), None)
        if match:
            return match
    if mode in {"demo", "internal"}:
        return {**DEMO_ACCOUNT, "id": account_id}
    return None


def proposal_gate(
    *,
    mode: str,
    qualification_state: str,
    explicit_customer_request: bool,
    problem_evidence_refs: list[str],
) -> tuple[bool, str, str]:
    if mode != "live":
        return True, "INTERNAL_HYPOTHESIS", "RESEARCH_OR_DEMO_ONLY"
    if explicit_customer_request:
        return True, "CUSTOMER_PROPOSAL_DRAFT", "EXPLICIT_CUSTOMER_REQUEST"
    if qualification_state in PROPOSAL_READY_STATES and problem_evidence_refs:
        return True, "CUSTOMER_PROPOSAL_DRAFT", "QUALIFIED_PROBLEM"
    return False, "BLOCKED", "QUALIFIED_PROBLEM_OR_EXPLICIT_REQUEST_REQUIRED"


def build_proposal(
    account: dict,
    offer: str,
    lang: str,
    timeline: str,
    mode: str,
    qualification_state: str,
    problem_evidence_refs: list[str],
    artifact_kind: str,
    gate_basis: str,
    price_approval_ref: str,
) -> dict:
    account_name = account.get("name") or account.get("id") or UNKNOWN
    visible_signal = account.get("visibleSignal") or UNKNOWN
    weakness_hypothesis = account.get("weaknessHypothesis") or UNKNOWN
    customer_fact_allowed = artifact_kind == "CUSTOMER_PROPOSAL_DRAFT" and bool(problem_evidence_refs)

    if customer_fact_allowed:
        understood_problem = {
            "value": weakness_hypothesis,
            "truth_class": "CUSTOMER_PROVIDED_OR_EVIDENCED",
            "evidence_refs": problem_evidence_refs,
        }
    else:
        understood_problem = {
            "value": weakness_hypothesis,
            "truth_class": "PATTERN_OR_HYPOTHESIS",
            "evidence_refs": [],
        }

    commercial_status = (
        "FOUNDER_APPROVED_REFERENCE_PRESENT"
        if price_approval_ref != UNKNOWN
        else "FOUNDER_APPROVAL_REQUIRED"
    )

    return {
        "meta": {
            "account_id": account.get("id", UNKNOWN),
            "account_name": account_name,
            "offer": offer,
            "language": lang,
            "timeline": timeline,
            "mode": mode,
            "artifact_kind": artifact_kind,
            "proposal_gate_basis": gate_basis,
            "qualification_state": qualification_state,
            "generated_at": dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
            "review_status": "pending_review",
            "external_send_authority": False,
        },
        "1_executive_context": _copy(
            lang,
            f"مسودة {offer} للجهة {account_name}. لا تُعد مرسلة أو مقبولة.",
            f"Draft {offer} for {account_name}. This is not sent or accepted.",
        ),
        "2_what_we_understood": understood_problem,
        "3_current_observed_state": {
            "value": visible_signal,
            "truth_class": "PATTERN_OR_SOURCE_SIGNAL" if not customer_fact_allowed else "EVIDENCED_CONTEXT",
            "evidence_refs": problem_evidence_refs if customer_fact_allowed else [],
        },
        "4_customer_confirmed_problem": understood_problem if customer_fact_allowed else {
            "value": UNKNOWN,
            "truth_class": "UNKNOWN",
            "evidence_refs": [],
        },
        "5_diagnostic_findings": [],
        "6_desired_outcome": _copy(
            lang,
            "يُحدد مع العميل ويُثبت في الاكتشاف؛ لا نتيجة مختلقة هنا.",
            "To be confirmed with the customer in discovery; no invented outcome here.",
        ),
        "7_proposed_approach": offer,
        "8_scope": [
            "customer-specific discovery/baseline",
            "agreed implementation workstreams",
            "verification and acceptance evidence",
        ],
        "9_exclusions": [
            "unapproved third-party spend",
            "work outside agreed scope",
            "production mutation without authority",
            "public proof without permission",
        ],
        "10_workstreams": ["diagnose", "design", "implement", "verify", "handover"],
        "11_solution_architecture": "CUSTOMER_SPECIFIC_TBD_AFTER_DISCOVERY",
        "12_ai_automation_role": "Only where evidence and governance support fit; human/L5 gates remain.",
        "13_integrations": [],
        "14_data_requirements": ["minimum necessary customer-provided evidence", "approved system exports where required"],
        "15_security_privacy": ["PDPL", "least privilege", "customer data boundary", "auditability"],
        "16_implementation_plan": ["baseline", "bounded pilot/implementation", "test", "acceptance"],
        "17_delivery_phases": ["prepare", "implement", "verify", "customer validate"],
        "18_responsibilities": {
            "dealix": ["bounded delivery", "evidence receipts", "change control"],
            "customer": ["named owner", "required evidence/access approvals", "acceptance feedback"],
        },
        "19_customer_dependencies": ["owner availability", "approved access", "timely acceptance decisions"],
        "20_acceptance_criteria": ["agreed before implementation", "evidence-backed", "customer-verifiable"],
        "21_measurement_method": "Baseline and measurement basis must be agreed before quantified value claims.",
        "22_timeline": timeline,
        "23_risks": ["scope uncertainty", "integration dependency", "data/access dependency"],
        "24_mitigations": ["bounded scope", "fail-closed authority", "evidence gates", "change control"],
        "25_assumptions": ["explicitly documented; never promoted to customer fact without evidence"],
        "26_support_boundary": "TBD_CUSTOMER_SPECIFIC",
        "27_change_control": "Material scope/price/terms changes require explicit approval.",
        "28_proof_customer_validation": "Work completion != customer value. Public proof requires customer permission.",
        "29_commercial_structure": {
            "status": commercial_status,
            "price_approval_ref": price_approval_ref,
            "fixed_public_price": False,
            "setup": "FOUNDER_APPROVAL_REQUIRED",
            "monthly": "FOUNDER_APPROVAL_REQUIRED",
            "currency": "TBD",
            "note": "Customer-specific commercial structure only after scope/effort/risk evidence and founder approval.",
        },
        "30_decision_required": "Customer/founder decision only after scope, acceptance and commercial structure are explicit.",
        "31_next_step": _copy(
            lang,
            "اكتشاف مؤهل أو قرار العميل بحسب الحالة الحالية.",
            "Qualified discovery or customer decision, according to the current evidence state.",
        ),
        "options": {
            "A": {"name": "minimum viable outcome", "difference": ["smallest bounded scope", "shorter timeline", "lowest capacity/risk"]},
            "B": {"name": "recommended outcome", "difference": ["core outcome scope", "balanced timeline", "recommended capacity"]},
            "C": {"name": "expanded outcome", "difference": ["broader scope", "more dependencies", "higher delivery capacity/risk"]},
        },
        # Compatibility fields for existing review tooling; values intentionally
        # contain no fixed price authority or fabricated ROI.
        "executive_summary": _copy(lang, f"مسودة {offer} لـ {account_name}.", f"Draft {offer} for {account_name}."),
        "client_situation_hypothesis": understood_problem,
        "scope": ["customer-specific discovery/baseline", "implementation", "verification"],
        "deliverables": ["agreed configured outcome", "evidence/acceptance receipt", "handover documentation"],
        "implementation_timeline": timeline,
        "governance": "Human/L5 approval remains required for material external effects.",
        "proof_plan": "Baseline -> delivery evidence -> customer acceptance -> customer-validated value -> optional public proof permission.",
        "client_responsibilities": ["provide approved evidence/access", "assign owner", "review acceptance"],
        "exclusions": ["unapproved spend", "out-of-scope work", "automatic public publishing"],
        "pricing": {
            "currency": "TBD",
            "setup": "FOUNDER_APPROVAL_REQUIRED",
            "monthly": "FOUNDER_APPROVAL_REQUIRED",
            "note": "No fixed price authority in proposal generation.",
        },
        "next_step": "Qualified discovery/customer decision; external send remains L5.",
        "signature_placeholder": "____________________",
        "offer_reference": offer,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--timeline", default="TBD_AFTER_DISCOVERY")
    parser.add_argument("--mode", choices=["demo", "internal", "live"], default="demo")
    parser.add_argument("--qualification-state", default="RESEARCH_ONLY")
    parser.add_argument("--problem-evidence-ref", action="append", default=[])
    parser.add_argument("--customer-requested", action="store_true")
    parser.add_argument("--price-approval-ref", default=UNKNOWN)
    args = parser.parse_args()

    try:
        offer = canonical_offer(args.offer)
    except ValueError as exc:
        print(str(exc))
        return 2

    allowed, artifact_kind, gate_basis = proposal_gate(
        mode=args.mode,
        qualification_state=args.qualification_state,
        explicit_customer_request=args.customer_requested,
        problem_evidence_refs=args.problem_evidence_ref,
    )
    if not allowed:
        print("PROPOSAL_GATE=BLOCKED")
        print("REASON=QUALIFIED_PROBLEM_OR_EXPLICIT_REQUEST_REQUIRED")
        return 2

    account = load_account(args.account_id, args.mode)
    if not account:
        print(f"account not found: {args.account_id}")
        return 1

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    languages = ["ar", "en"] if args.lang == "both" else [args.lang]
    today = dt.date.today().isoformat()
    offer_slug = offer.replace(" ", "_").replace("/", "_")
    written: list[Path] = []

    index: dict = {"proposals": [], "version": "2.0-truth-gated"}
    if INDEX_PATH.exists():
        try:
            index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    for lang in languages:
        proposal = build_proposal(
            account,
            offer,
            lang,
            args.timeline,
            args.mode,
            args.qualification_state,
            args.problem_evidence_ref,
            artifact_kind,
            gate_basis,
            args.price_approval_ref,
        )
        out_file = EXPORT_DIR / f"proposal-{account['id']}-{offer_slug}-{lang}-{today}.json"
        out_file.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(out_file)

        index.setdefault("proposals", []).append(
            {
                "id": f"prop-{account['id']}-{today}-{lang}",
                "accountId": account["id"],
                "offer": offer,
                "lang": lang,
                "timeline": args.timeline,
                "status": "draft" if artifact_kind == "CUSTOMER_PROPOSAL_DRAFT" else "internal_hypothesis",
                "artifactKind": artifact_kind,
                "proposalGateBasis": gate_basis,
                "externalSendAuthority": False,
                "priceAuthority": "FOUNDER_APPROVAL_REQUIRED",
                "createdAt": today,
                "path": str(out_file.relative_to(REPO_ROOT)),
            }
        )

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"PROPOSAL_GATE=PASS basis={gate_basis} artifact={artifact_kind}")
    for path in written:
        print(f"wrote {path}")
    print("EXTERNAL_SEND_AUTHORITY=false")
    print("PRICE_AUTHORITY=FOUNDER_APPROVAL_REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
