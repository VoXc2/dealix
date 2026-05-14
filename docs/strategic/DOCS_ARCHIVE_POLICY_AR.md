# سياسة أرشفة الوثائق Dealix

**الغرض:** منع الفوضى **بدون** كسر روابط أو اختبارات أو ذاكرة الفريق.

## القاعدة الذهبية

**Archive by classification first, not movement.**

**بالعربي:** نؤرشف ونصنّف **أولًا**؛ لا ننقل مئات الملفات دفعة واحدة ولا نحذف بدون قرار صريح. إعادة هيكلة فعلية تُؤجَّل حتى تستقر السجلات (انظر [DOCS_REVIEW_CADENCE_AR.md](DOCS_REVIEW_CADENCE_AR.md)).

## الحالات الرسمية

| الحالة | المعنى |
|--------|--------|
| **CANONICAL** | المصدر المعتمد للمجال؛ يُربط من [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md) أو [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md). |
| **ACTIVE** | مستخدم حاليًا لكنه ليس المصدر الوحيد. |
| **SUPPORTING** | يدعم ملفًا canonical ولا يُقرأ أولًا من قبل العميل/الشريك. |
| **PARTNER_SAFE** | يمكن إرساله لشريك بعد مراجعة (انظر [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md)). |
| **INVESTOR_SAFE** | يصلح لـ diligence أو deck بعد مراجعة. |
| **CLIENT_FACING** | يصلح للعميل ضمن نطاق Sprint/عقد. |
| **INTERNAL_ONLY** | لا يُخرج خارج Dealix (تشغيل، أسعار حساسة، سجلات). |
| **LEGACY** | قديم أو مكرر؛ يبقى في المسار الحالي؛ لا يقود قرارًا جديدًا. |
| **DEPRECATED** | لا يُستخدم في عروض أو تسليم جديد. |
| **ARCHIVED** | حفظ تاريخي فقط — المبدأ: تصنيف قبل النقل إلى مجلد `archive/` لاحقًا. |
| **GENERATED** | مُنتَج آليًا (مثل `_generated/*.json`)؛ المصدر هو السكربت + الملفات البشرية المدخلات. |

## قواعد سريعة

1. أي سطر جديد في [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md) يحدّد **من يفوز** عند التكرار المرقم.
2. التكرار (`docs/26_*` مرتين، `docs/30_*` مرتين، …) يُعالَج بـ **LEGACY / SUPPORTING** على المرآة، لا بحذف فوري.
3. `DEPRECATED` يتطلب تاريخًا وبديلًا في السجل أو في المصفوفة التجارية.
4. لا تُباع حزم Trust موحّدة قبل [BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md) — سياسة بيع، لا مجرد أرشفة.

## دورة الحياة

راجع [DOCS_ASSET_LIFECYCLE_AR.md](DOCS_ASSET_LIFECYCLE_AR.md).
