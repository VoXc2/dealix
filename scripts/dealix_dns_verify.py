#!/usr/bin/env python3
"""Wave 17 §35.2.6 — DNS deliverability live verify.

Fetches actual DNS records (SPF / DKIM / DMARC) for a sending domain and
passes them to Wave 14's :func:`check_deliverability` to produce a
single bilingual founder-action verdict.

Founder workflow:
    1. Run this script after adding DNS records at the domain registrar.
    2. Read the verdict (3 levels: ready_for_marketing / partial / founder_action_needed).
    3. If "founder_action_needed": copy the next-action text and update registrar.

Hard rules:
- Article 4: read-only DNS lookups; never writes any record.
- Article 8: returns `founder_action_needed` honestly when records absent —
  never silently passes.
- Article 11: composes existing :func:`check_deliverability`. Zero new
  business logic.

Sandbox-safe: works without dnspython by falling back to `dig` if
available; if neither installed, prints `DNS_LOOKUP_UNAVAILABLE` and
exits 2 (caller knows to install `dnspython` or `dig`).

Usage:
    # Basic check:
    python3 scripts/dealix_dns_verify.py --domain dealix.me

    # JSON output (for piping):
    python3 scripts/dealix_dns_verify.py --domain dealix.me --format json

    # With explicit DKIM selector (default: 'default'):
    python3 scripts/dealix_dns_verify.py --domain dealix.me --dkim-selector google
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.email.deliverability_check import (  # noqa: E402
    check_deliverability,
)


def _dnspython_lookup(qname: str, rtype: str) -> str | None:
    """Try dnspython first (preferred — pure-Python, deterministic)."""
    try:
        import dns.resolver  # type: ignore[import]
    except ImportError:
        return None
    try:
        answer = dns.resolver.resolve(qname, rtype, lifetime=5.0)
        # TXT records can have multiple "..." chunks; join them
        for rdata in answer:
            if rtype == "TXT":
                # rdata.strings is bytes; decode each chunk
                return "".join(s.decode("utf-8", errors="replace") for s in rdata.strings)
            return str(rdata)
    except Exception:
        return None
    return None


def _dig_lookup(qname: str, rtype: str) -> str | None:
    """Fallback to dig binary if dnspython not installed."""
    if not shutil.which("dig"):
        return None
    try:
        result = subprocess.run(
            ["dig", "+short", "+time=5", "+tries=1", rtype, qname],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    out = result.stdout.strip()
    if not out:
        return None
    # dig +short returns quoted TXT chunks; strip quotes + join
    if rtype == "TXT":
        chunks = []
        for line in out.splitlines():
            # Remove leading/trailing quotes per chunk
            chunks.append(line.strip().strip('"').replace('" "', ""))
        return "".join(chunks) if chunks else None
    return out.splitlines()[0]


def lookup(qname: str, rtype: str) -> str | None:
    """Look up a DNS record, preferring dnspython then dig."""
    return _dnspython_lookup(qname, rtype) or _dig_lookup(qname, rtype)


def verify_domain(
    *,
    domain: str,
    dkim_selector: str = "default",
    one_click_unsubscribe_supported: bool = False,
) -> dict:
    """Fetch + validate SPF/DKIM/DMARC records for a domain.

    Returns a dict matching DeliverabilityStatus.model_dump style
    (when dataclass) plus a `lookup_method` field naming which tool
    answered (dnspython / dig / none).
    """
    method: Literal["dnspython", "dig", "none"]
    if _dnspython_lookup("dealix.me", "A") is not None:
        method = "dnspython"
    elif _dig_lookup("dealix.me", "A") is not None:
        method = "dig"
    else:
        method = "none"

    spf_record = lookup(domain, "TXT")
    dkim_record = lookup(f"{dkim_selector}._domainkey.{domain}", "TXT")
    dmarc_record = lookup(f"_dmarc.{domain}", "TXT")

    # Filter SPF: TXT may have multiple records; pick the one starting v=spf1
    if spf_record and not spf_record.lower().startswith("v=spf1"):
        # Try to find a v=spf1 record in the response
        spf_record = None

    status = check_deliverability(
        domain=domain,
        spf_record=spf_record,
        dkim_record=dkim_record,
        dmarc_record=dmarc_record,
        one_click_unsubscribe_header_supported=one_click_unsubscribe_supported,
    )

    return {
        "domain": domain,
        "dkim_selector": dkim_selector,
        "lookup_method": method,
        "spf_found": status.spf.found,
        "spf_valid": status.spf.is_valid,
        "spf_raw": status.spf.raw_value,
        "dkim_found": status.dkim.found,
        "dkim_valid": status.dkim.is_valid,
        "dmarc_found": status.dmarc.found,
        "dmarc_valid": status.dmarc.is_valid,
        "overall_status": status.overall_status,
        "safe_to_send_marketing": status.safe_to_send_marketing,
        "safe_to_send_transactional": status.safe_to_send_transactional,
        "daily_cap_recommended": status.daily_cap_recommended,
        "next_founder_action_ar": status.next_founder_action_ar,
        "next_founder_action_en": status.next_founder_action_en,
        "is_estimate": True,  # Article 8
    }


def render_md(verdict: dict) -> str:
    """Bilingual markdown."""
    emoji = {
        "ready_for_marketing": "✅",
        "ready_for_transactional": "🟢",
        "needs_dkim": "🟡",
        "needs_dmarc": "🟡",
        "founder_action_needed": "🔴",
        "blocked_marketing": "🟠",
    }.get(verdict["overall_status"], "❓")

    lines = [
        f"# {emoji} DNS Deliverability Verdict — `{verdict['domain']}`",
        "",
        f"**Status:** `{verdict['overall_status']}`",
        f"**Lookup method:** `{verdict['lookup_method']}`",
        f"**Daily cap recommended:** {verdict['daily_cap_recommended']} emails/day",
        "",
        "| Record | Found | Valid |",
        "|---|---|---|",
        f"| SPF (`{verdict['domain']}` TXT) | {'✅' if verdict['spf_found'] else '❌'} | {'✅' if verdict['spf_valid'] else '❌'} |",
        f"| DKIM (`{verdict['dkim_selector']}._domainkey.{verdict['domain']}` TXT) | {'✅' if verdict['dkim_found'] else '❌'} | {'✅' if verdict['dkim_valid'] else '❌'} |",
        f"| DMARC (`_dmarc.{verdict['domain']}` TXT) | {'✅' if verdict['dmarc_found'] else '❌'} | {'✅' if verdict['dmarc_valid'] else '❌'} |",
        "",
        "## Send-safety",
        "",
        f"- Marketing emails: {'✅ READY' if verdict['safe_to_send_marketing'] else '🚫 NOT READY'}",
        f"- Transactional emails: {'✅ READY' if verdict['safe_to_send_transactional'] else '🚫 NOT READY'}",
        "",
        "## Next founder action",
        "",
        f"### 🇸🇦 {verdict['next_founder_action_ar']}",
        "",
        f"### 🇬🇧 {verdict['next_founder_action_en']}",
        "",
        "---",
        "_Article 4: DNS lookups are read-only. Article 8: is_estimate=True._",
    ]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--domain", default="dealix.me",
                   help="Sending domain (default: dealix.me).")
    p.add_argument("--dkim-selector", default="default",
                   help="DKIM selector (default: 'default'). Try 'google' for Google Workspace.")
    p.add_argument(
        "--unsubscribe-supported", action="store_true",
        help="Set if your email sender includes List-Unsubscribe + "
             "List-Unsubscribe-Post headers (required by Google 2024+).",
    )
    p.add_argument("--format", choices=("md", "json"), default="md")
    args = p.parse_args()

    verdict = verify_domain(
        domain=args.domain,
        dkim_selector=args.dkim_selector,
        one_click_unsubscribe_supported=args.unsubscribe_supported,
    )

    if verdict["lookup_method"] == "none":
        print(
            "DNS_LOOKUP_UNAVAILABLE: neither dnspython nor dig found.\n"
            "Install one of:\n"
            "  pip install dnspython\n"
            "  apt-get install dnsutils  (Debian/Ubuntu)",
            file=sys.stderr,
        )
        return 2

    if args.format == "json":
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
    else:
        print(render_md(verdict))

    # Exit 0 if ready_for_marketing OR ready_for_transactional;
    # exit 1 otherwise (cron-friendly).
    if verdict["overall_status"] in ("ready_for_marketing", "ready_for_transactional"):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
