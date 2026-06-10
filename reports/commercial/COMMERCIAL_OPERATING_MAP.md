# Commercial Operating Map — خريطة النظام التشغيلي التجاري
**Dealix — Agent #3**

> **الغرض:** خريطة بصرية/نصية تربط كل وحدة تجارية بالوحدات الأخرى، والمالكين، والتدفقات، والأدوات. هذا الملف مكافئ نصي لـ diagram — مرجع لأي agent لفهم كيف تتكامل الأجزاء.

---

## 1. Layer Architecture (طبقات النظام التجاري)

```
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 7: COMMERCIAL CONTROL ROOM (PHASE 14)                        │
│   /[locale]/ops/commercial-control | daily/weekly commands         │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 6: COMMERCIAL METRICS & DECISIONS (PHASE 1 + 12)            │
│   Founder rhythm | Metrics | Finance models | Decision rules       │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 5: POST-SALE (PHASE 11)                                      │
│   Customer Success | Renewal | Expansion | Client Health            │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 4: SALES OPERATIONS (PHASE 6 + 7 + 8)                       │
│   Sales process | Discovery | Proposal | Proof Pack | Objections    │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 3: PRICING & COMMERCIAL OFFERS (PHASE 4 + 5)                │
│   Product ladder | Pricing guardrails | Discount policy            │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 2: MARKET TARGETING (PHASE 2 + 3)                            │
│   ICP matrix | Buyer personas | Pain-to-offer mapping               │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 1: POSITIONING (PHASE 1)                                     │
│   Strategy | One-liner | Wedge | Horizons | Differentiation         │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 0: CHANNELS & PARTNERSHIPS (PHASE 9 + 10)                   │
│   Inbound | Email warm | WhatsApp after-consent | LinkedIn manual   │
│   Partners | Referrals | Content | Press | Events                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Entity Relationship Map (كيانات النظام التجاري)

```
┌──────────┐
│  ICP     │ ── 1:N ──> ┌────────────┐
│ Segment  │            │   Buyer    │
└──────────┘            │  Persona   │
                        └────────────┘
                              │ 1:N
                              ↓
                        ┌────────────┐         ┌──────────────┐
                        │   Lead     │ ──N:1──>│   Pain       │
                        │ (Prospect) │         │   Signal     │
                        └────────────┘         └──────────────┘
                              │ 1:N                   │ 1:1
                              ↓                       ↓
                        ┌────────────┐         ┌──────────────┐
                        │Opportunity │ ──N:1──>│   Offer      │
                        │ (Pipeline) │         │  (Product)   │
                        └────────────┘         └──────────────┘
                              │                       │
                              │ 1:1                   │ 1:1
                              ↓                       ↓
                        ┌────────────┐         ┌──────────────┐
                        │ Discovery  │ ──N:1──>│   Pricing    │
                        │   Note     │         │   Rule       │
                        └────────────┘         └──────────────┘
                              │
                              ↓
                        ┌────────────┐         ┌──────────────┐
                        │ Proposal   │ ──N:1──>│  Proof Pack  │
                        └────────────┘         └──────────────┘
                              │ 1:1
                              ↓
                        ┌────────────┐
                        │  Payment   │ (approval-required)
                        │   Handoff  │
                        └────────────┘
                              │ 1:1
                              ↓
                        ┌────────────┐
                        │  Delivery  │ (handoff to delivery OS)
                        └────────────┘
                              │ 1:1
                              ↓
                        ┌────────────┐         ┌──────────────┐
                        │  Active    │ ──1:N──>│  Weekly      │
                        │  Client    │         │  Health      │
                        └────────────┘         └──────────────┘
                              │ 1:1                   │ 1:N
                              ↓                       ↓
                        ┌────────────┐         ┌──────────────┐
                        │  Renewal   │ ──N:1──>│  Expansion   │
                        │  Decision  │         │  Offer       │
                        └────────────┘         └──────────────┘
```

**Plus cross-cutting:**
```
┌──────────────┐         ┌──────────────┐
│  Channel     │ ──N:N──>│   Lead       │ (where they came from)
└──────────────┘         └──────────────┘

┌──────────────┐         ┌──────────────┐
│  Partner     │ ──N:N──>│ Opportunity  │ (partner-sourced)
└──────────────┘         └──────────────┘

┌──────────────┐         ┌──────────────┐
│  Risk        │ ──1:N──>│ Opportunity  │ (flagged risks)
└──────────────┘         └──────────────┘
```

---

## 3. Owner Map (المالك لكل وحدة)

```
                        FOUNDER
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   CCO Strategy      Pricing Guard       Legal/Compliance
        │                  │                  │
   ICP Agent        Discount Policy    Risk Register
   Offer Catalog    Margin Floor       PDPL Review
   Motions          Final Approval     Claim Policy
   Channels                                 
   Partner Strategy                        
        │                                  
        │                                  
   ┌────┴─────┬──────────┬──────────┐      
   │          │          │          │      
Sales Lead  CS Lead   Partner   Finance
   │          │          │          │
Discovery   Onboarding Partner   CAC/LTV
Pipeline    Health     Pipeline  Margin
Proposal    Renewal    Models    Unit Econ
Proof       Expansion   Enablement Cash
Objection   Weekly       Margin    Reporting
              Reports    Split
```

---

## 4. Tool Map (الأدوات المستخدمة)

| الوحدة | الأداة | المرجع |
|--------|--------|---------|
| ICP | `icp_primary.yaml`, `icp_segments.yaml`, `icp_agency_wedge.yaml` | PHASE 2 |
| Personas | `data/commercial/buyer_personas.yaml` | PHASE 2 |
| Pain Matrix | `data/commercial/pain_to_offer.yaml` | PHASE 3 |
| Offer Catalog | `data/commercial/product_catalog.yaml` + `offers.yaml` | PHASE 4 |
| Pricing Rules | `data/commercial/pricing_rules.yaml` + `pricing.yaml` | PHASE 5 |
| Opportunities | `data/commercial/opportunities.jsonl` | PHASE 6 |
| Discovery Notes | `data/commercial/discovery_notes.jsonl` | PHASE 6 |
| Proposals | `os/15_PROPOSAL_TEMPLATE.md` + schemas | PHASE 7 |
| Proof Packs | `data/templates/proof_pack_ar.md` + schemas | PHASE 7 |
| Objections | `data/commercial/objections.yaml` | PHASE 8 |
| Channels | `CHANNEL_STRATEGY_AR.md` + child docs | PHASE 9 |
| Partners | `partner_rules.yaml` + `data/partners/partner_opportunities.jsonl` | PHASE 10 |
| Client Health | `data/customer_success/client_health.jsonl` | PHASE 11 |
| Finance | reports + approved registries | PHASE 12 |
| Risks | `COMMERCIAL_RISK_REGISTER_AR.md` | PHASE 13 |
| Control Room | `/[locale]/ops/commercial-control` | PHASE 14 |
| Tests | `tests/test_commercial_*.py` | PHASE 15 |
| Agents | `docs/agents/COMMERCIAL_AGENT_ROLES_AR.md` | PHASE 16 |

---

## 5. Decision Flow Map (تدفقات القرار)

### 5.1 Lead Decision Flow
```
New Lead
   ↓
[ICPScoringAgent] (uses icp_primary.yaml)
   ↓
score >= 15 → qualified_A
score >= 10 → qualified_B
score >= 6  → nurture
score < 6   → disqualify
   ↓
qualified_A/B
   ↓
[Channel Owner] (manual or warm)
   ↓
Discovery Scheduled
   ↓
[Discovery Agent]
   ↓
Discovery Done
   ↓
Pain Confirmed? ──No──> Disqualify or Nurture
   ↓ Yes
Product Match? ──No──> Nurture
   ↓ Yes
[Proposal Agent] (drafts)
   ↓
Founder Approves? ──No──> Revise
   ↓ Yes
[Payment Handoff Agent] (drafts)
   ↓
Founder Approves? ──No──> Revise
   ↓ Yes
Payment Received
   ↓
[Delivery OS Handoff]
   ↓
Active Delivery
   ↓
[Customer Success Agent] (weekly)
   ↓
Health Score
   ↓
Renewal Window? ──No──> Continue
   ↓ Yes
[Renewal Agent] (drafts)
   ↓
Founder Approves? ──No──> Revise
   ↓ Yes
Renewed ──or──> Lost
   ↓
Closed
```

### 5.2 Channel Decision Flow
```
Signal Detected
   ↓
Channel identified
   ↓
Channel rules satisfied? ──No──> Block
   ↓ Yes
Draft (agent)
   ↓
Founder approves? ──No──> Revise
   ↓ Yes
Manual send (founder)
   ↓
Reply received?
   ├─ No → nurture/blackhole
   └─ Yes → Discovery path (5.1)
```

### 5.3 Pricing Decision Flow
```
Need price
   ↓
In published range? ──Yes──> L1 auto
   ↓ No
   ↓
Discount < 15%? ──Yes──> L2 founder
   ↓ No
   ↓
Discount > 15%? ──Yes──> L3 founder + CCO + reason
   ↓ No
   ↓
Custom > 50K? ──Yes──> L4 founder + legal
   ↓ No
   ↓
Legal/sensitive? ──Yes──> L5 founder + counsel
   ↓ No
   ↓
Reject — no good price
```

### 5.4 Risk Decision Flow
```
Risk detected
   ↓
Severity?
   ↓
Low → log + monitor
   ↓
Medium → log + mitigate plan
   ↓
High → founder action within 24h
   ↓
Critical → founder action now + escalation
```

---

## 6. File Index (فهرس الملفات)

### 6.1 PHASE 0
- `reports/commercial/COMMERCIAL_GAP_AUDIT.md` — هذا الـ audit

### 6.2 PHASE 1
- `docs/commercial/COMMERCIAL_OPERATING_SYSTEM_AR.md` (foundation)
- `docs/commercial/COMMERCIAL_STRATEGY_AR.md`
- `docs/commercial/COMMERCIAL_DECISION_RULES_AR.md`
- `docs/commercial/FOUNDER_COMMERCIAL_RHYTHM_AR.md`
- `docs/commercial/COMMERCIAL_METRICS_AR.md`
- `reports/commercial/COMMERCIAL_OPERATING_MAP.md` (هذا الملف)

### 6.3 PHASE 2
- `docs/commercial/ICP_MATRIX_AR.md`
- `docs/commercial/MARKET_SEGMENTATION_AR.md`
- `docs/commercial/BUYER_PERSONAS_AR.md`
- `docs/commercial/DISQUALIFICATION_RULES_AR.md`
- `schemas/icp.schema.json`
- `schemas/buyer_persona.schema.json`
- `data/commercial/icp_segments.yaml`
- `data/commercial/buyer_personas.yaml`
- `reports/commercial/ICP_PRIORITY_REPORT.md`

### 6.4 PHASE 3
- `docs/commercial/PAIN_TO_OFFER_MATRIX_AR.md`
- `docs/commercial/OFFER_MATCHING_RULES_AR.md`
- `docs/commercial/PROBLEM_CATEGORY_MAP_AR.md`
- `schemas/pain_signal.schema.json`
- `schemas/offer_match.schema.json`
- `data/commercial/pain_to_offer.yaml`
- `reports/commercial/OFFER_MATCH_REVIEW.md`

### 6.5 PHASE 4
- `docs/commercial/PRODUCT_CATALOG_AR.md`
- `docs/commercial/OFFER_LADDER_AR.md`
- `docs/commercial/PACKAGING_STRATEGY_AR.md`
- `docs/commercial/SCOPE_AND_OUT_OF_SCOPE_AR.md`
- `docs/commercial/DELIVERABLES_LIBRARY_AR.md`
- `schemas/product_offer.schema.json`
- `data/commercial/product_catalog.yaml`
- `reports/commercial/PRODUCT_CATALOG_REVIEW.md`

### 6.6 PHASE 5
- `docs/commercial/PRICING_GUARDRAILS_AR.md`
- `docs/commercial/DISCOUNT_POLICY_AR.md`
- `docs/commercial/PAYMENT_TERMS_AR.md`
- `docs/commercial/PRICE_ANCHORING_GUIDE_AR.md`
- `docs/commercial/QUOTE_APPROVAL_POLICY_AR.md`
- `schemas/pricing_rule.schema.json`
- `data/commercial/pricing_rules.yaml`
- `reports/commercial/PRICING_RISK_REVIEW.md`

### 6.7 PHASE 6
- `docs/commercial/SALES_PROCESS_AR.md`
- `docs/commercial/PIPELINE_STAGES_AR.md`
- `docs/commercial/QUALIFICATION_RULES_AR.md`
- `docs/commercial/DISCOVERY_PROCESS_AR.md`
- `docs/commercial/NEXT_STEP_RULES_AR.md`
- `schemas/opportunity.schema.json`
- `schemas/discovery_note.schema.json`
- `data/commercial/opportunities.jsonl`
- `data/commercial/discovery_notes.jsonl`
- `reports/commercial/PIPELINE_REVIEW.md`

### 6.8 PHASE 7
- `docs/commercial/PROPOSAL_STRATEGY_AR.md`
- `docs/commercial/PROPOSAL_APPROVAL_POLICY_AR.md`
- `docs/commercial/PROOF_PACK_COMMERCIAL_GUIDE_AR.md`
- `docs/commercial/CASE_STUDY_POLICY_AR.md`
- `schemas/commercial_proposal.schema.json`
- `schemas/commercial_proof_pack.schema.json`
- `reports/commercial/PROPOSAL_COMMERCIAL_REVIEW.md`

### 6.9 PHASE 8
- `docs/commercial/OBJECTION_BANK_AR.md`
- `docs/commercial/SALES_ENABLEMENT_PLAYBOOK_AR.md`
- `docs/commercial/COMPETITOR_POSITIONING_AR.md`
- `docs/commercial/ROI_CONVERSATION_GUIDE_AR.md`
- `docs/commercial/RISK_REVERSAL_POLICY_AR.md`
- `data/commercial/objections.yaml`
- `reports/commercial/OBJECTION_REVIEW.md`

### 6.10 PHASE 9
- `docs/commercial/CHANNEL_STRATEGY_AR.md`
- `docs/commercial/COLD_EMAIL_CHANNEL_AR.md`
- `docs/commercial/WHATSAPP_AFTER_CONSENT_CHANNEL_AR.md`
- `docs/commercial/CONTENT_CHANNEL_AR.md`
- `docs/commercial/PARTNERSHIP_CHANNEL_AR.md`
- `docs/commercial/PRESS_CHANNEL_AR.md`
- `docs/commercial/REFERRAL_CHANNEL_AR.md`
- `reports/commercial/CHANNEL_STRATEGY_REVIEW.md`

### 6.11 PHASE 10
- `docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md`
- `docs/partnerships/PARTNER_PRICING_AND_MARGIN_AR.md`
- `docs/partnerships/PARTNER_PIPELINE_PROCESS_AR.md`
- `docs/partnerships/PARTNER_ENABLEMENT_KIT_AR.md`
- `docs/partnerships/PARTNER_QUALIFICATION_AR.md`
- `schemas/partner_opportunity.schema.json`
- `data/partners/partner_opportunities.jsonl`
- `reports/partnerships/PARTNER_COMMERCIAL_REVIEW.md`

### 6.12 PHASE 11
- `docs/customer_success/CUSTOMER_SUCCESS_OS_AR.md`
- `docs/customer_success/FIRST_30_DAYS_AR.md`
- `docs/customer_success/WEEKLY_VALUE_REPORT_AR.md`
- `docs/customer_success/CLIENT_HEALTH_SCORE_AR.md`
- `docs/customer_success/RENEWAL_PLAYBOOK_AR.md`
- `docs/customer_success/EXPANSION_PLAYBOOK_AR.md`
- `schemas/client_health.schema.json`
- `data/customer_success/client_health.jsonl`
- `reports/customer_success/CLIENT_HEALTH_REVIEW.md`

### 6.13 PHASE 12
- `docs/finance/COMMERCIAL_UNIT_ECONOMICS_AR.md`
- `docs/finance/OFFER_MARGIN_MODEL_AR.md`
- `docs/finance/CAC_PAYBACK_MODEL_AR.md`
- `docs/finance/CHANNEL_ROI_MODEL_AR.md`
- `docs/finance/SALES_CAPACITY_MODEL_AR.md`
- `docs/finance/RETAINER_REVENUE_MODEL_AR.md`
- `reports/finance/COMMERCIAL_FINANCE_REVIEW.md`

### 6.14 PHASE 13
- `docs/commercial/COMMERCIAL_RISK_REGISTER_AR.md`
- `docs/commercial/WALK_AWAY_RULES_AR.md`
- `docs/commercial/BAD_FIT_CLIENT_POLICY_AR.md`
- `docs/commercial/SCOPE_CREEP_POLICY_AR.md`
- `reports/commercial/COMMERCIAL_RISK_REVIEW.md`

### 6.15 PHASE 14
- `docs/commercial/COMMERCIAL_CONTROL_ROOM_SPEC_AR.md`
- `reports/commercial/COMMERCIAL_DAILY_COMMAND.md`
- `reports/commercial/COMMERCIAL_WEEKLY_REVIEW.md`

### 6.16 PHASE 15
- `tests/test_commercial_offer_mapping.py`
- `tests/test_pricing_requires_approval.py`
- `tests/test_no_guaranteed_revenue_claims.py`
- `tests/test_proposal_requires_qualified_opportunity.py`
- `tests/test_payment_handoff_requires_approval.py`
- `tests/test_walk_away_rules.py`
- `tests/test_partner_model_margin_rules.py`
- `tests/test_customer_success_handoff_required.py`
- `docs/evals/COMMERCIAL_SAFETY_EVALS_AR.md`
- `data/evals/commercial_safety_cases.jsonl`

### 6.17 PHASE 16
- `docs/agents/COMMERCIAL_AGENT_ROLES_AR.md`
- `docs/agents/COMMERCIAL_AGENT_PERMISSION_MATRIX_AR.md`
- `docs/agents/COMMERCIAL_AGENT_OUTPUT_CONTRACT_AR.md`

### 6.18 FINAL
- `reports/commercial/COMMERCIAL_EXPANSION_FINAL_REPORT.md`

---

## 7. Status Check (تطبيق خريطة الإنجاز)

| PHASE | عدد الملفات | الحالة |
|-------|-------------|--------|
| 0 | 1 | ✅ |
| 1 | 6 | 🔄 (current) |
| 2 | 9 | ⏳ |
| 3 | 7 | ⏳ |
| 4 | 8 | ⏳ |
| 5 | 8 | ⏳ |
| 6 | 10 | ⏳ |
| 7 | 7 | ⏳ |
| 8 | 7 | ⏳ |
| 9 | 8 | ⏳ |
| 10 | 8 | ⏳ |
| 11 | 9 | ⏳ |
| 12 | 7 | ⏳ |
| 13 | 5 | ⏳ |
| 14 | 3 | ⏳ |
| 15 | 10 | ⏳ |
| 16 | 3 | ⏳ |
| Final | 1 | ⏳ |
| **Total** | **~125 file operations** | |

---

## 8. Navigation Shortcuts

- للمبتدئ → `COMMERCIAL_OPERATING_SYSTEM_AR.md`
- لتسعير → `PRICING_GUARDRAILS_AR.md` + `pricing.yaml`
- لـ pipeline → `PIPELINE_STAGES_AR.md` + `stage_transitions.yaml`
- لـ customer success → `CUSTOMER_SUCCESS_OS_AR.md`
- لـ risk → `COMMERCIAL_RISK_REGISTER_AR.md`
- للقرار السريع → `COMMERCIAL_DECISION_RULES_AR.md`
- للـ agent → `COMMERCIAL_AGENT_ROLES_AR.md` (PHASE 16)
- للـ test → `tests/test_commercial_*.py` (PHASE 15)
- للـ UI → `COMMERCIAL_CONTROL_ROOM_SPEC_AR.md` (PHASE 14)

---

**هذه الخريطة هي reference دائم. كل PHASE يضيف إليها بدون تعديلها. PHASE 14+ يستهلكها (UI). PHASE 15 يحميها (tests). PHASE 16 يستفيد منها (agents).**
