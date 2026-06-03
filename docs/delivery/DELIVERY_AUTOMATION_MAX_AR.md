# Delivery Automation Max — أتمتة التسليم

ماذا يحدث عند `won`، وما البوابة التي تمنع تسليمًا ناقصًا.

---

## 1. عند `won` يُنشئ النظام

```
client_workspace
required_inputs_checklist
delivery_task_list
first_output_template
acceptance_gate
weekly_value_report
renewal_trigger
```

---

## 2. خط أنابيب التسليم

```
won
→ intake_required
→ inputs_received
→ delivery_started
→ first_output_ready
→ client_review
→ revision
→ accepted
→ weekly_value_report
→ renewal_candidate
```

---

## 3. بوابة التسليم (Delivery Gate)

لا يبدأ التسليم إذا نقص أيٌّ من:

```
selected_system
scope
required_inputs
success_metric
acceptance_criteria
owner
```

كل Account Pack يحمل مسبقًا `delivery_pack` و`required_inputs` و`acceptance_criteria`،
ما يجعل الانتقال من `won` إلى التسليم سلسًا.

---

## 4. الربط مع الحوكمة

- التسليم للعميل = **Act with Approval** (المؤسس يعتمد) حسب `company_os/governance/agent_permissions.md`.
- بيانات العميل في التسليم منفصلة عن بيانات الاستهداف (انظر `docs/privacy/`).

---

## 5. الحالة الحالية

أتمتة التسليم **موصّفة وجاهزة للتفعيل عند أول `won`**. لا توجد صفقات `won` في بيانات الـseed،
لذلك لا خطوط تسليم نشطة بعد — وهذا ما يعكسه `DAILY_SUPER_COMMAND.md` بأمانة.

---

*Version 1.0*
