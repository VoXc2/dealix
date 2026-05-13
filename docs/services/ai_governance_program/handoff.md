# AI Governance Program — Stage-6 (Deliver) Handoff

Owner: HoCS + HoLegal. Duration: 60 minutes, recorded. End of program (Month 1, 2, or 3 depending on tier). Emit `delivery.handoff_completed` event. Audience: customer sponsor (CTO/CIO/COO), DPO, HoLegal, board observer if enterprise tier.

## Handoff Packet Contents / محتويات الحزمة

Sent to customer 48 hours BEFORE the session:

1. **AI tool inventory** (CSV + bilingual report) per `ai_tool_inventory.md`.
2. **Data inventory** (ROPA-aligned CSV + narrative) per `data_inventory.md`.
3. **Risk register** (CSV + bilingual summary + heatmap) per `risk_assessment.md`.
4. **AI usage policy** (bilingual, 12–25 pages, version 1.0) per `policy_template.md`.
5. **Approval matrix** (CSV + implementation diff vs `dealix/trust/approval_matrix.py` + negative/positive test suite) per `approval_matrix.md`.
6. **Audit-trail blueprint + first monthly evidence pack** per `audit_requirements.md`.
7. **Board-briefing deck** (8 slides) for enterprise tier.
8. **Training recording** (3 hours: staff + manager + board tracks).
9. **Regulator-inspection dossier index** with links to every artifact.
10. **30-day post-handoff runbook** (one tuning round + ongoing escalation path).
11. **Renewal proposal** — managed governance retainer (see below in upsell hooks).
12. **PDPL Art. 13/14 footers + acceptable-use checklist** ready to publish internally.

## Session Agenda — 60 minutes / جدول الاجتماع — 60 دقيقة

### 60–45 min — Program Outcomes / نتائج البرنامج (15 min)
- Walk the executive summary: tools inventoried, datasets mapped, risks ranked, policy published, matrix live.
- KPI summary table:
  - Number of AI tools in inventory.
  - Number of datasets in ROPA.
  - Top 12 risks with owners and target close dates.
  - Approval matrix coverage (% of action kinds matched to approvers).
  - Audit-log coverage (% of AI invocations covered).
  - PDPL readiness checklist score.

### 45–15 min — Working Session / جلسة عمل (30 min)
- Walk the AI usage policy version 1.0 with HoLegal and DPO.
- Demonstrate the approval matrix live: a positive test (dispatch with matched approver) and a negative test (block without approver).
- Demonstrate the audit-log query for a sample tool invocation.
- Walk the monthly evidence pack with the DPO.
- Walk the regulator-inspection dossier index — show the < 24h SLA path.

### 15–0 min — Adoption, Risk & Renewal / التبني والمخاطر والتجديد (15 min)
- 30-day adoption plan: training rollout, policy publication, vendor renewal cycle.
- Top-3 residual risks the board should track.
- Renewal pathways (a managed governance retainer; an enterprise extension; a follow-on PDPL audit).
- DPO contact + NDMO notification rehearsal (tabletop exercise option in renewal).
- NPS-style quick score.
- Schedule 14-day proof-pack review (Stage-7 Prove) and 90-day program audit.

## Roles in the Room / الأدوار
- Dealix: HoCS (lead), HoLegal, governance analyst, CRO if SOW >= SAR 75,000.
- Customer: sponsor (CTO/CIO/COO), DPO (required), HoLegal (required), board observer for enterprise tier.

## Definition of Done / تعريف الإنجاز
- All 12 packet artifacts acknowledged in writing.
- Approval matrix signed by HoLegal and CEO (or sponsor-of-CEO).
- AI usage policy published internally within 14 days of handoff.
- First monthly evidence pack scheduled.
- Renewal proposal opened in CRM as next stage.
- Recording uploaded to project room.

## Upsell hooks (renewal pathways) / محاور التجديد
- **Managed Governance Retainer — SAR 18,000–60,000 / month, 12-month commit.** Monthly evidence-pack production, quarterly risk-register refresh, on-demand regulator-inspection support.
- **Annual PDPL Audit — SAR 40,000–120,000, fixed.** Independent audit pass with remediation plan.
- **Tabletop & Incident Drill — SAR 25,000–80,000, 2–6 weeks.** NDMO breach-notification rehearsal, SAMA/NCA inspection simulation.
- **Policy & Compliance Assistant (Company Brain extension) — SAR 20,000–100,000, 28 days.** RAG-backed answer engine on top of the published policy and audit register.
- **Enterprise Governance Program — SAR 250,000+ / year.** Multi-jurisdiction (KSA + GCC + GDPR-touchpoints), board reporting cadence, named delivery team.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_governance_program/offer.md`
- Scope: `docs/services/ai_governance_program/scope.md`
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Policy template: `docs/services/ai_governance_program/policy_template.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Audit requirements: `docs/services/ai_governance_program/audit_requirements.md`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- Approval matrix engine: `dealix/trust/approval_matrix.py`
- Trust pack — data governance: `docs/trust/data_governance.md`
- Trust pack — incident response: `docs/trust/incident_response.md`
- Enterprise risk register: `docs/legal/enterprise_risk_register.md`
- PDPL breach response: `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
- Compliance OS module: `auto_client_acquisition/compliance_os/`
- Agent governance module: `auto_client_acquisition/agent_governance/`
