# Dealix — Case Study Factory
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **الفكرة:** كل Proof Pack مادة توزيع خام. مصنع الحالات يحوّل عملاً سُلّم
> فعلاً إلى سلسلة أصول تسويقية — دون اختلاق رقم أو كشف اسم عميل.
> **Idea:** Every Proof Pack is raw distribution material. The factory
> turns delivered work into assets — without inventing a number or
> exposing a client name.

---

## خط الإنتاج — The Production Line

من حزمة إثبات واحدة إلى ثمانية أصول، كل أصل مشتق من السابق:

```
Proof Pack
   ↓
رؤية مجهّلة — Anonymized insight
   ↓
منشور LinkedIn — LinkedIn post
   ↓
فقرة نشرة بريدية — Newsletter section
   ↓
أصل شريك — Partner asset
   ↓
منشور بأسلوب الحالة — Case-style post
   ↓
شريحة ندوة — Webinar slide
   ↓
إجابة اعتراض — Objection answer (لغرفة البيع)
```

كل خطوة تأخذ من السابقة وتعيد صياغتها لجمهور مختلف. لا نبدأ من صفر في كل
أصل — نبدأ من الرؤية المجهّلة المُعتمدة.

---

## قواعد الادعاء الآمن — Safe-Claim Rules

غير قابلة للتفاوض، وتنطبق على كل أصل قبل النشر:

1. **لا اسم عميل دون إذن كتابي.** No client name without written
   permission. الإذن يُسجَّل ويُؤرَّخ (`no_unconsented_data`).
2. **لا أرقام غير مُتحقَّق منها.** No unverified numbers. كل رقم له مصدر
   حقيقي قابل للتتبّع، وإلا لا يُنشر (`no_fake_proof`, `no_unverified_outcomes`).
3. **صياغة كرؤية لا كادعاء.** Frame as insight, not claim. نقول «النمط
   الذي رأيناه» لا «نضمن لك هذه النتيجة». لا لغة عائد مضمون.

هذه القواعد امتداد مباشر لـ
[`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)
(حدود الأمان والثقة: لا scraping، لا واتساب بارد، لا أتمتة LinkedIn، لا
أدلة مُلفَّقة). نبرة وهوية كل أصل تتبع
[`../BRAND_PRESS_KIT.md`](../BRAND_PRESS_KIT.md) — حزمة الصحافة التي تحوي
السيرة الثنائية اللغة ونبرة العلامة الرسمية.

---

## مثال آمن — Safe Example

> **بالعربية:** «في عملنا مع شركة B2B في قطاع الخدمات، رصدنا أن نحو نصف
> الـ leads كانت تفتقد حقل مصدر القناة — ما يجعل ترتيب الأولويات تخميناً.
> بعد ترتيب البيانات، أصبحت فرق المبيعات تبدأ يومها بقائمة مرتّبة بدل
> قائمة عشوائية. النمط الذي نراه مراراً: المشكلة بيانات، لا جهد بيع.»
>
> **English:** "Working with a B2B services company, we found roughly
> half of leads were missing a channel-source field — making
> prioritization a guess. The pattern we keep seeing: it is a data
> problem, not an effort problem."

لماذا آمن: لا اسم عميل، الرقم تقريبي ومن البيانات الفعلية، الصياغة رؤية
(«النمط الذي نراه») لا وعد. القطاع عام بما يكفي ليمنع التعرّف على العميل.

---

## مثال غير آمن — Unsafe Example (ممنوع)

> ❌ «ضاعفنا مبيعات شركة [اسم صريح] ٣ أضعاف في ٣٠ يوماً — نضمن لك نفس
> النتيجة. اتصل الآن قبل أن يسبقك منافسوك.»

لماذا ممنوع — يخالف عدة بنود غير قابلة للتفاوض:

- يكشف اسم العميل دون إذم موثَّق (`no_unconsented_data`).
- رقم «٣ أضعاف» بلا مصدر مُتحقَّق (`no_fake_proof`, `no_unverified_outcomes`).
- «نضمن لك نفس النتيجة» لغة عائد مضمون — ممنوعة تماماً.
- نبرة ضغط تسويقي لا تطابق نبرة العلامة في حزمة الصحافة.

أي أصل بهذه الصياغة يُرفض في المراجعة ولا يُنشر.

---

## سير الاعتماد — Approval Flow

| الخطوة | المسؤول | الدليل |
|--------|---------|--------|
| اشتقاق الرؤية المجهّلة من Proof Pack | المؤسس | مصدر كل رقم مسجَّل |
| التحقق من إذن العميل (إن ذُكر شيء قابل للربط) | المؤسس | إذن كتابي مؤرَّخ |
| فحص قواعد الادعاء الآمن الثلاث | المؤسس | قائمة فحص مكتملة |
| النشر | المؤسس | تاريخ النشر + القناة |

لا نشر آلي. كل أصل خارجي يمرّ بموافقة بشرية صريحة قبل النشر —
`no_live_send`, `no_unaudited_changes`.

---

## الربط — Cross-links

- مصدر المادة الخام: [`CUSTOMER_SUCCESS_EXPANSION.md`](CUSTOMER_SUCCESS_EXPANSION.md)
  (مسار المحتوى أحد المسارات الخمسة بعد التسليم).
- النبرة والهوية: [`../BRAND_PRESS_KIT.md`](../BRAND_PRESS_KIT.md).
- الحدود غير القابلة للتفاوض: [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).
- التجميع الكمّي عبر عدة حالات: [`BENCHMARK_ENGINE.md`](BENCHMARK_ENGINE.md).

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
