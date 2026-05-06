# Sector Playbooks — V12 mapped to 11 sectors

> **One doc, not 11 modules.** This file is the founder's pocket
> reference for which V12 module + which Phase E template to apply
> per sector. NO new code. NO duplicate playbook engines.

## Why one doc, not 11 modules

The "build a `sector_os/` with 11 sector files" pattern is V13-tier
overbuild. V12 already has 9 OSes that work cross-sector. The
sector-specific knowledge that's actually useful is small enough to
fit in a single founder reference. When 3 paid pilots have shipped
in 1 sector, THEN extract that sector's repeatable assets into
real code. Not before.

## The 11 sectors (priority-ordered)

### 🟢 Tier-1 (start here — V11/V12 ready)

| # | Sector AR | Sector EN | Why first | Best V12 module fit |
|---|---|---|---|---|
| 1 | وكالات تسويق | Marketing agencies | Understand growth + need proof | Growth OS + Proof Pack |
| 2 | خدمات B2B | B2B services | Slow follow-up + need clarity | Sales OS + Customer Success OS |
| 3 | استشارات وتدريب | Consulting & training | Many leads, weak conversion | Sales OS + Mini Diagnostic |

### 🟡 Tier-2 (after 1 paid pilot in Tier-1)

| # | Sector AR | Sector EN | Best V12 module fit |
|---|---|---|---|
| 4 | SaaS محلي | Local SaaS | Support OS + Knowledge Base |
| 5 | تجارة إلكترونية | Ecommerce | Support OS + Compliance OS |
| 6 | عقار ومقاولات | Real estate / contracting | Sales OS + Delivery OS |

### 🔴 Tier-3 (after 3 paid pilots — high-sensitivity)

| # | Sector AR | Sector EN | Special rule |
|---|---|---|---|
| 7 | خدمات صحية | Healthcare services | NO medical advice — admin/scheduling only |
| 8 | تعليم وتدريب | Education | NO accreditation claims |
| 9 | لوجستيات / ميدانية | Logistics & field | SLA-heavy — Delivery OS focus |
| 10 | محلية (مطاعم/كافيهات) | Local (F&B) | Growth OS local-only channels |
| 11 | صناعية | Industrial services | Long sales cycle — Sales OS qualification |

## Per-sector quick reference

For each sector below: 1 ICP + 1 pain + 1 best-fit Dealix output + 1 thing Dealix MUST NOT do.

### 1. Marketing agencies

- **ICP:** 2-15 person agencies serving SMEs.
- **Pain:** Customers ask "where's my ROI?" — agency has no proof.
- **Dealix output:** Bilingual Proof Pack (per `dealix_proof_pack.py`).
- **MUST NOT:** Promise white-label before 3 paid pilots (per `partnership_os` rules).

### 2. B2B services

- **ICP:** Service shops (legal/accounting/consulting/IT) with sales team < 5.
- **Pain:** Leads cool because nobody follows up consistently.
- **Dealix output:** 7-day follow-up calendar + bilingual drafts (per Growth OS + Sales OS).
- **MUST NOT:** Auto-send. Drafts + manual sends only.

### 3. Consulting & training

- **ICP:** Independent consultants + small training firms.
- **Pain:** Many discovery calls, few close.
- **Dealix output:** `dealix_diagnostic` → 499 SAR Pilot offer (Sales OS objection-response for "too expensive").
- **MUST NOT:** Claim guaranteed enrollment.

### 4. Local SaaS

- **ICP:** SaaS with ≤ 50 paying SMEs.
- **Pain:** Support tickets repeat; KB stale.
- **Dealix output:** `support-os/classify` + `support-os/draft-response` + KB-gap detection.
- **MUST NOT:** Invent policy outside `docs/knowledge-base/`.

### 5. Ecommerce

- **ICP:** Saudi Shopify/Salla/Zid stores doing 10–500 orders/day.
- **Pain:** Refund + shipping support eats founder time.
- **Dealix output:** Support OS classifier + escalation policy.
- **MUST NOT:** Issue automated refunds. Escalate per `escalation_policy_ar_en.md`.

### 6. Real estate / contracting

- **ICP:** Brokers + small contractors.
- **Pain:** Lead inquiries arrive in waves; none qualified.
- **Dealix output:** Sales OS qualification (Growth Starter Pilot scope).
- **MUST NOT:** Claim "guaranteed sale" or "investment advice".

### 7. Healthcare services (high-sensitivity — Tier 3 only)

- **ICP:** Clinics with admin/booking/marketing teams.
- **Pain:** PDPL + appointment-confirmation friction.
- **Dealix output:** Compliance OS action-check + Support OS for **admin** questions only.
- **MUST NOT:** Output medical advice. Diagnosis-related queries → escalate per `privacy_pdpl_ar_en.md`.

### 8. Education

- **ICP:** Training providers + course creators.
- **Pain:** Enrollment funnel leaks at "I'll think about it".
- **Dealix output:** Sales OS objection-response + meeting-prep.
- **MUST NOT:** Claim accreditation outside actual record.

### 9. Logistics & field services

- **ICP:** Last-mile + on-site service teams.
- **Pain:** SLA breaches + customer-status confusion.
- **Dealix output:** Delivery OS sessions + SLA tracker.
- **MUST NOT:** Auto-message customers about delays without dispatcher approval.

### 10. Local (F&B / retail / personal services)

- **ICP:** Single-location restaurants/cafés/salons.
- **Pain:** Seasonal campaigns, online reviews, no consistent loop.
- **Dealix output:** Growth OS daily-plan with local-channel-only drafts.
- **MUST NOT:** Cold outreach. Warm-intro / inbound-only.

### 11. Industrial / B2B suppliers

- **ICP:** Industrial supply, machinery, parts.
- **Pain:** Long sales cycles, RFQs lost in inbox.
- **Dealix output:** Sales OS qualification + Delivery OS multi-stage tracking.
- **MUST NOT:** Promise turn-around shorter than the supply chain reality.

## How to use this doc

1. Founder picks a warm intro from their network.
2. Identify the sector from the 11 above.
3. Apply the sector's "Dealix output" using the existing V12 endpoint / V11 script.
4. Respect the sector's "MUST NOT".
5. Log a real proof event after delivery.
6. NEVER add a new sector module here without first shipping 3 paid pilots in an existing sector.

## Hard rules — re-asserted

- ❌ NO new sector_os/ Python module before 3 paid pilots in any single sector
- ❌ NO sector-specific automation that bypasses Compliance OS action-policy
- ❌ NO healthcare medical-advice output, ever
- ❌ NO real-estate "guaranteed sale" / "investment-advice" output, ever
- ✅ Every sector reuses the SAME 9 V12 OSes
- ✅ Every sector starts with the SAME 6-question Mini Diagnostic
- ✅ Every sector ends with the SAME `dealix_proof_pack.py` honest output
