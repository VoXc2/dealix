# AI Governance Program — AI Tool Inventory / جرد أدوات الذكاء الاصطناعي

Week-1 to Week-3 deliverable. Owner: HoCS + customer's CTO/CIO sponsor. Output: a CSV + a bilingual narrative report that lists every AI tool, model, and internal agent in active or shadow use across the customer's organization.

## Inventory schema / مخطط الجرد

| Column / العمود | Type | Notes |
|---|---|---|
| `tool_id` | string | stable identifier (`tool_<short>_<seq>`) |
| `tool_name` | string | display name (Claude, GPT-4o, internal "sales_drafter", ...) |
| `vendor` | enum | anthropic / openai / google / meta / aws_bedrock / internal / open_source / other |
| `category` | enum | foundation_model / agent / rag / embedding / classifier / vision / voice / other |
| `business_unit` | string | which BU uses it |
| `business_owner` | email | accountable person |
| `tech_owner` | email | accountable engineer |
| `is_customer_facing` | bool | does output reach an external party? |
| `pii_touched` | enum | none / hashed / identifiable / sensitive |
| `data_residency` | enum | ksa / gcc / us / eu / unknown |
| `lawful_basis` | enum | contract / consent / legitimate_interest / public_task |
| `evidence_level_required` | int | 0–5 (L0–L5), matches `dealix/trust/approval_matrix.py` |
| `approval_role` | enum | auto / csm / ae / head_cs / head_legal / cto / ceo |
| `contract_status` | enum | signed / pending / shadow / unknown |
| `monthly_spend_sar` | float | billed cost |
| `risk_score` | int | from `risk_assessment.md` |
| `last_reviewed` | ISO date | program ratification date |

**No row without `tool_name`, `vendor`, `business_owner`, `tech_owner`, `pii_touched`, and `data_residency`.** This is the inventory gate — partial entries are flagged and surfaced to the sponsor.

## Sources / مصادر التجميع
1. CTO / CIO interview (45 min) — declared inventory.
2. Finance vendor list (extract recurring AI vendor charges).
3. SSO directory (apps logged into by employees).
4. Browser / endpoint extension scan (optional, with customer consent).
5. Self-report survey to all team leads (anonymous shadow-AI declaration).
6. Code-repo scan for SDK imports (`anthropic`, `openai`, `google-generativeai`, etc.).

## Shadow-AI handling / التعامل مع الأدوات غير المعتمدة
- Discovered shadow tools are logged with `contract_status = shadow`.
- Each is ranked by the risk model in `risk_assessment.md`.
- Disposition options: ratify (with contract + DPA) / migrate (to an approved vendor) / retire.
- Customer signs off on disposition before the inventory is closed.

## Compliance gates / بوابات الامتثال
- [ ] PDPL Art. 13 — transparency obligations covered for any tool with `is_customer_facing = true`.
- [ ] PDPL Art. 14 — explicit consent posture documented for tools touching `identifiable` or `sensitive` PII.
- [ ] Sub-processor obligations checked against `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md`.
- [ ] Vendor DPAs sighted for every contracted tool.
- [ ] Data-residency conflicts flagged to HoLegal.

## Output artifacts / المخرجات
- `<customer>_ai_tool_inventory_<YYYYMMDD>.csv`
- 6–10 page bilingual narrative report with: total tool count, vendor mix, BU mix, shadow-AI count, top 10 risks, disposition recommendations.
- Linkage spreadsheet mapping each tool to one or more entries in `data_inventory.md`.

## Cross-links / روابط ذات صلة
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Approval matrix engine: `dealix/trust/approval_matrix.py`
- Vendor registry: `auto_client_acquisition/compliance_os/vendor_registry.py`
- Agent registry: `auto_client_acquisition/agent_governance/agent_registry.py`
- Enterprise risk register: `docs/legal/enterprise_risk_register.md`
- Sub-processor notification email: `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md`
