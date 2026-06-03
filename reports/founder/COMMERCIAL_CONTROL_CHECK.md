# Commercial Control Check
*Generated: 2026-06-03 — by scripts/commercial-control-check.js*

Result: 🔴 **FAIL** — 19 passed, 1 failed, 0 warnings.

## ❌ Hard violations
- external send is NOT enabled by default (no DEALIX_SEND/SEND_ENABLED=true)

## ✅ Guardrails enforced
- schemas parse cleanly (12 files)
- registry defines exactly 5 systems (found 5)
- daily draft distribution sums to 400 (found 400)
- every system has a starting price
- every email draft maps to a known system (0 bad)
- no email draft carries an auto-send readiness state (0 bad)
- no email draft contains guarantee-style claims (0 bad)
- no email draft targets a suppressed / do-not-contact company (0 bad)
- every email draft uses an allowed approval_status (0 bad)
- every intelligence pack has a valid recommended_system (0 bad)
- every intelligence pack has a best_contact_role (0 bad)
- every call brief has an opening line and discovery questions (0 bad)
- every mini proposal requires founder approval (0 bad)
- every mini proposal lists deliverables (0 bad)
- every mini proposal has a starter price (0 bad)
- no mini proposal contains guarantee-style claims (0 bad)
- no delivery pipeline started work without required inputs (0 bad)
- no weekly value report contains guarantee-style claims (0 bad)
- no secret-like fields present in data records (0 bad)

## Always-on policy
- 400 drafts/day required; 400 sends/day not enabled.
- No external send by default. Every email stays a draft until founder approval.
- No automated calling. Call briefs are for human callers only.
- No cold WhatsApp or LinkedIn automation. No purchased lists. No fake Re:/Fwd:.
- No guaranteed-revenue claims. Public or founder-provided data only. Respect do-not-contact.
