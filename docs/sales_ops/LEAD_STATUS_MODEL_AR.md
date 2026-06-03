# نموذج حالات العميل المحتمل (Lead Status Model)

> لوحة واحدة، ١٦ حالة، انتقال واضح. الـ AI يجهّز البطاقات، المؤسس يحرّكها.
> AI drafts. Human approves. System logs.

---

## 1. الحالات الست عشرة (بالترتيب)

| # | الحالة (token) | المعنى | المالك الافتراضي |
|---|----------------|--------|------------------|
| 1 | `researched` | تم بحث الشركة | research_owner |
| 2 | `need_card_ready` | بطاقة احتياج العميل جاهزة | research_owner |
| 3 | `draft_ready` | مسودة إيميل جاهزة ومُقيّمة | email_owner |
| 4 | `approved` | اعتمدها المؤسس | email_owner |
| 5 | `sent` | أُرسلت | email_owner |
| 6 | `call_due` | اتصال مستحق | call_owner |
| 7 | `called` | تم الاتصال | call_owner |
| 8 | `interested` | أبدى اهتمامًا | call_owner |
| 9 | `mini_proposal_ready` | عرض مصغّر جاهز | proposal_owner |
| 10 | `proposal_sent` | أُرسل العرض | proposal_owner |
| 11 | `won` | تم الإغلاق | proposal_owner |
| 12 | `delivery_started` | بدأ التسليم | delivery_owner |
| 13 | `active` | عميل نشط | delivery_owner |
| 14 | `renewal_candidate` | مرشّح للتجديد | delivery_owner |
| 15 | `lost` | خسارة | proposal_owner |
| 16 | `do_not_contact` | عدم التواصل (suppression) | governance |

---

## 2. قواعد الانتقال

```txt
researched → need_card_ready → draft_ready → approved → sent
sent → call_due → called → interested → mini_proposal_ready → proposal_sent → won
won → delivery_started → active → renewal_candidate
أي مرحلة → lost (مع سبب)
أي مرحلة → do_not_contact (suppression / opt-out)
```

- لا انتقال إلى `approved` إلا باعتماد بشري.
- لا انتقال إلى `sent` إلا بعد اجتياز Email Quality Gate.
- لا انتقال إلى `delivery_started` إلا بعد اجتياز Delivery Readiness Gate.

---

## 3. المصدر الآلي

تُحسب الحالات في `scripts/commercial-daily-plan.js` وتُخزَّن في `company_os/commercial/sales_board.json`، وتُعرض في `reports/sales_ops/SALES_OPS_BOARD_STATUS.md`.

> الفاحص يتحقق من اكتمال الحالات الـ16؛ نقص أي حالة = فشل.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
