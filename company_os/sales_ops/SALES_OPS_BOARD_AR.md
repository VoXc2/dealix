# لوحة عمليات المبيعات — Sales Ops Board

لوحة واحدة بسيطة لكل الفرص، تمكّنك من تسليم المتابعة لشخص آخر دون فوضى. مصدر
الحقيقة: `company_os/commercial/board.json`. الحالة المولّدة:
`reports/sales_ops/SALES_OPS_BOARD_STATUS.md` عبر `npm run commercial:plan`.

---

## الحالات الست عشرة (بالترتيب)

```
researched → need_card_ready → draft_ready → approved → sent →
call_due → called → interested → mini_proposal_ready → proposal_sent →
won → delivery_started → active → renewal_candidate
                                   (أو) lost / do_not_contact
```

| الحالة | المعنى | معيار الخروج للحالة التالية |
|--------|--------|------------------------------|
| researched | بحث مكتمل | Client Need Card جاهز |
| need_card_ready | بطاقة حاجة جاهزة | كتابة Draft |
| draft_ready | مسودة جاهزة | اعتماد المؤسس |
| approved | معتمدة للإرسال | إرسال |
| sent | أُرسلت | يحين وقت المكالمة |
| call_due | مكالمة مستحقة | إجراء المكالمة |
| called | تم الاتصال | تحديد الاهتمام |
| interested | مهتم | تجهيز Mini Proposal |
| mini_proposal_ready | عرض جاهز | اعتماد + إرسال |
| proposal_sent | عرض مُرسل | قرار العميل |
| won | تم الكسب | بدء التسليم |
| delivery_started | بدأ التسليم | تشغيل كامل |
| active | نشط | مرشّح تجديد |
| renewal_candidate | مرشّح تجديد | عرض تجديد |
| lost | خسارة | nurture لاحق |
| do_not_contact | حجب | لا تواصل |

---

## القاعدة

كل انتقال للحالة التالية يتطلب اجتياز بوابته (انظر `company_os/quality/`):
- `sent` يتطلب اجتياز بوابة الإيميل.
- `mini_proposal_ready` يتطلب اجتياز بوابة Mini Proposal.
- `delivery_started` يتطلب اجتياز بوابة جاهزية التسليم.

`do_not_contact` مرتبطة بقائمة الحجب `company_os/commercial/suppression.json`؛ أي draft
لشركة محجوبة يُرفض تلقائيًا.

---

## الملكية

كل فرصة لها ملاك في `OWNER_ASSIGNMENT_POLICY_AR.md`. تُعرض في تقرير اللوحة حتى يعرف
كل شخص دوره.
