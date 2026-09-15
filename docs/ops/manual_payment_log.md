# Dealix Manual Payment Log

> [!IMPORTANT]
> **HISTORICAL / NON-AUTHORITATIVE.** Current Dealix commercial authority is `config/company/commercial_truth_authority.json`: diagnostics are free; price, scope and duration are customer-specific after qualified discovery. This file does **not** prove Dealix current VAT-registration status. Verify current ZATCA/accounting evidence before issuing any tax invoice. For a resident person, the general mandatory VAT-registration threshold is taxable supplies above SAR 375,000; voluntary registration may apply above SAR 187,500. ZATCA Wave 25 uses SAR 187,500 as a separate e-invoicing integration-wave criterion for notified taxpayers based on VAT-taxable revenues in 2022–2025. Do not conflate the two thresholds.


**Every manual payment request and confirmation is logged here** until Moyasar KYC activates and automation takes over.

---

## Entry template (per payment request)

```
## [Invoice # DLX-2026-NNNNN] — [Company] — [Date]

**Lead ID:** L-2026-NNNN
**Plan:** Pilot 1 SAR / Starter 999 / Growth 2,999 / Scale 7,999 / Custom
**Amount (SAR):** ___
**Currency:** SAR
**VAT applied:** VERIFY CURRENT VAT REGISTRATION + SUPPLY TREATMENT / YES or NO with evidence reference
**Due date:** YYYY-MM-DD (+7 days from issue)

**Payment methods offered (in order):**
1. Bank transfer (IBAN to Sami's business account)
2. STC Pay to Sami's number
3. Moyasar hosted invoice (if KYC active) — URL: ___
4. Tap Payments (if Moyasar blocked) — URL: ___

**Invoice sent via:**
- [ ] WhatsApp
- [ ] Email
- [ ] Both

**Invoice sent at:** YYYY-MM-DD HH:MM
**Reminder 1 (if unpaid +3 days):** YYYY-MM-DD — status: ___
**Reminder 2 (if unpaid +5 days):** YYYY-MM-DD — status: ___

**Payment received:**
- [ ] YES — method: ___ / date: YYYY-MM-DD HH:MM / bank transaction ref: ___
- [ ] NO — reason: ___ / escalation: ___

**Receipt issued (PDF):** docs/revenue/invoices/2026/DLX-2026-NNNNN.pdf
**Customer confirmation sent at:** YYYY-MM-DD HH:MM

**Kickoff call booked:** YYYY-MM-DD HH:MM via Calendly
**Onboarding checklist started:** YES / NO

**Notes:** ___
```

---

## Rules

1. **Invoice issued within 15 minutes of verbal yes.** Use `FIRST_REVENUE_ATTEMPT.md` script.
2. **Never chase payment more than 2 times.** After reminder 2, escalate or disqualify.
3. **Confirm payment via bank app / STC Pay app** — do not trust customer screenshot alone.
4. **VAT:** never infer registration from this historical file or from gross revenue alone; verify current registration and taxable-supply treatment from authoritative accounting/ZATCA evidence.
5. **Refund within 7 days (Pilot)** if requested — no argument. The case study is worth more than 1 SAR.

---

## Monthly totals (update end-of-month)

```
## 2026-04 Summary

Invoices issued: __
Invoices paid: __
Total revenue received: __ SAR
Total pending: __ SAR
Refunds: __ SAR (__ customers)
Net: __ SAR

By plan:
- Pilot:   __ × 1 SAR = __
- Starter: __ × 999 SAR = __
- Growth:  __ × 2,999 SAR = __
- Scale:   __ × 7,999 SAR = __

Cumulative MRR (recurring only): __ SAR
```

---

## Reconciliation with bank statements

End of each month:
1. Download bank statement (business account)
2. Match each credit to an entry here
3. Flag any payment without an invoice entry (unexpected deposits)
4. Flag any invoice marked paid without a bank match (verify bank app)
5. Export reconciliation CSV to `docs/revenue/reconciliation_2026_MM.csv`

---

## Live entries

*No entries yet. First entry appears after first customer verbal yes.*

---

*Works without Moyasar KYC. Upgrades to automated reconciliation once `MOYASAR_SECRET_KEY` live.*
