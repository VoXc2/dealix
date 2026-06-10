# Commercial Agent Output Contract — عقد مخرجات الوكلاء التجاريين
**Dealix — Agent #3**

> **الغرض:** ما الذي يخرجه كل agent، بأي format، لأي consumer، مع أي approval. يضمن الاتساق.

---

## 1. Output Principles

### 1.1 The 5 C's
- **Consistent:** نفس format دائماً
- **Clear:** لا غموض
- **Complete:** كل الحقول المطلوبة
- **Compatible:** يحترم schemas
- **Citable:** كل claim له source

### 1.2 Standard Format
- YAML or JSON where structured
- Markdown where narrative
- Founder approval for external

---

## 2. Per-Agent Output Contract

### 2.1 CCO Strategy Agent

**Outputs:**
- Strategy update drafts (markdown)
- Motion rotation suggestions
- Focus override YAML
- KPI registry suggestions

**Format:** Markdown + YAML
**Schema:** `dealix/transformation/commercial_focus_override.yaml`
**Approval:** founder (L2)
**Consumer:** founder, CCO, board

**Sample:**
```yaml
- strategy_update_id: "su_2026_001"
- focus_change: "increase_marketing_agency_focus"
- rationale: "..."
- impact: "..."
- approval_required: L2
```

### 2.2 ICP Agent

**Outputs:**
- Lead scores (JSON)
- ICP segment updates (YAML)
- Persona recommendations
- Disqualification flags

**Format:** JSON + YAML
**Schema:** `schemas/icp.schema.json`, `schemas/buyer_persona.schema.json`
**Approval:** L1 (score), L2 (segment), L3 (disqualifier)
**Consumer:** Discovery, Proposal, CS

**Sample:**
```yaml
- lead_score: 16
- tier: "qualified_A"
- segment: "marketing_agency"
- persona: "agency_owner"
- disqualifier: "spam_indicator" # or "none"
```

### 2.3 Offer Catalog Agent

**Outputs:**
- Offer recommendations
- Pain-to-offer matches
- Catalog updates

**Format:** JSON + YAML
**Schema:** `schemas/product_offer.schema.json`, `data/commercial/product_catalog.yaml`
**Approval:** L2 (update), L3 (add/remove)
**Consumer:** Proposal, Discovery, Sales

**Sample:**
```yaml
- recommended_offer: "follow_up_recovery_workflow"
- confidence: "high"
- evidence_level: 2
- next_action: "schedule_workflow_design"
```

### 2.4 Pricing Guard Agent

**Outputs:**
- Pricing validations
- Approval routing
- Discount flags
- Margin warnings

**Format:** JSON
**Schema:** `schemas/pricing_rule.schema.json`
**Approval:** L1 (auto) → L2+ (founder)
**Consumer:** Proposal, Sales, Renewal

**Sample:**
```json
{
  "quote_id": "q_001",
  "valid": true,
  "approval_level": "L2",
  "margin_floor_ok": true,
  "warnings": [],
  "next": "founder_review"
}
```

### 2.5 Discovery Agent

**Outputs:**
- Discovery notes (JSONL)
- Call summaries
- Pain confirmation
- Next step recommendation

**Format:** JSONL
**Schema:** `schemas/discovery_note.schema.json`
**Approval:** L1 (note), L2 (next step)
**Consumer:** Proposal, Sales

**Sample:**
```json
{
  "id": "disc_001",
  "opportunity_id": "opp_001",
  "pain_categories": {"primary": "follow_up_chaos"},
  "pain_severity": "high",
  "next_step": "send_proposal",
  "approval_required": "L1"
}
```

### 2.6 Proposal Agent

**Outputs:**
- Proposal drafts (Markdown)
- Quote documents
- Approval routing
- Win/loss tracking

**Format:** Markdown + JSON
**Schema:** `schemas/commercial_proposal.schema.json`
**Approval:** L1-L5 (per quote)
**Consumer:** Client, Sales, CS

**Sample:**
```yaml
- proposal_id: "prop_001"
- opportunity_id: "opp_001"
- offer_id: "follow_up_recovery_workflow"
- price_sar: 12000
- approval_level: L1
- founder_approved: false
- valid_until: "2026-06-17"
```

### 2.7 Proof Pack Agent

**Outputs:**
- Proof packs (PDF/Markdown)
- Case studies (L4-L5)
- Anonymized examples
- ROI estimates (with is_estimate)

**Format:** PDF + JSON metadata
**Schema:** `schemas/commercial_proof_pack.schema.json`
**Approval:** L1 (L1-L2 evidence), L2 (L3), L3+ (L4-L5)
**Consumer:** Sales, CS, Marketing

**Sample:**
```json
{
  "id": "proof_001",
  "client_name": "Anonymized",
  "is_anonymized": true,
  "evidence_level": 2,
  "results": [{"metric": "leakage_reduction", "value": "30%", "is_estimate": true}]
}
```

### 2.8 Objection Agent

**Outputs:**
- Objection matches
- Response suggestions
- Pattern tracking
- Bank updates

**Format:** YAML + Markdown
**Schema:** `data/commercial/objections.yaml`
**Approval:** L1 (match), L2 (response), L3 (policy)
**Consumer:** Sales, Discovery, Proposal

**Sample:**
```yaml
- objection_id: "obj_price_too_high"
- matched: true
- response: "..."
- offer_to_suggest: "smaller_tier"
- risk_level: low
```

### 2.9 Partner Channel Agent

**Outputs:**
- Partner pipeline (JSONL)
- Performance reports
- Margin suggestions
- Termination recommendations

**Format:** JSONL + Markdown
**Schema:** `schemas/partner_opportunity.schema.json`
**Approval:** L2 (qualify), L3 (margin), L5 (white-label)
**Consumer:** founder, Sales

**Sample:**
```yaml
- partner_id: "partner_acme"
- opportunity_id: "popp_001"
- stage: "active"
- model: "referral"
- commission_pct: 15
```

### 2.10 Customer Success Agent

**Outputs:**
- Health scores (JSONL)
- Weekly reports (Markdown)
- Onboarding checklists
- Escalation alerts

**Format:** JSONL + Markdown
**Schema:** `schemas/client_health.schema.json`
**Approval:** L1 (report), L2 (escalation), L3 (termination)
**Consumer:** Client, CS, Renewal

**Sample:**
```yaml
- health_id: "health_001"
- client_id: "client_001"
- total: 82
- tier: "green"
- next_action: "continue_normal_cadence"
```

### 2.11 Renewal Agent

**Outputs:**
- Renewal drafts (Markdown)
- Expansion pitches
- Churn risk alerts
- Renewal forecast

**Format:** Markdown + JSON
**Approval:** L2 (terms), L3 (discount), L3 (termination)
**Consumer:** Client, Sales, CS

**Sample:**
```yaml
- renewal_id: "renew_001"
- client_id: "client_001"
- new_end: "2027-09-01"
- pricing_change: "none"
- expansion: true
- approval_level: L2
```

### 2.12 Finance Agent

**Outputs:**
- Revenue reports (Markdown)
- Margin analysis
- Runway forecast
- KPI updates

**Format:** Markdown + YAML
**Schema:** `dealix/transformation/kpi_founder_commercial_registry.yaml`
**Approval:** L1 (report), L2 (KPI update)
**Consumer:** founder, board

**Sample:**
```yaml
- period: "2026-05"
- revenue_total: TBD
- mrr_change: TBD
- runway_months: TBD
- is_estimate: false
- approval_required: L1
```

### 2.13 Commercial Risk Agent

**Outputs:**
- Risk register (YAML)
- Walk-away recommendations
- Compliance alerts
- Crisis alerts

**Format:** YAML
**Schema:** `dealix/transformation/risk_register.yaml` (existing)
**Approval:** L2 (add), L3 (walk-away), founder (crisis)
**Consumer:** founder, Compliance, Legal

**Sample:**
```yaml
- risk_id: "risk_001"
- category: "spam_request"
- severity: critical
- probability: low
- action: "hard_disqualify"
- status: open
```

### 2.14 Commercial Metrics Agent

**Outputs:**
- Daily command (Markdown)
- Weekly review (Markdown)
- Monthly close
- Cohort analysis

**Format:** Markdown
**Approval:** L1 (auto)
**Consumer:** founder, ops

**Sample:**
```markdown
# Daily Command
- Pipeline: TBD SAR
- Proposals: 3
- Founder decisions: 1
```

---

## 3. Cross-Cutting Standards

### 3.1 Approval
- All outputs that affect clients: founder approval
- All outputs that change policy: founder + L2+
- All internal reports: L1 (auto)

### 3.2 Audit
- Every output logged
- Date, time, agent, action
- Approval chain

### 3.3 Versioning
- v1, v2, v3...
- draft, review, approved, sent
- Locked after approval

### 3.4 Storage
- `data/commercial/` for commercial data
- `data/partners/` for partner data
- `data/customer_success/` for CS data
- `reports/commercial/` for reports

---

## 4. Schema Validation

### 4.1 Every Output
- ✅ Valid against schema
- ✅ All required fields
- ✅ Correct types
- ✅ Within enums

### 4.2 Tests
- `tests/test_commercial_*.py`
- Schema validation
- Field presence
- Approval chain

---

## 5. Output Rejection

### 5.1 If Rejected
- Document reason
- Return to agent
- Revise or escalate
- Update pattern

### 5.2 If Recurring
- Update agent
- Update policy
- Update contract

---

## 6. Companion Files

- Roles: `COMMERCIAL_AGENT_ROLES_AR.md`
- Permissions: `COMMERCIAL_AGENT_PERMISSION_MATRIX_AR.md`
- Existing: `dealix/config/agent_permissions.yaml`
- Existing: `dealix/contracts/schemas/`
- All `schemas/commercial_*.schema.json`

---

**Output contract = guarantee. كل agent = نفس format. كل format = schema. كل schema = test. founder يستلم، العميل يثق، النظام يحمي.**
