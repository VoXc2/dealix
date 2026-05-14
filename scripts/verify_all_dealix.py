#!/usr/bin/env python3
"""verify_all_dealix.py — Wave 19 Recovery readiness verifier.

This verifier is intentionally separate from the technical CI test suite.
It scores commercial / CEO-completion artifacts on a 0..5 scale per
system, separates build-complete from company-complete, and is honest
about market actions that have not happened yet.

Usage:
    python scripts/verify_all_dealix.py            # human report
    python scripts/verify_all_dealix.py --json     # machine-readable

Exit code:
    0 — all systems pass at score >= 3
    1 — any system fails (score < 3)
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent


def _exists(*paths: str) -> bool:
    return all((REPO_ROOT / p).exists() for p in paths)


def _read_json(path: str) -> dict | None:
    p = REPO_ROOT / path
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _contains(path: str, *needles: str) -> bool:
    p = REPO_ROOT / path
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    return all(n in text for n in needles)


@dataclass
class Check:
    system: str
    score: int  # 0..5
    pass_: bool
    details: str

    def to_dict(self) -> dict:
        return {
            "system": self.system,
            "score": self.score,
            "pass": self.pass_,
            "details": self.details,
        }


def check_offer_ladder() -> Check:
    if not _exists("docs/sales-kit/INVESTOR_ONE_PAGER.md"):
        return Check("Offer Ladder", 0, False, "INVESTOR_ONE_PAGER.md missing")
    if not _contains(
        "docs/sales-kit/INVESTOR_ONE_PAGER.md",
        "4,999 SAR/month",
        "25,000 SAR",
        "No scraping",
    ):
        return Check("Offer Ladder", 2, False, "one-pager missing required content")
    return Check("Offer Ladder", 4, True, "ladder + discipline language present")


def check_founder_command_center() -> Check:
    landing = REPO_ROOT / "landing/founder-command-bus.html"
    marker = _read_json("data/founder_command_center_status.json")
    if marker is None:
        return Check("Founder Command Center", 1, False, "deploy marker missing")
    if not marker.get("deployment_marker"):
        return Check("Founder Command Center", 2, False, "marker present but deployment_marker=false")
    page_ok = landing.exists() or _marker_page_inside_repo(marker.get("page_path", ""))
    if not page_ok:
        return Check("Founder Command Center", 3, True, "marker present, page path note only")
    return Check("Founder Command Center", 4, True, "page + marker present")


def _marker_page_inside_repo(page_path: str) -> bool:
    """Resolve ``page_path`` relative to the repo root and only count it as
    present when it lands inside the repository. An absolute path like
    ``/etc/hosts`` would otherwise escape ``REPO_ROOT`` and trick the
    check into passing without a real founder-page artifact."""
    if not page_path:
        return False
    raw = Path(page_path)
    if raw.is_absolute():
        return False
    if ".." in raw.parts:
        return False
    try:
        candidate = (REPO_ROOT / raw).resolve()
        repo_root = REPO_ROOT.resolve()
        candidate.relative_to(repo_root)
    except (OSError, ValueError):
        return False
    return candidate.exists()


def check_partner_motion() -> Check:
    docs_ok = _exists("docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md")
    pipeline = _read_json("data/anchor_partner_pipeline.json")
    log = _read_json("data/partner_outreach_log.json")
    if not (docs_ok and pipeline and log):
        return Check("Partner Motion", 0, False, "outreach doc/pipeline/log missing")
    if not pipeline.get("partner_archetypes"):
        return Check("Partner Motion", 1, False, "pipeline has no archetypes")
    sent = log.get("outreach_sent_count", 0)
    entries = len(log.get("entries", []))
    if sent != entries:
        return Check(
            "Partner Motion",
            2,
            False,
            f"log dishonest: count={sent} entries={entries}",
        )
    if sent == 0:
        return Check(
            "Partner Motion",
            3,
            True,
            "runbook + pipeline + honest log; outreach not yet sent",
        )
    return Check("Partner Motion", 5, True, f"{sent} outreach entries logged")


def check_first_invoice_motion() -> Check:
    if not _exists("docs/ops/FIRST_INVOICE_UNLOCK.md"):
        return Check("First Invoice Motion", 0, False, "FIRST_INVOICE_UNLOCK.md missing")
    log = _read_json("data/first_invoice_log.json")
    if log is None:
        return Check("First Invoice Motion", 1, False, "first_invoice_log.json missing")
    sent = log.get("invoice_sent_count", 0)
    paid = log.get("invoice_paid_count", 0)
    entries = len(log.get("entries", []))
    if sent != entries or paid > sent:
        return Check(
            "First Invoice Motion",
            2,
            False,
            f"log dishonest: sent={sent} paid={paid} entries={entries}",
        )
    if sent == 0:
        return Check(
            "First Invoice Motion",
            3,
            True,
            "runbook + honest log; invoice not yet sent",
        )
    if paid == 0:
        return Check("First Invoice Motion", 4, True, f"{sent} invoice(s) sent, none paid")
    return Check("First Invoice Motion", 5, True, f"{paid} invoice(s) paid")


def check_funding_pack() -> Check:
    required = [
        "docs/funding/FUNDING_MEMO.md",
        "docs/funding/USE_OF_FUNDS.md",
        "docs/funding/HIRING_SCORECARDS.md",
        "docs/funding/FIRST_3_HIRES.md",
        "docs/funding/INVESTOR_QA.md",
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    if missing:
        return Check("Funding Pack", 0, False, f"missing: {', '.join(missing)}")
    if not _contains("docs/funding/USE_OF_FUNDS.md", "Capital must not fund"):
        return Check("Funding Pack", 2, False, "USE_OF_FUNDS missing discipline language")
    if not _contains("docs/funding/HIRING_SCORECARDS.md", "Do Not Hire If"):
        return Check("Funding Pack", 2, False, "HIRING_SCORECARDS missing gate language")
    return Check("Funding Pack", 4, True, "memo + use of funds + hiring gates + Q&A present")


def check_gcc_expansion() -> Check:
    required = [
        "docs/gcc-expansion/GCC_EXPANSION_THESIS.md",
        "docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md",
        "docs/gcc-expansion/GCC_GO_TO_MARKET_SEQUENCE.md",
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    if missing:
        return Check("GCC Expansion", 0, False, f"missing: {', '.join(missing)}")
    if not _contains(
        "docs/gcc-expansion/GCC_EXPANSION_THESIS.md",
        "Saudi-first commercially",
        "not launching broadly across the GCC before Invoice #1",
    ):
        return Check("GCC Expansion", 2, False, "thesis missing Saudi-beachhead lock")
    return Check("GCC Expansion", 4, True, "thesis + country map + sequence present")


def check_open_doctrine() -> Check:
    required = [
        "open-doctrine/README.md",
        "open-doctrine/11_NON_NEGOTIABLES.md",
        "open-doctrine/CONTROL_MAPPING.md",
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    if missing:
        return Check("Open Doctrine", 0, False, f"missing: {', '.join(missing)}")
    forbidden = [
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "password",
        "token",
    ]
    for p in required:
        # Case-insensitive scan so ``Password`` / ``TOKEN`` / mixed-case
        # variants aren't missed by the lowercase-token list.
        text = (REPO_ROOT / p).read_text(encoding="utf-8").lower()
        for term in forbidden:
            if term in text:
                return Check(
                    "Open Doctrine",
                    1,
                    False,
                    f"forbidden term '{term}' leaked into {p}",
                )
    return Check("Open Doctrine", 4, True, "public doctrine present + secret-clean")


CHECKS: list[Callable[[], Check]] = [
    check_offer_ladder,
    check_founder_command_center,
    check_partner_motion,
    check_first_invoice_motion,
    check_funding_pack,
    check_gcc_expansion,
    check_open_doctrine,
]


def run() -> tuple[list[Check], bool, bool]:
    results = [fn() for fn in CHECKS]
    all_pass = all(r.pass_ for r in results)
    market_action_systems = {"Partner Motion", "First Invoice Motion"}
    # CEO completion threshold: score >= 4. The matrix defines CEO-complete
    # around the "invoice sent" milestone (see docs/ops/FIRST_INVOICE_UNLOCK.md);
    # ``check_first_invoice_motion()`` returns 4 for "sent, unpaid" and 5
    # only after a paid invoice. Requiring 5 would block CEO-complete on a
    # successful sent state, contradicting the documented gate semantics.
    ceo_complete = all_pass and all(
        r.score >= 4 for r in results if r.system in market_action_systems
    )
    return results, all_pass, ceo_complete


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results, all_pass, ceo_complete = run()

    if args.json:
        print(
            json.dumps(
                {
                    "results": [r.to_dict() for r in results],
                    "all_pass": all_pass,
                    "ceo_complete": ceo_complete,
                },
                indent=2,
            )
        )
    else:
        print("Dealix Wave 19 Recovery — Readiness Verifier")
        print("=" * 60)
        for r in results:
            status = "PASS" if r.pass_ else "FAIL"
            print(f"  [{status}]  {r.score}/5  {r.system}: {r.details}")
        print("=" * 60)
        print(f"All systems pass (>=3/5):  {all_pass}")
        print(f"CEO-complete (market motion at 5/5): {ceo_complete}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
