# تجارب التسعير / Pricing Experiments
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->
> القانون / Canonical: see [docs/COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md)

## 1. المبدأ / Principle

**العربية:** القاعدة الأساسية في التسعير: **بدل خفض السعر، خفّض النطاق**. خفض السعر يُضعف القيمة المُدرَكة ويفسد المرساة لكل عميل قادم. خفض النطاق يحافظ على السعر العادل لكل وحدة عمل، ويمنح العميل بداية صغيرة وآمنة. كل رقم يحمل تصنيف حقيقة: تقدير / ملحوظ / مؤكَّد من العميل / مؤكَّد بالدفع.

**English:** The core pricing rule: **don't lower the price — lower the scope** (بدل خفض السعر، خفّض النطاق). Cutting the price weakens perceived value and corrupts the anchor for every future buyer. Cutting the scope keeps a fair price per unit of work and gives the buyer a small, safe start. Every metric carries a truth label: Estimate / Observed / Client-confirmed / Payment-confirmed.

## 2. أمثلة خفض النطاق / Scope-Reduction Examples

| بدلًا من / Instead of | نفعل / We do |
|---|---|
| خصم 50% / a 50% discount | مراجعة 10 عملاء محتملين فقط / review only 10 leads |
| تشغيل الشركة كاملة / running the whole company | البدء بعميل واحد / start with one customer |
| سبرنت كامل / a full Sprint | البدء بـProof Pack واحد / start with one Proof Pack |

**العربية:** في كل صف، السعر لكل وحدة عمل ثابت — يتغير حجم العمل، لا قيمته.

**English:** In every row, the price per unit of work is unchanged — the volume of work changes, not its value.

## 3. الأسعار الرسمية الثابتة / Canonical Prices (Fixed)

| العرض / Offer | السعر / Price | الإيقاع / Cadence |
|---|---|---|
| التشخيص المجاني / Free Mini Diagnostic | 0 | one-time |
| سبرنت إثبات الإيرادات / Revenue Proof Sprint | 499 SAR | one-time |
| حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | 1,500 SAR | one-time |
| عمليات النمو الشهرية / Growth Ops Monthly | 2,999 SAR | per month |
| إضافة دعم العمليات / Support OS Add-on | 1,500 SAR | per month |
| غرفة قيادة الإدارة / Executive Command Center | 7,500 SAR | per month |
| منصة شركاء الوكالات / Agency Partner OS | custom | — |

**العربية:** أي طبقة أعلى من 7,500 ريال/شهر تُوسَم: `Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع`. التجارب لا تُنشئ سعرًا جديدًا.

**English:** Any tier above 7,500 SAR/month is labeled: `Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع`. Experiments do not create a new price.

## 4. التجارب المسموح بها / Allowed Experiments

### 4.1 تجربة خفض النطاق / Scope-Reduction Experiment

```text
الفرضية / Hypothesis:
  بداية أصغر تزيد عدد العملاء الذين يدفعون أول مرة
  a smaller start raises the count of first-time paying buyers
ما نغيّره / What we change:
  نعرض تدقيق 10 عملاء كنقطة دخول بدل السبرنت الكامل
  offer a 10-lead audit as the entry point instead of the full Sprint
كيف نقيس / How we measure:
  نسبة العروض المصغّرة التي وصلت إلى invoice_paid
  share of reduced-scope offers that reached invoice_paid
تصنيف النتيجة / Result truth label: Observed
```

### 4.2 تجربة تأطير عرض الدخول / Entry-Offer Framing Experiment

```text
الفرضية / Hypothesis:
  تأطير التشخيص المجاني كـ"فحص حلقة المتابعة" يرفع الطلب
  framing the free diagnostic as a "follow-up loop check" raises demand
ما نغيّره / What we change:
  عنوان ووصف صفحة التشخيص فقط — لا السعر
  the diagnostic page title and description only — not the price
كيف نقيس / How we measure:
  عدد طلبات التشخيص المؤهَّلة أسبوعيًا
  qualified diagnostic requests per week
تصنيف النتيجة / Result truth label: Observed
```

### 4.3 تجربة توجيه السُّلّم / Ladder-Routing Experiment

```text
الفرضية / Hypothesis:
  توصية المسار التالي عند التسليم ترفع التحول من سبرنت لاشتراك
  recommending the next step at delivery raises sprint-to-retainer conversion
ما نغيّره / What we change:
  نضيف خطوة توصية مسار واحدة في تسلسل التسليم
  add one path-recommendation step in the delivery sequence
كيف نقيس / How we measure:
  معدّل الانتقال من Sprint إلى Growth Ops Monthly
  rate of moving from Sprint to Growth Ops Monthly
تصنيف النتيجة / Result truth label: Observed
```

## 5. القاعدة الصارمة / The Hard Rule

**العربية:** `no_hidden_pricing` — التجارب لا تغيّر أبدًا سعرًا معلنًا بشكل سرّي. كل سعر معروض هو من السجل الرسمي في `COMMERCIAL_WIRING_MAP.md`. ما يتغير في التجربة هو **النطاق أو التأطير أو التوجيه** — لا الرقم المُعلن. أي عميلين يريان نفس العرض يريان نفس السعر.

**English:** `no_hidden_pricing` — experiments never secretly change a posted price. Every displayed price is from the canonical registry in `COMMERCIAL_WIRING_MAP.md`. What an experiment changes is the **scope, framing, or routing** — never the posted number. Any two buyers viewing the same offer see the same price.

## 6. حوكمة التجربة / Experiment Governance

**العربية:** كل تجربة تُسجَّل قبل بدئها: الفرضية، التغيير، المقياس، تاريخ البدء، تاريخ المراجعة. لا تُعمَّم نتيجة قبل بلوغ عيّنة كافية. النتائج تُذكر دائمًا بتصنيف حقيقة، ولا تُحوَّل إلى وعد بعائد. التجربة الفاشلة تُوثَّق كما الناجحة.

**English:** Every experiment is logged before it starts: hypothesis, change, metric, start date, review date. No result is generalized before a sufficient sample. Results are always stated with a truth label and never turned into a return promise. A failed experiment is documented the same as a successful one.

## 7. ما لا نختبره أبدًا / What We Never Test

**العربية:** لا نختبر: سعرًا سرّيًا مختلفًا لعميلين، خصمًا غير معلن، طبقة فوق 7,500 ريال مربوطة بالدفع، وعدًا بعائد كجزء من التأطير، أو إثباتًا مُختلَقًا لرفع التحويل.

**English:** We never test: a secret different price for two buyers, an undisclosed discount, a tier above 7,500 SAR wired to checkout, a return promise as part of framing, or fabricated proof to lift conversion.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
