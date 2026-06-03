# Dealix — Daily Operating Factory Completion Report

*Date: 2026-06-03*

تقرير إكمال طبقة المصنع التشغيلي اليومي للأنظمة الخمسة (Focus 5). يحوّل Dealix من
"مشروع AI" إلى مصنع تشغيل وبيع وتسليم يومي.

> **ملاحظة على الموضع:** المواصفة الأصلية ذكرت مسارات تحت `docs/...`، لكن `docs/`
> في هذا الريبو هو **الموقع المبني المنشور** (GitHub Pages: `docs/index.html` +
> `docs/assets/`). لتجنّب تعارض البناء، وُضعت الوثائق تحت `company_os/` (موطن
> العمليات، مثل `governance/` و`war_room/`)، وبقيت التقارير تحت `reports/` كما طُلب.

---

## 1. الملفات المنشأة/المعدّلة

### المحرك (Node ESM)
- `scripts/lib/commercial.js` — المنطق المشترك (تحميل، تسجيل، بوابات، أمان، عرض)
- `scripts/draft-quality-gate.js` — `npm run commercial:quality`
- `scripts/commercial-daily-plan.js` — `npm run commercial:plan`
- `scripts/commercial-control-check.js` — `npm run commercial:check`
- `scripts/commercial-daily-brief.js` — `npm run commercial:brief`
- `scripts/commercial.test.js` — 32 اختبار vitest
- `vitest.config.ts` — *(معدّل)* تضمين `scripts/**/*.test.js`

> هذه السكربتات الأربعة كانت **معرّفة في `package.json` لكنها مفقودة** (الكوميت
> "Add commercial outreach execution scripts" أضاف الأوامر فقط)، فكان `npm run
> commercial:all` يفشل. الآن أصبحت حقيقية وتعمل.

### البيانات (المصدر) — `company_os/commercial/`
`systems.json` · `draft_factory.json` · `suppression.json` · `board.json` ·
`content_calendar.json` · `partners.json` · `website_leads.json` · `README.md`

### الوثائق (عربي) — `company_os/`
- `founder_control/`: `DAILY_SUPER_COMMAND_SYSTEM_AR.md` · `FOUNDER_DAILY_OPERATING_RHYTHM_AR.md` · `FOUNDER_DECISION_GATES_AR.md`
- `sales_ops/`: `SALES_OPS_BOARD_AR.md` · `OWNER_ASSIGNMENT_POLICY_AR.md` · `LEAD_STATUS_MODEL_AR.md`
- `quality/`: `EMAIL_QUALITY_GATE_AR.md` · `CALL_BRIEF_QUALITY_GATE_AR.md` · `MINI_PROPOSAL_QUALITY_GATE_AR.md` · `DELIVERY_READINESS_GATE_AR.md`
- `content/FOCUS_5_CONTENT_ENGINE_AR.md` · `partners/FOCUS_5_PARTNER_CHANNEL_AR.md`
- `security/`: `UNTRUSTED_COMPANY_DATA_POLICY.md` · `PROMPT_INJECTION_GATE.md` · `AGENT_TOOL_USE_BOUNDARIES.md`

### التقارير المولّدة — `reports/`
`founder/DAILY_SUPER_COMMAND.md` · `founder/WEEKLY_BOARD_REVIEW.md` ·
`sales_ops/SALES_OPS_BOARD_STATUS.md` · `sales_ops/CALL_FOLLOWUP_QUEUE.md` ·
`quality/DAILY_QUALITY_GATE_REVIEW.md` · `quality/top_100_approval_queue.json` ·
`content/FOCUS_5_CONTENT_QUEUE.md` · `partners/FOCUS_5_PARTNER_PIPELINE.md` ·
`security/DAILY_AGENT_SECURITY_REVIEW.md` · `gtm/` (هذا التقرير)

---

## 2. الإيقاع التشغيلي اليومي

```
06:00 Research → 07:00 Intelligence Packs → 08:00 400 Drafts → 09:00 Quality Scoring →
10:00 Top 100 → 11:00 Email/Call Handoff → 13:00 Call Queue → 15:00 Mini Proposals →
17:00 Delivery Update → 19:00 Founder Daily Super Command
```

أمر واحد: `npm run commercial:all` (check → plan → quality → brief). التفاصيل:
`company_os/founder_control/FOUNDER_DAILY_OPERATING_RHYTHM_AR.md`.

---

## 3. نظام أمر القيادة للمؤسس

`reports/founder/DAILY_SUPER_COMMAND.md` يحتوي **13/13** قسمًا إلزاميًا، والسكربت
يتحقق ذاتيًا ويخرج بخطأ إن نقص أي قسم. القرار اليومي مشتق من البيانات (النظام الأعلى
أولوية + أوضح قطاع). الإرسال/التسعير/الاتصال تبقى بقرار بشري.

## 4. لوحة عمليات المبيعات

16 حالة كاملة من `researched` إلى `do_not_contact`، مع 5 ملاك لكل فرصة (أدوار لا
أسماء — PDPL). المخرج: `reports/sales_ops/SALES_OPS_BOARD_STATUS.md`.

## 5. بوابات الجودة

| البوابة | الشروط المنفّذة |
|--------|------------------|
| Email | 10 شروط رفض + نطاقات النقاط + شرط دخول Top 100 |
| Call | opening_line · questions · expected_objection · next_step |
| Mini Proposal | system · deliverables · timeline · starter_price · required_inputs · approval_required |
| Delivery | scope · required_inputs · success_metric · acceptance_criteria |

## 6. محركا المحتوى والشركاء

- المحتوى: محاور أسبوعية لكل نظام + قائمة 7 أيام، بلا case studies وهمية.
- الشركاء: 6 أنواع شركاء ↔ الأنظمة + أنبوب إحالة.

## 7. حدود الأمان

كل محتوى خارجي = بيانات غير موثوقة لا تتحول لتعليمات. بوابة حقن (8 أنماط)، منع أسرار
في التقارير، منع تسريب أسماء الأنظمة الداخلية، لا إرسال خارجي من الوكلاء، احترام
قائمة الحجب. المخرج: `reports/security/DAILY_AGENT_SECURITY_REVIEW.md`.

---

## 8. الاختبارات/الفحوص التي أُجريت (حقيقية)

| الفحص | الأمر | النتيجة |
|------|------|---------|
| وحدة المحرك | `npm test` | ✅ 32/32 اجتاز |
| المصنع كامل | `npm run commercial:all` | ✅ COMPLIANT |
| نوع TypeScript | `npm run check` (`tsc -b`) | ✅ exit 0 |
| أمر القيادة فيه 13 قسمًا | تحقق ذاتي في `commercial:brief` | ✅ 13/13 |
| Top 100 يستبعد < 75 / risk=high | اختبار + بوابة الجودة | ✅ (Top 100 = 7) |
| 16 حالة لوحة كاملة | اختبار | ✅ |
| بوابات الجودة فيها شروط فشل | اختبار (كل سبب) | ✅ |
| الأمان يعامل بيانات الشركة كغير موثوقة | اختبار + فحص | ✅ (1 حقن محتوى) |
| **اختبار سلبي:** تسليم بلا scope | كسر `OPP-012` مؤقتًا | ✅ خرج بكود 1 (CRITICAL) ثم استُعيد |
| **اختبار سلبي:** سر في تقرير | اختبار وحدة | ✅ CRITICAL |

نتائج دفعة اليوم: 18 draft → 4 top_priority · 3 approval_queue · 1 needs_rewrite ·
10 rejected (يغطي كل أسباب الرفض العشرة) · Top 100 = 7 · 0 critical · 0 high.

---

## 9. الفحوص الفاشلة/المتخطّاة ولماذا

- `npm run lint` يُظهر **23 خطأ سابق** في `src/` (`Governance.tsx`, `Prospects.tsx`,
  `trpc.tsx` — أخطاء `no-explicit-any` و`react-refresh`). **ليست من عملي**: لم ألمس
  أي ملف `.tsx`، وسكربتاتي `.js` لا يفحصها ESLint (يفحص `.ts/.tsx` فقط). تُركت كما هي
  لأن إصلاحها خارج نطاق هذه المهمة وقد يُدخل مخاطر في الواجهة.
- لم تُنشأ 400 مسودة فعلية: الدفعة البذرية 18 مسودة **تمثيلية** تُمارس كل قواعد
  البوابة؛ الهدف 400/يوم موثّق ويعمل نفس السكربت على أي حجم.
- طلبات الموقع `website_leads.json` مُعلّمة `demo:true` (أمثلة، ليست عملاء حقيقيين).

---

## 10. المخاطر المتبقية

1. **التكامل الحي**: المصنع مدفوع بملفات JSON يدوية. ربط بحث حقيقي + نموذج توليد
   المسودات + صندوق وارد للردود لم يُنفّذ بعد (خارج النطاق).
2. **الموقع → المصنع**: `website_leads.json` يحاكي تدفق النماذج؛ ربطه بنموذج الموقع
   الفعلي (`src/`) يحتاج عملًا في الواجهة/الـ API.
3. **أنماط الحقن/الأسرار** قائمة أساسية قابلة للتجاوز بصياغات جديدة؛ تحتاج توسيعًا
   دوريًا.
4. **ذكر "نضمن" في وثائق السياسة** يظهر فقط كـ *مثال ممنوع* داخل بوابة الجودة، لا
   كادعاء فعلي؛ الفحص الآلي يمسح المسودات والتقارير لا الوثائق.

---

## 11. خطوات المؤسس التالية

1. شغّل `npm run commercial:all` يوميًا واقرأ `reports/founder/DAILY_SUPER_COMMAND.md`.
2. اعتمد القرار الأهم، ثم العروض المعلّقة (2 بقيمة 7,500 ر.س افتتاحية).
3. أرسل لأعلى الشركات يدويًا (الإرسال بشري)، وكلّف `call_owner` بقائمة المكالمات.
4. حدّث `company_os/commercial/board.json` و`draft_factory.json` بالبيانات الحقيقية
   ليكبر المصنع تدريجيًا نحو 400/يوم.
5. (لاحقًا) اربط نموذج الموقع بـ `website_leads.json` لأتمتة Client Need Cards.

---

*هذا التقرير مكتوب يدويًا (ليس مولّدًا) ويلخّص عملًا تم التحقق منه فعليًا.*
