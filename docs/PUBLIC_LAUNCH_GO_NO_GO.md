# Public Launch — Go / No-Go

## Go فقط إذا تحققت كل البنود الحرجة

- [ ] استقرار الإنتاج ≥ 14 يوماً بدون حادث P1
- [ ] 5–10 عملاء beta؛ ≥ 3 دافعين فعليين (أو معيار بديل مكتوب في مجلس الإدارة)
- [ ] Terms، Privacy، DPA منشورة ومراجعقة قانونياً
- [ ] [`BILLING_RUNBOOK.md`](BILLING_RUNBOOK.md) مختبر sandbox→live
- [ ] [`WHATSAPP_PRODUCTION_CUTOVER.md`](WHATSAPP_PRODUCTION_CUTOVER.md) مكتمل إذا وُجد WhatsApp إنتاجي
- [ ] نسخ احتياطي واختبار استعادة موثّق
- [ ] [`PUBLIC_LAUNCH_CHECKLIST.md`](PUBLIC_LAUNCH_CHECKLIST.md) مكتمل تقريباً

## فحص جاهزية التشغيل قبل أي Cutover

- [ ] تأكيد أن health endpoints تعمل من خارج الشبكة (`/live`, `/ready`, `/health/deep`).
- [ ] تنفيذ smoke tests على نسخة staging ثم production وتوثيق النتائج في تذكرة الإطلاق.
- [ ] التأكد أن كل المفاتيح الحساسة موجودة عبر secrets manager (وليس `.env` محلي).
- [ ] التأكد من تفعيل المراقبة والتنبيهات (latency, error rate, payment failures).

## ملاحظة مهمة بخصوص "الاتصال بالسيرفر"

قبل طلب الاتصال بأي سيرفر (مثل `03e6bb4b-bdf5-4aa7-86ed-bc94fa293c0e`) يجب تحديد نوعه بوضوح:

1. **Railway / Render / Fly / K8s / VPS**.
2. طريقة الوصول: **CLI token** أو **SSH key** أو **kubectl context**.
3. الهدف من الجلسة: فحص logs، تنفيذ migration، أو smoke test.

بدون هذه البيانات، أي "اتصال" سيكون غير قابل للتحقق وقد يسبب تغييراً غير آمن في بيئة الإنتاج.

## No-Go típico

- لا عملية حوادث؛ لا secrets manager؛ لا إثبات فوترة؛ إرسال حي بدون بوابات.

## بعد القرار

- إذا لم يتحقق Go: ابقَ على تسمية **Paid Private Beta** حتى إغلاق الفجوات ([`PAID_BETA_SCORECARD.md`](PAID_BETA_SCORECARD.md)).
