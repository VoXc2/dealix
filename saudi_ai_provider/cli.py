"""Command-line interface for Saudi AI provider operating system."""

from __future__ import annotations

import argparse
from typing import Sequence

from .kpis import kpis_for_service
from .offers import build_pitch, generate_offer
from .pricing import package_for_segment, quote_service
from .roadmap import roadmap_for_days
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
            f"monthly={service['monthly_retainer_sar']} SAR"
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
    return 0


def _cmd_pitch(args: argparse.Namespace) -> int:
    print(build_pitch(args.service, lang=args.lang))
    return 0


def _cmd_offer(args: argparse.Namespace) -> int:
    outputs = generate_offer(args.service, args.segment, lang=args.lang)
    for name, path in outputs.items():
        print(f"{name}: {path}")
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

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
