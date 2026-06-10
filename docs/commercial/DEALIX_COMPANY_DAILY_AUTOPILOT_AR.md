# تشغيل الشركة اليومي — Dealix Commercial Autopilot

**الغرض:** وصف كيف «تعمل الشركة كل يوم» — أتمتة داخلية + موافقات المؤسس — دون كسر حوكمة Dealix.

**الوعد التشغيلي:** النظام يُولّد يومياً مسودات، أولويات War Room، تقارير، ولقطة Business NOW. المؤسس يوافق وينفّذ ~10 لمسات بشرية موافَق عليها.

**المحور الشامل (شركة جاهزة):** [DEALIX_COMPANY_READY_MASTER_AR.md](../company/DEALIX_COMPANY_READY_MASTER_AR.md)

**المراجع العليا:** [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) · [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) · [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md).

---

## 0) أي سكربت صباحاً؟

| السيناريو | الأمر |
|-----------|--------|
| **صباح كامل** (Business NOW + AEO verdict) | `bash scripts/run_founder_revenue_day.sh` |
| **صباح خفيف** (تجاري فقط) | `bash scripts/run_founder_commercial_day.sh` |
| **تحقق جاهزية** | `bash scripts/company_ready_verify.sh` |

جدول مقارنة: [DEALIX_COMPANY_READY_MASTER_AR.md §2](../company/DEALIX_COMPANY_READY_MASTER_AR.md#2-مقارنة-سكربتات-الصباح) · يوم واحد: [FOUNDER_REVENUE_DAY_ONE_AR.md](../ops/FOUNDER_REVENUE_DAY_ONE_AR.md)

---

## 1) جدول 24 ساعة (مرجع KSA / UTC)

| الوقت | ماذا | آلية |
|-------|------|------|
| **04:00 UTC** (07:00 KSA تقريباً) | مسودات إيراد + متابعات + تقرير يومي | GitHub [`daily-revenue-machine.yml`](../../.github/workflows/daily-revenue-machine.yml) |
| **صباح KSA** | موجز مؤسس + War Room + تذكير أدلة | `bash scripts/run_founder_commercial_day.sh` |
| **10:00–18:00 KSA** | موافقات، لمسات، ديمو، Discovery | يدوي — [FOUNDER_SELL_MOTION_AR.md](../ops/FOUNDER_SELL_MOTION_AR.md) |
| **مساء KSA** | Scorecard | `python scripts/founder_daily_scorecard.py --fill` |
| **أسبوعي (أحد)** | CTO anchor + checklist | [`cto_weekly_anchor.yml`](../../.github/workflows/cto_weekly_anchor.yml) |
| **عند الحاجة** | Business NOW snapshot | [`business_now_snapshot.yml`](../../.github/workflows/business_now_snapshot.yml) أو `scripts/run_business_now.sh` |

---

## 2) ما يعمل تلقائياً (بدون إرسال خارجي)

| Workflow / أمر | المخرجات |
|----------------|----------|
| `daily-revenue-machine` | `POST /api/v1/automation/revenue-machine/run` — `approval_mode: draft_only` |
| نفس الـ workflow | `POST /api/v1/automation/followups/run` |
| نفس الـ workflow | `POST /api/v1/automation/daily-report/generate` |
| `business_now_snapshot` | تحديث لقطة Business NOW |
| `daily_digest` | ملخص تشغيلي (إن مُفعّل) |
| `generate_weekly_content_drafts.py` | 5 مسودات LinkedIn → `var/content_drafts/` (لا نشر) |

**قاعدة:** أي خطوة تلمس عميلاً خارجياً = **مسودة في صندوق الموافقات** أو إرسال يدوي بعد موافقة.

---

## 3) ما يحتاج موافقة المؤسس

| الإجراء | بوابة |
|---------|--------|
| إرسال Gmail / LinkedIn | Approval Center · لا auto-DM |
| `message_sent_manual` | سجّل في [evidence_events_tracker.csv](operations/evidence_events_tracker.csv) |
| فاتورة / `invoice_sent` | نطاق معتمد — [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) |
| Proof Pack نهائي | مراجعة بشرية — [PROOF_PACK_TEMPLATE.md](../delivery/PROOF_PACK_TEMPLATE.md) |
| واتساب لعميل | **دافئ فقط** — لا cold blast |

**حوكمة قنوات:** [operations/COMMERCIAL_GOVERNANCE_GATES_AR.md](operations/COMMERCIAL_GOVERNANCE_GATES_AR.md) · [../governance/APPROVAL_POLICY.md](../governance/APPROVAL_POLICY.md).

---

## 4) Secrets وبيئة (قائمة تحقق)

### GitHub Actions (إنتاج)

| Secret | الاستخدام |
|--------|-----------|
| `DEALIX_API_BASE` | أساس URL للـ API (مثلاً `https://api.dealix.me`) |
| `DEALIX_API_KEY` | Bearer لـ revenue-machine |

بدونها: الـ workflow يتخطى التشغيل برسالة واضحة (لا فشل ضوضائي).

### محلي

| متغير | الاستخدام |
|--------|-----------|
| `DEALIX_API_URL` أو `NEXT_PUBLIC_API_URL` | افتراضي `http://localhost:8000` |
| `DEALIX_ADMIN_API_KEY` | `X-Admin-API-Key` لـ War Room و ops-autopilot |
| `APP_ENV=development` | لا إرسال خارجي تلقائي |

---

## 5) مسارات API و UI

| الغرض | المسار |
|--------|--------|
| **مركز قيادة المؤسس (صباح واحد)** | UI [`/[locale]/ops/founder`](../../frontend/src/app/[locale]/ops/founder/page.tsx) · [`FounderCommandCenter.tsx`](../../frontend/src/components/gtm/FounderCommandCenter.tsx) |
| War Room (قائمة) | `GET /api/v1/ops-autopilot/war-room?needs_follow_up=true&top_n=10` |
| War Room (ملخص) | `GET /api/v1/ops-autopilot/war-room/summary` |
| استهداف P0 | `GET /api/v1/ops-autopilot/targeting/pool` · `GET .../targeting/p0-today` · UI [`/ops/targeting`](../../frontend/src/app/[locale]/ops/targeting/page.tsx) |
| لوحة مؤسس | `GET /api/v1/ops-autopilot/founder-dashboard` |
| Revenue machine | `POST /api/v1/automation/revenue-machine/run` |
| Business NOW | `/ar/business-now` · API `GET /api/v1/business-now/snapshot` |
| War Room جدول | [`RevenueWarRoomTable.tsx`](../../frontend/src/components/gtm/RevenueWarRoomTable.tsx) |

---

## 6) سكربت الصباح الواحد

```bash
# من جذر المستودع
bash scripts/run_founder_commercial_day.sh

# بدون استدعاء API
bash scripts/run_founder_commercial_day.sh --dry-run

# مع Business NOW (أطول)
bash scripts/run_founder_commercial_day.sh --with-business-now
```

Windows:

```powershell
.\scripts\run_founder_commercial_day.ps1
.\scripts\run_founder_commercial_day.ps1 -DryRun
```

**التسلسل:** `run_dealix_daily_ops` → موجز `dealix_founder_daily_brief` → War Room sync + استيراد CSV → digest → سوشال → `data/war_room_today.json` → واجهة **`/ops/founder`** (War Room + موافقات + P0 + سوشال).

**تحقق إنتاج (اختياري):** `DEALIX_API_BASE=https://api.example.com python scripts/prod_smoke_check.py`

---

## 7) حلقة المحتوى الأسبوعية

1. **أحد/اثنين:** `python scripts/generate_weekly_content_drafts.py` — 5 مسودات LinkedIn من [AEO_CONTENT_CALENDAR_AR.md](operations/AEO_CONTENT_CALENDAR_AR.md) + [objection_engine_registry.yaml](operations/objection_engine_registry.yaml).
2. **مراجعة:** المؤسس يعدّل وينشر يدوياً (لا أتمتة نشر).
3. **بعد كل call:** حدّث اعتراضاً في Objection Engine → منشور الأسبوع التالي.

**KPI مرجعية:** 5 منشورات/أسبوع · نشرة/أسبوع · webinar/شهر — [MARKETING_FACTORY.md](../marketing/MARKETING_FACTORY.md).

---

## 8) مؤشرات نجاح يومية

- [ ] حدث أدلة واحد على الأقل في `evidence_events_tracker.csv`
- [ ] مسودات جديدة رُاجعت في Approval Center (إن وُجدت)
- [ ] أعلى 10 targets من War Room مُلمَسة أو مُجدولة
- [ ] لا `payment_received` وهمي — إيراد من دفع حقيقي فقط
- [ ] مساءً: scorecard مكتمل

**مؤشر أسبوعي:** Pilots نشطة + Proof Packs مسلّمة — [COMMERCIAL_WEEKLY_SCORECARD_AR.md](operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md).

---

## 9) تحقق الجاهزية

```bash
bash scripts/founder_go_live_verify.sh
```

يشمل فحوص التجاري (أطلس، سيادي، هذا الملف، orchestrator، workflow).

---

*آخر تحديث: 2026-05-17 — تشغيل يومي؛ العقود: [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).*
