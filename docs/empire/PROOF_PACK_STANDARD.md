# The Proof Pack Standard — معيار حزمة الإثبات

<!-- Layer: Empire | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة حاكمة:** **لا دليل، لا ادعاء.** Proof Pack هو أول منتج حقيقي لـ Dealix — وليس ملحقاً بالخدمة. ولا يُرفَع label فوق الدليل المتاح أبداً.

---

## 1. Proof Pack — أول منتج حقيقي

كل ما يبيعه Dealix يقود في النهاية إلى Proof Pack: حزمة موثّقة تجيب على "ما الذي حدث فعلاً بعد الـlead؟" بدليل، لا بوعد.

هذه الوثيقة **ملخص الـdoctrine**. أما **الأداة القانونية (canonical artifact)** فهي حزمة الإثبات الكاملة ذات الـ14 قسماً في `proof_os` — انظر `../../auto_client_acquisition/proof_os/`. عند أي اختلاف، يُرجَع إلى الأداة، لا إلى هذا الملخص.

### أقسام Proof Pack (ملخص الـdoctrine — 11 قسماً)

| # | القسم | المحتوى |
|---|-------|---------|
| 1 | Context | خلفية المشروع والقطاع |
| 2 | Inputs reviewed | المدخلات التي رُوجعت |
| 3 | Lead / workflow status | حالة الـlead أو الـworkflow |
| 4 | Source quality | جودة المصدر وموثوقيته |
| 5 | Owner gaps | فجوات الملكية — leads بلا مالك |
| 6 | Approval risks | مخاطر متعلقة بالموافقة |
| 7 | Follow-up gaps | فجوات المتابعة |
| 8 | Draft messages | مسودات الرسائل (جاهزة للمراجعة، لا للإرسال الآلي) |
| 9 | Recommended next actions | الإجراءات التالية الموصى بها |
| 10 | Truth labels | تصنيفات الصدق على كل ادعاء |
| 11 | Upgrade path | مسار الترقية المناسب |

هذه الـ11 قسماً ملخص doctrine؛ الأداة الكاملة في `proof_os` تحوي 14 قسماً قانونياً. الملخص لا يُنشئ مفردات بديلة.

---

## 2. Truth Labels — جدول التوفيق الواحد

لتجنّب أي مفردة ثالثة، يوجد **جدول توفيق واحد فقط** يربط labels الـdoctrine بطبقات `value_os` ومستويات الإثبات القائمة. لا قاموس جديد.

| Truth Label (doctrine) | value_os tier | شرط / علم إلزامي | proof level |
|------------------------|---------------|--------------------|-------------|
| Estimate — تقديري | `estimated` | يحمل علم `is_estimate` إلزامياً | — |
| Observed — ملاحَظ | `observed` | ملاحظة موثّقة | — |
| Client-confirmed — مؤكَّد من العميل | `client_confirmed` | يتطلب `source_ref` و`confirmation_ref` | Approved / Acted |
| Payment-confirmed — مؤكَّد بالدفع | `verified` | يتطلب `source_ref` | Revenue |
| Repeated workflow / Retainer-ready | — | إشارة توسّع (expansion signal) | ليست value tier |

ملاحظة مهمة: **Repeated workflow / Retainer-ready ليست طبقة قيمة** — هي إشارة توسّع تُغذّي الخطوة 8 (Expand) في الطريقة، ولا تُسجَّل كـvalue tier.

---

## 3. مستويات الإثبات القائمة — Existing Proof Levels

من `../PROOF_AND_CASE_STUDY_SYSTEM.md`، تسلسل مستويات الإثبات المعتمد:

```
Delivered → Approved → Acted → Impacted → Revenue
```

### المطابقة بين الطبقات

```
Truth Label            value_os tier        proof level
─────────────────────────────────────────────────────────
Estimate          →    estimated        →   (دون مستوى — تقدير)
Observed          →    observed         →   Delivered
Client-confirmed  →    client_confirmed →   Approved / Acted
Payment-confirmed →    verified         →   Revenue
─────────────────────────────────────────────────────────
Repeated workflow →    إشارة توسّع — لا tier ولا level
```

| مستوى الإثبات | المعنى | يقابله من Truth Labels |
|----------------|--------|--------------------------|
| Delivered | تم تسليم المخرج | Observed |
| Approved | وافق العميل | Client-confirmed |
| Acted | استخدم العميل المخرج فعلاً | Client-confirmed |
| Impacted | أثر تجاري موثّق | (يتطلب دليلاً أقوى من client_confirmed) |
| Revenue | إيراد حقيقي مُحصَّل | Payment-confirmed |

---

## 4. قاعدة عدم المبالغة — Never Overclaim

> **لا يُرفَع أي label فوق الدليل المتاح.**

- إن لم يوجد إلا تقدير → الـlabel هو `Estimate` ويحمل `is_estimate`. لا يُرفَع إلى `Observed`.
- `Client-confirmed` لا يُمنح بلا `source_ref` و`confirmation_ref`.
- `Payment-confirmed` / `verified` لا يُمنح بلا `source_ref` يثبت الدفع.
- مستوى `Impacted` لا يُدّعى بلا ربط مباشر موثّق بين مخرج Dealix والنتيجة.
- البيانات الناقصة تُكتب `insufficient_data` — لا تُملأ بتقدير متفائل.

هذه القاعدة هي تطبيق مباشر لـ"No fake proof" و"No guaranteed outcome claims" في الدستور، ولقاعدتي قفل الـdoctrine في طبقة الثقة.

---

## المرجع القانوني — Canonical source

- نظام الإثبات ودراسات الحالة (مستويات الإثبات): [`../PROOF_AND_CASE_STUDY_SYSTEM.md`](../PROOF_AND_CASE_STUDY_SYSTEM.md)
- حزمة إثبات العائد: [`../ROI_PROOF_PACK.md`](../ROI_PROOF_PACK.md)
- نظام الإثبات (الأداة القانونية — 14 قسماً): [`../../auto_client_acquisition/proof_os/`](../../auto_client_acquisition/proof_os/)
- نظام القيمة (طبقات القيمة): [`../../auto_client_acquisition/value_os/`](../../auto_client_acquisition/value_os/)
- معيار SOAEN (عنصر Evidence): [`./SOAEN_STANDARD.md`](./SOAEN_STANDARD.md)
- طبقة الثقة (قاعدتا قفل الـdoctrine): [`./TRUST_LAYER.md`](./TRUST_LAYER.md)
