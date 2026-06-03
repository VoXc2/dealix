# DSAR Response Templates (AR + EN)

> القوالب المستخدمة في الرد على طلبات أصحاب البيانات (DSAR). راجع `docs/ops/PDPL_RETENTION_POLICY.md` §4.

---

## A. إيصال الاستلام (24 ساعة من التقديم)

### عربي
```
الموضوع: استلام طلبك بخصوص بياناتك الشخصية — رقم #DSAR-{ID}

السلام عليكم {الاسم}،

استلمنا طلبك بتاريخ {التاريخ} الخاص بـ {access | rectification | erasure | portability}.

لتأكيد هويتك ومعالجة طلبك خلال المدة النظامية (30 يومًا)، نرجو إرسال:
- صورة من هوية وطنية أو إقامة سارية
- خطاب رسمي إذا كان الطلب نيابة عن طرف آخر

أرسلها على privacy@dealix.sa مع الإشارة لرقم الطلب #DSAR-{ID}.

سنرد عليك خلال 30 يومًا كحد أقصى. للاستفسار: privacy@dealix.sa.

DPO Dealix
```

### English
```
Subject: Receipt of your data subject request — #DSAR-{ID}

Dear {name},

We received your {access | rectification | erasure | portability} request on {date}.

To verify identity and fulfil your request within the legal 30-day window, please send:
- A copy of a valid Saudi national ID or residency
- An authorisation letter if the request is on behalf of another person

Send to privacy@dealix.sa quoting #DSAR-{ID}.

We will respond within 30 days at the latest. For questions: privacy@dealix.sa.

DPO, Dealix
```

---

## B. تأكيد المعالجة بعد التحقق من الهوية

```
الموضوع: تأكيد معالجة طلبك #DSAR-{ID}

تم التحقق من هويتك. سنقوم بـ {action_summary} وسنرسل التأكيد النهائي خلال {N} أيام
عمل. تاريخ الاستجابة المتوقع: {date}.

DPO Dealix
```

---

## C. رد طلب وصول (Access)

```
الموضوع: استجابة طلب الوصول #DSAR-{ID}

السلام عليكم {الاسم}،

تجد مرفقًا ملفًا مشفّرًا (AES-256) يحتوي على البيانات الشخصية التي يحتفظ بها Dealix
عنك في أنظمته التشغيلية. كلمة المرور سترسل في رسالة منفصلة عبر {channel}.

المحتويات (انظر manifest.json داخل الملف):
- البيانات الأساسية: ____
- سجلات التواصل: ____
- بيانات المدفوعات: ____
- سجلات التدقيق: ____
- إجمالي السجلات: {count}

ما هو غير مشمول:
- النسخ الاحتياطية المشفّرة في السكون (تنتهي صلاحيتها وفق دورة الاحتفاظ)
- تحليلات مُجهّلة الهوية

للاعتراض على دقة أو اكتمال البيانات، يمكنك تقديم طلب تصحيح خلال 30 يومًا.

DPO Dealix
```

---

## D. رد طلب تصحيح (Rectification)

```
الموضوع: تنفيذ طلب التصحيح #DSAR-{ID}

السلام عليكم {الاسم}،

قمنا بتصحيح البيانات التالية:
- {field}: من «{old_value}» إلى «{new_value}»

تم إخطار المعالجين الفرعيين التاليين بالتصحيح: {sub_processors}.

النفاذ يدخل حيز التنفيذ خلال 7 أيام عمل.

DPO Dealix
```

---

## E. رد طلب حذف (Erasure / Right to be Forgotten)

```
الموضوع: تنفيذ طلب الحذف #DSAR-{ID}

السلام عليكم {الاسم}،

تم حذف البيانات الشخصية التالية من أنظمتنا التشغيلية:
- جداول: {tables_list}
- إجمالي السجلات المحذوفة: {count}
- تاريخ التنفيذ: {date}

البيانات التي نحتفظ بها رغم طلب الحذف (وفقًا لاستثناءات قانونية):
- {category}: {legal_basis} (مدة: {retention_period})
  مثال: «سجلات المدفوعات: نظام الزكاة (10 سنوات)»

النسخ الاحتياطية تنتهي صلاحيتها وفق دورة 30 يومًا (راجع
سياسة الاحتفاظ على https://dealix.sa/privacy.html).

DPO Dealix
```

---

## F. رد طلب نقل (Portability)

```
الموضوع: استجابة طلب نقل البيانات #DSAR-{ID}

السلام عليكم {الاسم}،

تجد مرفقًا ملف بياناتك بصيغة JSON قياسية، قابلة للقراءة الآلية، مشفّرة AES-256.

الصيغة موثقة في:
https://dealix.sa/docs/data-portability-schema.json

DPO Dealix
```

---

## G. رفض الطلب — يجب أن يحدد السبب القانوني

```
الموضوع: استجابة طلبك #DSAR-{ID}

السلام عليكم {الاسم}،

بعد المراجعة، تعذّر علينا تنفيذ طلبك للأسباب التالية:
- {reason}

السند القانوني:
- {legal_reference}

لديك حق التظلم إلى:
- DPO Dealix: privacy@dealix.sa
- الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA): https://sdaia.gov.sa

DPO Dealix
```

---

## H. تمديد المدة (مرة واحدة، +30 يومًا، لطلبات معقدة)

```
الموضوع: تمديد مدة الرد على طلبك #DSAR-{ID}

السلام عليكم {الاسم}،

نظرًا لتعقيد طلبك (السبب: {reason}) سنحتاج 30 يومًا إضافية لاستكمال المعالجة.
تاريخ الرد النهائي المتوقع: {new_date}.

شكرًا لصبرك.

DPO Dealix
```

---

## سجل DSAR

كل طلب يُسجل في `docs/ops/dsar_log.md` بالتنسيق:

```
| #ID | تاريخ الاستلام | النوع | الحالة | تاريخ الرد | DPO المعالج | ملاحظات |
```

الحالات: `received` → `identity_verified` → `processing` → `extended` → `fulfilled` | `rejected`.
