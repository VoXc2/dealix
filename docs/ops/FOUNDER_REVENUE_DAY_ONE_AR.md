# يوم الإيراد للمؤسس — تشغيل يومي واحد

**الغرض:** ترتيب صباح–مساء–جمعة يربط الاستراتيجية بالتنفيذ **بدون تشتت**.  
**الأمر الموحّد:** `bash scripts/run_founder_revenue_day.sh` (Windows: `powershell -File scripts/run_founder_revenue_day.ps1`)

**ثلاثية المستندات:**

| متى | الملف |
|-----|--------|
| استراتيجية / شهر | [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](../commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) |
| 5 دقائق صباحاً | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| تكتيك + سوشال + فهرس | [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) |

---

## صباحاً (~15–30 دقيقة)

| # | دقيقة | إجراء | أمر / رابط |
|---|-------|--------|------------|
| 1 | 2 | تشغيل الحزمة اليومية | `run_founder_revenue_day.sh` |
| 2 | 5 | Control Tower (أسئلة في Master Plan) | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| 3 | 5 | قراءة Founder Brief (يُطبع من السكربت) | `dealix_founder_daily_brief.py` |
| 4 | 5 | أعلى 10 targets — War Room | UI: `/ar/business-now` · API: `GET /api/v1/ops-autopilot/war-room/summary` |
| 5 | 5 | 3–5 مسودات لمسات (يدوي بعد موافقة) | `POST /api/v1/revenue-os/anti-waste/check` قبل أي إرسال |

**قواعد:** لا واتساب بارد · لا LinkedIn تلقائي · لا revenue قبل `invoice_paid`.

---

## نهاراً — تصنيف الردود

| التصنيف | الإجراء |
|---------|--------|
| interested | Diagnostic Scope + موعد |
| objection | سجّل في [objection_engine_registry.yaml](../commercial/operations/objection_engine_registry.yaml) — مسودة رد |
| wrong_segment | أرشف — لا متابعة |
| referral | شكر + طلب warm intro |
| silence | متابعة واحدة بعد ~5 أيام — لا spam |

تفصيل: [FOUNDER_SELL_MOTION_AR.md](FOUNDER_SELL_MOTION_AR.md)

---

## مساءً (~2 دقيقة)

سجّل **حدث أدلة واحد** على الأقل في:

[evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv)

أحداث مرجعية: `message_sent_manual` · `reply_received` · `demo_booked` · `scope_requested` · `invoice_sent` · `payment_received` · `proof_pack_delivered` · `partner_intro_created`

---

## جمعة (~20 دقيقة)

| إجراء | مرجع |
|--------|------|
| Scorecard أسبوعي | [COMMERCIAL_WEEKLY_SCORECARD_AR.md](../commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md) |
| حزمة محتوى أسبوعية (مسودات) | `python scripts/generate_commercial_content_pack.py` |
| صفحة AEO للأسبوع | [AEO_CONTENT_CALENDAR_AR.md](../commercial/operations/AEO_CONTENT_CALENDAR_AR.md) |
| 1 منشور LinkedIn من الحزمة (بعد موافقة) | [MARKETING_FACTORY.md](../marketing/MARKETING_FACTORY.md) |

---

## واجهات المنتج

| السطح | مسار |
|-------|------|
| Business NOW | `/ar/business-now` |
| Cloud / founder | `/ar/cloud` · `/ops/founder` (حسب النشر) |
| Approval queue | Approval Center في API/UI حسب البيئة |

---

## أسبوعياً — مولّد المحتوى

```bash
python scripts/generate_commercial_content_pack.py
```

المخرجات في `docs/commercial/operations/drafts/` (gitignored) — **لا نشر تلقائي**.

---

*آخر تحديث: 2026-05-17*
