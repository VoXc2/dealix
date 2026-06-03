# قائمة التحقق اليومية للفاوندر — Dealix
# Founder Daily Execution Checklist
# وقت التنفيذ: 45 دقيقة (8:00 - 8:45 ص الرياض)

---

## الصباح — قبل 9:00 ص (20 دقيقة)

### 1. مراجعة الحالة (5 دق)
- [ ] افتح `/api/v1/commercial/daily-brief` واقرأ الملخص
- [ ] راجع أي pipeline أحداث من الليلة الماضية
- [ ] تحقق من حالة Railway (API + Worker + Watchdog)

### 2. تواصل العملاء — مراجعة المسودات (10 دق)
- [ ] راجع أي warm intro drafts في `/api/v1/commercial/warm-intro/draft`
- [ ] وافق على الرسائل الجيدة ✅ أو عدّل ✏️
- [ ] **لا ترسل أي رسالة بدون مراجعة** (NO_LIVE_SEND)

### 3. فرص الـ Pipeline (5 دق)
- [ ] افتح قائمة العملاء المحتملين
- [ ] حدد 3 أسماء للتواصل اليوم
- [ ] اختر قالب واتساب المناسب من `data/templates/warm_intro_whatsapp_ar.md`

---

## منتصف اليوم (10 دقائق)

### 4. متابعة العملاء الحاليين
- [ ] هل هناك رد من أي عميل تواصلنا معه؟
- [ ] هل يحتاج pilot نشط تحديثاً اليوم؟
- [ ] هل هناك proof event يجب توثيقه؟

---

## المساء — قبل 6:00 م (15 دقيقة)

### 5. التوثيق اليومي
- [ ] سجّل كل تواصل فعلي تم اليوم
- [ ] أضف أي proof event جديد عبر `/api/v1/commercial/proof/build`
- [ ] حدّث حالة الـ pipeline للعملاء النشطين

### 6. تقييم اليوم (5 دق)
- [ ] كم رسالة أُرسلت اليوم؟ ___
- [ ] كم رد استلمنا؟ ___
- [ ] هل تم توثيق proof event؟ نعم / لا
- [ ] ما الإجراء الأهم لغد؟ ___

---

## مؤشرات الأسبوع — تُراجع كل خميس

| المؤشر | الهدف الأسبوعي | الفعلي |
|---------|----------------|--------|
| رسائل warm intro مُرسَلة | 5 | ___ |
| ردود مستلمة | 2+ | ___ |
| تشخيصات مجانية مُجدولة | 1 | ___ |
| pilots نشطة | --- | ___ |
| proof events موثقة | 1 | ___ |
| MRR حالي | --- | ___ ريال |

---

## القواعد الذهبية للفاوندر

1. **التواصل أولاً** — اليوم بلا رسالة واحدة = يوم ضائع
2. **الموافقة دائماً** — لا إرسال بدون مراجعتك الشخصية
3. **التوثيق الحي** — الدليل اللي ما يتوثق = دليل غير موجود
4. **الإثبات قبل البيع** — Proof Pack قبل عرض Managed Ops
5. **الصدق مع الأرقام** — لا نبالغ، لا نُضخّم

---

## روابط سريعة

```bash
# تشخيص جديد
curl -X POST https://api.dealix.me/api/v1/commercial/diagnostic/generate \
  -H "X-API-Key: $DEALIX_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"الشركة","sector":"b2b_services"}'

# مسودة warm intro
curl -X POST https://api.dealix.me/api/v1/commercial/warm-intro/draft \
  -H "X-API-Key: $DEALIX_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prospect_name":"الاسم","company_name":"الشركة","sector":"b2b_services"}'

# بدء pilot
curl -X POST https://api.dealix.me/api/v1/commercial/pilot/start \
  -H "X-API-Key: $DEALIX_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"account_id":"acc-001","company_name":"الشركة"}'

# رابط دفع
curl -X POST https://api.dealix.me/api/v1/commercial/payment/link \
  -H "X-API-Key: $DEALIX_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"service_tier":"sprint_499","customer_name":"الاسم"}'

# ملخص يومي
curl https://api.dealix.me/api/v1/commercial/daily-brief \
  -H "X-API-Key: $DEALIX_ADMIN_API_KEY"
```

---

*آخر تحديث: 2026 | Dealix v3.0*
