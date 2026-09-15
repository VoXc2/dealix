# 💰 Dealix — Revenue Readiness Status

> [!IMPORTANT]
> **HISTORICAL / NON-AUTHORITATIVE.** Current Dealix commercial authority is `config/company/commercial_truth_authority.json`: diagnostics are free; price, scope and duration are customer-specific after qualified discovery. This file does **not** prove Dealix current VAT-registration status. Verify current ZATCA/accounting evidence before issuing any tax invoice. For a resident person, the general mandatory VAT-registration threshold is taxable supplies above SAR 375,000; voluntary registration may apply above SAR 187,500. ZATCA Wave 25 uses SAR 187,500 as a separate e-invoicing integration-wave criterion for notified taxpayers based on VAT-taxable revenues in 2022–2025. Do not conflate the two thresholds.


**Last updated:** 2026-04-24
**Status:** PARTIALLY READY — can collect via manual Moyasar invoices; full automation blocked by Railway deploy.

---

## Revenue Path (7 Layers)

| Layer | Status | Evidence | Gap |
|-------|--------|----------|-----|
| 1. Pricing | ✅ VERIFIED READY | Defined in repo + landing | — |
| 2. Quote/Proposal | 🟡 PARTIAL | Enterprise template exists | No self-serve quote |
| 3. Invoice generation | 🟡 PARTIAL | HTML template + Moyasar API | Not automated |
| 4. Payment gateway | 🟡 PARTIAL | Moyasar integration code ready | Not deployed |
| 5. Confirmation | ❌ NOT READY | No email on payment | Needs Railway + email service |
| 6. Customer record | ❌ NOT READY | No CRM active | Needs HubSpot setup |
| 7. Follow-up | ✅ VERIFIED READY | Cadence defined, manual | — |

**Launch-ready via manual fallback:** YES
**Fully automated revenue:** NO (requires Railway + HubSpot + SendGrid setup)

---

## Manual Revenue Flow (Available Today)

```
Lead contacts you (WhatsApp/LinkedIn/email)
    ↓
You send Calendly link for demo
    ↓
Demo call (30 min, your Zoom/Meet)
    ↓
You verbally close pilot (1 SAR)
    ↓
You manually create Moyasar invoice (2 min in dashboard)
    ↓
You send payment link via WhatsApp
    ↓
Customer pays → Moyasar confirms
    ↓
You manually send welcome email
    ↓
You manually start onboarding
```

**Volume ceiling:** ~10 customers before breaking.

---

## Automated Revenue Flow (Future, after Railway deploy)

```
Lead submits form on landing page
    ↓
Dealix AI qualifies via chat
    ↓
Auto-books demo in Calendly
    ↓
Day of demo: auto-reminder sent
    ↓
Post-demo: auto-sends Moyasar invoice
    ↓
Payment → webhook updates DB
    ↓
Welcome email automated
    ↓
Onboarding sequence starts
```

**Volume ceiling:** 1000+ customers.

---

## Pricing Architecture

### Self-serve Tiers
| Plan | Price/mo (SAR) | Target |
|------|----------------|--------|
| Pilot | 1 (7-day trial) | Evaluation |
| Starter | 999 | 1-3 reps |
| Growth | 2,999 | 4-10 reps |
| Scale | 7,999 | 10+ reps |

### Setup Fees (one-time, optional)
| Service | Price (SAR) |
|---------|-------------|
| Basic setup | 1,000 |
| CRM integration | 3,000 |
| White-label | 15,000 |

### Partner Pricing (commissions paid from MRR)
| Partner type | Commission % |
|--------------|--------------|
| Referral only | 10% for 12 months |
| Service provider | 20% lifetime |
| Agency partner | 25% lifetime |

---

## Invoice Numbering Scheme

Format: `DLX-YYYY-NNNNN`
- DLX-2026-00001 (first invoice)
- DLX-2026-00002
- ... sequential

Keep tracker in Google Sheet:
| Invoice # | Date | Customer | Amount | Plan | Status | Paid Date |
|-----------|------|----------|--------|------|--------|-----------|

---

## ZATCA / VAT Requirements

**Historical state note — not current authority:**
- Current Dealix VAT-registration status is **NOT_PROVEN by this file**.
- For a resident person, mandatory VAT registration generally applies when annual taxable supplies exceed SAR 375,000; voluntary registration may apply above SAR 187,500, subject to current ZATCA rules and entity-specific facts.
- Verify current accounting/ZATCA evidence before issuing a tax invoice.

**Historical operational note — do not use as a current tax decision rule:**
1. Verify the entity's current VAT-registration status and the supply's tax treatment from authoritative evidence.
2. Consult a qualified accountant/tax adviser when registration or invoice treatment is uncertain.
3. Use ZATCA-compliant invoicing controls when they are actually applicable to the registered entity and transaction.
4. **Do not claim legal/tax compliance from this file.**

**Tool recommendation:** Wafeq (29 SAR/month) — Saudi-native, ZATCA-ready when needed.

---

## Refund Policy

**Pilot (1 SAR, 7 days):**
- Unconditional refund if requested within trial period
- Processed within 7 days

**Starter/Growth/Scale (monthly):**
- 30-day money-back guarantee
- Prorated refund for unused month after 30 days
- No refund after 90 days

**Scale (annual):**
- 30-day full refund
- After 30 days: prorated monthly-equivalent refund
- Enterprise contracts: custom terms in MSA

---

## Payment Methods Supported

| Method | Status | Gateway |
|--------|--------|---------|
| Mada | Via Moyasar | ✅ |
| Visa / Mastercard | Via Moyasar | ✅ |
| Apple Pay | Via Moyasar | ✅ |
| STC Pay | Via Moyasar | ✅ |
| Bank Transfer | Direct to bank | ✅ Manual |
| SADAD | Not yet | 🟡 Future |
| Crypto | Not planned | ❌ |

---

## Daily Revenue Operations

See `docs/growth/DAILY_REVENUE_OPERATING_SYSTEM.md` for the full operating rhythm.

**Key daily checks:**
1. Morning: Moyasar dashboard for overnight payments
2. Process new payments → confirmation email
3. Onboard any new customers within 4 hours
4. Update CRM with payment data

---

## Final Readiness Verdict

**Can Dealix collect money today?**
✅ YES — via manual Moyasar invoicing.

**Can Dealix collect money at scale?**
❌ NO — requires Railway backend deployment first.

**First Revenue:**
Expected within 7-14 days if outreach is started today.

**Sustainable $10K+ MRR:**
Expected month 3-4 if daily system is followed.

**$100K+ MRR:**
Expected month 9-12 with successful partner channel.
