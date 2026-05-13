# Statement of Work — Company Brain Sprint

**Dealix Project ID:** `{{project_id}}`
**SOW ID:** `{{sow_id}}`
**Date:** `{{date}}`
**Governing law:** Kingdom of Saudi Arabia

## 1. Parties

| Role | Entity |
|------|--------|
| Service Provider | Dealix (CR `{{dealix_cr}}`, VAT `{{dealix_vat}}`) |
| Customer | `{{customer_name_ar}}` / `{{customer_name_en}}` (CR `{{customer_cr}}`) |

## 2. Offer

**Company Brain Sprint — Files → Cited Internal Assistant**
- **Duration:** 21 business days
- **Fee:** SAR 20,000 (excl. VAT)
- **VAT (15%):** SAR 3,000
- **Total:** **SAR 23,000** (incl. VAT)
- **Payment terms:** Net 14 after countersignature; 50% upfront, 50% on delivery.

## 3. Scope — Inclusions

- Ingest up to 500 documents (PDF / Docs / KB / policies).
- PII detection + redaction for sensitive content before indexing.
- RAG indexing with source / chunk-level citation tracking.
- Web / Slack / Teams query interface for one team (≤ 20 seats).
- 3-tier access rules (Admin / Team / Read-only).
- Freshness tracking (auto-flag for docs > 90 days old).
- 2-hour recorded team training.

## 4. Out of Scope

- Documents beyond 500 (overage billed per Pricing).
- More than one team (requires higher tier).
- Custom CRM / professional-network integrations.

## 5. Customer Inputs Required

1. Document inventory (file names + categories).
2. Permissions matrix (who sees what).
3. Sensitive document flagging.
4. 10 sample questions the assistant should answer.
5. Document-owner contacts per category.

## 6. Success Criteria (binding)

- ≥ 95% of test answers carry a verifiable citation.
- Zero PII surfaced in assistant outputs.
- Access rules enforced (verified on 3 personas).
- Documents > 90 days flagged in the freshness report.
- Customer team confirms self-service usability post-training.

## 7. Hard Product Rule

> **No source = no answer.** When the retriever cannot return ≥ 1 source meeting
> the confidence floor, the assistant must reply "insufficient evidence —
> لا توجد أدلة كافية في القاعدة المعرفية." rather than hallucinate.

## 8. Delivery Standard + SLA

- Follows the 8-stage Dealix Delivery Standard + 5-gate QA (floor 80/100).
- Delivery: 21 business days from countersignature.
- Issue response: P95 < 1 business day.

## 9. Compliance

- PDPL Art. 5 lawful basis (contract).
- PII redaction enforced before indexing.
- Audit trail appended to immutable event store.
- Right-to-erasure SLA: < 72 hours.

## 10. Liabilities and Caps

Total liability capped at total fees paid. Dealix does not guarantee any
specific operational outcome beyond the binding success criteria above.

## 11. Renewal Path

Stage 8 (Expand): **Sales Knowledge Assistant** (SAR 15K–60K), **Policy
Assistant** (SAR 20K–100K), or **Enterprise Company Brain** (per Enterprise
pricing).

## 12. Signatures

| For Dealix | For `{{customer_name_en}}` |
|------------|-----------------------------|
| Name: | Name: |
| Role: | Role: |
| Date: | Date: |
| Signature: | Signature: |
