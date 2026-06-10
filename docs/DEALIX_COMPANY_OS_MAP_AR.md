# خريطة نظام Dealix التشغيلي — DEALIX_COMPANY_OS_MAP_AR

> **خريطة بصرية** للعلاقات بين الأنظمة الـ 4 الجديدة (29/30/31/33) والأنظمة القائمة (legacy). ASCII tree + جدول cross-references.
>
> **آخر تحديث:** 2026-06-03
> **المالك:** Agent #35 — Final Integration
> **الإصدار:** v1.0
> **language:** Arabic-first

---

## 1) خريطة شاملة (Master ASCII Tree)

```
═══════════════════════════════════════════════════════════════════════════
                          DEALIX COMPANY OS — FULL MAP
═══════════════════════════════════════════════════════════════════════════

  LEGACY (قائم)                          NEW WAVE 29-33 (جديد)
  ──────────────                          ─────────────────────
                                           
  ┌──────────────────────┐                 ┌─────────────────────────┐
  │ COMMERCIAL OS        │◄── feeds ──────│ 4. OFFER PAGES (33)     │
  │ (docs/commercial/)   │                 │  docs/offers/           │
  │                      │                 │  6 pages + FAQ + CTA    │
  └──────────┬───────────┘                 └────────────┬────────────┘
             │                                          │
             │ (Lead, ICP, Pricing)                    │ (CTA → WhatsApp/Calendly)
             ▼                                          ▼
  ┌──────────────────────┐                 ┌─────────────────────────┐
  │ SALES LEGACY         │◄── sales ──────│ 1. ENTERPRISE SALES (29)│
  │ (docs/sales/)        │   motion        │  docs/enterprise_sales/ │
  │                      │                 │  11 docs, ABM, MAP,     │
  └──────────────────────┘                 │  Discovery, Risk        │
             ▲                             └────────────┬────────────┘
             │                                          │
             │ (proposal template)                      │ (Pilot contract)
             │                                          ▼
  ┌──────────────────────┐                 ┌─────────────────────────┐
  │ LEGAL (DPA/MSA)      │◄── signs ───────│ DELIVERY (legacy)       │
  │ (docs/legal/)        │                 │  docs/delivery/         │
  └──────────────────────┘                 │  docs/phase-e/          │
                                           └────────────┬────────────┘
                                                        │
                                                        │ (proof events, KPIs)
                                                        ▼
                                           ┌─────────────────────────┐
                                           │ 3. DATA PRODUCTS (31)   │
                                           │  docs/data_products/    │
                                           │  8 docs, benchmarks,    │
                                           │  message library, etc.  │
                                           └────────────┬────────────┘
                                                        │
                                                        │ (consume evidence)
                                                        ▼
                                           ┌─────────────────────────┐
                                           │ 2. AI GOVERNANCE (30)   │
                                           │  docs/ai_governance/    │
                                           │  9 docs, A0-A5,         │
                                           │  Lifecycle, Eval,       │
                                           │  Incident Response      │
                                           └────────────┬────────────┘
                                                        │
                                                        │ (gates every action)
                                                        ▼
                                           ┌─────────────────────────┐
                                           │ SECURITY + RA (legacy)  │
                                           │  docs/security/         │
                                           │  docs/responsible_ai/   │
                                           └─────────────────────────┘
```

---

## 2) جدول الصلات (Cross-Reference Table)

| من (FROM) | إلى (TO) | نوع العلاقة | السبب |
|-----------|---------|-------------|-------|
| **Offers (33)** | Commercial OS | **feeds** | CTA → WhatsApp/Calendly → Lead في pipeline |
| **Offers (33)** | Sales Legacy | **aligns** | نفس نبرة + نفس FAQ (link) |
| **Enterprise Sales (29)** | Commercial OS | **extends** | ABM + Tier-1 فوق ICP الموجود |
| **Enterprise Sales (29)** | Enterprise Rollout | **hands-off** | MAP ينتهي عند توقيع → Rollout يبدأ |
| **Enterprise Sales (29)** | Enterprise (readiness) | **aligns** | يطلب نفس Security/Privacy/Procurement |
| **Delivery (legacy)** | Enterprise Sales (29) | **feedback** | Pilot outcomes ترجع كـ Deal Risk update |
| **Delivery (legacy)** | Data Products (31) | **emits** | يولّد proof events + delivery_patterns |
| **Data Products (31)** | Enterprise Sales (29) | **informs** | sector_benchmarks تغذّي ABM scoring |
| **Data Products (31)** | Offers (33) | **informs** | best_offer من sector_benchmarks → CTA |
| **Data Products (31)** | Data Governance | **upstream** | يستهلك data_quality + PII rules |
| **AI Governance (30)** | كل action | **gates** | Default-Deny على external_action |
| **AI Governance (30)** | Governance (legacy) | **extends** | Lifecycle + Eval فوق AI_ACTION_TAXONOMY |
| **AI Governance (30)** | Responsible AI | **aligns** | share risk_classifier |
| **AI Governance (30)** | Security | **escalates** | P1/P2 → incident_runbook |

---

## 3) أين تذهب كل مخرجات (Where Outputs Go)

```
┌─────────────────────┐
│ OUTREACH / PROPOSAL │ ──→ leads to ──→ MUTUAL_ACTION_PLAN (29)
└─────────────────────┘                     │
                                            ▼
                                   PILOT (delivery/)
                                            │
                                            ▼
┌─────────────────────┐              PROOF PACK (delivery/)
│ DATA OBSERVATIONS   │ ◄─── writes ──┘
│ (delivery events)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ DATA PRODUCTS JSONL │ ──→ informs ──→ OFFER CTA + SCORING (33 + 29)
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  REPORTS weekly     │ ──→ reviewed by ──→ FOUNDER (governance review)
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  AI GOVERNANCE      │ ──→ gates every external_action (email, WhatsApp, ...)
│  (Daily Eval)       │     Default-Deny
└─────────────────────┘
```

---

## 4) تدفّق المبيعات المؤسسي (Enterprise Sales Flow)

```
┌────────────────┐
│ 1. ABM LIST    │  (Tier-1/2/3 — needs founder input)
│  accounts.jsonl│
└───────┬────────┘
        ▼
┌────────────────┐
│ 2. TAP         │  (14 fields per account)
│ target_account │
└───────┬────────┘
        ▼
┌────────────────┐
│ 3. STAKEHOLDER │  (10 buyer roles)
│ MAPPING        │
└───────┬────────┘
        ▼
┌────────────────┐
│ 4. DISCOVERY   │  (90-min agenda)
└───────┬────────┘
        ▼
┌────────────────┐
│ 5. MAP         │  (10 milestones)
│ mutual_action_ │
│   plan.jsonl   │
└───────┬────────┘
        ▼
┌────────────────┐
│ 6. BUSINESS    │  (1-pager)
│    CASE        │
└───────┬────────┘
        ▼
┌────────────────┐
│ 7. PILOT SOW   │  (4 phases)
└───────┬────────┘
        ▼
┌────────────────┐
│ 8. EXPANSION   │  (channel, team, multi-dept)
│    PATH        │
└───────┬────────┘
        ▼
┌────────────────┐
│ 9. DEAL RISK   │  (weekly review)
│   (9 risks)    │
└────────────────┘
```

---

## 5) تدفّق الحوكمة (Governance Flow)

```
┌────────────────────┐
│ Agent registers in │ ──→ agent_registry.jsonl
│ AI Governance OS   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Lifecycle policy   │ ──→ agent_permissions.jsonl
│ (A0-A5)            │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Daily / weekly     │ ──→ agent_evals.jsonl
│ evaluation         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Risk detected?     │
│   YES ──→ Incident │ ──→ agent_incidents.jsonl
│   NO  ──→ continue │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Human approval     │ ──→ external_action (allowed if approved)
│ boundary           │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Action executed    │ ──→ audit_log (governance ledger)
└────────────────────┘
```

---

## 6) تدفّق منتجات البيانات (Data Products Flow)

```
┌────────────────────┐
│ Raw events from    │  (delivery, outreach, sales)
│ legacy systems     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Data Governance    │  (PII redaction, classification)
│ (legacy)           │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Data Products JSONL│
│ - sector_benchmarks│  (8 rows, evidence_level)
│ - message_perf     │  (8 rows)
│ - objection_pattern│  (12 rows)
│ - delivery_patterns│  (13 rows)
│ - renewal_triggers │  (8 rows)
│ - pricing_sens.    │  (7 rows)
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 7 Libraries        │ ──→ consumed by Sales (29) + Offers (33)
│ 7 docs             │
└────────────────────┘
```

---

## 7) ملخص الحدود (Boundary Summary)

| النظام | يبدأ عند | ينتهي عند | لا يدخل في |
|--------|---------|-----------|-----------|
| **Enterprise Sales (29)** | قائمة ABM Tier-1 | توقيع Pilot SOW | Delivery execution (داخل المؤسسة) |
| **AI Governance (30)** | تسجيل agent في `agent_registry.jsonl` | Retiring agent | نمذجة الوكلاء (تفصيل تقني) |
| **Data Products (31)** | Proof event + observed data | Benchmark + library row | Real-time inference |
| **Offers (33)** | landing page live | CTA click | Onboarding (بعد click) |

> التفاصيل الكاملة في [`../docs/SYSTEM_BOUNDARIES.md`](../docs/SYSTEM_BOUNDARIES.md).

---

## Open Questions for Founder

1. هل تريد **diagram مرئي** (Mermaid أو PNG) بدلاً من ASCII tree؟ — يمكن إنشاءه من نفس البيانات.
2. هل هذه الخريطة تكفي كـ **onboarding doc** للموظف الجديد، أم تحتاج نسخة مبسّطة (1 page)؟
3. هل يجب أن يكون كل رابط في الخريطة **مرجع فعلي مفعّل**، أم نكتفي بـ "اذهب إلى docs/X/"؟
