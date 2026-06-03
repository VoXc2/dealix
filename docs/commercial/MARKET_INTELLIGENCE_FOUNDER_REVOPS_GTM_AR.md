# مؤسس · RevOps مستمر · GTM — من السرعة إلى محرك حوكَم

**الجمهور:** سامي (مؤسس) · dealix-pm · dealix-sales  
**آخر تحديث:** 2026-05-18

---

## 1) حقيقة السوق (founder-led sales)

| مرحلة | ما يحدث | خطر بدون نظام | رد Dealix |
|-------|---------|---------------|-----------|
| 0 → أول إيراد | سرعة + علاقات | لا ICP | War Room + seed targeting |
| ~500K ARR | تنوع عملاء | playbook ضعيف | Motion A + evidence CSV |
| ~1M ARR | أول توظيف مبيعات | CRM فوضى | Revenue Memory قبل التوظيف |
| 1–3M ARR | founder bottleneck | جودة صفقات تنخفض | Decision Passport + anti-waste |

**مصادر فئة:** [100 Founders — founder-led sprint](https://www.100founders.ai/p/the-founder-led-sales-sprint) · [RevOps On-Demand — governed engine](https://www.revopson-demand.com/insights/founder-led-sales-to-governed-revenue-engine)

---

## 2) RevOps «مستمر» vs خطة سنوية

| خطة سنوية ثابتة | RevOps مستمر (Dealix) |
|------------------|------------------------|
| أهداف تتقادم في Q2 | [`MASTER_COMMERCIAL_OPERATING_PLAN_AR.md`](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) يومي |
| CRM منعزل عن المالية | KPI import + Business Now |
| territories يدوية | `rotate_agency_targets.py` + seed CSV |
| لا أدلة على القرار | `evidence_events_tracker.csv` |

**مرجع:** [Fullcast — continuous GTM](https://www.fullcast.com/content/continuous-gtm-management-revops/)

---

## 3) آلة اليوم (ربط سكربتات)

| وقت | هدف | أمر |
|-----|-----|-----|
| صباح | موجز + War Room + سوشال مسودة | `scripts/run_founder_commercial_day.sh` |
| نهار | اجتماعات Motion A | `scripts/founder_motion_a_pipeline.py` |
| مساء | سطر أدلة | `scripts/founder_evening_evidence.py` |
| أسبوع | scorecard | `scripts/founder_weekly_scorecard.py` |
| بوابة paid | تحقق | `scripts/verify_paid_launch_readiness.py` |

**واجهة:** `/ar/ops/founder` · `/ar/ops/war-room` · `/ar/ops/marketing`

---

## 4) مؤشرات أسبوعية (لا تخترع أرقام CRM)

| مؤشر | مصدر حقيقة |
|------|------------|
| اجتماعات محجوزة | Calendly + evidence |
| مسودات بانتظار موافقة | ops marketing API |
| أول دفع diagnostic | `FIRST_PAID_DIAGNOSTIC_DOD` |
| pipeline motion A | `agency_accounts_seed.csv` |

**قاعدة:** [`kpi_founder_commercial_import.yaml`](../../dealix/transformation/kpi_founder_commercial_import.example.yaml) — انسخ واملأ من CRM فقط.

---

## 5) رسائل Why Now للمؤسس (للاستخدام في المحتوى)

1. «الفضول ليس نية شراء — Decision Passport يفرّق.»
2. «تكلفة الانتظار ترتفع عندما يتسارع التحول الرقمي — لماذا الآن وليس العام الماضي.»
3. «قبل توظيف مندوب: وثّق الاكتشاف في Revenue Memory.»

---

## 6) Motions الأربعة (تذكير)

| Motion | متى | وثيقة |
|--------|-----|-------|
| A — وكالات ABM | الآن | `operations/GTM_DUAL_TRACK` · seed CSV |
| B — inbound | بعد funnel PASS | `COMMERCIAL_LAUNCH_CHECKLIST` |
| C — شركاء | بعد Proof | `operations/` partner pack |
| D — enterprise | بعد 3 proofs | enterprise package |

---

## 7) انتقال إلى «محرك حوكَم»

```mermaid
flowchart LR
  FL[Founder_magic]
  DOC[Documented_playbook]
  RM[Revenue_Memory]
  HIRE[First_sales_hire]
  FL --> DOC --> RM --> HIRE
```

**معيار الجاهزية للتوظيف:** 50+ discovery موثّقة · ICP واحد dominant · CRM stages ثابتة · Decision Passport لكل صفقة > X SAR.

---

## 8) روابط

- [`FOUNDER_OPERATING_SYSTEM_AR.md`](../ops/FOUNDER_OPERATING_SYSTEM_AR.md)
- [`DEALIX_REVENUE_WAR_ROOM_AR.md`](../ops/DEALIX_REVENUE_WAR_ROOM_AR.md)
- [`operations/FOUNDER_SALES_LOOP_AR.md`](operations/FOUNDER_SALES_LOOP_AR.md)
- [`MARKET_INTELLIGENCE_IMPLEMENTATION_PLAYBOOK_AR.md`](MARKET_INTELLIGENCE_IMPLEMENTATION_PLAYBOOK_AR.md)
