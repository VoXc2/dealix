# Dealix Privacy — تقليل بيانات العملاء المحتملين

> *آخر تحديث: 2026-06-03* — متوافق مع توجّه PDPL/SDAIA (راجع `company_os/governance/pdpl_checklist.md`)

نجمع **أقل قدر** من البيانات العامة اللازمة للتأهيل والتواصل المشروع — لا أكثر.

---

## مبدأ تقليل البيانات (Data Minimization)

```txt
data minimization      — فقط ما يلزم للتأهيل والتواصل
purpose limitation     — استخدام واحد: تواصل تجاري مشروع
no secrets in prompts  — لا أسرار في أي مرحلة
separate prospect data from client data
delete/anonymize on request
```

---

## ما يُسمح بجمعه (مصادر عامة فقط)

| الحقل | الشرط |
|-------|-------|
| اسم الشركة | عام |
| القطاع/المدينة | عام |
| صفحة التواصل الرسمية | عامة |
| إيميل/هاتف منشور رسميًا | منشور علنًا (C3) |
| روابط تواصل عامة | عامة |
| إشارة عامة ملحوظة (public_signal) | ملحوظة علنًا، لا تخمين |

## ما لا يُجمع

```txt
❌ بيانات شخصية حسّاسة لأفراد
❌ أرقام/إيميلات من قوائم مشتراة أو مسرّبة
❌ جهات اتصال مُختلقة
❌ أي PII خام يوضع في أدوات AI عامة
```

كل حقل يحمل `source` (المصدر العام) و`last_checked_at`. بلا مصدر = لا يُستخدم.

---

## فصل البيانات

```txt
Prospect data  →  company_os/revenue/prospects.csv   (محتملون — بيانات عامة)
Client data    →  مساحة عميل منفصلة + حوكمة PDPL      (عملاء — بيانات خاصة)
```

لا تُخلَط بيانات العملاء المحتملين ببيانات العملاء المتعاقدين.

---

## الحقوق والحذف

```txt
عند طلب الحذف/التجهيل: يُنفَّذ فورًا وتُضاف الجهة إلى Suppression.
الاحتفاظ الافتراضي: حسب data_handling_checklist (90 يومًا للبيانات الخاصة).
```

راجع أيضًا: `DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md`،
`CLIENT_DATA_HANDLING_AR.md`، `SECRET_HANDLING_POLICY_AR.md`.

---

*Dealix Prospect Data Minimization | Version 1.0 | 2026-06-03*
