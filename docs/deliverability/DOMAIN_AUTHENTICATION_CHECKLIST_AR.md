# Domain Authentication Checklist — قائمة مصادقة الدومين

> SPF + DKIM + DMARC هي الأساس. بدونها، الرسائل الشرعية تذهب للسبام.

---

## SPF (Sender Policy Framework)

- [ ] سجل SPF منشور في DNS.
- [ ] يتضمّن كل مرسِل معتمد (مزوّد الإرسال).
- [ ] لا يتجاوز 10 عمليات بحث DNS.
- [ ] ينتهي بـ `~all` أو `-all`.

## DKIM (DomainKeys Identified Mail)

- [ ] مفتاح DKIM منشور في DNS.
- [ ] التوقيع مفعّل على المرسِل.
- [ ] طول المفتاح ≥ 1024-bit (يفضّل 2048).
- [ ] التحقق من نجاح التوقيع في رسائل اختبار.

## DMARC

- [ ] سجل DMARC منشور (`_dmarc.<domain>`).
- [ ] السياسة على الأقل `p=quarantine` (الهدف `p=reject`).
- [ ] تقارير `rua` مفعّلة للمراقبة.
- [ ] محاذاة SPF/DKIM مع الدومين الظاهر (alignment).

---

## حالة Dealix الحالية

| العنصر | الحالة | المصدر |
|--------|--------|--------|
| SPF | ✅ | `deliverability_state.json` |
| DKIM | ✅ | `deliverability_state.json` |
| DMARC | ✅ (quarantine) | `deliverability_state.json` |

> القيم أعلاه تعكس الحالة المسجّلة في الملف الآلي. حدّثها عند أي تغيير DNS.

---

## التحقق الآلي

`check_deliverability_readiness.py` يفشل الإرسال إذا كان أي من SPF/DKIM/DMARC
غير `true` في `deliverability_state.json`.

---

## أخطاء شائعة

```txt
- نسيان تضمين مزوّد جديد في SPF بعد التبديل.
- DKIM موقّع لكن غير محاذٍ للدومين الظاهر.
- DMARC على p=none فقط (مراقبة بلا حماية).
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
