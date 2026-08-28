#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ops/POSTHOG_EVENTS.md"
SNIPPET = ROOT / "landing/posthog_snippet.html"

REQUIRED = (
    "qualified_visit",
    "diagnostic_start",
    "diagnostic_submit",
    "real_interaction",
    "verified_relationship",
    "qualified_problem",
    "discovery_booked",
    "discovery_completed",
    "proposal_sent",
    "pilot_agreed",
    "payment_verified",
    "delivery_proof",
    "referral",
    "expansion",
)

FORBIDDEN = (
    "pilot_1sar",
    "starter, growth, scale",
    "Landing → Pilot ($1)",
    "checkout_started (plan=pilot_1sar)",
    "amount: 1",
    "pricing_tier_click",
)


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    snippet = SNIPPET.read_text(encoding="utf-8")
    combined = doc + "\n" + snippet

    missing = [event for event in REQUIRED if event not in doc]
    stale = [marker for marker in FORBIDDEN if marker in combined]
    if missing or stale:
        print("DEALIX_MARKETING_ATTRIBUTION_CONTRACT=FAIL")
        if missing:
            print("MISSING=" + ",".join(missing))
        if stale:
            print("STALE=" + ",".join(stale))
        return 1

    if "disable_session_recording: true" not in snippet:
        print("DEALIX_MARKETING_ATTRIBUTION_CONTRACT=FAIL")
        print("MISSING=session_recording_default_off")
        return 1

    if "autocapture: false" not in snippet:
        print("DEALIX_MARKETING_ATTRIBUTION_CONTRACT=FAIL")
        print("MISSING=autocapture_default_off")
        return 1

    print("DEALIX_MARKETING_ATTRIBUTION_CONTRACT=PASS")
    print(f"BUSINESS_EVENTS={len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
