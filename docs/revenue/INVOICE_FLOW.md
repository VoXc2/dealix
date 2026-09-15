# Invoice Flow

> [!IMPORTANT]
> **HISTORICAL / NON-AUTHORITATIVE.** Current Dealix commercial authority is `config/company/commercial_truth_authority.json`: diagnostics are free; price, scope and duration are customer-specific after qualified discovery. This file does **not** prove Dealix current VAT-registration status. Verify current ZATCA/accounting evidence before issuing any tax invoice. For a resident person, the general mandatory VAT-registration threshold is taxable supplies above SAR 375,000; voluntary registration may apply above SAR 187,500. ZATCA Wave 25 uses SAR 187,500 as a separate e-invoicing integration-wave criterion for notified taxpayers based on VAT-taxable revenues in 2022–2025. Do not conflate the two thresholds.


## Current: Manual (via Moyasar dashboard)
1. Customer agrees to purchase
2. Create invoice in Moyasar: amount + description + customer email
3. Copy invoice URL
4. Send to customer via WhatsApp/email
5. Customer pays
6. Moyasar confirms (webhook if backend running, else dashboard)
7. Manual welcome email
8. Manual onboarding

## Future: Automated (after Railway deploy)
See `api/routers/webhooks.py` for the backend flow.

## Invoice numbering
Format: DLX-YYYY-NNNNN (sequential)

## VAT/ZATCA
Current Dealix VAT-registration status is **NOT_PROVEN here**. Verify current ZATCA/accounting evidence before issuing a tax invoice.
