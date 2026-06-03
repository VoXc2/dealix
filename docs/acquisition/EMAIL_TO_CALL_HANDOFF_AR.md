# Email → Call Handoff — تسليم العمل بين الإيميل والاتصال

**الهدف:** أن تقدر تعطي شخصًا آخر قائمة اتصال جاهزة. أنت ترسل (أو تعتمد) الإيميلات، وشخص ثانٍ يتابع بالاتصال — وكلاهما يعمل من نفس البيانات بلا التباس.

- **الطابور:** [`reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md`](../../reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md)

---

## 1. المسار

```txt
Company Intelligence Pack
   │  (email_subject + email_draft = مسودة)
   ▼
🟡 قائمة موافقة المؤسس  ── يعتمد ──►  إرسال البريد (يدوي/معتمد)
   │
   ▼
Call Brief (CB-xxx)  ──►  متصل بشري يتابع
   │
   ▼
Mini Proposal (MP-xxx)  ──►  بعد اهتمام العميل (بموافقة المؤسس)
   │
   ▼
Delivery Pipeline (DP-xxx)  ──►  إذا وافق العميل
```

## 2. من يفعل ماذا؟

| الدور | المهمة | البوابة |
|------|--------|---------|
| النظام (Dealix) | يولّد Pack + Need Card + Email draft + Call Brief + Mini Proposal | تلقائي (تجهيز فقط) |
| المؤسس | يعتمد مسودة البريد والعرض | 🟡 موافقة إلزامية |
| المُرسِل | يرسل البريد المعتمد | يدوي |
| المتصل البشري | يتابع عبر Call Brief | لا اتصال آلي |
| المؤسس | يعتمد الانتقال للتسليم | بوابة التسليم |

## 3. حالة كل صف في الطابور

كل صف في `EMAIL_TO_CALL_HANDOFF_QUEUE.md` يبيّن:

```txt
Company · System · Email subject (draft) · Email status (🟡 awaiting approval) · Call Brief id · Contact role · Next step
```

مثال:

```txt
TrainMe KSA · WhatsApp Client OS · «سبرنت 7 أيام لترتيب محادثات واتساب…» · 🟡 Draft — awaiting approval · CB-007 · Operations Manager · مكالمة 20 دقيقة…
```

---

## 4. قواعد صارمة (Hard rules)

```txt
- لا إرسال بريد خارجي تلقائيًا (يبقى مسودة حتى موافقة المؤسس).
- لا اتصال آلي بالعملاء — Call Brief لمتصل بشري فقط.
- لا واتساب بارد آلي، ولا أتمتة LinkedIn.
- لا قوائم مشتراة، ولا عناوين Re:/Fwd: مزيّفة.
- لا وعود عائد مضمونة.
- احترام قائمة عدم التواصل (do_not_contact / suppression).
```

تُفحَص هذه القواعد آليًا في [`scripts/acquisition_delivery_check.py`](../../scripts/acquisition_delivery_check.py).
