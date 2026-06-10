# مكتبة المخرجات — Dealix Deliverables Library (AR)

> **مكتبة مرجعية لكل deliverable قابل للتسليم.** كل خدمة في
> `services.yaml` تستهلك عدداً من هذه المخرجات. كل مخرج له: اسم،
> قالب مرجعي، صيغة، owner، معيار قبول.

**الحالة:** مسودة — Phase 3 من Agent #15
**التاريخ:** 2026-06-03

---

## 1. المخرجات الأساسية (Core Deliverables)

### 1.1 Proof Pack

- **الاسم:** حزمة إثبات (PDF)
- **القالب:** `data/templates/proof_pack_ar.md`
- **الصيغة:** PDF (8-12 صفحة)
- **Owner:** Dealix founder
- **الاستخدام:** Revenue Leakage Diagnostic, Follow-up Recovery,
  Pilot closure
- **Acceptance:** ≥ 3 leaks موثّقة + 3 توصيات مرتبة + خطة 30 يوم

### 1.2 Proposal

- **الاسم:** عرض (PDF / DOCX)
- **القالب:** `data/templates/proposal_499_sar_ar.md`
- **الصيغة:** PDF / DOCX (800–2000 كلمة)
- **Owner:** Dealix
- **الاستخدام:** كل service قبل البدء
- **Acceptance:** Signed by client

### 1.3 WhatsApp Templates (10)

- **الاسم:** 10 قوالب WhatsApp
- **القالب:** `data/templates/whatsapp_templates_collection.md`
- **الصيغة:** Meta-approved template
- **Owner:** Dealix
- **الاستخدام:** Follow-up Recovery Workflow
- **Acceptance:** 10 templates معتمدة من العميل (case_study_permissions)

### 1.4 Runbook

- **الاسم:** Runbook الموظف
- **القالب:** TBD
- **الصيغة:** Markdown / PDF
- **Owner:** Dealix
- **الاستخدام:** Follow-up Recovery Workflow
- **Acceptance:** ≥ 4 سيناريوهات موثّقة

### 1.5 Weekly Report

- **الاسم:** تقرير أسبوعي
- **القالب:** TBD
- **الصيغة:** Markdown / Email
- **Owner:** Dealix
- **الاستخدام:** كل service متكرر
- **Acceptance:** ≤ 800 كلمة + جدول أرقام

### 1.6 Onboarding Welcome Message

- **الاسم:** رسالة ترحيب
- **القالب:** TBD
- **الصيغة:** Email / WhatsApp
- **Owner:** Dealix
- **الاستخدام:** كل service عند البدء
- **Acceptance:** خلال 24 ساعة من التوقيع

### 1.7 Daily Brief

- **الاسم:** الموجز اليومي
- **القالب:** TBD
- **الصيغة:** WhatsApp / Email
- **Owner:** Dealix
- **الاستخدام:** AI Revenue Ops Starter
- **Acceptance:** يوصل 8:00 AM ± 30 دقيقة

### 1.8 Quarterly Review

- **الاسم:** مراجعة ربع سنوية
- **القالب:** TBD
- **الصيغة:** Slides + 60-min call
- **Owner:** Dealix + client
- **الاستخدام:** Full Revenue OS
- **Acceptance:** Action items مسجّلة

### 1.9 Renewal Proposal

- **الاسم:** عرض تجديد
- **القالب:** TBD
- **الصيغة:** PDF
- **Owner:** Dealix
- **الاستخدام:** قبل انتهاء العقد بـ 30 يوم
- **Acceptance:** Decision خلال 14 يوم

### 1.10 Optimization Report

- **الاسم:** تقرير تحسين
- **القالب:** TBD
- **الصيغة:** Markdown / PDF
- **Owner:** Dealix
- **الاستخدام:** Monthly Optimization Retainer
- **Acceptance:** ≤ 5 أيام عمل من الشهر

## 2. مخرجات متخصصة (Specialized)

### 2.1 Risk Score

- **API:** `GET /api/v1/kpi/health-score`
- **الاستخدام:** Pilot triage

### 2.2 Customer Readiness

- **API:** integrated in `/api/v1/leads`
- **الاستخدام:** Pipeline qualification

### 2.3 Proof Event

- **API:** `POST /api/v1/proof-events`
- **الاستخدام:** Proof ledger

## 3. القوالب المرجعية (Reference Templates)

كل deliverable يشير إلى قالب في `data/templates/`:

| Deliverable | Template |
| --- | --- |
| Proof Pack | `data/templates/proof_pack_ar.md` |
| Proposal | `data/templates/proposal_499_sar_ar.md` |
| Warm Intro (WhatsApp) | `data/templates/warm_intro_whatsapp_ar.md` |
| Daily Checklist | `data/templates/founder_daily_checklist.md` |
| WhatsApp Templates | `data/templates/whatsapp_templates_collection.md` |

## 4. عملية الإضافة (Adding a Deliverable)

1. **قالب** جديد في `data/templates/`.
2. **Entry** في `deliverables.jsonl`:
   ```json
   {
     "deliverable_id": "del_2026_xxx_01",
     "name": "...",
     "template_ref": "data/templates/...",
     "format": "pdf|md|docx|...",
     "due_offset_days": 5,
     "owner": "..."
   }
   ```
3. **Acceptance criteria** في `acceptance_criteria.jsonl`.
4. **PR** + مراجعة.

## 5. المخاطر

1. **Template drift** ⇒ كل تحديث للقالب يحتاج PR.
2. **Missing owner** ⇒ لا يُسلَّم deliverable.
3. **Over-customization** ⇒ scope creep.

## 6. المراجع

- `data/productized_services/services.yaml` — catalog
- `data/productized_services/deliverables.jsonl` — records
- `data/productized_services/acceptance_criteria.jsonl` — criteria
- `docs/productized_services/PRODUCTIZED_SERVICES_OS_AR.md` — OS
- `docs/productized_services/ACCEPTANCE_CRITERIA_LIBRARY_AR.md` — criteria lib
- `data/templates/` — template source
