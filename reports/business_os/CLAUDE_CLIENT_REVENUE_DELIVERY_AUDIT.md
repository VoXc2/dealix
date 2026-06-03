# Dealix — Client / Revenue / Delivery Audit
## تدقيق طبقات العميل والإيراد والتسليم (Agent #2)

> **التاريخ:** 2026-06-03
> **النطاق:** الطبقات التي تأتي بعد اهتمام السوق (GTM): واتساب بعد الموافقة، بوابة العميل الآمنة، فحص الجاهزية، بطاقات الإجراء، مصنع العروض، مصنع أدلة الإثبات، تسليم الدفع، التسليم، التجديد، نجاح العملاء، غرفة قيادة المؤسس.
> **القاعدة الذهبية:** لا تكرّر ولا تُعِد كتابة أساس السوق/التجاري الموجود في `company_os/`. وسّع الناقص فقط، واربط بالموجود.

---

## 0. منهجية التدقيق

تم فحص الجذر والمسارات التالية فعليًا (وليس افتراضيًا):

`README.md`, `info.md`, `package.json`, `.env.example`, `.backend-features.json`,
`company_os/**`, `docs/**`, `scripts/**`, `api/**`, `src/**`, `db/**`, `contracts/**`,
وتاريخ git (`git log`).

**النتيجة الأساسية:** بنية المستودع الحقيقية **تختلف** عن المسارات التي افترضها نص المهمة. لا يوجد `docs/whatsapp/`, `docs/client_portal/`, `schemas/`, `data/`, `reports/`, `tests/` (Python) قبل هذا العمل. يوجد بدلًا منها طبقة أعمال ناضجة تحت `company_os/`. لذلك:

- أنشأنا المسارات التي طلبتها المهمة حرفيًا (لا تتعارض مع أي ملف قائم).
- ربطناها صراحةً بأساس `company_os/` القائم لمنع الازدواجية المفاهيمية.
- وثّقنا التعارضات/التكرارات الموجودة أصلًا (انظر القسم 9).

---

## 1. مستندات/ملفات واتساب الموجودة

| العنصر | الموقع | الحالة | ملاحظة |
|---|---|---|---|
| قناة واتساب كأحد قنوات المتابعة | `db/schema.ts` → جدول `followups.channel` enum: `email \| whatsapp \| phone` | موجود (بنية بيانات فقط) | لا يوجد تدفق واتساب، ولا جلسات، ولا بطاقات إجراء، ولا فحص جاهزية |
| إشارة لفقد استفسارات واتساب كألم سوقي | `company_os/revenue/outreach_queue.json` (OUT-003 TrainMe), `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md` | موجود (محتوى تسويقي) | يصف الألم، لا يبني نظام واتساب |
| خيار قناة الاتصال في الـIntake | `company_os/delivery/p1_intake_template.md` (□ WhatsApp) | موجود (خانة اختيار) | لا توجد سياسة موافقة/خصوصية لواتساب |

**الخلاصة:** **لا يوجد WhatsApp Client OS**. لا تدفقات، لا بطاقات إجراء، لا فحص جاهزية، لا قوالب، لا سياسة موافقة، لا تسليم بشري، لا مقاييس. ❗ فجوة كاملة.

---

## 2. مستندات/ملفات بوابة العميل الموجودة

| العنصر | الموقع | الحالة |
|---|---|---|
| مصادقة المستخدم (Kimi OAuth) | `api/auth-router.ts`, `api/kimi/*`, `src/hooks/useAuth.ts`, `src/pages/Login.tsx` | موجود (مصادقة داخلية للمؤسس فقط) |
| تخزين S3 (رفع ملفات محتمل) | `package.json` → `@aws-sdk/client-s3`, `@aws-sdk/s3-request-presigner` | موجود (تبعية، غير مستخدمة في كود واضح) |
| سياسة تسليم البيانات | `company_os/governance/data_handling_checklist.md`, `pdpl_checklist.md` | موجود (سياسة، ليست بوابة) |

**الخلاصة:** **لا توجد Secure Client Portal** موجّهة للعميل. لا مسارات `/client/*`، لا رفع آمن موجّه للعميل، لا تدفق صلاحيات، لا مراجعة عروض/أدلة عبر بوابة. ❗ فجوة كاملة (مع توفر لبنات: S3 + Auth).

---

## 3. مستندات العروض/الإثبات/الدفع الموجودة

| العنصر | الموقع | الحالة | علاقتنا |
|---|---|---|---|
| كتالوج العروض (SKUs) | `company_os/revenue/proposals.json` (PROP-P1, PROP-P2-SMALL/MEDIUM/ENTERPRISE) | موجود ✅ | **مصدر الحقيقة** — سنربط كتالوجنا به، لا نكرره |
| قالب Proof Pack | `company_os/delivery/proof_pack_template.md` | موجود ✅ | سنوسّعه إلى "Proof Pack Factory" ونربط، لا نعيد كتابته |
| مولّد Proof Pack | `scripts/generate_proof_pack.py` (+ نسخة مكررة) | موجود ✅ | نستفيد منه كمرجع |
| جدول العروض في DB | `db/schema.ts` → `proposals` (clientName, service, package, valueSar, status, approver, deliverables) | موجود ✅ | نطابق سكيمَتنا معه |
| جدول المدفوعات في DB | `db/schema.ts` → `payments` (invoiceId, amountSar, status) | موجود ✅ | نبني تسليم الدفع فوقه |
| موجّه العروض/المدفوعات API | `api/proposal-router.ts`, `api/finance-router.ts` | موجود ✅ | نقطة امتداد |
| طابور الموافقات | `company_os/governance/approval_queue.json` + `db/schema.ts` → `approvalQueue` | موجود ✅ | كل عرض/دفع يمر عبره |

**الخلاصة:** أساس قوي. الناقص: **Proposal Factory** و**Payment Handoff** و**Contract Handoff Policy** كأنظمة موثّقة بسكيمات وبطاقات إجراء وبوابات موافقة صريحة وربط إلزامي بالكتالوج. ⚠️ جزئي.

---

## 4. مستندات التسليم الموجودة

| العنصر | الموقع | الحالة |
|---|---|---|
| SOP تسليم P1 | `company_os/delivery/p1_delivery_sop.md` | موجود ✅ |
| قالب Intake | `company_os/delivery/p1_intake_template.md` | موجود ✅ |
| خطة نجاح العميل | `company_os/delivery/client_success_plan.md` | موجود ✅ (تشمل KPIs، مخاطر، تجديد، إحالة) |
| قالب Proof Pack | `company_os/delivery/proof_pack_template.md` | موجود ✅ |

**الخلاصة:** يوجد أساس تسليم جيد لكنه **غير مربوط بسلسلة GTM→Won→Delivery**. الناقص: **Sales→Delivery Handoff** رسمي، **معايير قبول**، **أول 14 يوم**، **تقرير القيمة الأسبوعي** كنظام بسكيمات/بيانات/تقارير، و**حارس النطاق (Scope Guard)**. ⚠️ جزئي.

---

## 5. مستندات التجديد/نجاح العملاء الموجودة

| العنصر | الموقع | الحالة |
|---|---|---|
| خطة نجاح العميل (تشمل التجديد/الإحالة/الترقية) | `company_os/delivery/client_success_plan.md` | موجود ✅ (قالب) |
| سلّم الترقية (P1→P2) | `company_os/revenue/proposals.json` + `proof_pack_template.md` §7 | موجود ضمنيًا |
| اقتصاديات الوحدة | `company_os/finance/unit_economics.md` | موجود ✅ |

**الخلاصة:** **لا يوجد Customer Success OS / Renewal OS** كنظام مستقل: لا Client Health Score، لا محرك تجديد، لا سلّم ترقية موثّق، لا قاعدة "لا تجديد بدون قيمة مُسلَّمة". ❗ فجوة شبه كاملة (يوجد قالب واحد فقط).

---

## 6. ملفات الواجهة / غرفة القيادة الموجودة

| العنصر | الموقع | الحالة |
|---|---|---|
| صفحات الواجهة | `src/pages/` → `Dashboard`, `Finance`, `Governance`, `Prospects`, `Home`, `LandingPage`, `Login`, `NotFound` | موجود ✅ |
| موجّهات tRPC | `api/router.ts` + `auth/finance/followup/governance/proposal/prospect/warroom-router.ts` | موجود ✅ |
| مكونات UI (shadcn، 40+) | `src/components/ui/*` | موجود ✅ (tabs, card, table, dialog, sidebar…) |
| تقارير غرفة الحرب (Markdown) | `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md`, `WEEKLY_CEO_BRIEF.md`, `RISKS.md`, `SCORECARD_REPORT.md` | موجود ✅ |

**الخلاصة:** يوجد Dashboard وحوكمة ومالية ومحتملون، **لكن لا توجد Founder Super Control Room** موحّدة بالتبويبات المطلوبة (واتساب، بوابة، عروض، أدلة، مدفوعات، تسليم، تجديد…) ولا "أمر المؤسس اليومي" الموحّد. سنسلّم **مواصفة** (Spec) كما طُلب صراحةً، دون زر إرسال خارجي في v1. ⚠️ جزئي (لبنات UI متوفرة).

---

## 7. السكيمات/ملفات البيانات الموجودة

| النوع | الموقع | ملاحظة |
|---|---|---|
| سكيمة قاعدة البيانات | `db/schema.ts` (Drizzle/MySQL) | جداول: users, prospects, followups, proposals, payments, approvalQueue, aiActionLedger |
| عقود/أنواع | `contracts/types.ts`, `constants.ts`, `errors.ts` | أنواع API |
| بيانات الأعمال (JSON/CSV/JSONL) | `company_os/{revenue,governance,finance}/*` | pipeline, proposals, prospects, followups, objections, outreach_queue, payments, approval_queue, ai_action_ledger |
| سكيمات JSON Schema مستقلة | **غير موجودة** ❗ | لا يوجد مجلد `schemas/` |

**الخلاصة:** لا توجد سكيمات JSON Schema للكيانات الجديدة (جلسة واتساب، بطاقة إجراء، تقييم العميل، صلاحية، تسليم بشري، عرض، Proof Pack، تسليم دفع، تسليم، صحة عميل، تجديد…). ❗ فجوة كاملة.

---

## 8. الملفات الناقصة (Missing)

تم إنشاؤها أو ستُنشأ في هذا العمل:

- **حوكمة شاملة:** `AGENTS.md` (عقد الحوكمة الموحّد) — كان **غير موجود**.
- **خريطة نظام الأعمال:** `docs/business_os/*` (6 مستندات) + `reports/business_os/COMPLETE_BUSINESS_OS_MAP.md`.
- **WhatsApp Client OS:** كامل `docs/whatsapp/*` (15)، `schemas/whatsapp_*`, `schemas/client_assessment|permission`, `schemas/human_handoff|support_ticket`, `data/whatsapp/*` (8)، `reports/whatsapp/*` (8).
- **Secure Client Portal:** `docs/client_portal/*` (8)، `schemas/client_portal_*`, `schemas/client_upload`, `data/client_portal/*`, `reports/client_portal/*`.
- **Revenue Execution:** `docs/revenue_execution/*` (5)، `schemas/proposal|proof_pack|payment_handoff|revenue_action_card`, `data/{proposals,proof_packs,payments,revenue}/*`, `reports/revenue_execution/*`.
- **Client Delivery OS:** `docs/delivery/*` (10)، `schemas/delivery_*|client_onboarding|weekly_value_report`, `data/delivery/*`, `reports/delivery/*`.
- **Customer Success / Renewal:** `docs/customer_success/*` (6)، `docs/renewal/*` (4)، `schemas/client_health|renewal|upsell_opportunity`, `data/{customer_success,renewals}/*`, `reports/{customer_success,renewal}/*`.
- **Founder Super Control Room:** `docs/founder_control/*` (4)، `reports/founder/*` (3).
- **Tests + Evals:** `tests/test_*.py` (8) + مشغّل قائم على المكتبة القياسية، `docs/evals/*`, `data/evals/*`.
- **CI/أدوات:** `scripts/client_revenue_delivery_check.py`, `.github/workflows/*`.

**ملاحظة مهمة:** لا يوجد `Makefile` (المهمة ذكرت `make doctor`/`make security-smoke`) — سنوفّر بديلًا عبر سكربت Python + سكربتات npm، ونوثّق غياب make.

---

## 9. الملفات المكررة/المتعارضة (موجودة قبل عملنا)

> هذه نتائج تدقيق على وضع المستودع القائم — **لم نُنشئها ولن نحذف عمل أحد**. نوثّقها فقط ونوصي.

1. **تكرار جذري لكامل company_os:** يوجد `company_os/company_os/**` كنسخة شبه كاملة من `company_os/**` (delivery, finance, governance, marketing, revenue, scripts, war_room). هذا تكرار فعلي يسبب لبسًا في "مصدر الحقيقة".
   - **التوصية:** اعتماد `company_os/` (المستوى الأول) كمصدر حقيقة، واعتبار `company_os/company_os/` نسخة قديمة للأرشفة/الحذف بقرار المؤسس. **لم نلمسها.**
2. **تكرار سكربتات Python:** `scripts/*.py` (الجذر) ≈ `company_os/company_os/scripts/*.py`. سكربتات الجذر تشير عبر `parent.parent` إلى `company_os/` (المستوى الأول) — وهي النسخة الصحيحة العاملة.
3. **سكربتات npm معطوبة (مرجع مفقود):** `package.json` يعرّف `commercial:check/plan/quality/brief` تشير إلى `scripts/commercial-*.js` **غير موجودة** (المجلد يحوي Python فقط). أي `npm run commercial:*` سيفشل.
   - **التوصية:** هذه من اختصاص أساس السوق/التجاري (Agent #1). **لم نصلحها** تفاديًا لتكرار/تعارض النطاق؛ وثّقناها كخطر (انظر التقرير النهائي).
4. **اختلاف enum الباقات:** `db/schema.ts` `proposals.package` = `Basic|Standard|Premium`، بينما الكتالوج الفعلي `company_os/revenue/proposals.json` = `P1 / P2-SMALL/MEDIUM/ENTERPRISE`. عدم توافق محتمل.
   - **التوصية:** اعتماد معرّفات الكتالوج (`data/catalog/product_catalog.json`) كمصدر حقيقة لربط العروض، مع توثيق الفجوة لمواءمة لاحقة في DB.
5. **`docs/` يحوي SPA مبني:** `docs/index.html` + `docs/assets/index-*.js/css` (لقطة بناء). أضفنا مجلدات توثيق (`docs/business_os/` …) بجانبها دون أي تعارض (الـSPA يخدم index.html + assets فقط).

---

## 10. نقاط التوسعة الآمنة (Safe Extension Points)

| نقطة التوسعة | كيف نمتد بأمان |
|---|---|
| `company_os/governance/{agent_permissions.md, approval_queue.json, ai_action_ledger.jsonl}` | نعيد استخدام نفس نموذج المستويات/الموافقة/السجل. كل كيان جديد يحمل `requires_approval/approved/risk` + نضيف `evidence_level`. |
| `company_os/revenue/proposals.json` | مصدر حقيقة الكتالوج. كل `proposal.product_id` يجب أن ∈ الكتالوج. |
| `db/schema.ts` (proposals/payments/approvalQueue/aiActionLedger/followups.channel=whatsapp) | سكيماتنا الجديدة تتوافق مع أسماء الحقول الموجودة لتسهيل ربط مستقبلي. |
| `@aws-sdk/s3-*` + Kimi Auth | لبنات جاهزة لبوابة العميل (روابط منتهية الصلاحية، رفع موقّع، صلاحيات أقل امتياز). |
| `src/components/ui/*` (tabs, card, table) | لبنات جاهزة لتنفيذ مواصفة غرفة القيادة لاحقًا. |
| `scripts/governance_check.py` | نمط مرجعي لسكربت فحص جديد `client_revenue_delivery_check.py`. |
| تقارير `company_os/war_room/*.md` | نمط مرجعي لتقارير الطوابير/الغرفة الجديدة. |

---

## 11. ترتيب التنفيذ الموصى به

1. **AGENTS.md** — عقد الحوكمة الموحّد (المستويات L1–L5، evidence_level، risk، الافتراضات: dry_run=true/approval_required=true/send_enabled=false، الخطوط الحمراء). يحكم كل ما بعده.
2. **Business OS Map** — تعريف كل نظام (مهمة/مدخلات/مخرجات/مسموح/ممنوع/تقارير/إيقاع/قرارات المؤسس) + خريطة العلاقات.
3. **السكيمات (schemas/)** — تثبيت العقود قبل البيانات والمستندات حتى تشير المستندات لأسماء حقول حقيقية.
4. **الكتالوج + البيانات (data/)** — كتالوج المنتجات (مصدر الحقيقة للربط) + بذور JSONL/YAML آمنة (dry-run، بلا أسرار/PII).
5. **WhatsApp Client OS** (بعد الموافقة) — التدفقات، بطاقات الإجراء، فحص الجاهزية، التسليم البشري.
6. **Secure Client Portal** — المسارات، الرفع الآمن، الصلاحيات، مراجعة العروض/الأدلة، تسليم الدفع.
7. **Revenue Execution** — Proposal/Proof/Payment Factory + Contract Handoff Policy.
8. **Client Delivery OS** — Handoff، أول 14 يوم، معايير القبول، حارس النطاق، تقرير القيمة الأسبوعي.
9. **Customer Success / Renewal** — Health Score، أول 30 يوم، محرك التجديد، سلّم الترقية ("لا تجديد بلا قيمة مُسلَّمة").
10. **Founder Super Control Room** — المواصفة + التقارير اليومية/الأسبوعية + سجل القرار.
11. **Tests + Evals + CI** — اختبارات الثوابت الأمنية (8) + فحص + Workflow.
12. **التقرير النهائي + التحقق + الدفع + PR (Draft).**

---

## ملحق: الثوابت غير القابلة للتفاوض (مطبّقة في كل ما يلي)

- لا أتمتة واتساب باردة. واتساب فقط بعد: موافقة صريحة / رد إيجابي / حجز / تعبئة نموذج / علاقة عميل قائمة.
- لا مفاتيح API في واتساب. لا أسرار في الدردشة/السجلات/الـPrompts/الـJSONL/التقارير/قضايا GitHub.
- البوابة الآمنة فقط للأسرار/الملفات/الصلاحيات.
- لا سعر نهائي بلا موافقة المؤسس. لا إرسال رابط دفع بلا موافقة. لا وعد قانوني/تعاقدي بلا تسليم بشري.
- لا ضمان ROI. لا أدلة/دراسات حالة مزيّفة.
- كل عرض يُطابَق بالكتالوج. كل توصية لها `evidence_level`.
- كل الإجراءات الخارجية افتراضيًا: `dry_run=true`, `approval_required=true`, `send_enabled=false`.

*أُنشئ بواسطة Agent #2 — Client + Revenue + Delivery Operating OS. لا يُعاد كتابة أساس السوق/التجاري.*
