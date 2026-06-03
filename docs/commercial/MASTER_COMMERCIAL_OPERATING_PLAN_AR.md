# Master Commercial Operating Plan — خطة تصريف Dealix التجارية الشاملة

**الغرض:** نقطة دخول يومية واحدة للمؤسس — يربط الاستراتيجية، الغرفة، الأدلة، المراحل، والحوكمة **دون** تغيير اتجاه المنتج.

**مرساة اليوم (مع War Room + Founder OS):** [../ops/FOUNDER_DAILY_ANCHOR_AR.md](../ops/FOUNDER_DAILY_ANCHOR_AR.md) · **تنفيذ الخطة الشاملة:** [../ops/FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md](../ops/FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md)

**مراجعة شاملة (36 قسمًا):** [COMMERCIAL_OPS_QUICK_REFERENCE_AR.md](COMMERCIAL_OPS_QUICK_REFERENCE_AR.md) · [COMMERCIAL_VALUE_MAP_AR.md](COMMERCIAL_VALUE_MAP_AR.md) · [MARKET_INTELLIGENCE_MASTER_INDEX_AR.md](MARKET_INTELLIGENCE_MASTER_INDEX_AR.md)

**المرجع الشامل (استراتيجية + سوشال + استهداف + تكتيك + تعظيم قيمة):** [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) · [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md).  
**أقوى خطة موسّعة (134 مهمة + قرار أسبوعي + ريترو):** [FOUNDER_STRONGEST_PLAN_AR.md](FOUNDER_STRONGEST_PLAN_AR.md) · `python scripts/founder_strongest_plan_status.py`  
**تشغيل يومي موحّد:** [FOUNDER_REVENUE_DAY_ONE_AR.md](../ops/FOUNDER_REVENUE_DAY_ONE_AR.md) · `bash scripts/run_founder_revenue_day.sh` (أو `run_founder_commercial_day.sh` بدون business_now) — هذا الملف **5 دقائق** بعد الموجز.

**القرار الحالي:** لا بناء مزايا جديدة قبل **أول Diagnostic مدفوع + Proof Pack مسلّم**. استخدم ما بُني.

---

## Soft Launch vs Paid Launch

| مرحلة | ماذا يعني | تحقق |
|-------|-----------|------|
| **Soft Launch (الآن)** | صفحة بيع عامة `/ar` · funnel · آلة يومية · فواتير يدوية | [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](COMMERCIAL_LAUNCH_CHECKLIST_AR.md) · `py -3 scripts/verify_commercial_launch_ready.py` |
| **Paid Launch (لاحقاً)** | Moyasar live · HubSpot · Calendly · PostHog | [../LAUNCH_GATES.md](../LAUNCH_GATES.md) — FOUNDER_ACTION |

**لا ادعاء** «إطلاق كامل» حتى اكتمال بوابات LAUNCH_GATES (24/30+). Soft Launch **لا يفعّل** إرسال بارد أو LinkedIn آلي.

### FOUNDER_ACTION (Paid Launch)

| تكامل | إجراء |
|--------|--------|
| Moyasar | مفاتيح test/live → G2 checkout |
| HubSpot + Calendly | tokens → lead E2E (G3) |
| PostHog | API key → funnel (O3) |
| Gmail OAuth | مسودات بريد — [GMAIL_OAUTH_SETUP_CHECKLIST.md](../ops/GMAIL_OAUTH_SETUP_CHECKLIST.md) |

أول Diagnostic: [operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md) + [MANUAL_PAYMENT_SOP.md](../ops/MANUAL_PAYMENT_SOP.md).

---

## مرجعان يوميان (ابدأ هنا كل صباح)

| # | المستند | متى |
|---|---------|-----|
| 1 | [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) | Control Tower، 4 Motions، SOAEN، Offer Matrix، AEO، شركاء |
| 2 | [FULL_OPS_CLOSE_ENGINE_AR.md](FULL_OPS_CLOSE_ENGINE_AR.md) | هندسة قرار الشراء، Champion/Procurement، زوايا الإغلاق |

**ثم افتح التشغيل:** [operations/README.md](operations/README.md) — مسار الإغلاق، تتبع الأحداث، DoD، Motion A، شركاء، AEO، scorecard، حوكمة.

---

## مسار اليوم (5 دقائق)

**أمر واحد (أقصى أتمتة بحوكمة — صباح):** `bash scripts/founder_one_command.sh` · تحقق: `py -3 scripts/verify_full_autonomous_ops_stack.py` · واجهة: `/ar/ops/founder` · [FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md](FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md)

1. **Control Tower** — أجب عن: أفضل شريحة؟ رسالة؟ Proof؟ اعتراض؟ توقف؟ شريك؟ waste؟ no-build؟  
2. **War Room** — [DEALIX_REVENUE_WAR_ROOM_AR.md](../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) — أعلى 10 targets + متابعات + أحداث أدلة اليوم.  
3. **Evidence** — سجّل حدثاً واحداً على الأقل في [operations/evidence_events_tracker.csv](operations/evidence_events_tracker.csv).  
4. **مساءً** — `py -3 scripts/founder_evening_evidence.py --append` · [COMMERCIAL_WEEKLY_SCORECARD_AR.md](operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md) (جمعة).

---

## المراحل (خريطة تنفيذ)

| مرحلة | الهدف | مرجع |
|-------|--------|------|
| 0 | آلة إغلاق + Discovery قبل ديمو | [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md) |
| 1 | أول `payment_received` + `proof_pack_delivered` | [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md) |
| 2 | تكرار Motion A (وكالة) | [operations/motion_a_agency/](operations/motion_a_agency/) |
| 3 | شريك + إحالة | [PARTNER_ONBOARDING_KIT_AR.md](operations/PARTNER_ONBOARDING_KIT_AR.md) |
| 4 | AEO + Objection Engine | [AEO_CONTENT_CALENDAR_AR.md](operations/AEO_CONTENT_CALENDAR_AR.md) · [objection_engine_registry.yaml](operations/objection_engine_registry.yaml) |
| 5 | منصة | بعد تكرار الأدلة — لا تسبق الإيراد |

---

## SOAEN (في كل touchpoint)

**Source → Owner → Approval → Evidence → Next Action** — تفصيل في [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) §4.

---

## Motions (توجيه سريع)

| Motion | متى | مسار |
|--------|-----|------|
| **A** Agency | وكالة/حملات لعملاء | Audit → Agency Proof Pack → Co-sell → Partner |
| **B** Direct | عيادة/عقار/B2B متابعة | Risk Score → Audit → Diagnostic → Sprint |
| **C** Consultant | CRM/automation | Diagnostic layer → Handoff → Proof layer |
| **D** Executive | CEO/حوكمة AI | RevOps Diagnostic → Executive OS → Retainer |

**الوتد الحالي:** Motion **A** أولاً.

---

## أدوات جاهزة

| أداة | مسار |
|------|------|
| Sales Kit | [../sales-kit/START_HERE.md](../sales-kit/START_HERE.md) |
| حزم وأسعار | [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) |
| Proof Pack (تسليم) | [../delivery/PROOF_PACK_TEMPLATE.md](../delivery/PROOF_PACK_TEMPLATE.md) |
| Sample Proof (مغناطيس) | [operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md](operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md) |
| غرفة تصريف | [DEALIX_REVENUE_WAR_ROOM_AR.md](../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) |
| حلقة يومية | [DAILY_COMMERCIAL_LOOP_AR.md](../ops/DAILY_COMMERCIAL_LOOP_AR.md) |
| حوكمة قنوات | [COMMERCIAL_GOVERNANCE_GATES_AR.md](operations/COMMERCIAL_GOVERNANCE_GATES_AR.md) |

---

## مؤشر أسبوعي واحد (قبل التوسع)

**Pilots النشطة** + **Proof Packs مسلّمة هذا الأسبوع** — قالب في [COMMERCIAL_WEEKLY_SCORECARD_AR.md](operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md).

---

## آلة اليوم الكاملة (Sovereign GTM — governed autopilot)

**أمر واحد صباحاً:**

```bash
bash scripts/run_founder_commercial_day.sh
# Windows: powershell -File scripts/run_founder_commercial_day.ps1
# يوم كامل (بوابات + مساء): powershell -File scripts/run_value_plan_day.ps1
# لقطة موحّدة: py -3 scripts/export_value_plan_snapshot.py
# API: GET /api/v1/ops-autopilot/founder/value-plan
```

**ماذا يشغّل:** موجز مؤسس · مزامنة War Room (`data/war_room_today.json`) · **استيراد أهداف CSV** (`import_war_room_targets.py --apply`) · Commercial Digest · منشور LinkedIn اليوم (مسودة).

**للتوسّع (Business NOW + كل sub-steps):** `bash scripts/run_founder_revenue_day.sh` — لا يستبدل الأمر أعلاه؛ يكمّله عند الحاجة.

**اختياري:**

| متغير / أمر | الغرض |
|-------------|--------|
| `DEALIX_SYNC_EVIDENCE=1` | مزامنة CSV → `POST /api/v1/evidence/events` |
| `DEALIX_BUSINESS_NOW_QUICK=1` | لقطة Business NOW |
| `python scripts/commercial_war_room_sync.py --trigger-targeting` | مسودات email (draft_only) |

**Secrets (GitHub Actions + محلي):**

| Secret | الاستخدام |
|--------|-----------|
| `DEALIX_API_BASE` | API للوحة + evidence sync |
| `DEALIX_ADMIN_API_KEY` | `X-Admin-API-Key` |
| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة الأحداث |

**Cron:** [.github/workflows/founder_commercial_daily.yml](../../.github/workflows/founder_commercial_daily.yml) (05:00 UTC Sun–Thu) · مسودات بريد/LinkedIn: [daily-revenue-machine.yml](../../.github/workflows/daily-revenue-machine.yml).

**Config:** [dealix/config/social_content_queue.yaml](../../dealix/config/social_content_queue.yaml) · [dealix/config/icp_agency_wedge.yaml](../../dealix/config/icp_agency_wedge.yaml) · [operations/targeting/agency_accounts_seed.csv](operations/targeting/agency_accounts_seed.csv).

**سياسة:** نظامي بالكامل — **الإرسال الخارجي بموافقة يدوية** (لا cold WhatsApp · لا LinkedIn آلي).

---

*آخر تحديث: 2026-05-17 — مرجع تنفيذي؛ لا يستبدل العقود أو [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).*
