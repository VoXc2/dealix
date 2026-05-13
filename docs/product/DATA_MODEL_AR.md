# نموذج البيانات — الدستور · المعايير التأسيسية

**الطبقة:** الدستور · المعايير التأسيسية
**المالك:** قائد الخلفية
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [DATA_MODEL.md](./DATA_MODEL.md)

## السياق
يصف هذا الملف نموذج البيانات التطبيقي المعتمد لـ Dealix. هو رؤية
العلاقات بين الكيانات التي تشترك فيها المنصة وبوابة النماذج وحوكمة
وقت التشغيل وطبقة التقارير. يرتبط بـ
`docs/BEAST_LEVEL_ARCHITECTURE.md` للصورة المعمارية، وبـ
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` لتقوية طبقة التخزين،
وبـ `docs/product/ADVANCED_DATA_MODEL.md` (الشقيق L2) للنموذج
الموسَّع. تعريفات الحقول في `docs/data/DATA_SCHEMA_LIBRARY.md`.

## قائمة الكيانات
- **Client** — شركة سعودية متعاقدة تشتري خدمات Dealix.
- **Workspace** — حدود بيئة معزولة لكل عميل.
- **Project** — ارتباط تسليم تحت بيئة.
- **ServicePackage** — العرض المُنتَج المختار للمشروع.
- **DataSource** — مصدر بيانات مسجَّل (CRM، ملف، API).
- **Dataset** — شريحة مُصدَّرة من مصدر، مطابقة لمخطط.
- **Record** — صف داخل مجموعة.
- **Account** — سجل حساب أعمال (AccountSchema).
- **ContactHint** — إشارة بدون بيانات شخصية عن دور جهة اتصال.
- **Opportunity** — فرصة في أنبوب البيع مرتبطة بحساب.
- **Draft** — مادة ينتجها الذكاء بانتظار المراجعة/الموافقة.
- **Workflow** — تسلسل محدد من خطوات الذكاء والبشر.
- **Approval** — موافقة مُسجَّلة وفق المصفوفة.
- **AuditEvent** — حدث حوكمة/تشغيل غير قابل للتعديل.
- **GovernanceEvent** — نتيجة فحص وقت تشغيل.
- **ProofEvent** — حدث أثر تجاري قابل للقياس.
- **Report** — تقرير تنفيذي أو تشغيلي مُولَّد.
- **AIRun** — سجل استدعاء نموذج لغوي.
- **QAReview** — مراجعة جودة وسلامة مُسجَّلة.
- **CapitalAsset** — أصل قابل لإعادة الاستخدام في سجل الملكية.
- **FeatureCandidate** — طلب متكرر يطفو إلى ميزة.
- **PlaybookUpdate** — تغيير إصداري لدليل.
- **ClientHealthScore** — درجة صحة دورية لكل عميل.
- **CapabilityScore** — درجة نضج لكل قدرة لكل عميل.

## العلاقات الرئيسية
- لـ `Client` عدة `Workspace`.
- لـ `Workspace` عدة `Project` وعدة `DataSource`.
- لـ `Project` `ServicePackage` واحد وعدة `Workflow`.
- لـ `Workflow` عدة `AIRun`، وكل `AIRun` قد ينتج `Draft`.
- `Draft` يلزمه `QAReview` و`Approval` قبل أن يصبح مخرجًا مُسلَّمًا.
- `DataSource` تنتج عدة `Dataset`، ولكل مجموعة درجة جاهزية بيانات.
- `Dataset` تحوي عدة `Record` (حسابات، إشارات اتصال، أو كيانات وفق
  المخطط).
- `Opportunity` تشير لحساب ومشروع ومالك.
- `GovernanceEvent` و`AuditEvent` و`ProofEvent` للإضافة فقط وتشير
  لـ `AIRun` أو `Approval`.
- `CapitalAsset` ترتبط بالمشروع وسير العمل المُنتج.
- `ClientHealthScore` تجمع `ProofEvent` و`QAReview` و
  `CapabilityScore`.

## التعدد
- كل كيان عدا `CapitalAsset` و`FeatureCandidate` محدود ببيئة واحدة.
- الوصول عبر البيئات يلزمه `Approval` فئة C.
- دفاتر التدقيق والحوكمة والذكاء مُقسَّمة حسب البيئة ومنسوخة لمستودع
  حوكمة خاص بـ Dealix.

## المعرّفات
- كل معرّفات الكيانات نصوص بادئة مثل `CLT-` و`PRJ-` و`DS-` و
  `AIR-` و`AUD-` و`APV-`.
- المعرّفات ثابتة لا تُعاد ويُنشئها النظام.
- معرّفات أصحاب البيانات في سجلات PDPL تُخزَّن مُجزَّأة (hash).

## استراتيجية الفهرسة
- دفاتر الإضافة فقط (AuditEvent, GovernanceEvent, ProofEvent, AIRun)
  مُقسَّمة زمنيًا.
- جداول Account وOpportunity وDraft مُفهرسة ببيئة + مفتاح ترتيب
  زمني.
- الفهارس النصية الكاملة محصورة بحقول بلا بيانات شخصية افتراضًا.

## دورة الحياة
- `Drafts`: `created` → `qa_review` → `approval_pending` →
  `approved` أو `rejected` → `delivered`.
- `Datasets`: `ingested` → `scored` → `usable` → `archived`.
- `Projects`: `intake` → `discover` → `build` → `validate` →
  `delivered` → `proved` → `expanded` أو `closed`.

## الواجهات
| المدخلات | المخرجات | المالك | الوتيرة |
|---|---|---|---|
| طلب تعديل مخطط | خطة ترحيل | قائد الخلفية | لكل تغيير |
| اقتراح كيان جديد | تحديث مخطط ER | قائد الخلفية | لكل تغيير |
| قرار تعدد | تحديث سياسة وصول | قائد الحوكمة | لكل تغيير |
| تصميم فهرس | اعتماد خطة الاستعلام | قائد الخلفية | لكل تغيير |

## المقاييس
- **انحراف المخطط** — كيانات في الإنتاج تخالف هذا النموذج. المستهدف:
  0.
- **حوادث وصول عبر البيئات** — المستهدف: 0.
- **زمن الإضافة للدفاتر p95** — المستهدف: ≤ 200 مللي ثانية.

## ذات صلة
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — المعمارية المرجعية.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — تقوية الخلفية.
- `docs/product/ADVANCED_DATA_MODEL.md` — النموذج الموسَّع (L2).
- `docs/data/DATA_SCHEMA_LIBRARY.md` — مكتبة المخططات.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
