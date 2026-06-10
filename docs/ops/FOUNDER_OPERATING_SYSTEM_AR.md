# نظام تشغيل المؤسس — Dealix Founder Operating System

**الغرض:** صورة واحدة لكيف «تعمل الشركة كل يوم» — أتمتة داخلية + موافقات المؤسس، بدون إرسال بارد.

**الوعد:** النظام يُولّد الأولويات والمسودات والتقارير؛ المؤسس يوافق وينفّذ ~10 لمسات بشرية.

**خطة المؤسس الشاملة (تنفيذ):** [FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md](FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md) · **Backlog 50+:** [FOUNDER_MAX_OPS_BACKLOG_AR.md](FOUNDER_MAX_OPS_BACKLOG_AR.md) · **مرساة اليوم (3 مراجع):** [FOUNDER_DAILY_ANCHOR_AR.md](FOUNDER_DAILY_ANCHOR_AR.md) · `py -3 scripts/founder_comprehensive_plan_status.py`

---

## 1) أمر صباحي واحد (canonical)

```bash
# موحّد (موصى به — أتمتة كاملة بحوكمة)
py -3 scripts/run_dealix_unified_founder_day.py

# أو الطبقة الكلاسيكية فقط:
bash scripts/run_founder_commercial_day.sh
```

| Flag | معنى |
|------|------|
| `--dry-run` | خطة فقط |
| `--with-business-now` | لقطة Business NOW |
| `--full` | business_now + `DEALIX_SYNC_EVIDENCE=1` على digest |

**بديل (wrapper):** `bash scripts/run_founder_revenue_day.sh` = commercial + business_now.

**مخرجات:**

- `data/founder_briefs/brief_YYYY-MM-DD.md`
- `data/founder_briefs/commercial_YYYY-MM-DD.md`
- `data/war_room_today.json`

---

## 2) ثلاثية المستندات

**المرساة اليومية الثلاث (ابدأ هنا):** [FOUNDER_DAILY_ANCHOR_AR.md](FOUNDER_DAILY_ANCHOR_AR.md) — ① هذا الملف · ② MASTER · ③ [DEALIX_REVENUE_WAR_ROOM_AR.md](DEALIX_REVENUE_WAR_ROOM_AR.md)

| الطبقة | متى | الملف |
|--------|-----|--------|
| Thesis + قمع + SoT | أسبوع/شهر | [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](../commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) |
| 5 دقائق صباحاً | كل يوم | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| أقوى خطة (134 مهمة + قرار أسبوعي) | أسبوع 0 / ريترو | [FOUNDER_STRONGEST_PLAN_AR.md](../commercial/FOUNDER_STRONGEST_PLAN_AR.md) · `python scripts/founder_strongest_plan_status.py` · حلقة أحد: `bash scripts/founder_weekly_loop.sh` |
| فل أوبس ذاتي كامل | أمر واحد | `python scripts/run_dealix_complete_autonomous_day.py` · `bash scripts/founder_cadence.sh --complete` |
| تكتيك + سوشال + ICP | تنفيذ عميق | [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) |
| يوم واحد (تفصيل) | مرجع يومي | [FOUNDER_REVENUE_DAY_ONE_AR.md](FOUNDER_REVENUE_DAY_ONE_AR.md) |
| 24 ساعة + CI | جدول زمني | [DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md](../commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md) |

---

## 3) جدول 24 ساعة (ملخص)

| الوقت | ماذا |
|-------|------|
| 04:00 UTC | [daily-revenue-machine.yml](../../.github/workflows/daily-revenue-machine.yml) — مسودات `draft_only` |
| 05:00 UTC أحد–خميس | [founder_commercial_daily.yml](../../.github/workflows/founder_commercial_daily.yml) |
| 06:00 UTC أحد | [founder_weekly_verify.yml](../../.github/workflows/founder_weekly_verify.yml) — `founder_weekly_loop.sh` + strongest-plan pytest |
| صباح KSA | `run_founder_commercial_day.sh` |
| نهار | 3–5 لمسات بعد موافقة |
| مساء | سطر في [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) |
| جمعة | scorecard + محتوى أسبوعي |

---

## 4) واجهات `/ops/*`

| مسار | الغرض |
|------|--------|
| `/ar/ops/founder` | لوحة يوم واحدة + sovereign GTM |
| `/ar/ops/war-room` | جدول 7 أعمدة + تحديث حالة |
| `/ar/ops/marketing` | مسودة LinkedIn اليوم |
| `/ar/ops/approvals` | مركز الموافقات |
| `/ar/ops/sales` | pipeline |
| `/ar/ops/evidence` | سجل أدلة |
| `/ar/ops` | hub — بطاقات سريعة |

**Business NOW:** `/ar/business-now`

---

## 5) استهداف دوّار (Motion A)

- Pool: [agency_accounts_seed.csv](../commercial/operations/targeting/agency_accounts_seed.csv)
- ICP: [icp_agency_wedge.yaml](../../dealix/config/icp_agency_wedge.yaml)
- تدوير يومي: `commercial_war_room_sync.py` يختار 10 P0 (cooldown 3 أيام)
- يدوي: `python scripts/rotate_agency_targets.py --dry-run` · `--apply`

---

## 6) محتوى أسبوعي + موافقات

```bash
python scripts/generate_weekly_content_drafts.py
python scripts/generate_commercial_content_pack.py   # weekly JSON + markdown drafts
python scripts/queue_content_drafts_for_approval.py --dry-run
python scripts/queue_content_drafts_for_approval.py   # يكتب في Approval Store محلياً
```

**لا نشر تلقائي** — انسخ إلى LinkedIn بعد الموافقة.

---

## 7) تحقق النظام

```bash
bash scripts/verify_founder_operating_system.sh
# أسبوعياً (CI): .github/workflows/founder_weekly_verify.yml
py -3 scripts/verify_commercial_launch_ready.py
```

**Dogfooding:** `py -3 scripts/founder_dogfooding_war_room_sync.py` — [DEALIX_DOGFOODING_WAR_ROOM_AR.md](DEALIX_DOGFOODING_WAR_ROOM_AR.md)

---

## 8) حوكمة (ثابت)

- لا cold WhatsApp · لا LinkedIn/Gmail آلي · لا revenue قبل `invoice_paid`
- كل إرسال خارجي: مسودة + موافقة + `POST /api/v1/revenue-os/anti-waste/check`

---

*آخر تحديث: 2026-05-18*
