# بوابة جودة العرض المصغّر (Mini Proposal Quality Gate)

> أي رد إيجابي أو اتصال ناجح يتحول فورًا إلى Mini Proposal — لكنه لا يُرسل آليًا.
> AI drafts. Human approves. System logs.

---

## 1. متى يتولّد العرض المصغّر؟

```txt
positive_reply
send_more_info
price_question
successful_call
diagnostic_request
```

---

## 2. محتوى العرض المصغّر

```txt
Recommended System
Why this system
First Sprint
Deliverables
Timeline
Starter Price
Required Inputs
Expected First Proof
Next Step
Approval Required
```

---

## 3. لا يُرسل تلقائيًا

لأنه يحتوي سعرًا ونطاقًا وقد يترتب عليه التزام:

```txt
approval_status = pending_founder_approval
```

---

## 4. متى تفشل البوابة (Gate fails if)

تفشل البوابة إذا نقص أي عنصر (fail conditions):

```txt
لا يوجد system
لا يوجد deliverables
لا يوجد timeline
لا يوجد starter price
لا يوجد required inputs
لا يوجد approval_required
```

---

## 5. التسعير

الأسعار الافتتاحية مرجعها `company_os/revenue/proposals.json` و`systems.json`. **كل تسعير يتطلب اعتماد المؤسس** — لا قرار تسعير من الـ AI (خط أحمر في الحوكمة).

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
