# مكتبة معايير القبول — Dealix Acceptance Criteria Library (AR)

> **مكتبة معايير القبول لكل deliverable قابل للقياس.** كل معيار:
> قابل للقياس، له owner، له measurement method.

**الحالة:** مسودة — Phase 3 من Agent #15
**التاريخ:** 2026-06-03

---

## 1. المبادئ (Principles)

1. **Measurable:** كل معيار يُقاس (رقم، %، boolean، manual review).
2. **Owned:** كل معيار له owner يوقّع.
3. **Time-bound:** كل معيار له deadline.
4. **Documented:** كل معيار في `acceptance_criteria.jsonl`.

## 2. المعايير العامة (Universal Criteria)

تنطبق على **كل** deliverable:

| # | المعيار | القياس | Owner |
| - | --- | --- | --- |
| U1 | No secrets in deliverable | grep + manual review | founder |
| U2 | No fake claims (L0 claims forbidden) | claims matrix | founder |
| U3 | Arabic glossary compliance | term match | Agent #14 |
| U4 | Voice compliance (ARABIC_BRAND_VOICE_AR) | manual review | Agent #14 |
| U5 | Voice test (§ Voice Test) | manual review | Agent #14 |
| U6 | Channel length compliance | word count | Agent #14 |
| U7 | Single CTA per message | manual review | Agent #14 |
| U8 | No banned wording | string match | Agent #13 |
| U9 | Approved by legal review (if needed) | `data/legal/legal_reviews.jsonl` | Agent #13 |
| U10 | Source citations (if claim) | ref check | founder |

## 3. المعايير الخاصة بكل Deliverable

### 3.1 Proof Pack

| # | المعيار | القياس |
| - | --- | --- |
| PP1 | ≥ 3 leaks محددة بأرقام | manual review |
| PP2 | التوصيات مرتبة حسب الأثر | manual |
| PP3 | خطة 30 يوم (3–5 خطوات أسبوعية) | manual |
| PP4 | جلسة نتائج (60 دقيقة) مُسلَّمة | calendar event |
| PP5 | Claim tier ≥ L2 (مصدر موثّق) | evidence check |
| PP6 | Named client requires `csp_*` APPROVED | `case_study_permissions.jsonl` |

### 3.2 Proposal

| # | المعيار | القياس |
| - | --- | --- |
| PR1 | موقّع من العميل | signature |
| PR2 | نطاق واضح (in / out of scope) | manual |
| PR3 | سعر ضمن range الـ service | catalog check |
| PR4 | Timeline ≤ timeline_days.max | catalog check |
| PR5 | First-7-days plan موجود | manual |
| PR6 | Arabic voice compliance | Agent #14 |

### 3.3 WhatsApp Templates

| # | المعيار | القياس |
| - | --- | --- |
| WT1 | 10 templates معتمدة من العميل | signature |
| WT2 | Each template < 60 words | word count |
| WT3 | Each template has 1 CTA | manual |
| WT4 | Each template respects opt-in | manual |
| WT5 | No cold-outreach wording | string match |
| WT6 | No guaranteed claims | string match |
| WT7 | Meta templates approved (if sending) | Meta dashboard |

### 3.4 Runbook

| # | المعيار | القياس |
| - | --- | --- |
| RB1 | ≥ 4 سيناريوهات موثّقة | count |
| RB2 | كل سيناريو: input → action → output | manual |
| RB3 | Rollback path موجود | manual |
| RB4 | Owner معيّن لكل سيناريو | manual |

### 3.5 Weekly Report

| # | المعيار | القياس |
| - | --- | --- |
| WR1 | ≤ 800 كلمة | word count |
| WR2 | جدول أرقام (≥ 5 metrics) | manual |
| WR3 | Decisions logged in proof ledger | API check |
| WR4 | y-ويصل خلال 5 أيام من الأسبوع | timestamp |
| WR5 | Arabic voice compliance | Agent #14 |

### 3.6 Daily Brief

| # | المعيار | القياس |
| - | --- | --- |
| DB1 | يوصل 8:00 AM ± 30 دقيقة | timestamp |
| DB2 | ≤ 200 كلمة | word count |
| DB3 | Role-specific | manual |
| DB4 | ≥ 1 actionable | manual |
| DB5 | Arabic voice compliance | Agent #14 |

### 3.7 Quarterly Review

| # | المعيار | القياس |
| - | --- | --- |
| QR1 | Action items مسجّلة | meeting notes |
| QR2 | KPIs (≥ 5) | manual |
| QR3 | Trend vs. last quarter | chart |
| QR4 | ≥ 1 surprise / insight | manual |
| QR5 | Sign-off from executive sponsor | signature |

### 3.8 Renewal Proposal

| # | المعيار | القياس |
| - | --- | --- |
| RN1 | Decision خلال 14 يوم | timestamp |
| RN2 | Demonstrates value (Δ from baseline) | manual |
| RN3 | Pricing respects `pricing.md` | founder |
| RN4 | No fake urgency | manual |
| RN5 | Arabic voice compliance | Agent #14 |

### 3.9 Optimization Report

| # | المعيار | القياس |
| - | --- | --- |
| OR1 | ≤ 5 أيام عمل من الشهر | timestamp |
| OR2 | 1–2 A/B tests documented | manual |
| OR3 | Impact measured (delta) | data |
| OR4 | Next month hypotheses | manual |
| OR5 | Arabic voice compliance | Agent #14 |

## 4. عملية الإضافة (Adding a Criterion)

1. **PR** على `data/productized_services/acceptance_criteria.jsonl`.
2. **Format:**
   ```json
   {
     "acceptance_id": "acc_2026_xxx_NN",
     "service_id": "...",
     "deliverable_ref": "...",
     "criterion": "...",
     "measurement": "manual_review|word_count|api_check|...",
     "owner": "..."
   }
   ```
3. **مراجعة** من المؤسس + Agent #13.
4. **تحديث** هذا الـ doc.

## 5. المعايير الملغية (Deprecated)

أي معيار مُلغى ⇒ يُسجَّل في `CHANGELOG.md` مع السبب.

## 6. مخاطر

1. **Over-specification** ⇒ يبطئ التسليم.
2. **Subjective criteria** ⇒ خلاف في التفسير ⇒ manual review واضح.
3. **Missing measurement** ⇒ لا يمكن التحقق.

## 7. المراجع

- `data/productized_services/services.yaml` — catalog
- `data/productized_services/deliverables.jsonl` — records
- `data/productized_services/acceptance_criteria.jsonl` — records
- `docs/productized_services/PRODUCTIZED_SERVICES_OS_AR.md` — OS
- `docs/productized_services/DELIVERABLES_LIBRARY_AR.md` — deliverables
- `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` — claims
- `docs/localization/ARABIC_BRAND_VOICE_AR.md` — voice
