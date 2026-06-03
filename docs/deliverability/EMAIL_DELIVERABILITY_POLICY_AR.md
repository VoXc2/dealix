# Email Deliverability Policy — سياسة قابلية تسليم البريد

> الإنتاج شيء والإرسال شيء آخر. هذه السياسة تحمي الدومين وتضمن وصول الرسائل
> الشرعية إلى صندوق الوارد، لا إلى السبام.

---

## شروط الإرسال

```txt
1. SPF جاهز
2. DKIM جاهز
3. DMARC جاهز
4. unsubscribe/suppression موجود
5. do-not-contact محترم
6. لا purchased lists
7. لا fake Re/Fwd
8. لا claims مضمونة
9. no sudden volume spike
```

المصدر الآلي للحالة: `company_os/deliverability/deliverability_state.json`.
يتحقق منها: `python dealix.py deliverability-check`.

---

## لماذا هذه الشروط؟

مزوّدو البريد الكبار (مثل Gmail) يشترطون مصادقة المرسِل عبر SPF و DKIM،
ويطلبون DMARC للمرسلين بكميات كبيرة، مع one-click unsubscribe للرسائل
التسويقية ومراقبة معدلات السبام. تجاهل هذه الشروط = وصول إلى السبام أو حظر
الدومين بالكامل.

---

## الفصل بين الإنتاج والإرسال

| البُعد | الإنتاج | الإرسال |
|--------|---------|---------|
| السقف | جودة الـ draft | deliverability + موافقة |
| يوم 1 | حتى 400/يوم | 10–25 يدوي |
| المخاطرة | جودة | حرق الدومين |

---

## بوابات السياسة

| البوابة | الحالة المطلوبة |
|---------|------------------|
| Authentication | SPF + DKIM + DMARC = pass |
| Compliance | unsubscribe + suppression + do-not-contact = active |
| Lists | purchased_lists = false |
| Honesty | fake_reply_fwd = false, guaranteed_claims = false |
| Volume | no sudden spike |
| Health | spam < hard cap, bounce < hard cap |

أي بوابة فاشلة = إيقاف الإرسال حتى تُصلَح.

---

## الملفات المرتبطة

- `SENDING_VOLUME_POLICY_AR.md` — حدود الحجم والرفع التدريجي.
- `DOMAIN_AUTHENTICATION_CHECKLIST_AR.md` — إعداد SPF/DKIM/DMARC.
- `SPAM_RATE_MONITORING_AR.md` — مراقبة السبام.
- `UNSUBSCRIBE_AND_SUPPRESSION_POLICY_AR.md` — إلغاء الاشتراك والكبت.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
