#!/usr/bin/env python3
"""Wave 6 Phase 2 — first prospect intake script.

Writes to docs/wave6/live/first_prospect_intake.json (gitignored).
Refuses to overwrite an existing file unless --force.
Validates fields against the template + Wave 6 hard rules.

NEVER commit the live file. NEVER include raw PII (email/phone/ID).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

LIVE_DIR = Path("docs/wave6/live")
LIVE_PATH = LIVE_DIR / "first_prospect_intake.json"
TEMPLATE_PATH = Path("docs/wave6/FIRST_PROSPECT_INTAKE_TEMPLATE.json")

VALID_SECTORS = {
    "real_estate", "agencies", "services", "consulting",
    "training", "construction", "hospitality", "logistics",
}
VALID_REGIONS = {"Riyadh", "Jeddah", "Eastern", "other"}
VALID_LANGS = {"ar", "en", "both"}
VALID_CONSENT = {
    "pending", "granted_for_diagnostic",
    "granted_for_demo", "withdrawn",
}

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"\+?\d[\d\s().-]{6,}\d")
_SAUDI_ID_RE = re.compile(r"\b[12]\d{9}\b")


def _scan_for_pii(value: str, field: str) -> list[str]:
    findings = []
    if _EMAIL_RE.search(value):
        findings.append(f"raw_email_in:{field}")
    if _PHONE_RE.search(value):
        findings.append(f"raw_phone_in:{field}")
    if _SAUDI_ID_RE.search(value):
        findings.append(f"raw_saudi_id_in:{field}")
    return findings


def build_intake(args) -> dict:
    intake = {
        "company_name": args.company_name,
        "sector": args.sector,
        "region": args.region,
        "website": args.website,
        "current_growth_problem": args.growth_problem or "",
        "current_sales_problem": args.sales_problem or "",
        "current_support_problem": args.support_problem or "",
        "current_channels": [c.strip() for c in (args.channels or "").split(",") if c.strip()],
        "team_size": int(args.team_size) if args.team_size else 0,
        "decision_maker": args.decision_maker,
        "known_relationship": args.relationship,
        "consent_status": args.consent_status,
        "preferred_language": args.language,
        "notes": args.notes or "",
        "intake_version": "wave6_v1",
        "is_real_data": True,
        "is_template": False,
    }
    return intake


def validate(intake: dict) -> list[str]:
    errors: list[str] = []

    if not intake.get("company_name") or intake["company_name"].startswith("<"):
        errors.append("company_name required (no placeholder)")
    if intake.get("sector") not in VALID_SECTORS:
        errors.append(f"sector must be one of {sorted(VALID_SECTORS)}")
    if intake.get("region") not in VALID_REGIONS:
        errors.append(f"region must be one of {sorted(VALID_REGIONS)}")
    if intake.get("known_relationship") != "warm_intro":
        errors.append("known_relationship must be 'warm_intro' (Wave 6 cold blocked)")
    if intake.get("consent_status") not in VALID_CONSENT:
        errors.append(f"consent_status must be one of {sorted(VALID_CONSENT)}")
    if intake.get("preferred_language") not in VALID_LANGS:
        errors.append(f"preferred_language must be one of {sorted(VALID_LANGS)}")

    # PII scan on free-text fields
    for field in [
        "current_growth_problem", "current_sales_problem",
        "current_support_problem", "decision_maker", "notes",
    ]:
        value = intake.get(field, "") or ""
        if isinstance(value, str):
            findings = _scan_for_pii(value, field)
            errors.extend(findings)

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 first prospect intake")
    p.add_argument("--company-name", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--website", default=None)
    p.add_argument("--growth-problem", default="")
    p.add_argument("--sales-problem", default="")
    p.add_argument("--support-problem", default="")
    p.add_argument("--channels", default="", help="Comma-separated")
    p.add_argument("--team-size", default="0")
    p.add_argument("--decision-maker", default="<ROLE-PLACEHOLDER>")
    p.add_argument("--relationship", default="warm_intro")
    p.add_argument("--consent-status", default="pending")
    p.add_argument("--language", default="ar")
    p.add_argument("--notes", default="")
    p.add_argument("--force", action="store_true", help="Overwrite existing file")
    p.add_argument("--out-path", default=str(LIVE_PATH), help="Output path (default: live/)")
    args = p.parse_args()

    out = Path(args.out_path)
    if out.exists() and not args.force:
        print(f"REFUSING: {out} exists; pass --force to overwrite", file=sys.stderr)
        return 2

    intake = build_intake(args)
    errors = validate(intake)
    if errors:
        print("VALIDATION_ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(intake, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote {out}")
    print(f"  is_real_data: {intake['is_real_data']}")
    print(f"  consent_status: {intake['consent_status']}")
    print(f"  WARNING: this file is gitignored — never commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
