# ICP Matrix — مصفوفة العميل المثالي
**Dealix — Agent #3**

> **الغرض:** توسيع `icp_primary.yaml` (الموجود) بمصفوفة شاملة لـ 10 شرائح B2B سعودية، مع تقييم كمي لكل شريحة (urgency, budget, delivery, proof, risk).

---

## 1. المبدأ التوجيهي

**كل شريحة لها:** score من 0-5 على 11 بُعد، plus first offer، disqualifiers، priority rank.

**Score interpretation:**
- 5 = excellent fit (priority)
- 4 = strong fit
- 3 = acceptable
- 2 = weak (still possible with founder approval)
- 1 = poor (default reject)
- 0 = block (disqualifier)

---

## 2. Primary ICPs (10 شرائح)

### 2.1 Marketing Agency (الوتد — Motion A)

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 5 | leads متكررة |
| Sales process maturity | 3 | يعتمد على owner |
| Urgency | 4 | campaigns مستمرة |
| Budget fit | 4 | Diagnostic 9,999 + Retainer 4,999/mo |
| Decision maker access | 5 | Agency Owner = decision maker |
| Delivery complexity | 3 | proof pack + workflow |
| Proof speed | 5 | 7-14 يوم ممكن |
| Risk level | 2 | PDPL simple, no regulated |
| First offer | diagnostic_standard | 9,999 SAR |
| Disqualifiers | spam_request, no_clients | |
| **Total** | **36/50 (P1)** | |

**ملاحظة:** هو الوتد. كل optimization أول يبدأ هنا.

### 2.2 Training Companies

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 5 | enrollment inquiries متكررة |
| Sales process maturity | 2 | enrollment form chaos |
| Urgency | 4 | courses تبدأ بمواعيد |
| Budget fit | 4 | 8,000-18,000 OK |
| Decision maker access | 4 | owner/training manager |
| Delivery complexity | 3 | follow-up workflow |
| Proof speed | 4 | 14 يوم |
| Risk level | 2 | student data privacy |
| First offer | follow_up_recovery | 12,000 SAR |
| Disqualifiers | no_enrollment, no_data | |
| **Total** | **30/50 (P1)** | |

### 2.3 Clinics

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 4 | appointments daily |
| Sales process maturity | 2 | phone/WhatsApp chaos |
| Urgency | 5 | appointments تضيع |
| Budget fit | 4 | 8,000-18,000 OK |
| Decision maker access | 4 | clinic manager |
| Delivery complexity | 4 | appointment + follow-up + no-show |
| Proof speed | 3 | 21 يوم (sensitive) |
| Risk level | 3 | health data = PDPL sensitive |
| First offer | follow_up_recovery_with_PDPL_review | 15,000 SAR |
| Disqualifiers | health_data_no_PDPL_review, no_appointment_system | |
| **Total** | **33/50 (P1)** | |

### 2.4 Real Estate Teams

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 5 | viewing inquiries |
| Sales process maturity | 2 | slow response = lost leads |
| Urgency | 5 | leads تبرد بسرعة |
| Budget fit | 4 | 9,999-25,000 OK |
| Decision maker access | 3 | depends on broker structure |
| Delivery complexity | 3 | viewing follow-up + CRM |
| Proof speed | 4 | 14 يوم |
| Risk level | 2 | personal data |
| First offer | follow_up_recovery | 12,000 SAR |
| Disqualifiers | broker_individual_no_company, no_office | |
| **Total** | **31/50 (P1)** | |

### 2.5 Recruitment Agencies

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 4 | clients + candidates |
| Sales process maturity | 3 | depends on agency |
| Urgency | 4 | placements time-sensitive |
| Budget fit | 3 | 9,999-18,000 |
| Decision maker access | 4 | agency owner |
| Delivery complexity | 3 | multi-side follow-up |
| Proof speed | 3 | 21 يوم |
| Risk level | 2 | candidate data |
| First offer | ai_revenue_ops_starter | 18,000 SAR |
| Disqualifiers | no_CRM, only_linkedin_manual | |
| **Total** | **29/50 (P1)** | |

### 2.6 Professional Services Firms (legal, accounting, consulting)

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 3 | inquiry-based |
| Sales process maturity | 3 | partner-led |
| Urgency | 3 | slow cycle |
| Budget fit | 3 | 9,999-25,000 |
| Decision maker access | 3 | partner-led |
| Delivery complexity | 3 | proposal follow-up |
| Proof speed | 3 | 21 يوم |
| Risk level | 3 | confidential clients |
| First offer | proposal_factory | 18,000 SAR |
| Disqualifiers | partner_led_no_authority, no_partner_signoff | |
| **Total** | **25/50 (P2)** | |

### 2.7 Local SaaS / Service Firms

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 4 | trials + demos |
| Sales process maturity | 3 | sales-led |
| Urgency | 4 | ARR pressure |
| Budget fit | 4 | 18,000-35,000 |
| Decision maker access | 4 | founder/sales lead |
| Delivery complexity | 4 | RevOps needed |
| Proof speed | 3 | 30 يوم |
| Risk level | 2 | internal data |
| First offer | ai_revenue_ops_starter | 25,000 SAR |
| Disqualifiers | no_founder_signoff, technical_debt_block | |
| **Total** | **31/50 (P1)** | |

### 2.8 Education Providers (universities, language schools, institutes)

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 5 | admissions متكررة |
| Sales process maturity | 3 | season-dependent |
| Urgency | 4 | admissions season |
| Budget fit | 4 | 15,000-35,000 |
| Decision maker access | 4 | admissions manager |
| Delivery complexity | 3 | multi-channel follow-up |
| Proof speed | 3 | 30 يوم |
| Risk level | 3 | student data |
| First offer | ai_revenue_ops_starter | 25,000 SAR |
| Disqualifiers | no_admissions_data, no_season | |
| **Total** | **32/50 (P1)** | |

### 2.9 Logistics / Service Operations

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 4 | quote requests |
| Sales process maturity | 3 | quote-dependent |
| Urgency | 4 | service urgency |
| Budget fit | 3 | 15,000-25,000 |
| Decision maker access | 3 | ops manager |
| Delivery complexity | 4 | quote workflow + tracking |
| Proof speed | 3 | 30 يوم |
| Risk level | 2 | operational data |
| First offer | ai_revenue_ops_starter | 22,000 SAR |
| Disqualifiers | no_digital_quote, manual_only | |
| **Total** | **29/50 (P1)** | |

### 2.10 Restaurant Groups (multi-location)

| البُعد | Score | Note |
|--------|-------|------|
| Lead flow maturity | 4 | campaigns + reservations |
| Sales process maturity | 2 | inconsistent |
| Urgency | 3 | marketing-driven |
| Budget fit | 3 | 9,999-18,000 |
| Decision maker access | 4 | group owner |
| Delivery complexity | 3 | multi-location |
| Proof speed | 3 | 30 يوم |
| Risk level | 2 | customer data |
| First offer | follow_up_recovery | 12,000 SAR |
| Disqualifiers | single_location_no_growth, no_marketing | |
| **Total** | **27/50 (P2)** | |

---

## 3. ملخص الترتيب (Priority Ranking)

| Rank | Segment | Total | Tier |
|------|---------|-------|------|
| 1 | Marketing Agency | 36 | P1 — Wedge |
| 2 | Clinics | 33 | P1 |
| 3 | Education Providers | 32 | P1 |
| 4 | Real Estate | 31 | P1 |
| 5 | Local SaaS | 31 | P1 |
| 6 | Training Companies | 30 | P1 |
| 7 | Recruitment | 29 | P1 |
| 8 | Logistics | 29 | P1 |
| 9 | Restaurant Groups | 27 | P2 |
| 10 | Professional Services | 25 | P2 |

---

## 4. Companion Files

- **YAML:** `data/commercial/icp_segments.yaml` (extending `dealix/config/icp_segments.yaml`)
- **Schema:** `schemas/icp.schema.json`
- **Personas:** `BUYER_PERSONAS_AR.md` + `data/commercial/buyer_personas.yaml`
- **Disqualifiers:** `DISQUALIFICATION_RULES_AR.md`
- **Priority Report:** `reports/commercial/ICP_PRIORITY_REPORT.md`

---

## 5. ICP Refresh Cadence

- **Weekly:** Review conversion by ICP
- **Monthly:** Adjust scores based on actual data
- **Quarterly:** Add/remove segments based on signals
- **Yearly:** Full ICP strategy review

---

**Note:** هذا الملف **تكميلي** لـ `icp_primary.yaml` و `icp_segments.yaml` و `icp_agency_wedge.yaml` — لا يحل محلها.
