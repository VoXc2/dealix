# Legal Engagement Tracker — Dealix

**Status:** DRAFT — to be filled by founder before customer #1
**Owner:** Sami (founder)
**Last updated:** 2026-05-07
**Companion docs:** `docs/PRIVACY_PDPL_READINESS.md` · `docs/DPA_PILOT_TEMPLATE.md` · `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` · Plan §23.5.5

> **Why this doc exists:** Wave 7 §23.5.5 — PDPL violation = up to 5,000,000 SAR fine + criminal exposure (up to 2 years for sensitive data). 48 enforcement decisions issued by SDAIA in 2025-2026. **No paid customer onboarded until DPA is lawyer-signed.**

---

## 1. Lawyer engagement state

| Field | Value |
|---|---|
| Lawyer / firm name | _NOT_YET_ENGAGED_ |
| Primary contact (name + email) | _TBD_ |
| Specialty | Saudi PDPL + corporate law (B2B SaaS) |
| Retainer agreed | _TBD_ SAR |
| Engagement letter signed at | _TBD_ |
| Estimated turnaround | 5-10 business days for first deliverable batch |
| Renewal date | _TBD_ |

---

## 2. Candidate firms (for first quote — pick 2-3 to email)

| # | Firm | Reason | Contact path |
|---|---|---|---|
| 1 | Clyde &amp; Co KSA | Published 2026 PDPL enforcement guide; deep PDPL analytics | clydeco.com/en/locations/saudi-arabia |
| 2 | Baker McKenzie KSA | Global tech-SaaS depth + KSA presence | bakermckenzie.com/en/locations/middle-east/saudi-arabia |
| 3 | AlTamimi &amp; Company | Largest regional firm; PDPL practice | tamimi.com |
| 4 | Eversheds Sutherland | Tech sector focus | eversheds-sutherland.com |
| 5 | AlSabhan &amp; Partners | Saudi-only boutique; SME pricing | alsabhanlaw.com |

**Selection criteria:** PDPL specialty + B2B SaaS familiarity + Saudi-Arabic-native attorney + retainer ≤15K SAR for first batch.

---

## 3. Deliverables required from lawyer

Listed in order of P0 → P2.

### P0 — block paying customer #1

| # | Deliverable | Source doc to review | Due | Status |
|---|---|---|---|---|
| L1 | DPA template lawyer-signed | `docs/DPA_PILOT_TEMPLATE.md` | day 7 | NOT_STARTED |
| L2 | Privacy Policy v2 attestation | `landing/privacy.html` (currently "v1 under review") | day 7 | NOT_STARTED |
| L3 | Terms of Service v2 attestation | `landing/terms.html` (currently "v1 under review") | day 7 | NOT_STARTED |
| L4 | Subprocessor disclosure check | `landing/subprocessors.html` | day 10 | NOT_STARTED |

### P1 — block customer #4 (scale gate)

| # | Deliverable | Source doc to review | Due | Status |
|---|---|---|---|---|
| L5 | DSAR (data subject request) procedure | `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` | day 14 | NOT_STARTED |
| L6 | Breach response plan | _TBD_ doc | day 21 | NOT_STARTED |
| L7 | Cross-border data transfer clause review | inside DPA | day 21 | NOT_STARTED |

### P2 — block first agency partner

| # | Deliverable | Source doc to review | Due | Status |
|---|---|---|---|---|
| L8 | Partner referral agreement template | `docs/PARTNER_LEGAL_AGREEMENT.md` | day 30 | NOT_STARTED |
| L9 | Co-marketing agreement template | _TBD_ doc | day 60 | NOT_STARTED |

---

## 4. SDAIA registration (founder action — no lawyer needed)

| Step | Source | Status |
|---|---|---|
| Create SDAIA business account | sdaia.gov.sa portal | NOT_STARTED |
| Submit Dealix entity record (Controller info) | online form | NOT_STARTED |
| Receive registration confirmation | email + portal | NOT_STARTED |
| File registration number in `docs/SECURITY_PDPL_CHECKLIST.md` | locally | NOT_STARTED |

**Cost:** 0 SAR (online, free). **ETA:** 7 calendar days from submission.

---

## 5. Cost ceiling + payment schedule

| Item | Estimate | Cap |
|---|---|---|
| Initial lawyer retainer (P0 batch L1-L4) | 5,000-10,000 SAR | 15,000 SAR |
| Hourly rate for ad-hoc questions | 800-1,500 SAR/hr | 5h/month |
| Cybersecurity insurance (deferred to month 4) | 2,500-5,000 SAR/year | _N/A_ |
| Annual SDAIA compliance audit (year 2+) | _TBD_ | _TBD_ |

**Total Year 1 legal budget:** ≤25,000 SAR (~5% of first MRR cohort).

---

## 6. Fallback if lawyer not engaged by day 7

**Option A — delay customer #1.** Push close to day 14+, do NOT take payment without DPA. Communicate honestly to prospect: _"نحتاج 7 أيّام إضافيّة لإكمال المراجعة القانونيّة لاتفاقيّة المعالجة."_

**Option B — engage emergency lawyer.** Use Stripe Atlas / Clerky model: pre-vetted Saudi corporate lawyer for fixed 3,500 SAR same-week turnaround. (Verify availability before relying on this.)

**Option C — abort.** If 14 days pass without legal coverage, pause the entire Wave 7 plan and re-evaluate. Reputation > revenue.

---

## 7. Update cadence

This file updates **weekly** during founder Friday review (per `docs/V14_FOUNDER_DAILY_OPS.md` §5).

Append a row to §3 status column whenever a deliverable moves: NOT_STARTED → IN_REVIEW → SIGNED.

Once all P0 items signed → unblock customer #1 onboarding.

---

## 8. Hard rules

- ❌ Never sign a customer DPA before lawyer-attested L1
- ❌ Never publish privacy.html / terms.html v2 before lawyer L2/L3 attestation
- ❌ Never share customer PII with external party without DPA chain (Controller → Processor → sub-processor) signed
- ✅ Always log lawyer interactions in this file (date · question · answer)
- ✅ Always cc lawyer on PDPL data subject requests (DSAR) until L5 procedure is signed off

> **Disclaimer:** This document is an internal tracker. It is NOT a substitute for legal counsel. All clauses, templates, and procedures referenced herein require lawyer review before reliance.
