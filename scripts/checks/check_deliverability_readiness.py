#!/usr/bin/env python3
"""
Dealix Check: Email Deliverability Readiness

Production (drafting) is decoupled from sending. Sending requires:
SPF/DKIM/DMARC, working unsubscribe + suppression, do-not-contact respected,
no purchased lists, no fake Re/Fwd, no guaranteed claims, no sudden volume
spike, and spam/bounce rates under their hard caps.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

REQUIRED_DOCS = [
    "docs/deliverability/EMAIL_DELIVERABILITY_POLICY_AR.md",
    "docs/deliverability/SENDING_VOLUME_POLICY_AR.md",
    "docs/deliverability/DOMAIN_AUTHENTICATION_CHECKLIST_AR.md",
    "docs/deliverability/SPAM_RATE_MONITORING_AR.md",
    "docs/deliverability/UNSUBSCRIBE_AND_SUPPRESSION_POLICY_AR.md",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — EMAIL DELIVERABILITY READINESS")

    d = load_json("company_os/deliverability/deliverability_state.json")
    if d is None:
        r.fail("deliverability_state.json missing or invalid")
        return r.render()

    auth = d.get("authentication", {})
    for key in ("spf", "dkim", "dmarc"):
        r.check(auth.get(key) is True,
                f"{key.upper()} configured",
                f"{key.upper()} NOT configured — sending blocked")

    comp = d.get("compliance", {})
    for key in ("unsubscribe_present", "one_click_unsubscribe",
                "do_not_contact_respected", "suppression_list_active"):
        r.check(comp.get(key) is True,
                f"{key} = true", f"{key} must be true before sending")

    for key in ("purchased_lists", "fake_reply_fwd",
                "guaranteed_claims", "sudden_volume_spike"):
        r.check(comp.get(key) is False,
                f"{key} = false", f"{key} must be false — policy violation")

    spam = d.get("spam", {})
    rate = spam.get("spam_rate_pct", 0)
    warn = spam.get("spam_rate_warn_pct", 0.1)
    hard = spam.get("spam_rate_hard_pct", 0.3)
    r.check(rate < hard,
            f"spam rate {rate}% under hard cap {hard}%",
            f"spam rate {rate}% at/above hard cap {hard}% — stop sending")
    if rate >= warn:
        r.warn(f"spam rate {rate}% at/above warning threshold {warn}%")

    bounce = d.get("bounce_rate_pct", 0)
    bounce_hard = d.get("bounce_rate_hard_pct", 2.0)
    r.check(bounce < bounce_hard,
            f"bounce rate {bounce}% under hard cap {bounce_hard}%",
            f"bounce rate {bounce}% at/above hard cap {bounce_hard}%")

    vol = d.get("volume", {})
    cur = vol.get("current_daily_volume", 0)
    cap = vol.get("max_daily_volume_for_mode", 0)
    r.check(cur <= cap,
            f"daily volume {cur} within mode cap {cap}",
            f"daily volume {cur} exceeds mode cap {cap} — throttle")

    r.require_files(REQUIRED_DOCS, label="deliverability doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
