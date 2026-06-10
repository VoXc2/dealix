# Full Ops Autonomous — تشغيل تجاري ذاتي كامل (بحوكمة)

**الغرض:** أقصى أتمتة ممكنة **بدون** كسر non-negotiables — مقارنة بأفضل ممارسات GTM 2026 ثم التنفيذ في Dealix.

---

## مقارنة البحث (2025–2026) vs Dealix

| بعد | السوق (بحث) | Dealix | الأفضل؟ |
|-----|-------------|--------|---------|
| طبقات الأدوات | 4–6 مدمجة | Revenue OS + War Room + Approvals | نعم — أقل تشتيت |
| الإرسال | مسودة ثم موافقة؛ autonomous لاحقاً لقنوات منخفضة المخاطر | **دائماً** موافقة قبل خارجي | نعم للسعودية/PDPL |
| 2026 consensus | AI يمسود — المؤسس يوافق ويرسل؛ لا autosend كامل | strongest_ops + cockpit + complete day | نعم — يطابق Leadyra/Gangly HITL |
| ABM | موجات حسابات | موجة 1–3 في `gtm_abm_wave1.yaml` | نعم |
| القياس | TTV · retention | evidence CSV + TTV في GTM stack | نعم |
| الإغلاق | بشري فقط | founder-led حتى تكرار الرسالة | نعم |

**الخلاصة:** «فل أوبس ذاتي» هنا = **كل ما يمكن آليّاً داخل الريبو**؛ ليس إرسالاً بارداً أو إغلاق صفقات بالذكاء الاصطناعي.

---

## أمر واحد (موصى به — أقصى أتمتة)

```bash
# أقصى تغطية (حوكمة + commercial day + full ops core):
bash scripts/founder_one_command.sh
powershell -File scripts/founder_one_command.ps1
py -3 scripts/run_dealix_complete_autonomous_day.py
py -3 scripts/run_dealix_complete_autonomous_day.py --dry-run   # خطة فقط
py -3 scripts/verify_full_autonomous_ops_stack.py             # بوابة PASS/FAIL

# بديل أخف (بدون commercial day الكامل):
py -3 scripts/run_dealix_unified_founder_day.py
py -3 scripts/run_dealix_unified_founder_day.py --quick
```

`run_dealix_complete_autonomous_day.py` يشغّل: governed morning → strongest ops → `run_founder_commercial_day` → full ops core → `founder_strongest_plan_status` (+ مساء/أسبوع اختياري).

**مقارنة بحث 2026 (ProductQuant · Athenic · RevOps cadence):**

| ممارسة سوقية | Dealix |
|--------------|--------|
| GTM كـ operating system وليس PDF | 134 مهمة YAML + CI أسبوعي |
| مراجعة أسبوعية بأدلة قابلة للتحقق | evidence CSV + scorecard |
| إيقاع pipeline يومي/أسبوعي | commercial day + War Room P0 |
| Human-in-the-loop قبل الإرسال | draft_only · `/ops/approvals` |
| لا أتمتة إغلاق/تفاوض بالذكاء الاصطناعي | founder-led حتى Proof + دفع |

**الحكم:** لسوق B2B سعودي founder-led، هذا المسار **أقوى من** «بوت إرسال كامل» و**مكافئ أو أفضل من** تكديس 10+ أدوات منفصلة — لأن الحوكمة والامتثال مدمجان في المنتج.

---

## ما يُشغَّل تلقائياً (صباح)

| طبقة | ماذا | أمر |
|------|------|-----|
| **موحّد** | كل الطبقات أعلاه | `py -3 scripts/run_dealix_unified_founder_day.py` |
| كامل | 16+ خطوة (digest، سوشال، soft launch، …) | `bash scripts/run_founder_commercial_day.sh` |
| نواة سريعة | War Room · dogfooding · pack · value plan · motion A | `py -3 scripts/run_full_commercial_ops_autopilot.py --execute` |
| لقطة فقط | JSON للواجهة/API | `GET .../founder/full-autonomous-ops` |
| واجهة | مركز قيادة + زر صباح ذاتي | `/ar/ops/founder` |
| أقوى خطة (مهام اليوم) | brief + قرار أسبوعي | `py -3 scripts/run_founder_strongest_ops.py --morning` |

---

## ما يبقى للمؤسس (لا يُؤتمت)

1. موافقة وإرسال LinkedIn / Gmail (`/ops/approvals`)
2. Discovery / Demo / تفاوض
3. `payment_received` و`proof_pack_delivered` حقيقيان في CSV
4. CRM → `kpi_founder_commercial_import.yaml`

---

## طيف HITL 2026 (لماذا Dealix أفضل من «إرسال كامل»)

| المستوى | متى | Dealix |
|---------|-----|--------|
| AI يقترح — المؤسس ينفّذ | قناة جديدة | War Room |
| **AI يمسود — المؤسس يوافق** | **افتراضي** | `/ops/approvals` |
| AI ينفّذ — مراجعة عينة | بعد ترميز 10+ صفقة | توسيع idempotent فقط |
| AI مستقل | غير مناسب مبكراً | **ممنوع** cold send |

مرجع: GTMStack HITL · Konnector B2B 2026 — «ابدأ بالموافقة ثم خفّف».

## مسار يوم كامل

```text
05:00 UTC  CI: founder_commercial_daily.yml → run_dealix_unified_founder_day.py --quick
صباحاً    /ops/founder → «يوم موحّد» أو scripts/founder_one_command.ps1
نهاراً     War Room + /ops/approvals
مساءً      cockpit/run-evening أو founder_evening_evidence.py
جمعة       cockpit/run-weekly أو founder_cadence.sh --weekly
```

---

## API

- `GET /api/v1/ops-autopilot/founder/cockpit` — **لوحة موحّدة** (benchmark + strongest ops + backlog + طابور)
- `POST /api/v1/ops-autopilot/founder/cockpit/run-unified-day` — **يوم موحّد كامل** من الواجهة (`quick` اختياري)
- `POST /api/v1/ops-autopilot/founder/cockpit/run-morning` — نواة صباح فقط (War Room · packs · تحققات)
- `POST /api/v1/ops-autopilot/founder/cockpit/run-evening` — مساء (تذكير أدلة + brief)
- `POST /api/v1/ops-autopilot/founder/cockpit/run-weekly` — أسبوع (scorecard + brief)
- `GET /api/v1/ops-autopilot/founder/full-autonomous-ops`
- `POST /api/v1/ops-autopilot/founder/full-autonomous-ops/run` (body: `dry_run` default false)
- `GET /api/v1/ops-autopilot/founder/strongest-ops?mode=morning|evening|weekly|full`
- `GET /api/v1/ops-autopilot/founder/strongest-plan` — قائمة 134 مهمة + `full_ops_bridge`

---

## مراجع

- [GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md](GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md)
- [FOUNDER_OPERATING_SYSTEM_AR.md](../ops/FOUNDER_OPERATING_SYSTEM_AR.md)
- `dealix/commercial_ops/full_ops_autopilot.py`
