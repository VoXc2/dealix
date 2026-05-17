# Capital Model — نموذج رأس المال

<!-- Layer: Empire | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة حاكمة:** كل مشروع يبني أصولاً، لا نقداً فقط.
> مشروعٌ ينتهي بنقد بلا أصل = مشروع غير استراتيجي (Constitution belief 4).

---

## المبدأ

النقد يُنفَق. الأصل يتراكم. Dealix لا تقيس النجاح بالإيراد وحده — بل
بما **بقي بعد المشروع**: قالب، أداة، رؤية، إثبات، علاقة. هذا ما يحوّل
سلسلة مشاريع إلى مؤسسة لها قيمة مستقلة عن المؤسس.

> Belief 4: مشاريع لا تُنشئ رأس مال = ليست استراتيجية.

كل مشروع يُسأل قبل إغلاقه: **ماذا بنيتَ يبقى؟**

---

## أنواع رأس المال الخمسة

```
Service Capital   → عروض، scopes، checklists، معايير QA
Product Capital   → أدوات، modules، APIs، dashboards، أتمتة
Knowledge Capital → playbooks، اعتراضات، رؤى قطاعية، مخاطر حوكمة
Trust Capital     → Proof Packs، رؤى بأسلوب حالة، شهادات، audit logs
Market Capital    → جمهور، شركاء، إحالات، benchmarks، محتوى سلطة
```

| النوع | ما يتراكم | أين يُسجَّل |
|-------|-----------|------------|
| Service Capital | قدرة التسليم المتكررة | offer ladder, SOPs |
| Product Capital | ما يعمل دون المؤسس | repo, capital ledger |
| Knowledge Capital | ما تعرفه المؤسسة | playbooks, sales-kit |
| Trust Capital | ما يُثبت الادعاء | Proof Pack system |
| Market Capital | من يعرف Dealix ويثق | authority + benchmark |

النوعان الأخيران — Trust وMarket — هما الأبطأ بناءً والأصعب تقليداً،
ولذلك هما الأعلى قيمة على المدى الطويل.

---

## قاعدة الإنتاج الإلزامية

> كل مشروع يجب أن يُنتج **أصل Trust واحداً على الأقل**
> **+ أصل Knowledge أو Product واحداً على الأقل**.

مشروعٌ ينتهي دون أصلين من هذا النوع لا يُعدّ مكتملاً استراتيجياً — حتى
لو دفع العميل بالكامل. النقد وحده ليس مخرجاً كافياً.

أمثلة على أصول صالحة من Sprint واحد:
- **Trust:** Proof Pack موثّق + رؤية مجهولة المصدر.
- **Knowledge:** اعتراض جديد مُوثَّق في sales-kit، أو نمط فجوة قطاعي.
- **Product:** checklist جديد، أو template، أو module داخلي صغير.

---

## سجلّ رأس المال — Capital Ledger

كل أصل يُسجَّل صراحةً — لا أصل في الذاكرة فقط. السجلّ هو الذاكرة
المؤسسية التي تُثبت أن المشروع كان استراتيجياً.

السجلّ يُدار عبر:
[`../../auto_client_acquisition/capital_os/capital_ledger.py`](../../auto_client_acquisition/capital_os/capital_ledger.py)

```
إغلاق مشروع
   → تحديد الأصول المُنتَجة (النوع + الوصف)
   → asset_types.py  (تصنيف الأصل ضمن الأنواع الخمسة)
   → capital_ledger.py (تسجيل دائم)
   → فحص القاعدة: Trust ≥ 1 و(Knowledge أو Product) ≥ 1؟
       → لا: المشروع غير مكتمل استراتيجياً — راجِع المخرجات
       → نعم: إغلاق
```

التسجيل يخضع لبند No PII: الأصل يُوصف بنمطه لا بهوية العميل.

---

## كيف ينمو رأس المال عبر الزمن

| المرحلة | رأس المال الغالب |
|---------|------------------|
| المشاريع 1–5 | Service + بداية Knowledge وTrust |
| المشاريع 6–15 | Product يبدأ بالظهور من التكرار |
| المشاريع 16+ | Market Capital (benchmarks، سلطة) يتراكم |

لا نقفز للأمام: Product Capital لا يُبنى قبل تكرار حقيقي
(انظر [`PRODUCTIZATION_PATH.md`](PRODUCTIZATION_PATH.md))، وMarket Capital
لا يُنشر قبل عيّنة كافية (انظر [`BENCHMARK_ENGINE.md`](BENCHMARK_ENGINE.md)).

---

## المرجع القانوني — Canonical source

- [`../../auto_client_acquisition/capital_os/capital_ledger.py`](../../auto_client_acquisition/capital_os/capital_ledger.py) — سجلّ رأس المال (المرجع التقني).
- [`../institutional/DEALIX_CONSTITUTION.md`](../institutional/DEALIX_CONSTITUTION.md) — الدستور: Belief 4 (مشاريع بلا رأس مال = غير استراتيجية).

*لا ضمانات. لا إثبات مختلق. كل أصل يُسجَّل بنمطه لا بهوية عميله — Estimated value is not Verified value.*
