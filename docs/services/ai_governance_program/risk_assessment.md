# AI Governance Program — Risk Assessment / تقييم المخاطر

Week-2 to Week-6 deliverable depending on tier. Owner: HoCS + HoLegal + customer's CTO/CIO + DPO. Output: a Saudi-specific risk register that combines AI tool inventory and data inventory into ranked risks with likelihood, impact (SAR), owner, and mitigation.

## Risk schema / مخطط الخطر

| Column / العمود | Type | Notes |
|---|---|---|
| `risk_id` | string | `risk_<short>_<seq>` |
| `risk_name_ar` | string | bilingual |
| `risk_name_en` | string | |
| `category` | enum | pdpl / sama / nca / sdaia / contractual / model_safety / vendor / shadow_ai / operational |
| `related_tools` | tool_id list | from `ai_tool_inventory.md` |
| `related_datasets` | dataset_id list | from `data_inventory.md` |
| `likelihood` | enum | rare / unlikely / possible / likely / almost_certain |
| `impact_sar_estimate` | float | quantified or "structural" if unbounded |
| `impact_description` | string | bilingual |
| `inherent_score` | int | 1–25 (5 x 5 matrix before mitigation) |
| `mitigation` | string | the action plan |
| `residual_score` | int | 1–25 after mitigation |
| `owner` | email | accountable role |
| `target_close_date` | ISO date | |
| `monitoring_method` | string | how the risk is observed in production |
| `evidence_pointer` | url/path | where the evidence lives (audit log, ticket, doc) |

## Risk categories — Saudi-specific lens / المنظور السعودي

### PDPL (Personal Data Protection Law)
- Lawful basis missing (PDPL Art. 5).
- Transparency notice missing (PDPL Art. 13).
- Consent for sensitive data missing (PDPL Art. 14).
- Cross-border transfer without safeguards.
- DSR > 72h response time.
- Breach notification > 72h to NDMO.

### SAMA / NCA (where applicable to BFSI)
- AI in credit / fraud decisions without explainability documentation.
- Outsourcing without prior SAMA notification.
- Model governance gaps under SAMA Cybersecurity Framework.

### SDAIA / National AI Authority
- High-risk AI use without registered governance.
- Foundation model in customer-facing flow without provenance documentation.

### Model safety / agent risk
- Prompt-injection risk on customer-facing assistants.
- Hallucination risk where "no source = no answer" is not enforced.
- Autonomous external action risk (e.g., autosend) — must route through approval matrix.

### Vendor / shadow-AI risk
- Sub-processor not disclosed.
- Vendor without DPA.
- Shadow tool not under approval matrix.

### Operational / contractual
- Audit log gaps.
- Inability to evidence right-to-erasure.
- Open items from `docs/legal/enterprise_risk_register.md`.

## Scoring rubric / قواعد التقييم

| Likelihood x Impact | 1 (negligible) | 2 (minor) | 3 (moderate) | 4 (major) | 5 (severe) |
|---|---|---|---|---|---|
| 1 (rare) | 1 | 2 | 3 | 4 | 5 |
| 2 (unlikely) | 2 | 4 | 6 | 8 | 10 |
| 3 (possible) | 3 | 6 | 9 | 12 | 15 |
| 4 (likely) | 4 | 8 | 12 | 16 | 20 |
| 5 (almost certain) | 5 | 10 | 15 | 20 | 25 |

- Score 16–25 -> escalate to CEO + board within 24 hours of finding.
- Score 9–15 -> mitigation plan within 30 days.
- Score 4–8 -> mitigation plan within 90 days.
- Score 1–3 -> monitor.

## Output artifacts / المخرجات
- `<customer>_risk_register_<YYYYMMDD>.csv` (the canonical register).
- Bilingual narrative summary (6–12 pages) with top 12 risks and recommended approvals.
- Heatmap (likelihood x impact) plotted by category.
- Board-briefing deck (8 slides) for enterprise tier.

## Gates / بوابات
- [ ] PDPL Art. 13/14 risks identified and owned.
- [ ] Every score-16+ risk has an owner + target close date.
- [ ] Cross-reference with `docs/legal/enterprise_risk_register.md` reconciled (no contradictions).
- [ ] Customer sponsor signs the register.

## Cross-links / روابط ذات صلة
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Audit requirements: `docs/services/ai_governance_program/audit_requirements.md`
- Enterprise risk register: `docs/legal/enterprise_risk_register.md`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- PDPL breach response: `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- Cross-border transfer addendum: `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`
- Compliance OS risk engine: `auto_client_acquisition/compliance_os/risk_engine.py`
- Agent governance policy: `auto_client_acquisition/agent_governance/policy.py`
