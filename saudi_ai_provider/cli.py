"""Command-line interface for Saudi AI provider operating system."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .agent_stack import render_agent_application_plan, render_segment_rollout_plan
from .commercial import compute_recurring_model, generate_customer_proposal_bundle, load_intake
from .dashboards import export_dashboard_bundle
from .enterprise_playbook import generate_enterprise_playbook_bundle
from .go_live_sales import render_go_live_sales_plan, render_signature_readiness
from .kpis import kpis_for_service
from .launch_ops import build_launch_pack, render_offer_stack
from .offers import build_pitch, generate_offer
from .pricing import compute_roi, package_for_segment, quote_service
from .roadmap import roadmap_for_days
from .monetization import (
    compute_proposal_scorecard,
    orchestrate_renewal_expansion,
    recommend_auto_package,
)
from .verifier import print_verification_report, verify_sellable


def _cmd_verify(_args: argparse.Namespace) -> int:
    result = verify_sellable()
    print_verification_report(result)
    return 0 if result.sellable_now else 1


def _cmd_package(args: argparse.Namespace) -> int:
    services = package_for_segment(args.segment)
    print(f"Segment package: {args.segment}")
    total_setup = 0.0
    total_monthly = 0.0
    for service in services:
        total_setup += service["setup_fee_sar"]
        total_monthly += service["monthly_retainer_sar"]
        print(
            f"- {service['service_id']}: setup={service['setup_fee_sar']} SAR, "
            f"monthly={service['monthly_retainer_sar']} SAR, "
            f"sla={service['sla']['label']}"
        )
    print(f"Total setup: {round(total_setup, 2)} SAR")
    print(f"Total monthly: {round(total_monthly, 2)} SAR")
    return 0


def _cmd_quote(args: argparse.Namespace) -> int:
    quote = quote_service(
        service_id=args.service,
        employees=args.employees,
        discount=args.discount,
        segment=args.segment,
    )
    print(f"Service: {quote.service_id}")
    print(f"Segment: {quote.segment}")
    print(f"Setup fee (list): {quote.setup_fee_sar} SAR")
    print(f"Implementation fee (after discount): {quote.implementation_fee_sar} SAR")
    print(f"Monthly retainer: {quote.monthly_retainer_sar} SAR")
    print(f"Annual contract value: {quote.annual_contract_value_sar} SAR")
    print(f"Discount applied: {quote.discount_applied:.2f}")
    print(f"Gross margin target: {quote.gross_margin_target:.2f}")
    print(f"SELLABLE_NOW: {'true' if quote.sellable else 'false'}")
    if quote.reasons:
        for reason in quote.reasons:
            print(f"- {reason}")
    return 0 if quote.sellable else 1


def _cmd_roadmap(args: argparse.Namespace) -> int:
    phases = roadmap_for_days(args.days)
    print(f"Roadmap horizon: {args.days} days")
    for phase in phases:
        print(f"{phase['name']} ({phase['start_day']}–{phase['end_day']})")
        for outcome in phase["outcomes"]:
            print(f"- {outcome}")
    return 0


def _cmd_kpis(args: argparse.Namespace) -> int:
    kpi = kpis_for_service(args.service)
    print(f"Service: {args.service}")
    print(f"North Star: {kpi['north_star']}")
    print("Business KPIs:")
    for item in kpi["business_kpis"]:
        print(f"- {item}")
    print("Operational KPIs:")
    for item in kpi["operational_kpis"]:
        print(f"- {item}")
    print("Guardrail KPIs:")
    for item in kpi["guardrail_kpis"]:
        print(f"- {item}")
    print("Targets:")
    for item in kpi["target_benchmarks"]:
        print(f"- {item}")
    print("Evidence:")
    print("- before/after KPI baseline export")
    print("- workflow execution logs")
    print("- sampled customer conversations and CRM records")
    return 0


def _cmd_pitch(args: argparse.Namespace) -> int:
    print(build_pitch(args.service, lang=args.lang))
    return 0


def _cmd_offer(args: argparse.Namespace) -> int:
    outputs = generate_offer(args.service, args.segment, lang=args.lang)
    for name, path in outputs.items():
        print(f"{name}: {path}")
    return 0


def _cmd_roi(args: argparse.Namespace) -> int:
    projection = compute_roi(
        args.service,
        {
            "monthly_tickets": args.tickets,
            "avg_agent_cost_sar": args.agent_cost,
            "automation_rate": args.automation_rate,
            "critical_incidents_annual": args.critical_incidents_annual,
            "avg_incident_cost_sar": args.avg_incident_cost_sar,
            "prevention_rate": args.prevention_rate,
            "incident_hours_monthly": args.incident_hours_monthly,
            "cost_per_downtime_hour_sar": args.cost_per_downtime_hour_sar,
            "reduction_rate": args.reduction_rate,
            "monthly_pipeline_sar": args.monthly_pipeline_sar,
            "conversion_lift_rate": args.conversion_lift_rate,
        },
    )
    print(f"Service Family: {projection.service_family}")
    print(f"Projected Monthly Savings: {projection.monthly_savings_sar} SAR")
    print(f"Projected Annual ROI: {projection.annual_roi_sar} SAR")
    return 0


def _cmd_proposal(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    outputs = generate_customer_proposal_bundle(
        service_id=args.service,
        intake=intake,
        lang=args.lang,
        segment=args.segment,
    )
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


def _cmd_dashboard_export(args: argparse.Namespace) -> int:
    metrics: dict = {}
    if args.metrics_json:
        metrics = json.loads(Path(args.metrics_json).read_text(encoding="utf-8"))
    outputs = export_dashboard_bundle(
        output_dir=Path(args.output_dir) if args.output_dir else None,
        metrics=metrics,
    )
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


def _cmd_recurring_model(args: argparse.Namespace) -> int:
    result = compute_recurring_model(
        setup_fee_sar=args.setup_fee,
        monthly_retainer_sar=args.monthly,
        months=args.months,
        expansion_rate=args.expansion_rate,
    )
    print(f"Setup Fee: {result.setup_fee_sar} SAR")
    print(f"Monthly Retainer: {result.monthly_retainer_sar} SAR")
    print(f"Months: {result.months}")
    print(f"Expansion Rate: {result.expansion_rate:.2%}")
    print(f"Projected Total Revenue: {result.total_revenue_sar} SAR")
    print(f"Projected ARR Run Rate: {result.arr_run_rate_sar} SAR")
    return 0


def _cmd_proposal_scorecard(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    scorecard = compute_proposal_scorecard(args.service, intake)
    print(f"Service: {args.service}")
    print(f"Proposal Score: {scorecard.total_score}")
    print(f"Recommendation: {scorecard.recommendation}")
    print("Dimension Scores:")
    for key, value in scorecard.dimension_scores.items():
        print(f"- {key}: {value}")
    if scorecard.blockers:
        print("Blockers:")
        for blocker in scorecard.blockers:
            print(f"- {blocker}")
    else:
        print("Blockers: none")
    return 0 if scorecard.recommendation != "HOLD" else 1


def _cmd_auto_package(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    result = recommend_auto_package(intake, max_services=args.max_services)
    print(f"Segment: {result.segment}")
    print(f"Rationale: {result.rationale}")
    print("Recommended Services:")
    for item in result.ranked_services:
        print(
            f"- {item['service_id']} | fit_score={item['fit_score']} | "
            f"setup={item['setup_fee_sar']} SAR | monthly={item['monthly_retainer_sar']} SAR"
        )
    return 0


def _cmd_renewal_orchestrator(args: argparse.Namespace) -> int:
    customer_state = load_intake(Path(args.customer_state_file))
    result = orchestrate_renewal_expansion(customer_state)
    print(f"Renewal Risk: {result.renewal_risk}")
    print("Renewal Actions:")
    for action in result.renewal_actions:
        print(f"- {action}")
    print("Expansion Candidates:")
    if result.expansion_candidates:
        for service in result.expansion_candidates:
            print(f"- {service}")
    else:
        print("- none")
    print(f"Next Review Date: {result.next_review_date}")
    print("Rationale:")
    for item in result.rationale:
        print(f"- {item}")
    return 0


def _cmd_p2_monetization(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    customer_state = load_intake(Path(args.customer_state_file))
    scorecard = compute_proposal_scorecard(args.service, intake)
    package = recommend_auto_package(intake, max_services=args.max_services)
    renewal = orchestrate_renewal_expansion(customer_state)

    print("P2_MONETIZATION_SUMMARY")
    print(f"Service: {args.service}")
    print(f"ProposalScore: {scorecard.total_score} ({scorecard.recommendation})")
    print(f"Segment: {package.segment}")
    print("TopPackageRecommendations:")
    for item in package.ranked_services:
        print(f"- {item['service_id']} ({item['fit_score']})")
    print(f"RenewalRisk: {renewal.renewal_risk}")
    print("ExpansionCandidates:")
    if renewal.expansion_candidates:
        for service in renewal.expansion_candidates:
            print(f"- {service}")
    else:
        print("- none")
    return 0


def _cmd_offer_stack(args: argparse.Namespace) -> int:
    print(render_offer_stack(segment=args.segment, lang=args.lang))
    return 0


def _cmd_launch_pack(args: argparse.Namespace) -> int:
    verification = verify_sellable()
    result = build_launch_pack(
        segment=args.segment,
        lang=args.lang,
        verification=verification,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"launch_pack: {result.output_path}")
    print(f"included_services: {len(result.included_services)}")
    for service_id in result.included_services:
        print(f"- {service_id}")
    return 0 if verification.sellable_now else 1


def _cmd_agent_apps(args: argparse.Namespace) -> int:
    print(
        render_agent_application_plan(
            service_id=args.service,
            profile=args.profile,
            lang=args.lang,
        )
    )
    return 0


def _cmd_agent_rollout(args: argparse.Namespace) -> int:
    print(
        render_segment_rollout_plan(
            segment=args.segment,
            profile=args.profile,
            lang=args.lang,
        )
    )
    return 0


def _cmd_enterprise_playbook(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    bundle = generate_enterprise_playbook_bundle(
        service_id=args.service,
        intake=intake,
        profile=args.profile,
        segment=args.segment,
        lang=args.lang,
        output_dir=Path(args.output_dir) if args.output_dir else None,
    )
    print(f"profile: {bundle.profile}")
    print(f"proposal: {bundle.proposal}")
    print(f"sow: {bundle.sow}")
    print(f"kpi_contract: {bundle.kpi_contract}")
    print(f"governance_contract: {bundle.governance_contract}")
    return 0


def _cmd_go_live_sales(args: argparse.Namespace) -> int:
    print(render_go_live_sales_plan(segment=args.segment, lang=args.lang, max_plays=args.max_plays))
    return 0


def _cmd_signature_readiness(args: argparse.Namespace) -> int:
    accepted = str(args.governance_contract_accepted).strip().lower() in {"1", "true", "yes", "y"}
    print(
        render_signature_readiness(
            stage=args.stage,
            buyer_commitment=args.buyer_commitment,
            proof_level=args.proof_level,
            risk_status=args.risk_status,
            governance_contract_accepted=accepted,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m saudi_ai_provider",
        description="Saudi AI Provider operating CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="Run strict sellable verifier")
    verify.set_defaults(func=_cmd_verify)

    package = sub.add_parser("package", help="Show recommended package by segment")
    package.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    package.set_defaults(func=_cmd_package)

    quote = sub.add_parser("quote", help="Generate quote for a service SKU")
    quote.add_argument("--service", required=True)
    quote.add_argument("--employees", required=True, type=int)
    quote.add_argument("--discount", type=float, default=0.0)
    quote.add_argument("--segment", choices=["smb", "mid_market", "enterprise"])
    quote.set_defaults(func=_cmd_quote)

    roadmap = sub.add_parser("roadmap", help="Generate execution roadmap")
    roadmap.add_argument("--days", type=int, default=180)
    roadmap.set_defaults(func=_cmd_roadmap)

    kpis = sub.add_parser("kpis", help="Show KPI tree for service")
    kpis.add_argument("--service", required=True)
    kpis.set_defaults(func=_cmd_kpis)

    pitch = sub.add_parser("pitch", help="Generate one-line pitch for a service")
    pitch.add_argument("--service", required=True)
    pitch.add_argument("--lang", choices=["ar", "en"], default="ar")
    pitch.set_defaults(func=_cmd_pitch)

    offer = sub.add_parser("offer", help="Generate offer and SOW markdown files")
    offer.add_argument("--service", required=True)
    offer.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    offer.add_argument("--lang", choices=["ar", "en"], default="ar")
    offer.set_defaults(func=_cmd_offer)

    generate_offer_alias = sub.add_parser(
        "generate-offer",
        help="Generate full commercial offer artifacts",
    )
    generate_offer_alias.add_argument("--service", required=True)
    generate_offer_alias.add_argument(
        "--segment", required=True, choices=["smb", "mid_market", "enterprise"]
    )
    generate_offer_alias.add_argument("--industry", default="general")
    generate_offer_alias.add_argument("--lang", choices=["ar", "en"], default="ar")
    generate_offer_alias.set_defaults(func=_cmd_offer)

    roi = sub.add_parser("roi", help="Compute ROI projection for service")
    roi.add_argument("--service", required=True)
    roi.add_argument("--tickets", type=float, default=0.0)
    roi.add_argument("--agent-cost", type=float, default=0.0, dest="agent_cost")
    roi.add_argument("--automation-rate", type=float, default=0.0, dest="automation_rate")
    roi.add_argument("--critical-incidents-annual", type=float, default=0.0)
    roi.add_argument("--avg-incident-cost-sar", type=float, default=0.0)
    roi.add_argument("--prevention-rate", type=float, default=0.0)
    roi.add_argument("--incident-hours-monthly", type=float, default=0.0)
    roi.add_argument("--cost-per-downtime-hour-sar", type=float, default=0.0)
    roi.add_argument("--reduction-rate", type=float, default=0.0)
    roi.add_argument("--monthly-pipeline-sar", type=float, default=0.0)
    roi.add_argument("--conversion-lift-rate", type=float, default=0.0)
    roi.set_defaults(func=_cmd_roi)

    proposal = sub.add_parser("proposal", help="Generate customer-specific proposal bundle")
    proposal.add_argument("--service", required=True)
    proposal.add_argument("--intake-file", required=True)
    proposal.add_argument("--segment", choices=["smb", "mid_market", "enterprise"])
    proposal.add_argument("--lang", choices=["ar", "en"], default="ar")
    proposal.set_defaults(func=_cmd_proposal)

    dashboard = sub.add_parser(
        "dashboard-export",
        help="Export executive/sales/delivery/risk dashboard JSON files",
    )
    dashboard.add_argument("--metrics-json")
    dashboard.add_argument("--output-dir")
    dashboard.set_defaults(func=_cmd_dashboard_export)

    recurring = sub.add_parser(
        "recurring-model",
        help="Project recurring managed-operations revenue model",
    )
    recurring.add_argument("--setup-fee", type=float, required=True)
    recurring.add_argument("--monthly", type=float, required=True)
    recurring.add_argument("--months", type=int, default=12)
    recurring.add_argument("--expansion-rate", type=float, default=0.05)
    recurring.set_defaults(func=_cmd_recurring_model)

    proposal_score = sub.add_parser(
        "proposal-scorecard",
        help="Compute proposal scorecard for a customer intake",
    )
    proposal_score.add_argument("--service", required=True)
    proposal_score.add_argument("--intake-file", required=True)
    proposal_score.set_defaults(func=_cmd_proposal_scorecard)

    auto_package = sub.add_parser(
        "auto-package",
        help="Recommend best package mix for customer intake",
    )
    auto_package.add_argument("--intake-file", required=True)
    auto_package.add_argument("--max-services", type=int, default=5)
    auto_package.set_defaults(func=_cmd_auto_package)

    renewal = sub.add_parser(
        "renewal-orchestrator",
        help="Generate renewal and expansion orchestration plan",
    )
    renewal.add_argument("--customer-state-file", required=True)
    renewal.set_defaults(func=_cmd_renewal_orchestrator)

    p2 = sub.add_parser(
        "p2-monetization",
        help="Run proposal scorecard + package recommendation + renewal orchestration",
    )
    p2.add_argument("--service", required=True)
    p2.add_argument("--intake-file", required=True)
    p2.add_argument("--customer-state-file", required=True)
    p2.add_argument("--max-services", type=int, default=5)
    p2.set_defaults(func=_cmd_p2_monetization)

    offer_stack = sub.add_parser(
        "offer-stack",
        help="Render high-value enterprise service stack by segment",
    )
    offer_stack.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    offer_stack.add_argument("--lang", choices=["ar", "en"], default="ar")
    offer_stack.set_defaults(func=_cmd_offer_stack)

    launch_pack = sub.add_parser(
        "launch-pack",
        help="Generate final launch pack markdown including readiness verdict",
    )
    launch_pack.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    launch_pack.add_argument("--lang", choices=["ar", "en"], default="ar")
    launch_pack.add_argument("--output")
    launch_pack.set_defaults(func=_cmd_launch_pack)

    agent_apps = sub.add_parser(
        "agent-apps",
        help="Show best Hermes/OpenClaw applications for a service",
    )
    agent_apps.add_argument("--service", required=True)
    agent_apps.add_argument("--profile", choices=["hermes_agents", "openclaw_runtime", "hybrid_governed_execution"])
    agent_apps.add_argument("--lang", choices=["ar", "en"], default="ar")
    agent_apps.set_defaults(func=_cmd_agent_apps)

    agent_rollout = sub.add_parser(
        "agent-rollout",
        help="Show Hermes/OpenClaw rollout profile map for a segment",
    )
    agent_rollout.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    agent_rollout.add_argument("--profile", choices=["hermes_agents", "openclaw_runtime", "hybrid_governed_execution"])
    agent_rollout.add_argument("--lang", choices=["ar", "en"], default="ar")
    agent_rollout.set_defaults(func=_cmd_agent_rollout)

    enterprise_playbook = sub.add_parser(
        "enterprise-playbook",
        help="Generate profile-aware proposal, SOW, KPI contract, and governance contract",
    )
    enterprise_playbook.add_argument("--service", required=True)
    enterprise_playbook.add_argument("--intake-file", required=True)
    enterprise_playbook.add_argument("--profile", choices=["hermes_agents", "openclaw_runtime", "hybrid_governed_execution"])
    enterprise_playbook.add_argument("--segment", choices=["smb", "mid_market", "enterprise"])
    enterprise_playbook.add_argument("--lang", choices=["ar", "en"], default="ar")
    enterprise_playbook.add_argument("--output-dir")
    enterprise_playbook.set_defaults(func=_cmd_enterprise_playbook)

    go_live_sales = sub.add_parser(
        "go-live-sales",
        help="Render daily go-live sales runbook for a segment",
    )
    go_live_sales.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    go_live_sales.add_argument("--lang", choices=["ar", "en"], default="ar")
    go_live_sales.add_argument("--max-plays", type=int, default=5)
    go_live_sales.set_defaults(func=_cmd_go_live_sales)

    signature_readiness = sub.add_parser(
        "signature-readiness",
        help="Evaluate if the deal is ready for signature ask",
    )
    signature_readiness.add_argument("--stage", required=True)
    signature_readiness.add_argument("--buyer-commitment", required=True, choices=["low", "medium", "high"])
    signature_readiness.add_argument("--proof-level", required=True, choices=["L0", "L1", "L2", "L3", "L4", "L5"])
    signature_readiness.add_argument("--risk-status", required=True, choices=["low", "medium", "high"])
    signature_readiness.add_argument("--governance-contract-accepted", required=True)
    signature_readiness.set_defaults(func=_cmd_signature_readiness)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
