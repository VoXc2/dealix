# بوابة جودة العرض المصغّر — Mini Proposal Quality Gate

أي رد إيجابي أو اتصال ناجح يتحول فورًا إلى Mini Proposal. المنطق: `miniProposalGate`
في `scripts/lib/commercial.js`.

---

## متى يتولّد؟

```
positive_reply / send_more_info / price_question /
successful_call / diagnostic_request
```

## المحتوى

```
Recommended System     النظام الموصى به
Why this system        لماذا هذا النظام
First Sprint           أول سبرنت
Deliverables           المخرجات
Timeline               الجدول الزمني
Starter Price          السعر الافتتاحي
Required Inputs         المدخلات المطلوبة
Expected First Proof   أول إثبات متوقع
Next Step              الخطوة التالية
Approval Required       اعتماد مطلوب
```

## تفشل البوابة إذا

| السبب | الوصف |
|------|-------|
| `no_system` | لا يوجد نظام |
| `no_deliverables` | لا توجد مخرجات |
| `no_timeline` | لا يوجد جدول زمني |
| `no_starter_price` | لا يوجد سعر افتتاحي |
| `no_required_inputs` | لا توجد مدخلات مطلوبة |
| `no_approval_required` | `approval_required` ليس `true` |

---

## قاعدة الاعتماد

Mini Proposal **لا يُرسَل تلقائيًا** لأنه يحمل سعرًا ونطاقًا وقد يترتب عليه التزام.
يبقى في الحالة:

```
approval_status = pending_founder_approval
```

ويظهر في `DAILY_SUPER_COMMAND.md` ضمن "العروض بانتظار الاعتماد" حتى يقرر المؤسس.
