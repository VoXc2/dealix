# Company Brain Sprint — Data Request / طلب البيانات

Sent to the customer at end of Day-1 discovery. Sealed-credentials vault only for transfer. All artifacts encrypted at rest. Lawful basis (PDPL Art. 5 — contract) recorded. No source = no answer is a hard product rule — the customer must agree before ingest begins.

## Required document inventory / جرد المستندات المطلوب

A spreadsheet (one row per document or one row per folder) with these columns:

| Column / العمود | Type | Notes |
|---|---|---|
| `doc_title` | string | Human-readable, AR or EN. |
| `category` | enum | sales / hr / support / ops / policy / finance / legal |
| `owner_email` | string | SME who can answer questions about the doc. |
| `source_path` | string | URL, file share, or vault path. |
| `sensitivity` | enum | public / internal / restricted / pii |
| `last_modified` | ISO 8601 | Drives the >90-day freshness flag. |
| `intended_audience` | enum | admin / team / read_only |

**No row without these 7 columns. No document is indexed unless every column is filled.** This is enforced by the ingest gate.

## Recommended inputs / مفضّل

- 10 sample questions employees ask today (drives the eval set).
- Permissions matrix: role -> categories visible.
- Existing FAQ doc (if any) to seed common answers.
- Bilingual glossary if AR/EN terminology diverges.

## Optional inputs / اختياري

- Existing intranet search export (volume, top queries).
- Previous "where is that PDF?" tickets from Support.
- Department-specific abbreviations list.

## Document scope / نطاق المستندات

- Up to **500 documents** in base scope.
- Formats: PDF, DOCX, MD, KB articles, HTML.
- Each <= 50 MB.
- Overage: SAR 30 per additional document, capped at +500.

## Provenance & compliance rules / قواعد المصدر والامتثال

1. **No source = no answer.** The assistant refuses unless a qualifying source citation exists. Customer signs this rule at intake.
2. PII passes through `dealix/trust/pii_detector.py` BEFORE indexing. Findings are redacted in the index; originals retained per customer retention policy.
3. Sensitive-flagged docs go to the restricted access tier; verified across 3 personas in QA.
4. PDPL Art. 13/14 notices apply to any external delivery of an answer (e.g., to a customer-facing rep) — assistant adds the footer automatically.
5. Right-to-erasure: < 72 hours from request, removing the doc + all derived chunks + audit-log marker.

## Drop-off format / تسليم البيانات

- Inventory: `.xlsx` or `.csv` with all 7 columns.
- Documents: zipped archive uploaded to sealed vault. NEVER email.
- File name: `<customer>_brain_inventory_<YYYYMMDD>.csv`.

## Hard stops / حدود فاصلة

- Inventory < 7-column compliance -> ingest paused, request fix.
- Sensitive docs not flagged -> halt and rescope sensitivity audit (extra 2 days).
- Customer asks for answers without source citation -> reject; route to a non-RAG product.

## Cross-links

- Intake: `docs/services/company_brain_sprint/intake.md`
- Scope: `docs/services/company_brain_sprint/scope.md`
- PII detector: `dealix/trust/pii_detector.py`
- Audit module: `dealix/trust/audit.py`
- Data governance: `docs/trust/data_governance.md`
- PDPL readiness: `docs/PRIVACY_PDPL_READINESS.md`
- Company Brain module: `auto_client_acquisition/company_brain/`
