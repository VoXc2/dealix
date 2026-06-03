# Unsubscribe & Suppression Policy — سياسة إلغاء الاشتراك والكبت

> لكل مستلم حق إيقاف الرسائل بنقرة واحدة. الكبت (Suppression) يضمن ألا نراسل
> من طلب التوقف أو من هو على قائمة عدم التواصل.

---

## قواعد إلغاء الاشتراك

```txt
1. رابط unsubscribe واضح في كل رسالة تسويقية.
2. one-click unsubscribe مدعوم (بدون خطوات إضافية).
3. تنفيذ طلب الإلغاء خلال مدة قصيرة (فورًا حيثما أمكن).
4. لا إعادة إضافة من ألغى اشتراكه.
```

---

## قائمة الكبت (Suppression List)

| المصدر | يُضاف إلى الكبت |
|--------|------------------|
| طلب unsubscribe | نعم، فورًا |
| do-not-contact | نعم |
| bounce صلب متكرّر | نعم |
| شكوى سبام | نعم |

قبل أي إرسال: قارن القائمة المستهدفة بقائمة الكبت واستبعد المتطابقين.

---

## حالة Dealix

| البند | الحالة |
|-------|--------|
| unsubscribe موجود | ✅ |
| one-click | ✅ |
| suppression list فعّالة | ✅ |
| do-not-contact محترم | ✅ |

المصدر: `company_os/deliverability/deliverability_state.json`.

---

## التحقق الآلي

`check_deliverability_readiness.py` يفشل إذا كان أي من:
`unsubscribe_present`, `one_click_unsubscribe`, `do_not_contact_respected`,
`suppression_list_active` ليس `true`.

---

## قاعدة صارمة

```txt
لا purchased lists.
لا جهات مخترعة.
لا إرسال لمن طلب التوقف.
احترام do-not-contact غير قابل للتفاوض.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
