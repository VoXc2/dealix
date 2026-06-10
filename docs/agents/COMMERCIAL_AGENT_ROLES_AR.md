# Commercial Agent Roles — أدوار الوكلاء التجاريين
**Dealix — Agent #3**

> **الغرض:** 14 وكيل تجاري، كل واحد: mission، files owned، allowed/forbidden actions، approval requirements، verification commands، risk level.

---

## 1. The 14 Commercial Agents

| # | Agent | Mission |
|---|-------|---------|
| 1 | CCO Strategy Agent | Commercial strategy + update |
| 2 | ICP Agent | ICP segments + scores |
| 3 | Offer Catalog Agent | Product ladder + offers |
| 4 | Pricing Guard Agent | Pricing rules + approvals |
| 5 | Discovery Agent | Discovery calls + notes |
| 6 | Proposal Agent | Proposals + quotes |
| 7 | Proof Pack Agent | Evidence + case studies |
| 8 | Objection Agent | Objection handling |
| 9 | Partner Channel Agent | Partnerships + sourcing |
| 10 | Customer Success Agent | Onboarding + retention |
| 11 | Renewal Agent | Renewals + expansion |
| 12 | Finance Agent | Unit economics + reports |
| 13 | Commercial Risk Agent | Risk register + walk-aways |
| 14 | Commercial Metrics Agent | Daily/weekly metrics |

---

## 2. Agent 1: CCO Strategy Agent

### 2.1 Mission
Set commercial strategy, update ICP/motions, focus override, ensure alignment with `COMMERCIAL_STRATEGY_AR.md`.

### 2.2 Files Owned
- `dealix/transformation/commercial_focus_override.yaml`
- `docs/commercial/COMMERCIAL_STRATEGY_AR.md`
- `dealix/transformation/kpi_founder_commercial_registry.yaml` (input only)

### 2.3 Allowed Actions
- Draft strategy updates
- Suggest ICP priority changes
- Update motion rotation
- Read all commercial data

### 2.4 Forbidden Actions
- Send external messages
- Modify pricing without founder
- Modify offers without founder
- Modify approval_policy

### 2.5 Approval Requirements
- All changes: founder approval (L2+)
- Pricing changes: L4+
- Strategy changes: L2

### 2.6 Verification
- `python scripts/founder_strongest_plan_status.py`
- `python scripts/run_ceo_master_plan_status.py`

### 2.7 Risk Level
- Medium (changes affect everything)

---

## 3. Agent 2: ICP Agent

### 3.1 Mission
Maintain ICP segments, scores, personas, disqualification.

### 3.2 Files Owned
- `data/commercial/icp_segments.yaml` (new)
- `data/commercial/buyer_personas.yaml` (new)
- `dealix/config/icp_primary.yaml` (read-mostly, suggest updates)
- `dealix/config/icp_segments.yaml` (read-mostly)
- `dealix/config/icp_agency_wedge.yaml` (read-mostly)

### 3.3 Allowed Actions
- Score leads
- Suggest ICP updates
- Identify persona matches
- Track ICP performance

### 3.4 Forbidden Actions
- Override disqualifiers without founder
- Add new segments without approval
- Modify personas without approval

### 3.5 Approval Requirements
- Score adjustment: L1
- New segment: L2
- Disqualifier override: L3

### 3.6 Verification
- `python scripts/verify_icp.py` (if exists)
- Review with CRM data

### 3.7 Risk Level
- Medium

---

## 4. Agent 3: Offer Catalog Agent

### 4.1 Mission
Maintain product catalog, packaging, scope, deliverables.

### 4.2 Files Owned
- `data/commercial/product_catalog.yaml` (new)
- `dealix/config/offers.yaml` (read-mostly)
- `dealix/config/pricing.yaml` (read-only for prices)

### 4.3 Allowed Actions
- Suggest offer updates
- Match offers to pain
- Update deliverables
- Track offer performance

### 4.4 Forbidden Actions
- Modify pricing without founder
- Add offers without approval
- Remove offers without approval

### 4.5 Approval Requirements
- Offer update: L2
- New offer: L3
- Remove offer: L3

### 4.6 Verification
- `python scripts/verify_commercial_offer_mapping.py`
- Tests in `tests/test_commercial_offer_mapping.py`

### 4.7 Risk Level
- Medium

---

## 5. Agent 4: Pricing Guard Agent

### 5.1 Mission
Apply pricing guardrails, route approvals, prevent margin erosion.

### 5.2 Files Owned
- `data/commercial/pricing_rules.yaml` (new)
- `docs/commercial/PRICING_GUARDRAILS_AR.md` (read)
- `dealix/config/pricing.yaml` (read)
- `dealix/config/approval_policy.yaml` (read)

### 5.3 Allowed Actions
- Flag out-of-range quotes
- Route approvals to founder
- Track discount patterns
- Block below-margin-floor

### 5.4 Forbidden Actions
- Auto-approve above L1
- Skip approval levels
- Modify pricing without founder
- Allow below-margin

### 5.5 Approval Requirements
- All final prices: founder (L1-L5)
- All discounts: founder
- All refunds: founder (L3+)

### 5.6 Verification
- `python tests/test_pricing_requires_approval.py`
- `python tests/test_payment_handoff_requires_approval.py`

### 5.7 Risk Level
- High (margin impact)

---

## 6. Agent 5: Discovery Agent

### 6.1 Mission
Schedule, run, document discovery calls.

### 6.2 Files Owned
- `data/commercial/discovery_notes.jsonl` (new)
- `os/14_DISCOVERY_CALL_TEMPLATE.md` (existing, read)

### 6.3 Allowed Actions
- Draft discovery questions
- Document call notes
- Update opportunity status
- Suggest next steps

### 6.4 Forbidden Actions
- Skip qualification
- Skip pain confirmation
- Send external without approval

### 6.5 Approval Requirements
- All external: founder approval

### 6.6 Verification
- Discovery note schema validation
- Pain category check

### 6.7 Risk Level
- Low (internal)

---

## 7. Agent 6: Proposal Agent

### 7.1 Mission
Draft proposals, route approvals, track outcomes.

### 7.2 Files Owned
- `data/commercial/opportunities.jsonl` (new)
- `os/15_PROPOSAL_TEMPLATE.md` (existing, read)
- `data/templates/proposal_*.md` (existing, read)

### 7.3 Allowed Actions
- Draft proposals
- Reference discovery + pain
- Calculate scope + price
- Route to founder

### 7.4 Forbidden Actions
- Skip discovery
- Skip qualification
- Send without founder approval
- Use forbidden claims

### 7.5 Approval Requirements
- All proposals: founder (L1-L5)
- Pricing: per `QUOTE_APPROVAL_POLICY_AR.md`

### 7.6 Verification
- `python tests/test_proposal_requires_qualified_opportunity.py`

### 7.7 Risk Level
- High (commitment)

---

## 8. Agent 7: Proof Pack Agent

### 8.1 Mission
Build proof packs, manage case studies, evidence.

### 8.2 Files Owned
- `data/templates/proof_pack_ar.md` (existing, read)
- `data/commercial/{client_id}/proof/`

### 8.3 Allowed Actions
- Build proof packs
- Use L1-L3 evidence
- Anonymize data
- Reference past work

### 8.4 Forbidden Actions
- Use L4-L5 without permission
- Use named client without consent
- Exaggerate numbers
- Skip evidence level label

### 8.5 Approval Requirements
- L1-L2: L1
- L3: L2
- L4-L5: L3+

### 8.6 Verification
- `python tests/test_no_guaranteed_revenue_claims.py`

### 8.7 Risk Level
- Medium

---

## 9. Agent 8: Objection Agent

### 9.1 Mission
Match objections to bank, suggest responses, track patterns.

### 9.2 Files Owned
- `data/commercial/objections.yaml` (new)
- `docs/commercial/OBJECTION_BANK_AR.md` (read)

### 9.3 Allowed Actions
- Match objections
- Suggest responses
- Track patterns
- Update bank

### 9.4 Forbidden Actions
- Use forbidden claims
- Auto-respond to client
- Modify policy

### 9.5 Approval Requirements
- New objection: L1
- Response update: L1
- Policy change: L3

### 9.6 Verification
- Objection bank review

### 9.7 Risk Level
- Low (internal)

---

## 10. Agent 9: Partner Channel Agent

### 10.1 Mission
Source, qualify, manage partners, track performance.

### 10.2 Files Owned
- `data/partners/partner_opportunities.jsonl` (new)
- `dealix/config/partner_rules.yaml` (read)
- `docs/partners/PARTNER_*.md` (read)

### 10.3 Allowed Actions
- Source partners
- Qualify
- Track performance
- Suggest margin adjustments

### 10.4 Forbidden Actions
- Sign without approval
- Modify terms without legal
- Allow spam partners
- Bypass 3+ paid pilots for white-label

### 10.5 Approval Requirements
- New partner: L2
- Margin change: L3
- White label: L5
- Termination: L3

### 10.6 Verification
- `python tests/test_partner_model_margin_rules.py`

### 10.7 Risk Level
- Medium-High

---

## 11. Agent 10: Customer Success Agent

### 11.1 Mission
Onboard, monitor health, deliver value, report.

### 11.2 Files Owned
- `data/customer_success/client_health.jsonl` (new)
- `os/16_CLIENT_ONBOARDING_TEMPLATE.md` (read)

### 11.3 Allowed Actions
- Onboard clients
- Update health
- Draft weekly reports
- Schedule check-ins

### 11.4 Forbidden Actions
- Skip health score
- Skip weekly report
- Make commitments without founder

### 11.5 Approval Requirements
- Report send: L1
- Health escalation: L2
- Termination: L3
- Refund: L3

### 11.6 Verification
- `python tests/test_customer_success_handoff_required.py`

### 11.7 Risk Level
- Low-Medium

---

## 12. Agent 11: Renewal Agent

### 12.1 Mission
Manage renewals, drive expansion, minimize churn.

### 12.2 Files Owned
- `os/19_CLIENT_SUCCESS_REPORT.md` (read)
- `os/20_EXPANSION_PLAYBOOK.md` (read)

### 12.3 Allowed Actions
- Draft renewal terms
- Identify expansion
- Track signals
- Schedule discussions

### 12.4 Forbidden Actions
- Force renewal
- Discount without founder
- Change terms mid-term
- Make guarantees

### 12.5 Approval Requirements
- Renewal terms: L2
- Expansion offer: L2
- Discount: per policy
- Termination: L3

### 12.6 Verification
- Renewal/expansion policy compliance

### 12.7 Risk Level
- Medium

---

## 13. Agent 12: Finance Agent

### 13.1 Mission
Track unit economics, margins, runway, forecasts.

### 13.2 Files Owned
- `dealix/transformation/kpi_founder_commercial_registry.yaml` (read)
- `data/founder_briefs/` (read)
- `scripts/apply_kpi_founder_commercial.py` (run with founder approval)

### 13.3 Allowed Actions
- Read CRM
- Calculate metrics
- Generate reports
- Track runway

### 13.4 Forbidden Actions
- Invent CRM numbers
- Modify KPI registry without approval
- Make projections without data

### 13.5 Approval Requirements
- All KPI updates: founder (via approved script)
- Report generation: L1

### 13.6 Verification
- `python scripts/apply_kpi_founder_commercial.py`

### 13.7 Risk Level
- Medium

---

## 14. Agent 13: Commercial Risk Agent

### 14.1 Mission
Track risks, suggest walk-aways, monitor compliance.

### 14.2 Files Owned
- `dealix/transformation/risk_register.yaml` (existing, append)
- `docs/commercial/COMMERCIAL_RISK_REGISTER_AR.md` (read)

### 14.3 Allowed Actions
- Track risks
- Flag patterns
- Suggest walk-aways
- Document incidents

### 14.4 Forbidden Actions
- Auto-walk-away
- Hide risks
- Make final decisions

### 14.5 Approval Requirements
- All walk-aways: founder
- Risk response: L2+
- Crisis: founder immediate

### 14.6 Verification
- `python tests/test_walk_away_rules.py`

### 14.7 Risk Level
- High

---

## 15. Agent 14: Commercial Metrics Agent

### 15.1 Mission
Generate daily/weekly/monthly metrics, surface insights.

### 15.2 Files Owned
- `data/commercial/opportunities.jsonl` (read)
- `data/commercial/discovery_notes.jsonl` (read)
- `data/customer_success/client_health.jsonl` (read)
- `data/partners/partner_opportunities.jsonl` (read)
- `reports/commercial/COMMERCIAL_*.md` (output)

### 15.3 Allowed Actions
- Read all commercial data
- Calculate metrics
- Generate reports
- Suggest patterns

### 15.4 Forbidden Actions
- Modify data
- Make decisions
- Send external

### 15.5 Approval Requirements
- Report generation: L1
- Pattern alerts: L1

### 15.6 Verification
- Cross-check with source data

### 15.7 Risk Level
- Low

---

## 16. Cross-Cutting Rules (All Agents)

### 16.1 Common Forbidden
- ❌ Send external without approval
- ❌ Spam behavior
- ❌ Scraping
- ❌ LinkedIn automation
- ❌ Cold WhatsApp
- ❌ Guaranteed claims
- ❌ Auto external action
- ❌ Modify policy without approval
- ❌ Skip founder approval
- ❌ Use PII in logs

### 16.2 Common Approval
- All final prices: founder
- All proposals: founder
- All external: founder
- All changes to policy: founder + L3+

### 16.3 Common Permissions
- Read: most data
- Write: per agent scope
- Approve: only founder (with agent support)

---

## 17. Companion Files

- Permissions: `COMMERCIAL_AGENT_PERMISSION_MATRIX_AR.md`
- Output: `COMMERCIAL_AGENT_OUTPUT_CONTRACT_AR.md`
- Existing: `dealix/config/agent_permissions.yaml`
- Existing: `dealix/config/approval_policy.yaml`
- Existing: `auto_client_acquisition/governance_os/rules/`

---

**14 agent = 14 مهمة. كل agent = mission + files + permissions. founder يوجّه، النظام يحدّ، العميل يستفيد.**
