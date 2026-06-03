# نموذج حالة العميل المحتمل — Lead Status Model

تعريف دقيق لكل حالة ومعيار دخولها وخروجها، حتى لا تتحرك الفرص بشكل عشوائي.

---

## الانتقالات المسموحة

```
researched ──▶ need_card_ready ──▶ draft_ready ──▶ approved ──▶ sent
   └──────────────────────────────────────────────────────▶ do_not_contact
sent ──▶ call_due ──▶ called ──▶ interested ──▶ mini_proposal_ready ──▶ proposal_sent
called ─────────────────────────▶ lost
proposal_sent ──▶ won ──▶ delivery_started ──▶ active ──▶ renewal_candidate
proposal_sent ──▶ lost
```

---

## معايير الحالة

| الحالة | يدخلها عندما | يخرج منها عندما | البوابة |
|--------|--------------|------------------|---------|
| researched | اكتمل البحث | اكتملت Need Card | — |
| need_card_ready | Need Card جاهزة | كُتبت المسودة | — |
| draft_ready | المسودة مكتوبة | اعتمدها المؤسس | Email Gate |
| approved | اعتمدها المؤسس | أُرسلت فعليًا | — |
| sent | أُرسلت | حان وقت المتابعة | — |
| call_due | مرّ وقت كافٍ بعد الإرسال | تم الاتصال | Call Gate |
| called | تم الاتصال | عُرف مستوى الاهتمام | — |
| interested | أبدى اهتمامًا | جُهّز العرض | — |
| mini_proposal_ready | Mini Proposal جاهز | اعتمده المؤسس وأُرسل | Mini Proposal Gate |
| proposal_sent | أُرسل العرض | قرار العميل | — |
| won | وافق العميل | بدأ التسليم | Delivery Gate |
| delivery_started | بدأ التسليم | تشغيل كامل | Delivery Gate |
| active | تشغيل كامل | اقترب التجديد | — |
| renewal_candidate | اقترب التجديد | تجديد أو خسارة | — |
| lost | رفض/توقف | nurture بعد مدة | — |
| do_not_contact | طلب عدم تواصل أو حجب | لا يخرج | Suppression |

---

## القاعدة

لا تُرفَع فرصة لحالة تتطلب بوابة قبل اجتياز تلك البوابة. `npm run commercial:check`
يرصد أي فرصة في `delivery_started/active` بدون نطاق ومعايير قبول ويعتبرها مخالفة حرجة.
