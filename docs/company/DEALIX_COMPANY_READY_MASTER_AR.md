# Dealix — الشركة جاهزة (محور التشغيل الشامل)

**الغرض:** نقطة دخول **واحدة** للمؤسس — تربط الاستراتيجية، التشغيل اليومي الآلي، التسعة أنظمة، CI، الواجهة، والتحقق — دون البحث في مئات الملفات.

**الوعد:** «الشركة تعمل لوحدها» = كل يوم يُولَّد: مسودات إيراد، أولويات War Room، موجز مؤسس، مسودة سوشال، تذكير أدلة — وأنت توافق وتلمس (~10 لمسات). **ليس** إرسالاً آلياً بلا موافقة.

**حد أمان:** لا واتساب بارد · لا LinkedIn auto-DM · لا Gmail خارجي بدون موافقة · لا أرقام CRM وهمية.

---

## 1) ابدأ هنا — ثلاثة أوامر

| متى | الأمر | ماذا يفعل |
|-----|--------|-----------|
| **Soft Launch (بوابة واحدة)** | `bash scripts/verify_dealix_commercial_go_live.sh` | Founder OS + commercial + company ready |
| **تحقق جاهزية** (أسبوعي) | `bash scripts/company_ready_verify.sh` | وثائق + pytest تجاري + orchestrator |
| **صباح canonical** | `bash scripts/run_founder_commercial_day.sh` | brief + War Room + outreach drafts + digest + AEO |
| **صباح + Business NOW** | `bash scripts/run_founder_revenue_day.sh` | wrapper فوق commercial |
| **إطلاق Railway** | `bash scripts/official_launch_verify.sh` | prod API (اختياري) |

Windows: `scripts/company_ready_verify.ps1` · `run_founder_revenue_day.ps1` · `run_founder_commercial_day.ps1`

---

## 2) مقارنة سكربتات الصباح

| | `run_founder_commercial_day` | `run_founder_revenue_day` |
|---|-------------------------------|---------------------------|
| Business NOW | اختياري `--with-business-now` | نعم (wrapper) |
| Founder brief | نعم | نعم |
| KPI commercial `--status` | ضمن المسار | نعم |
| War Room sync | نعم | نعم |
| Commercial digest | نعم | نعم |
| Social queue اليوم | نعم | نعم |
| AEO أسبوع + verdict | نعم (خطوة 6/6) | نعم (wrapper يشمل commercial) |
| مسودات لمسة P0 | نعم (`outreach_drafts`) | نعم |
| المدة التقريبية | 5–15 دقيقة | 15–30 دقيقة |

**مرجع يومي تفصيلي:** [FOUNDER_REVENUE_DAY_ONE_AR.md](../ops/FOUNDER_REVENUE_DAY_ONE_AR.md) · [DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md](../commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md)

---

## 3) جدول CI (تشغيل آلي)

| Workflow | التوقيت (UTC) | المخرج | إرسال خارجي |
|----------|---------------|--------|-------------|
| [daily-revenue-machine.yml](../../.github/workflows/daily-revenue-machine.yml) | 04:00 يومياً | مسودات Gmail/LinkedIn + followups + تقرير | **لا** — `draft_only` |
| [founder_commercial_daily.yml](../../.github/workflows/founder_commercial_daily.yml) | 05:00 أحد–خميس | brief + digest artifacts | **لا** |
| [business_now_snapshot.yml](../../.github/workflows/business_now_snapshot.yml) | مجدول | لقطة Business NOW | **لا** |
| [cto_weekly_anchor.yml](../../.github/workflows/cto_weekly_anchor.yml) | اثنين 06:00 | checklist + KPIs | **لا** |
| [founder_content_weekly.yml](../../.github/workflows/founder_content_weekly.yml) | جمعة 06:00 | حزمة محتوى أسبوعية (artifact) | **لا** |

**Secrets (GitHub):** `DEALIX_API_BASE` · `DEALIX_API_KEY` (revenue-machine) · `DEALIX_ADMIN_API_KEY` (اختياري للـ digest sync) · `DEALIX_SYNC_EVIDENCE=1` (اختياري)

---

## 4) يوم المؤسس (90 دقيقة)

```mermaid
flowchart LR
  auto [CI_04UTC_drafts]
  morning [run_founder_revenue_day]
  approve [Approvals_WarRoom]
  touches [10_touches_manual]
  evidence [evidence_csv]
  evening [founder_daily_scorecard]
  auto --> morning --> approve --> touches --> evidence --> evening
```

| كتلة | إجراء | مرجع |
|------|--------|------|
| صباح | تشغيل revenue day + قراءة الموجز | هذا الملف §1 |
| 5 دقائق | Control Tower | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| نهار | موافقات + لمسات + Discovery قبل ديمو | [FOUNDER_SELL_MOTION_AR.md](../ops/FOUNDER_SELL_MOTION_AR.md) |
| مساء | scorecard + صف في CSV أدلة | [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) |
| جمعة | scorecard أسبوعي + حزمة محتوى | [COMMERCIAL_WEEKLY_SCORECARD_AR.md](../commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md) |

---

## 5) التسعة أنظمة → أين تقرأ

| نظام | مرجع تشغيل | كود / API |
|------|------------|-----------|
| Strategy | [DEALIX_AI_OPERATING_COMPANY_AR.md](../commercial/DEALIX_AI_OPERATING_COMPANY_AR.md) §1 | `strategy_os` |
| Data | نفس المرجع §2 | `data_os` · Source Registry |
| Governance | [APPROVAL_POLICY.md](../governance/APPROVAL_POLICY.md) · [SOAEN](../empire/SOAEN_STANDARD.md) | `governance_os` |
| Delivery | [PROOF_PACK_TEMPLATE.md](../delivery/PROOF_PACK_TEMPLATE.md) | `delivery_os` |
| Value | [PROOF_PACK_STANDARD.md](../empire/PROOF_PACK_STANDARD.md) | `value_os` |
| Sales / GTM | [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](../commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) | `revenue_ops_autopilot` · War Room |
| Support | [SUPPORT_AUTOPILOT.md](../support/SUPPORT_AUTOPILOT.md) | `support` router |
| Partners | [PARTNER_ONBOARDING_KIT_AR.md](../commercial/operations/PARTNER_ONBOARDING_KIT_AR.md) | `partners` |
| Capital / FinOps | [CAPITAL_MODEL.md](../empire/CAPITAL_MODEL.md) | KPI import |

**خريطة كود:** [CODE_MAP_OS_TO_MODULES_AR.md](../commercial/CODE_MAP_OS_TO_MODULES_AR.md)

---

## 6) عمق تجاري (لا تستبدل هذا الملف)

| الطبقة | الملف |
|--------|--------|
| فهرس إيراد | [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](../commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) |
| استراتيجية + سوشال + استهداف | [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) |
| 5 دقائق صباحاً | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| أسعار عقود (SoT) | [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) |
| empire/ استراتيجية شركة | [../empire/](../empire/) |

---

## 7) محتوى وسوشال (أي سكربت؟)

| سكربت | متى | مخرج |
|--------|-----|------|
| `social_queue_today.py` | **يومي** (ضمن commercial day) | منشور LinkedIn اليوم للمراجعة |
| `generate_commercial_content_pack.py` | **جمعة** | `docs/commercial/operations/drafts/` |
| `generate_weekly_content_drafts.py` | عند الحاجة | `var/content_drafts/YYYY-Www.json` |

تفصيل: [operations/README.md](../commercial/operations/README.md)

---

## 8) واجهة المؤسس

| مسار | الغرض |
|------|--------|
| `/[locale]/ops/founder` | لوحة مؤسس + War Room + روابط سريعة |
| `/[locale]/ops/war-room` | جدول 7 أعمدة |
| `/[locale]/approvals` | موافقات قبل إرسال |
| `/[locale]/business-now` | قرار استراتيجي + simulate |
| `/[locale]/cloud` | مركز Cloud |
| `/[locale]/ops/marketing` | تسويق تشغيلي |
| `/[locale]/ops/evidence` | سجل أدلة |

**متغير UI:** `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` للوحات ops.

---

## 9) مؤشرات أسبوعية (قبل التوسع)

- **Pilots نشطة** + **Proof Packs مسلّمة** — [COMMERCIAL_WEEKLY_SCORECARD_AR.md](../commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md)
- أحداث أدلة من [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv)
- KPI حقيقي فقط: `kpi_founder_commercial_import.yaml` + `apply_kpi_founder_commercial.py`

---

## 10) تحقق سريع

```bash
bash scripts/company_ready_verify.sh
# أو وثائق فقط:
bash scripts/company_ready_verify.sh --docs-only
```

عند **PASS:** شغّل `run_founder_revenue_day.sh` ثم راجع `/ar/ops/founder`.

---

*آخر تحديث: 2026-05-17 — محور شركة؛ لا يستبدل العقود أو [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md).*
