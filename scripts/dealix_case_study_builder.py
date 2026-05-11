#!/usr/bin/env python3
"""Wave 16 §C3 — Case Study auto-generator CLI.

Reads proof events from a JSONL file and generates a case study draft
(bilingual narrative + safety findings + candidate metadata).

This is the founder's tool to convert a customer's accumulated proof
events into a customer-facing case study after all 3 publish gates
pass:
  1. evidence_level >= customer_confirmed
  2. consent_for_publication=True
  3. approval_status=approved

Hard rules:
- Article 4: NEVER auto-publishes. Output is draft_only — founder
  reviews + invokes approve_candidate() separately.
- Article 8: refuses to build if zero publishable events; lists rejected
  events with reasons (no fabrication).
- Article 11: thin wrapper over `case_study_engine.builder` — zero new
  business logic.
- NO_FAKE_PROOF: rejects events without explicit consent + approval.

Usage:
    # Build from a JSONL file of proof events:
    python3 scripts/dealix_case_study_builder.py \\
        --customer-handle acme-real-estate \\
        --sector real_estate \\
        --events data/customers/acme-real-estate/proof_events.jsonl

    # Print to stdout (md or json):
    python3 scripts/dealix_case_study_builder.py \\
        --customer-handle acme-real-estate \\
        --events events.jsonl \\
        --format json

    # Demo mode (uses 3 example fully-publishable events):
    python3 scripts/dealix_case_study_builder.py --demo
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.case_study_engine.builder import (  # noqa: E402
    build_candidate,
    select_publishable,
)


_DEMO_EVENTS = [
    {
        "event_id": "demo_evt_001",
        "evidence_level": "customer_confirmed",
        "consent_for_publication": True,
        "approval_status": "approved",
        "pii_redacted": True,
        "summary_ar": "تشخيص فرص أولية: 12 عميل محتمل في القطاع العقاري بالرياض.",
        "summary_en": "Initial diagnostic: 12 prospects in Riyadh real estate sector.",
        "metric_label": "Prospects identified",
        "metric_value": 12,
    },
    {
        "event_id": "demo_evt_002",
        "evidence_level": "payment_confirmed",
        "consent_for_publication": True,
        "approval_status": "approved",
        "pii_redacted": True,
        "summary_ar": "تأكيد دفع Sprint 499 ر.س — 7 أيام تسليم.",
        "summary_en": "Sprint payment 499 SAR confirmed — 7-day delivery committed.",
        "metric_label": "Time to payment",
        "metric_value": "3 days from diagnostic",
    },
    {
        "event_id": "demo_evt_003",
        "evidence_level": "customer_confirmed",
        "consent_for_publication": True,
        "approval_status": "approved",
        "pii_redacted": True,
        "summary_ar": "تسليم Proof Pack مع 9 مخرجات + توصية Next Best Offer.",
        "summary_en": "Proof Pack delivered with 9 deliverables + Next Best Offer recommendation.",
        "metric_label": "Deliverables shipped",
        "metric_value": 9,
    },
]


def load_events_from_jsonl(path: Path) -> list[dict]:
    """Read one event per line from a JSONL file."""
    if not path.exists():
        raise FileNotFoundError(f"events file not found: {path}")
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        events.append(json.loads(line))
    return events


def render_md(result: dict, customer_handle: str, sector: str | None) -> str:
    """Bilingual markdown — founder review + customer review."""
    candidate = result["candidate"]
    safety = result.get("safety_findings", [])
    rejected = result.get("rejected", [])

    lines = [
        f"# Case Study Draft — {customer_handle}",
        "",
        f"**Sector:** {sector or '—'}",
        f"**Candidate ID:** `{candidate['candidate_id']}`",
        f"**Proof events used:** {len(candidate.get('proof_event_ids', []))}",
        f"**Consent status:** {candidate.get('consent_status', 'unknown')}",
        f"**Redaction status:** {candidate.get('redaction_status', 'unknown')}",
        "",
        "---",
        "",
        "## السرد العربي · Arabic Narrative",
        "",
        candidate.get("narrative_draft_ar", "—"),
        "",
        "## English Narrative",
        "",
        candidate.get("narrative_draft_en", "—"),
        "",
    ]

    if safety:
        lines.extend([
            "---",
            "",
            "## ⚠️  Safety findings",
            "",
            *[f"- {f}" for f in safety],
            "",
        ])

    if rejected:
        lines.extend([
            "---",
            "",
            f"## Rejected events ({len(rejected)})",
            "",
            "Article 8: these events did NOT meet the publish gate; reasons below.",
            "",
            "| Event ID | Rejection reasons |",
            "|---|---|",
        ])
        for r in rejected:
            reasons = ", ".join(r.get("reasons", []))
            lines.append(f"| `{r.get('event_id', '?')}` | {reasons} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Next steps (founder action)",
        "",
        "1. Review narrative for accuracy + Saudi-cultural fit",
        "2. Run `case_study_engine.request_quote(candidate_id=...)` "
        "to ask customer for verbatim quote",
        "3. Once quote received: `case_study_engine.approve_candidate(...)` "
        "to mark publishable",
        "4. Render to `landing/case-studies/<sector>-<n>.html` "
        "(after final approval)",
        "",
        "_Article 4: NEVER publish without `approval_status=approved` "
        "AND `consent_signature_id` populated. NO_FAKE_PROOF._",
        f"_Generated: {datetime.now(UTC).isoformat(timespec='seconds')}_",
    ])
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--customer-handle", default="demo-customer",
                   help="Customer handle (snake-case-or-dashed).")
    p.add_argument("--sector", default=None,
                   help="Customer sector (real_estate / agency / b2b_services / etc.)")
    p.add_argument("--events", default=None,
                   help="Path to JSONL file of proof events.")
    p.add_argument("--objection", default=None,
                   help="Sales objection this case study answers.")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--demo", action="store_true",
                   help="Use 3 hard-coded demo events (sandbox-safe).")
    p.add_argument("--out", default=None,
                   help="Write to file (default: stdout).")
    args = p.parse_args()

    # Load events
    if args.demo:
        events = _DEMO_EVENTS
    elif args.events:
        events = load_events_from_jsonl(Path(args.events))
    else:
        print(
            "ERROR: provide --events <path> OR --demo",
            file=sys.stderr,
        )
        return 2

    # Pre-flight: select publishable
    selection = select_publishable(events)
    if selection["publishable_count"] == 0:
        # Article 8: no fabrication — refuse honestly
        print(
            "REFUSED · Article 8: zero events meet the publish gate.\n"
            f"  total_input={selection['total_input']}\n"
            f"  rejected={len(selection['rejected'])}\n"
            "  reasons (top 3):",
            file=sys.stderr,
        )
        for r in selection["rejected"][:3]:
            print(f"    - {r}", file=sys.stderr)
        return 1

    # Build candidate (raises ValueError if 0 publishable — already handled)
    result = build_candidate(
        customer_handle=args.customer_handle,
        events=events,
        sector=args.sector,
        objection_addressed=args.objection,
    )

    # Render
    if args.format == "json":
        # Make CaseStudyCandidate model_dump-able if it's a Pydantic model
        candidate = result["candidate"]
        candidate_dict = (
            candidate.model_dump() if hasattr(candidate, "model_dump")
            else dict(candidate)
        )
        rendered = json.dumps(
            {
                "customer_handle": args.customer_handle,
                "sector": args.sector,
                "candidate": candidate_dict,
                "safety_findings": result.get("safety_findings", []),
                "rejected": result.get("rejected", []),
                "is_estimate": True,  # Article 8
                "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
            ensure_ascii=False, indent=2, default=str,
        )
    else:
        # The builder returns the candidate as a CaseStudyCandidate;
        # convert to dict for rendering.
        candidate_obj = result["candidate"]
        candidate_dict = (
            candidate_obj.model_dump() if hasattr(candidate_obj, "model_dump")
            else dict(candidate_obj)
        )
        result_for_render = {
            **result,
            "candidate": candidate_dict,
        }
        rendered = render_md(result_for_render, args.customer_handle, args.sector)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"WROTE · {out_path} · {len(rendered)} chars", file=sys.stderr)
    print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
