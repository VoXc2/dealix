#!/usr/bin/env python3
"""V18 Revenue Portfolio Control Plane — deterministic cycle runner (#1277).

Consumes canonical Founder OS evidence and the V18 portfolio_os modules to
produce the founder command artifact. Pure L3 internal execution: no external
send, no merge, no production mutation, no invented proof.

Inputs (read-only):
- /opt/dealix/company-os/founder-os/current/LATEST_TRUTH.json
- /opt/dealix/company-os/founder-os/tables/SCOPED_RELATIONSHIPS.tsv
- /opt/dealix/company-os/founder-os/tables/EVENT_INTERACTIONS.tsv
- /opt/dealix/company-os/founder-os/current/REVENUE_MESH_V18.md (policy reference)

Outputs:
- reports/founder/V18_PORTFOLIO_COMMAND_<ts>.json
- reports/founder/V18_PORTFOLIO_COMMAND_<ts>.md
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

FO = Path("/opt/dealix/company-os/founder-os")

from auto_client_acquisition.portfolio_os.buyability import (
    BuyingGroup,
    BuyingGroupMember,
    BuyingRole,
    RoleConfidence,
    assess_buyability,
)
from auto_client_acquisition.portfolio_os.capacity import (
    CapacityAllocation,
    CapacityBudget,
    allocate_capacity,
)
from auto_client_acquisition.portfolio_os.command import build_portfolio_command
from auto_client_acquisition.portfolio_os.distribution import (
    build_distribution_edge,
    evaluate_proof_reuse,
)
from auto_client_acquisition.portfolio_os.events import (
    EventAllocation,
    optimize_event_plan,
)
from auto_client_acquisition.portfolio_os.experiments import (
    Experiment,
    ExperimentRegistry,
    register_experiment,
    validate_experiment,
)
from auto_client_acquisition.portfolio_os.partners import (
    PartnerPath,
    assess_partner_path,
)
from auto_client_acquisition.portfolio_os.portfolio import (
    PortfolioItem,
    PortfolioLane,
)

# ── Evidence load (canonical, read-only) ──────────────────────────────────

def load_truth() -> dict:
    p = FO / "current" / "LATEST_TRUTH.json"
    if p.exists():
        return json.loads(p.read_text())
    return {}

def load_relationships() -> list[dict[str, str]]:
    p = FO / "tables" / "SCOPED_RELATIONSHIPS.tsv"
    if not p.exists():
        return []
    lines = p.read_text().splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows

def load_event_interactions() -> list[dict[str, str]]:
    p = FO / "tables" / "EVENT_INTERACTIONS.tsv"
    if not p.exists():
        return []
    lines = p.read_text().splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows

truth = load_truth()
rels = load_relationships()
interactions = load_event_interactions()

now = datetime.now(UTC)
ts = now.strftime("%Y%m%dT%H%M%SZ")

# ── Portfolio items (evidence-bound only) ─────────────────────────────────

items: list[PortfolioItem] = [
    PortfolioItem(
        item_id="pi-big5-2026",
        lane=PortfolioLane.EVENT_RELATIONSHIP.value,
        current_stage="EVENT_READY",
        relationship_state="no_relationship_yet",
        buyability_score=0.0,
        evidence_strength=0,
        expected_next_evidence="two-way conversation + followup permission (Big5 30 Aug)",
        time_to_evidence_days=2,
        founder_minutes=360,
        agent_cost=0.2,
        delivery_load=0,
        risk=2,
        reversibility=5,
        strategic_reuse=3,
        proof_potential=4,
        recurring_potential=2,
        probability_of_movement=0.5,
        company="Big 5 Construct Saudi",
        assumptions=(
            "day-1 targets: 3 conversations, 2 followup permissions, 1 problem, 1 qualification candidate",
            "exhibitor != lead; only real two-way exchange creates evidence",
        ),
    ),
    PortfolioItem(
        item_id="pi-leap-karizma",
        lane=PortfolioLane.EVENT_RELATIONSHIP.value,
        current_stage="INBOUND_OBSERVED",
        relationship_state="observed_only",
        buyability_score=0.0,
        evidence_strength=1,
        expected_next_evidence="two-way exchange with Eman Louzon (KARIZMA)",
        time_to_evidence_days=4,
        founder_minutes=240,
        agent_cost=0.3,
        delivery_load=0,
        risk=2,
        reversibility=5,
        strategic_reuse=3,
        proof_potential=3,
        recurring_potential=3,
        probability_of_movement=0.4,
        company="KARIZMA",
        assumptions=(
            "observed LEAP connection request only; no two-way exchange verified",
            "founder reviews connection request in LEAP app; no external send by agent",
        ),
    ),
    PortfolioItem(
        item_id="pi-imini-001",
        lane=PortfolioLane.WARM_NETWORK.value,
        current_stage="NEGOTIATION",
        relationship_state="real_relationship",
        buyability_score=0.0,
        evidence_strength=4,
        expected_next_evidence="founder-approved counter send + payment proof (founder income lane)",
        time_to_evidence_days=3,
        founder_minutes=10,
        agent_cost=0.1,
        delivery_load=1,
        risk=2,
        reversibility=4,
        strategic_reuse=2,
        proof_potential=2,
        recurring_potential=0,
        probability_of_movement=0.7,
        company="iMini / Jannie",
        assumptions=(
            "FOUNDER_INCOME scope: NOT Dealix revenue; tracked separately",
            "AP-006 counter draft ready ($150 target, $80 fallback); send requires founder approval",
        ),
    ),
    PortfolioItem(
        item_id="pi-nelc-naseej",
        lane=PortfolioLane.B2G_PARTNER_GO.value,
        current_stage="DRAFT_READY",
        relationship_state="no_relationship_yet",
        buyability_score=0.0,
        evidence_strength=1,
        expected_next_evidence="one two-way partner conversation before 2026-09-03",
        time_to_evidence_days=6,
        founder_minutes=20,
        agent_cost=0.3,
        delivery_load=0,
        risk=3,
        reversibility=5,
        strategic_reuse=4,
        proof_potential=3,
        recurring_potential=3,
        probability_of_movement=0.3,
        company="NASEEJ FOR TECHNOLOGY (NELC prime)",
        assumptions=(
            "NELC 260839004837 partner-go; highest complementarity + accessibility",
            "draft only; send:false until founder approval",
            "public/tender research is not a relationship",
        ),
    ),
    PortfolioItem(
        item_id="pi-linnk-001",
        lane=PortfolioLane.WARM_NETWORK.value,
        current_stage="OUTBOUND_SENT",
        relationship_state="no_reply_proven",
        buyability_score=0.0,
        evidence_strength=2,
        expected_next_evidence="inbound reply OR bounded follow-up draft approval",
        time_to_evidence_days=7,
        founder_minutes=15,
        agent_cost=0.1,
        delivery_load=0,
        risk=2,
        reversibility=5,
        strategic_reuse=1,
        proof_potential=1,
        recurring_potential=2,
        probability_of_movement=0.2,
        company="Linnk Arabia",
        assumptions=("SENT_EMAIL 2026-08-21, NO_REPLY_PROVEN; wait or bounded follow-up only",),
    ),
    PortfolioItem(
        item_id="pi-leap29-001",
        lane=PortfolioLane.WARM_NETWORK.value,
        current_stage="OUTBOUND_SENT",
        relationship_state="no_reply_proven",
        buyability_score=0.0,
        evidence_strength=2,
        expected_next_evidence="inbound reply OR bounded follow-up draft approval",
        time_to_evidence_days=7,
        founder_minutes=15,
        agent_cost=0.1,
        delivery_load=0,
        risk=2,
        reversibility=5,
        strategic_reuse=1,
        proof_potential=1,
        recurring_potential=2,
        probability_of_movement=0.2,
        company="Leap29 Saudi",
        assumptions=("SENT_EMAIL 2026-08-21, NO_REPLY_PROVEN; wait or bounded follow-up only",),
    ),
]

# ── Buyability assessments (UNKNOWN valid, never invented) ────────────────

imini_group = BuyingGroup(
    account_id="acc-imini-001",
    members=(
        BuyingGroupMember(
            role=BuyingRole.ECONOMIC_BUYER.value,
            source="TWO_WAY_EMAIL_2026-08-24",
            observed_fact="Jannie sent concrete terms ($80 base, bonus structure)",
            role_confidence=RoleConfidence.HIGH.value,
            relationship_state="real_relationship",
            concern="price ceiling and deliverable scope",
            evidence_needed="final counter acceptance",
            proof_needed="none",
            next_action="founder approves AP-006 counter",
        ),
    ),
)
karizma_group = BuyingGroup(
    account_id="acc-karizma",
    members=(
        BuyingGroupMember(
            role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
            source="LEAP_APP_CONNECTION_REQUEST",
            observed_fact="Eman Louzon CEO sent inbound connection request; no two-way exchange",
            role_confidence=RoleConfidence.LOW.value,
            relationship_state="observed_only",
            concern="UNKNOWN",
            next_action="founder reviews connection request in LEAP app",
        ),
    ),
)
nelc_group = BuyingGroup(
    account_id="acc-nelc",
    members=(
        BuyingGroupMember(
            role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
            source="PUBLIC_TENDER_260839004837_RESEARCH",
            observed_fact="NELC prime candidate identified; no named buyer or two-way exchange",
            role_confidence=RoleConfidence.UNKNOWN.value,
            relationship_state="no_relationship_yet",
            concern="UNKNOWN",
            next_action="partner conversation to map buying group",
        ),
    ),
)

assessments = [
    assess_buyability(
        "acc-imini-001",
        group=imini_group,
        factor_evidence={
            "PROBLEM_FIT": "strong: creator distribution need confirmed in email",
            "TRUST": "strong: two-way negotiation exchange",
            "ECONOMIC_DEFENSIBILITY": "moderate: $150 vs $80 walk-away",
            "DECISION_REVERSIBILITY": "strong: non-exclusive, organic, one revision",
        },
    ),
    assess_buyability("acc-karizma", group=karizma_group),
    assess_buyability("acc-nelc", group=nelc_group),
]

# ── Event allocation (real canonical windows, physically feasible) ────────

event_allocations = [
    EventAllocation(
        allocation_id="ev-big5-day1",
        event_name="BIG5",
        day="2026-08-30",
        start_hour=16,
        end_hour=22,
        venue="Riyadh Front / ROSHN Front",
        focus="construction, hvac, fm, industrial",
        expected_relationship_value=5,
        probability=0.5,
        strategic_reuse=3,
        travel_cost=1,
        founder_hours=6,
    ),
    EventAllocation(
        allocation_id="ev-leap-day1",
        event_name="LEAP",
        day="2026-08-31",
        start_hour=9,
        end_hour=16,
        venue="RECC Malham",
        focus="saudi_b2b_saas, ai_it, partners",
        expected_relationship_value=4,
        probability=0.4,
        strategic_reuse=3,
        travel_cost=2,
        founder_hours=7,
    ),
    EventAllocation(
        allocation_id="ev-big5-day2",
        event_name="BIG5",
        day="2026-08-31",
        start_hour=18,
        end_hour=22,
        venue="Riyadh Front / ROSHN Front",
        focus="construction, hvac, fm, industrial",
        expected_relationship_value=4,
        probability=0.4,
        strategic_reuse=2,
        travel_cost=1,
        founder_hours=4,
    ),
]

# Event-week capacity: explicit assumption (default 600 min is a normal week;
# an event week legitimately raises founder field time — recorded as assumption).
event_plan = optimize_event_plan(
    event_allocations,
    event_hours_cap=20,
    founder_minutes_cap=1800,
)

# ── Capacity (full portfolio, fail closed) ────────────────────────────────

capacity_demands = [
    CapacityAllocation(
        lane=PortfolioLane.EVENT_RELATIONSHIP.value,
        founder_minutes=sum(a.founder_hours * 60 for a in event_allocations),
        event_hours=sum(a.founder_hours for a in event_allocations),
    ),
    CapacityAllocation(
        lane=PortfolioLane.WARM_NETWORK.value,
        founder_minutes=10 + 15 + 15,
    ),
    CapacityAllocation(
        lane=PortfolioLane.B2G_PARTNER_GO.value,
        founder_minutes=20,
    ),
]
capacity_budget = CapacityBudget(founder_minutes=1800, event_hours=20)
capacity_result = allocate_capacity(capacity_budget, capacity_demands)

# ── Distribution edges + proof reuse gates ────────────────────────────────

distribution_edges = [
    build_distribution_edge(
        asset="Free Mini Diagnostic",
        audience="Big 5 construction/FM operations leaders",
        buying_group_role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
        channel="event conversation",
        buying_situation="event discovery",
        cta="book 20-minute diagnostic",
        evidence="planned; no live proof yet",
        outcome="diagnostic request",
    ),
    build_distribution_edge(
        asset="iMini creator video proof",
        audience="founder LinkedIn followers",
        buying_group_role=BuyingRole.ECONOMIC_BUYER.value,
        channel="FOUNDER_LINKEDIN_NATIVE",
        buying_situation="content proof",
        cta="follow for proof",
        evidence="pending iMini consent",
        outcome="reusable content proof (gated)",
    ),
]

proof_reuse = [
    evaluate_proof_reuse(
        "proof-imini-video",
        customer_permission_state="unknown",
        claim_support="creator distribution capability",
        source="founder-email-chain",
        provenance="AP-006",
        sensitivity="internal",
    ),
    evaluate_proof_reuse(
        "proof-synthetic-event-20260827",
        customer_permission_state="unknown",
        claim_support="event capture chain mechanics",
        source="synthetic_event_big5_2026",
        provenance="synthetic-event-proof-20260827.json",
        sensitivity="internal",
    ),
]

# ── Experiments (bounded; no SCALE without outcome) ───────────────────────

experiments = ExperimentRegistry()
exp_defs = [
    Experiment(
        experiment_id="exp-big5-day1",
        hypothesis="Evening stand conversations at Big5 yield 2+ followup permissions per 3 conversations",
        segment="construction/hvac/fm",
        account_cohort="big5-2026",
        buying_group_role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
        offer="Free Mini Diagnostic",
        channel="event",
        asset="diagnostic pitch",
        cta="book diagnostic",
        expected_evidence="3 two-way conversations + 2 followup permissions on 2026-08-30",
        start="2026-08-30",
        end="2026-08-31",
        founder_minutes=360,
        agent_cost=0.2,
        delivery_cost=0,
        outcome="",
        decision="",
    ),
    Experiment(
        experiment_id="exp-leap-karizma",
        hypothesis="Responding to inbound LEAP connection requests within 24h yields two-way exchanges",
        segment="saudi_b2b_saas",
        account_cohort="leap-2026",
        buying_group_role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
        offer="Free Mini Diagnostic",
        channel="LEAP app",
        asset="connection reply",
        cta="two-way exchange",
        expected_evidence="two-way exchange with KARIZMA CEO",
        start="2026-08-31",
        end="2026-09-03",
        founder_minutes=120,
        agent_cost=0.2,
        delivery_cost=0,
        outcome="",
        decision="",
    ),
    Experiment(
        experiment_id="exp-nelc-draft",
        hypothesis="A partner-go draft to the NELC prime candidate opens one two-way partner conversation",
        segment="b2g",
        account_cohort="nelc-260839004837",
        buying_group_role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
        offer="partner lane",
        channel="email",
        asset="partner draft",
        cta="conversation",
        expected_evidence="one two-way partner conversation before 2026-09-03",
        start="2026-08-28",
        end="2026-09-03",
        founder_minutes=20,
        agent_cost=0.3,
        delivery_cost=0,
        outcome="",
        decision="",
    ),
]
for exp in exp_defs:
    errs = validate_experiment(exp)
    if errs:
        print(f"experiment rejected: {exp.experiment_id} {errs}")
    else:
        experiments, _ = register_experiment(experiments, exp)

# ── Partner paths (relationship evidence required) ────────────────────────

partner_assessments = [
    assess_partner_path(
        "rel-imini-001",
        PartnerPath.CUSTOMER_REFERRAL.value,
        relationship_evidence="TWO_WAY_EMAIL negotiation 2026-08-24",
        consent_state="unknown",
        plausible=True,
        next_action="ask Jannie for referral only after deal closes, with explicit consent",
    ),
    assess_partner_path(
        "rel-nelc",
        PartnerPath.B2G_PRIME.value,
        relationship_evidence="",
        plausible=False,
    ),
]

# ── Compose the founder command ───────────────────────────────────────────

verified_revenue = float(truth.get("economic_truth", {}).get("verified_revenue_sar", 0) or 0)
command = build_portfolio_command(
    generated_at=now.isoformat(),
    items=items,
    verified_revenue_sar=verified_revenue,
    closest_verified_money_path=(
        "NONE — 0 verified revenue. Closest REAL path: Big 5 30 Aug–2 Sep "
        "(first evidence-backed relationship -> diagnostic -> quote -> paid pilot). "
        "iMini is founder income, not Dealix revenue."
    ),
    assessments=assessments,
    event_plan=event_plan,
    distribution_edges=distribution_edges,
    proof_reuse=proof_reuse,
    experiments=experiments,
    capacity_budget=capacity_budget,
    capacity_allocation=capacity_result,
)

# ── Attach governance truth + evidence inputs (report-only, no fabrication) ──
report = {
    "schema": "dealix.v18.portfolio-command.v1",
    "generated_at": now.isoformat(),
    "source_truth": truth.get("economic_truth", {}),
    "evidence_inputs": {
        "scoped_relationships": [
            {"entity": r.get("entity"), "state": r.get("state"), "commercial_truth": r.get("commercial_truth")}
            for r in rels
        ],
        "event_interactions_observed": [
            {"event": i.get("event"), "person": i.get("person"), "company": i.get("company"), "state": i.get("state")}
            for i in interactions
        ],
    },
    "command": command.to_dict(),
    "event_plan": event_plan.to_dict(),
    "capacity": capacity_result.to_dict(),
    "partner_paths": [p.to_dict() for p in partner_assessments],
    "experiments": experiments.to_dict(),
    "governance": {
        "external_send": "APPROVAL_FIRST",
        "merge_main": "NEVER_AUTO",
        "production_mutation": "NEVER_AUTO",
        "payment": "NEVER_AUTO",
        "tender_submission": "NEVER_AUTO",
        "infrastructure_freeze": True,
        "self_test_quarantine": True,
    },
}

out_dir = REPO_ROOT / "reports" / "founder"
out_dir.mkdir(parents=True, exist_ok=True)
json_path = out_dir / f"V18_PORTFOLIO_COMMAND_{ts}.json"
md_path = out_dir / f"V18_PORTFOLIO_COMMAND_{ts}.md"

json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

md_lines = [
    "# Dealix V18 Portfolio Command",
    "",
    f"Generated: {now.isoformat()}",
    "",
    "## Economic Truth",
    f"- Verified revenue (SAR): {verified_revenue}",
    f"- Real relationships (Dealix scope): {truth.get('economic_truth', {}).get('real_contacts', 0)}",
    f"- Verified paid pilots: {truth.get('economic_truth', {}).get('verified_paid_pilots', 0)}",
    f"- Pipeline pressure: {truth.get('economic_truth', {}).get('generated_pipeline_pressure', 'UNKNOWN')}",
    "",
    "## TOP 5 Portfolio Moves",
]
for i, m in enumerate(command.top_moves, 1):
    md_lines.append(
        f"{i}. {m.lane}: {m.company or m.item_id} — {m.expected_next_evidence or 'evidence capture'}"
    )
md_lines += [
    "",
    "## Buyability Gaps",
]
md_lines += [f"- {g}" for g in command.top_buyability_gaps] or ["- (none recorded — no qualified accounts yet)"]
md_lines += ["", "## Decision Risks"]
md_lines += [f"- {r}" for r in command.top_decision_risks] or ["- (none recorded)"]
md_lines += [
    "",
    "## Event Allocation",
    f"- Next event priority: {command.next_event_priority or 'none'}",
    f"- Plan feasible: {event_plan.feasible}",
]
for a in event_plan.allocations:
    md_lines.append(f"  - {a.event_name} {a.day} {a.start_hour}:00-{a.end_hour}:00 @ {a.venue} (score {a.score():.2f})")
for c in event_plan.conflicts:
    md_lines.append(f"  - CONFLICT: {c.allocation_id_a} vs {c.allocation_id_b} ({c.reason})")
md_lines += [
    "",
    "## Partner / B2G",
    "- NELC prime: NASEEJ draft ready (send:false). ELM, TUWAIQ are alternates.",
    "- iMini: CUSTOMER_REFERRAL plausible only after close + explicit consent.",
    "- Public tender research is NOT a relationship.",
    "",
    "## Experiments",
    f"- Scale: {command.experiments_scale or 'none'}",
    f"- Retest: {command.experiments_retest or 'none'}",
    f"- Stop: {command.experiments_stop or 'none'}",
    f"- Invalid: {command.experiments_invalid or 'none'}",
    "",
    "## Capacity",
    f"- {command.capacity_summary or 'not computed'}",
    f"- Event founder hours total: {event_plan.founder_hours_total}",
    "",
    "## GitHub",
    "- #1277 Revenue Portfolio Control Plane (this artifact) — implementation surface branch: feat/revenue-portfolio-control-v18-20260828",
    "- #1275 Revenue Mesh V17 implementation: MERGED",
    "- #1276 Unified Commercial OS implementation: OPEN (mergeable) — founder decision",
    "- #1281 V18 server control activation: OPEN Draft (adapter only, no duplicate surface)",
    "- #1273/#1274: OPEN (owners of account-level WHAT and campaign HOW)",
    "",
    "## Approvals Needed",
    "- AP-006: iMini counter send $150 (founder external income; founder sends from Gmail)",
    "- NELC prime approach draft to NASEEJ (send:false until approved)",
    "- V16_ROOT_CORRECTION.sh as root (cleanup of contaminated self-test copies)",
    "- PR #1276 merge decision (Unified Commercial OS)",
    "- KARIZMA LEAP connection request: founder reviews in LEAP app",
    "",
    "## Learning",
    "- No reply is not a loss; NO_REPLY_PROVEN stays a stall until evidence changes.",
    "- Research is not pipeline: 53 web searches today produced 0 verified revenue.",
    "- Event capacity fails closed unless the event-week budget is explicit (assumption recorded).",
    "",
    "## North Star",
    "FIRST VERIFIED PAID PILOT",
    "",
    "## Next Autonomous L0-L4 Action",
    command.next_autonomous_action or "none",
    "",
]
md_path.write_text("\n".join(md_lines) + "\n")

print(f"WROTE {json_path}")
print(f"WROTE {md_path}")
print("TOP5:", [m.item_id for m in command.top_moves])
print("EVENT_FEASIBLE:", event_plan.feasible)
print("CAPACITY:", capacity_result.feasible, [v.to_dict() for v in capacity_result.violations])
print("PROOF_REUSE:", [(p.proof_id, p.reusable, p.reasons) for p in proof_reuse])
