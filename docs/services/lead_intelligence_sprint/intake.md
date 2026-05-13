# Lead Intelligence Sprint — Intake Questions

## Day-1 Discovery (30 min, recorded)

1. What does your company sell — in one sentence (AR + EN)?
2. Who is your ideal customer? (industry, size, region)
3. Which Saudi cities or regions do you target?
4. What data do you currently have? (CRM, spreadsheet, none?)
5. Where did this data come from? (own collection, partners, public sources?)
6. Do you have prior relationship or consent with these contacts?
7. What is your current sales process — from lead to close?
8. Name one successful customer and why they bought.
9. Words / claims you must avoid in messaging.
10. The single outcome you want from this Sprint.

## Required schema for input data (CSV / Excel)

| Column | Required? | Notes |
|--------|-----------|-------|
| company_name_ar | yes | Arabic legal/trading name |
| company_name_en | optional | English name |
| vertical | yes | one of: bfsi / retail_ecomm / healthcare / logistics / etc. |
| region | yes | city code |
| source | yes | provenance of the record |
| commercial_registration | recommended | 10 digits |
| vat_number | recommended | 15 digits, starts with 3 |
| email | optional | |
| phone | optional | Saudi mobile preferred |
| domain | optional | |
| triggers | optional | comma-separated tags (tender / funding / hire / …) |
| headcount | optional | int |
| annual_revenue_sar | optional | float |
| updated_at | recommended | ISO datetime |

## Compliance acknowledgements (Day-1 sign-off)

- [ ] PDPL Art. 13 notice will be included in every outreach draft.
- [ ] No outbound action will be executed without per-message customer approval.
- [ ] Customer asserts lawful basis for processing the provided records.
