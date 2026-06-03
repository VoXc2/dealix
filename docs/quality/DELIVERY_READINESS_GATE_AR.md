# بوابة جاهزية التسليم (Delivery Readiness Gate)

> لا تبِع نظامًا إلا وهو جاهز للتسليم. لا يبدأ التسليم إذا نقص أي مدخل.
> AI drafts. Human approves. System logs.

---

## 1. جاهزية التسليم لكل نظام

| النظام | جاهزية التسليم المطلوبة |
|--------|--------------------------|
| Revenue Operating System | Leakage Map + Workflow + Report Template |
| Executive Command OS | KPI Map + Daily Report + Decision Log |
| Follow-up Recovery OS | Queue + Status Model + Message Set |
| WhatsApp Client OS | Flow Map + Action Cards + Handoff Policy |
| Proposal & Proof OS | Proposal Template + Proof Pack + Scope Block |

> المرجع: `company_os/commercial/systems.json` (حقل `delivery_readiness`).

---

## 2. متى تفشل البوابة (Gate fails if)

تفشل البوابة (وتتحول الحالة إلى `delivery_blocked`) إذا نقص أي مما يلي (fail conditions):

```txt
لا يوجد client
لا يوجد selected_system
لا يوجد scope
لا يوجد required_inputs
لا يوجد starter_price
لا يوجد delivery_pack
لا يوجد success_metric
لا يوجد acceptance_criteria
```

> الحد الأدنى الإلزامي للفاحص: `scope` + `required inputs` + `success metric` + `acceptance criteria`.

---

## 3. الربط بالتسليم القائم

يتكامل هذا مع SOP التسليم الحالي: `company_os/delivery/p1_delivery_sop.md` و`p1_intake_template.md` و`proof_pack_template.md`. لا انتقال إلى `delivery_started` على اللوحة إلا بعد اجتياز هذه البوابة.

---

## 4. حدود الأمان والامتثال

- بيانات العميل تُعالَج وفق `company_os/governance/data_handling_checklist.md` و`pdpl_checklist.md`.
- لا يُرسل الـ AI أي تسليم للعميل؛ التسليم باعتماد المؤسس فقط.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
