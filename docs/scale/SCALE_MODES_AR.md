# Scale Modes — كيف نرفع الإنتاج بدون تدمير الجودة

> القاعدة الأساسية: **الإنتاج (Account Packs / Drafts) يتوسع أسرع من الإرسال.**
> الإرسال الفعلي محكوم بـ deliverability وجودة الردود وصحة الدومين.

---

## مستويات التوسع

| Mode | Account Packs/day | Sends/day | Calls/day | شروط |
|------|------------------:|----------:|----------:|------|
| Dry Run | 25 | 0 | 0 | اختبار داخلي |
| Soft Launch | 50–100 | 10–25 يدوي | 5–15 | Score ≥ 75 |
| Controlled Launch | 200 | 25–75 | 20–40 | Score ≥ 85 |
| Full Launch | 400 | Controlled only | 40–80 | Score ≥ 90 |
| Scale | 600–1000 | حسب deliverability | فريق تشغيل | أسبوعان جودة |

المصدر الرسمي للأرقام: `company_os/scale/scale_state.json`.

---

## القاعدة

```txt
Account Packs can scale faster than sending.
Draft production can be 400/day from day one.
Actual sending is controlled by deliverability, reply quality, and domain health.
```

البريد ليس مجرد عدد. مزوّدو البريد (مثل Gmail) يشترطون authentication مثل
SPF/DKIM، و DMARC للمرسلين الكبار، ويطلبون one-click unsubscribe للرسائل
التسويقية، مع مراقبة معدلات spam؛ لذلك **الإنتاج شيء والإرسال شيء آخر**.

---

## الفرق بين الإنتاج والإرسال

| البُعد | الإنتاج (Production) | الإرسال (Sending) |
|--------|---------------------|-------------------|
| ما هو؟ | Account Packs + Drafts | إرسال فعلي خارجي |
| من ينفّذ؟ | وكلاء L1–L3 | المؤسس بعد موافقة |
| السقف | جودة الـ Account Pack | deliverability + reply quality |
| يوم 1 | حتى 400 draft/day | 10–25 يدوي فقط |
| الخطر | جودة منخفضة | حرق الدومين |

---

## شروط الانتقال بين الأوضاع

| الانتقال | الشرط |
|----------|-------|
| Dry Run → Soft Launch | Account Pack Quality ≥ 75 + فحوصات أمان تمر |
| Soft Launch → Controlled | Score ≥ 85 + deliverability pass + ردود إيجابية |
| Controlled → Full | Score ≥ 90 + capacity utilization < 80% |
| Full → Scale | أسبوعان من الجودة المستقرة + فريق تشغيل + capacity مثبتة |

---

## قاعدة الفرملة

```txt
إذا انخفض Account Pack Quality < عتبة الوضع → ارجع وضعًا للخلف.
إذا تجاوز spam rate الحد التحذيري → ثبّت الإرسال.
إذا تجاوز Delivery Capacity Utilization 80% → لا ترفع الإرسال.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
