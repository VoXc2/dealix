# AI Governance Program — Data Inventory / جرد البيانات

Week-1 to Week-4 deliverable. Owner: HoCS + customer's DPO. Output: a ROPA-aligned (Record of Processing Activities) CSV + a bilingual narrative report listing every dataset, data flow, and processing activity that touches AI tooling.

## Inventory schema / مخطط الجرد

| Column / العمود | Type | Notes |
|---|---|---|
| `dataset_id` | string | stable identifier (`ds_<short>_<seq>`) |
| `dataset_name` | string | display name |
| `system_of_record` | string | CRM, ERP, ticketing, lakehouse, custom DB |
| `data_categories` | enum list | identity / contact / financial / health / employment / device / behavioural / sensitive |
| `volume_records` | int | rough count |
| `volume_growth_per_month` | int | |
| `data_subjects` | enum list | customers / employees / vendors / leads / minors |
| `lawful_basis` | enum | contract / consent / legitimate_interest / legal_obligation / public_task (PDPL Art. 5) |
| `purpose_ar` | string | bilingual purpose statement |
| `purpose_en` | string | |
| `retention_days` | int | aligns with `docs/DATA_RETENTION_POLICY.md` |
| `storage_location` | enum | ksa / gcc / us / eu / multi |
| `cross_border_transfer` | bool | triggers `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` |
| `consumer_ai_tools` | tool_id list | links to `ai_tool_inventory.md` |
| `pii_class` | enum | none / hashed / identifiable / sensitive |
| `dpo_owner` | email | accountable per record |
| `last_audit_date` | ISO date | |
| `dsr_route` | string | how a data subject request is fulfilled |

**No row without `dataset_id`, `data_categories`, `lawful_basis`, `pii_class`, `dpo_owner`.** This is the data-inventory gate.

## Sources / مصادر التجميع
1. DPO interview + existing ROPA (if any).
2. Database catalog scan (Snowflake / BigQuery / Postgres / S3 buckets).
3. Integration map (existing `docs/INTEGRATION_CONTRACT_MAP.md` style document).
4. Privacy notices / consent banners (customer-facing surfaces).
5. Cross-reference with `ai_tool_inventory.md` to ensure every AI tool maps to declared data sources.

## PDPL alignment / المواءمة مع نظام حماية البيانات
- **PDPL Art. 5 — Lawful basis** captured per dataset.
- **PDPL Art. 13** — transparency notice text drafted for any customer-facing flow.
- **PDPL Art. 14** — explicit consent posture documented for identifiable or sensitive PII.
- **PDPL Art. 18-21** — DSR routes (access / correction / erasure / objection) defined per dataset.
- Cross-border transfers flagged for assessment against the Saudi Data & AI Authority (SDAIA) guidance.

## Cross-references / إحالات متبادلة

| Concern | Source doc |
|---|---|
| Retention rules | `docs/DATA_RETENTION_POLICY.md` |
| Cross-border transfer | `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` |
| Breach response | `docs/PDPL_BREACH_RESPONSE_PLAN.md` |
| DSR templates | `docs/legal/DSAR_RESPONSE_TEMPLATES.md` |
| Sub-processors | `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md` |
| DPA template | `docs/legal/DPA_TEMPLATE_AR.md` |
| Consent ledger module | `auto_client_acquisition/compliance_os/consent_ledger.py` |
| ROPA module | `auto_client_acquisition/compliance_os/ropa.py` |
| Data-subject-request module | `auto_client_acquisition/compliance_os/data_subject_requests.py` |

## Output artifacts / المخرجات
- `<customer>_data_inventory_<YYYYMMDD>.csv`
- ROPA-aligned narrative report (8–14 pages bilingual).
- Data-flow diagrams: one per BU + a master map.
- Linkage spreadsheet: dataset_id <-> tool_id from `ai_tool_inventory.md`.

## Compliance gates / بوابات الامتثال
- [ ] Every dataset has a lawful basis (PDPL Art. 5).
- [ ] Customer-facing flows carry PDPL Art. 13/14 notice text.
- [ ] Cross-border transfers acknowledged or remediated.
- [ ] DSR < 72-hour SLA route confirmed per dataset.
- [ ] Sub-processors disclosed and DPAs on file.

## Cross-links / روابط ذات صلة
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Data governance: `docs/trust/data_governance.md`
- Privacy readiness: `docs/PRIVACY_PDPL_READINESS.md`
- Compliance OS module: `auto_client_acquisition/compliance_os/`
