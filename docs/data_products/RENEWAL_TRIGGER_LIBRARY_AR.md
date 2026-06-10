# مكتبة إشارات التجديد — Renewal Trigger Library

> **٨ إشارات تجديد** مع طريقة الكشف، كتيّب التدخل، المالك، وتوقيت
> التجديد (شهر ٩ review / شهر ١٠ قرار / شهر ١١ إغلاق). + إطار **save
> vs let-go**.

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0  
**Schema:** `schemas/renewal_trigger.schema.json`  
**البيانات:** `data/data_products/renewal_triggers.jsonl` (8 إشارات)

---

## 1. الإشارات الثماني (8 Triggers)

| # | الإشارة | الخطورة الافتراضية | المالك |
| - | --- | --- | --- |
| 1 | `usage_drop` | high | csm |
| 2 | `stakeholder_change` | high | csm |
| 3 | `missed_check_in` | medium | csm |
| 4 | `scope_creep` | medium | csm |
| 5 | `budget_cycle` | low | csm |
| 6 | `leadership_change` | high | founder |
| 7 | `competitor_mention` | high | csm |
| 8 | `low_nps` | critical | founder |

---

## 2. توقيت التجديد (Renewal Timing)

- **Month 9 review:** فحص صحي شامل + KPI review.
- **Month 10 decision:** قرار save-or-let-go + عرض التجديد.
- **Month 11 close:** توقيع + handover.

> الانحراف عن هذا الإطار (مثلاً: تجديد متأخر في شهر 8) يحتاج تبرير
> من CSM Lead.

---

## 3. الإشارة ١ — `usage_drop` (تراجع الاستخدام)

- **الكشف:** weekly product_usage signal vs baseline، تراجع > 30% مُستمر أسبوعين.
- **مصدر البيانات:** product_usage.
- **الخطورة:** high.
- **كتيّب التدخل (3 خطوات):**
  1. **Day 2 (csm):** رسالة عربية تُسأل عن العائق: `لاحظت تراجع استخدام [workflow]. فيه عائق تقني أو أولوية ضايعة؟ ١٠ دقائق أفهم وأحل.`
  2. **Day 5 (csm):** اجتماع health-check 20 دقيقة مع sales lead.
  3. **Day 14 (founder):** تدخل شخصي إذا لم يتعافى.
- **Save vs Let-go:** 
  - **Save:** السبب قابل للإصلاح < 30 يوم، stakeholder مُشارك.
  - **Let-go:** تراجع > 60% مُستمر 4 أسابيع، لا stakeholder متاح.

---

## 4. الإشارة ٢ — `stakeholder_change` (تغيّر صاحب المصلحة)

- **الكشف:** LinkedIn + CRM stakeholder map diff؛ flag لمُقرِّر جديد.
- **مصدر البيانات:** stakeholder_map.
- **الخطورة:** high.
- **كتيّب التدخل:**
  1. **Day 3 (csm):** تهنئة + صفحة تعريفية: `مبروك المنصب. أرسل لك صفحة واحدة: من Dealix، ماذا أنجزنا مع [السابق]، وما الخطوات القادمة.`
  2. **Day 10 (sales):** mini discovery مع الـ stakeholder الجديد.
  3. **Day 30 (founder):** تصعيد إذا لم يتفاعل.
- **Save vs Let-go:** Save إذا كان المُقرِّر الجديد متاحاً والميزانية مُتوارثة. Let-go إذا لم يكن هناك تواصل في 30 يوم والشخص السابق رحل.

---

## 5. الإشارة ٣ — `missed_check_in` (فقدان جلسة المراجعة)

- **الكشف:** weekly_reporting missed أسبوعين متتاليين.
- **الخطورة:** medium.
- **كتيّب التدخل:**
  1. **Day 1 (csm):** تنبيه لطيف: `فاتتنا آخر مراجعتين. نقفل الأسبوع هذي ١٥ دقيقة.`
  2. **Day 7 (csm):** إعادة جدولة خلال 7 أيام، تقليل الإيقاع إذا لزم.
  3. **Day 14 (founder):** مكالمة مباشرة إذا 3 missed متتالية.
- **Save vs Let-go:** Save إذا أمكن downshift للإيقاع. Let-go إذا لم يُستعد الإيقاع.

---

## 6. الإشارة ٤ — `scope_creep` (توسعة نطاق)

- **الكشف:** حجم change request > 20% delta في ربع.
- **الخطورة:** medium.
- **كتيّب التدخل:**
  1. **Day 3 (csm):** كمّ النطاق: `المتطلبات الجديدة = [X] ساعة إضافية.`
  2. **Day 7 (sales):** تحويل إلى upsell.
  3. **Day 14 (founder):** تخفيض scope رسمياً إذا لا ميزانية.
- **Save vs Let-go:** Save إذا تحوّل creep إلى upsell > 30% من ACV. Let-go إذا لم يُموَّل والجودة تنزل.

---

## 7. الإشارة ٥ — `budget_cycle` (دورة الميزانية)

- **الكشف:** السنة المالية للعميل + procurement calendar.
- **الخطورة:** low (proactive).
- **كتيّب التدخل:**
  1. **Day -90 (csm):** ملاحظة تجديد استباقية: ROI تراكمي + ٣ سيناريوهات سعر.
  2. **Day -60 (csm):** حزمة procurement-ready.
  3. **Day -14 (founder):** توقيع نهائي شخصي.
- **Save vs Let-go:** Save إذا كان الإشعار استباقي. Let-go إذا كانت الميزانية مجمّدة.

---

## 8. الإشارة ٦ — `leadership_change` (تغيّر القيادة)

- **الكشف:** LinkedIn + news + CRM diff.
- **الخطورة:** high.
- **كتيّب التدخل:**
  1. **Day 3 (csm):** تهنئة + transition memo.
  2. **Day 14 (founder):** مكالمة إعادة تأطير للعلاقة.
  3. **Day 30 (founder):** إنهاء منظّم إذا لم يحدث تفاعل.
- **Save vs Let-go:** Save إذا القائد الجديد متاح + يستخدم outputs. Let-go إذا تغيّرت القيادة > 2 مرة في 12 شهر.

---

## 9. الإشارة ٧ — `competitor_mention` (ذكر منافس)

- **الكشف:** support_ticket أو call notes فيها اسم منافس.
- **الخطورة:** high.
- **كتيّب التدخل:**
  1. **Day 2 (csm):** اعتراف + سؤال: `ما الذي تبحث عنه في [المنافس]؟`
  2. **Day 7 (sales):** جدول مقارنة صادق بدون FUD.
  3. **Day 14 (founder):** مكالمة حسم.
- **Save vs Let-go:** Save إذا كانت الفجوة قابلة للإصلاح في المنتج أو السعر. Let-go إذا الفجوة هيكلية.

---

## 10. الإشارة ٨ — `low_nps` (NPS منخفض)

- **الكشف:** nps_survey ربع سنوي، promoter share < 30%.
- **الخطورة:** critical.
- **كتيّب التدخل:**
  1. **Day 2 (csm):** detractor recovery call 48 ساعة.
  2. **Day 7 (founder):** مراجعة هيكلية للقضية.
  3. **Day 60 (founder):** اجتماع حاسم save-or-let-go.
- **Save vs Let-go:** Save إذا كانت الشكوى محددة وقابلة للإصلاح. Let-go إذا كانت منتشرة + > 3 حوادث تصعيد.

---

## 11. إطار Save vs Let-go (الإطار الموحّد)

| الحالة | Save criteria | Let-go criteria |
| --- | --- | --- |
| root cause قابل للإصلاح < 30 يوم | ✓ | |
| stakeholder نشط ومتاح | ✓ | |
| ROI فعلي أو مرتقب | ✓ | |
| التكلفة المتوقعة للإنقاذ < LTV المُسترد | ✓ | |
| < 2 من criteria أعلاه | | ✓ |
| > 2 leadership changes في 12 شهر | | ✓ |
| usage drop > 60% مُستمر 4 أسابيع | | ✓ |
| شكوى منتشرة + > 3 تصعيدات | | ✓ |

> **القاعدة:** قرار Let-go لا يعني فشل. يعني قرار **استثمار** في عملاء
> لديهم LTV أعلى.

---

## 12. KPIs للتجديد

- **Renewal rate:** % عملاء جدّدوا من المؤهلين.
- **Save rate:** % من at-risk تم إنقاذهم.
- **Time-to-renewal:** أيام من month 9 review إلى close.
- **NPS promoter share:** quarterly.

---

## 13. المراجع (References)

- `schemas/renewal_trigger.schema.json`
- `data/data_products/renewal_triggers.jsonl`
- `data/customer_success/client_health.jsonl`
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`
- `docs/RENEWAL_TIMING_FRAMEWORK_AR.md` (إن وُجد).
- `docs/data_products/PRICING_SENSITIVITY_LIBRARY_AR.md`
