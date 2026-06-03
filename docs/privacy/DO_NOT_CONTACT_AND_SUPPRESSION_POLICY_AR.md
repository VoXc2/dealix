# Dealix Privacy — سياسة عدم الإزعاج والـ Suppression

> *آخر تحديث: 2026-06-03*

نحترم كل طلب بعدم التواصل فورًا، ونمنع الإرسال للقنوات غير المؤكدة.

---

## قائمة Suppression / Do-Not-Contact

أي جهة في هذه القائمة **لا تُرسَل لها رسالة ولا يُتصَل بها** تحت أي ظرف.

الملف التشغيلي: `company_os/governance/do_not_contact.csv`

تُضاف الجهة إلى القائمة عند:

```txt
- نتيجة اتصال/ردّ = do_not_contact
- طلب صريح بإيقاف التواصل
- إلغاء اشتراك (unsubscribe)
- شكوى spam
- طلب حذف بيانات
```

قبل أي إرسال أو اتصال، **يُفحَص الهدف مقابل هذه القائمة أولًا**.

---

## قاعدة الثقة قبل التواصل

من `QUALITY_GATES_AR.md` §1:

```txt
C0 / C1  →  لا إرسال ولا اتصال. أعد البحث أو نموذج رسمي فقط.
C2+      →  مؤهّل بعد بقية البوابات + موافقة المؤسس.
```

**لماذا؟** الإرسال لمن لم يشترك أو لقوائم غير مؤكدة يرفع احتمال تصنيف الرسائل
كـ spam ويضرّ سمعة الدومين. لذلك:

```txt
❌ لا قوائم مشتراة
❌ لا قواعد بيانات مسرّبة
❌ لا cold WhatsApp
❌ لا اتصال آلي
```

---

## حقول السجل (Suppression Record)

```txt
identifier (company / email / phone — كما هو منشور علنًا)
reason (do_not_contact / unsubscribe / complaint / deletion_request)
added_at
added_by
```

---

## التحقّق

- يدويًا: قبل خطوة 12:00 (Send/Call Handoff) في الحلقة اليومية.
- آليًا: ضمن الفحوص الحوكمية والـ `scripts/operating_factory_check.py`.

راجع أيضًا: `PROSPECT_DATA_MINIMIZATION_AR.md`،
`docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY_AR.md`.

---

*Dealix Do-Not-Contact & Suppression Policy | Version 1.0 | 2026-06-03*
