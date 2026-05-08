#!/usr/bin/env python3
"""Wave 7.7 — Founder pre-approved rules CLI.

Usage:
    dealix_founder_rules.py add
    dealix_founder_rules.py list
    dealix_founder_rules.py disable RULE_ID
    dealix_founder_rules.py audit [--limit N]

Hard rules (enforced both here AND in the engine):
  - DEALIX_FOUNDER_RULES_SECRET env var is required (fail-closed).
  - WhatsApp / LinkedIn / Phone are PERMANENTLY blocked from rules.
  - High / blocked risk levels are PERMANENTLY blocked.
  - Rules are HMAC-SHA256 signed; tampering invalidates them.
  - Default TTL is 30 days; refresh requires founder to re-sign.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Allow running this script directly from a checked-out repo.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.approval_center.founder_rules import (  # noqa: E402
    DEFAULT_RULE_TTL_DAYS,
    FounderRuleEngine,
    _BLOCKED_AUTO_CHANNELS,
)

SECRET_ENV_VAR = "DEALIX_FOUNDER_RULES_SECRET"


def _require_secret_or_exit() -> None:
    if not os.environ.get(SECRET_ENV_VAR, ""):
        print(
            f"ERROR: environment variable {SECRET_ENV_VAR} is required.\n"
            "  Set it to a strong random string and re-run (fail-closed).\n"
            "  ar: متغير البيئة مطلوب لتوقيع القاعدة قبل المتابعة.",
            file=sys.stderr,
        )
        sys.exit(2)


def _prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def cmd_add(args: argparse.Namespace) -> int:
    _require_secret_or_exit()
    engine = FounderRuleEngine()

    print()
    print("== Add a founder rule (HMAC-signed) ==")
    print("ar: إضافة قاعدة موافقة مسبقة موقعة من المؤسس")
    print(
        "Permanently blocked channels: "
        + ", ".join(sorted(_BLOCKED_AUTO_CHANNELS))
    )
    print()

    name = _prompt("Rule name (short label)")
    channel = _prompt("Channel (email | dashboard)", default="email").lower()
    if channel in _BLOCKED_AUTO_CHANNELS:
        print(
            f"REFUSED: channel '{channel}' is permanently blocked.\n"
            "  ar: هذه القناة محظورة دائماً من القواعد المسبقة.",
            file=sys.stderr,
        )
        return 2

    customer_handle = _prompt(
        "Customer handle (e.g. acme-real-estate or '*')", default="*"
    )
    action_type = _prompt(
        "Action type (e.g. faq_reply or '*')", default="faq_reply"
    )
    max_risk_level = _prompt(
        "Max risk level (low | medium)", default="low"
    ).lower()
    min_confidence_str = _prompt("Min confidence (0.0–1.0)", default="0.9")
    try:
        min_confidence = float(min_confidence_str)
    except ValueError:
        print("ERROR: min_confidence must be a number 0.0–1.0", file=sys.stderr)
        return 2

    content_pattern_regex = _prompt(
        "Content pattern regex (optional, leave empty to skip)"
    )
    if content_pattern_regex:
        print(
            "  WARNING: regex matching can produce false positives. "
            "Test thoroughly before relying on this in production.\n"
            "  ar: تحذير — مطابقة التعبير العادي قد تعطي نتائج غير دقيقة."
        )

    ttl_days_str = _prompt(
        "TTL days (1–90)", default=str(DEFAULT_RULE_TTL_DAYS)
    )
    try:
        ttl_days = int(ttl_days_str)
    except ValueError:
        print("ERROR: ttl_days must be an integer 1–90", file=sys.stderr)
        return 2
    ttl_days = max(1, min(ttl_days, 90))

    notes = _prompt("Notes (optional)")

    try:
        rule = engine.create_rule(
            name=name,
            channel=channel,
            customer_handle=customer_handle,
            action_type=action_type,
            max_risk_level=max_risk_level,
            min_confidence=min_confidence,
            content_pattern_regex=content_pattern_regex,
            notes=notes,
            ttl_days=ttl_days,
        )
        engine.append_rule(rule)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print()
    print(f"Rule created. id={rule.rule_id}")
    print(f"  Rule signed with HMAC. Active until {rule.expires_at}.")
    print("  Refresh required after expiry.")
    print(f"  ar: القاعدة موقعة. سارية حتى {rule.expires_at}.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    _require_secret_or_exit()
    engine = FounderRuleEngine()
    rules = engine.list_rules()
    if not rules:
        print("(no rules)")
        return 0
    print(
        f"{'rule_id':<32} {'name':<24} {'channel':<10} "
        f"{'enabled':<8} {'expires_at':<32} {'sig':<4}"
    )
    print("-" * 116)
    for r in rules:
        sig_ok = "OK" if engine.verify_signature(r) else "BAD"
        print(
            f"{r.rule_id:<32} {r.name[:24]:<24} {r.channel:<10} "
            f"{str(r.enabled):<8} {r.expires_at:<32} {sig_ok:<4}"
        )
    return 0


def cmd_disable(args: argparse.Namespace) -> int:
    _require_secret_or_exit()
    engine = FounderRuleEngine()
    found = engine.disable_rule(args.rule_id)
    if not found:
        print(f"ERROR: rule {args.rule_id} not found", file=sys.stderr)
        return 2
    print(f"Rule {args.rule_id} disabled.")
    print(f"  ar: تم تعطيل القاعدة {args.rule_id}.")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    engine = FounderRuleEngine()
    rows = engine.list_recent_matches(limit=args.limit)
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dealix_founder_rules",
        description="Manage founder pre-approved rules (Wave 7.7).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Interactively add a new rule.")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all rules.")
    p_list.set_defaults(func=cmd_list)

    p_disable = sub.add_parser("disable", help="Disable a rule by id.")
    p_disable.add_argument("rule_id")
    p_disable.set_defaults(func=cmd_disable)

    p_audit = sub.add_parser("audit", help="Show recent rule matches.")
    p_audit.add_argument("--limit", type=int, default=20)
    p_audit.set_defaults(func=cmd_audit)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
