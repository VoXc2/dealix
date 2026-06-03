# معايير قبول الأنظمة (System Acceptance Criteria)

> لكل نظام معايير قبول صريحة تُربط بمخرجاته. عند تحقّقها يوافق العميل وينتقل الـ pipeline إلى `accepted`،
> ثم يصبح ممكنًا `weekly_value_report` ثم `renewal_candidate`. المرجع الموحّد: `/home/user/dealix/AGENTS.md`.

الجمهور: **Delivery Operator** + **العميل** (يوافق).

---

## كيف يعمل القبول

```txt
first_output_ready → client_review → (العميل يوافق على المعايير) → accepted
   → weekly_value_report (قيمة ملاحَظة فقط) → renewal_candidate (دليل قيمة/توسّع)
```

قواعد ثابتة:
- لا قبول مبني على ادعاء إيراد مضمون.
- المخرجات المرتبطة موصوفة في `SYSTEM_DELIVERY_CHECKLISTS_AR.md`.

---

## 1. `revenue_os` — نظام تشغيل الإيرادات

| المعيار | المخرج المرتبط |
|---|---|
| كل فرصة لها status | Opportunity Stage Model |
| كل status له next action | Follow-up Workflow |
| كل next action له draft أو إجراء | Draft Templates |
| يوجد تقرير واضح للإدارة | Daily/Weekly Revenue Report |

- [ ] كل فرصة لها status — (Opportunity Stage Model).
- [ ] كل status له next action — (Follow-up Workflow).
- [ ] كل next action له draft أو إجراء — (Draft Templates).
- [ ] يوجد تقرير واضح للإدارة — (Daily/Weekly Revenue Report).

---

## 2. `executive_command_os` — نظام القيادة التنفيذية

| المعيار | المخرج المرتبط |
|---|---|
| التقرير اليومي يعطي قرارًا واضحًا | Daily Command Report |
| المخاطر مرتبة | Risk/Priority Matrix |
| الفرص مرتبة | Risk/Priority Matrix |
| التنفيذ له owner | Executive Action Board |

- [ ] التقرير اليومي يعطي قرارًا واضحًا — (Daily Command Report).
- [ ] المخاطر مرتبة — (Risk/Priority Matrix).
- [ ] الفرص مرتبة — (Risk/Priority Matrix).
- [ ] التنفيذ له owner — (Executive Action Board).

---

## 3. `followup_recovery_os` — نظام استرجاع المتابعات

| المعيار | المخرج المرتبط |
|---|---|
| كل lead له حالة | Lead Status Model |
| كل حالة لها رسالة | Follow-up Message Set |
| كل رسالة لها وقت متابعة | Reminder Rhythm |
| كل أسبوع يوجد recovery report | Recovery Report |

- [ ] كل lead له حالة — (Lead Status Model).
- [ ] كل حالة لها رسالة — (Follow-up Message Set).
- [ ] كل رسالة لها وقت متابعة — (Reminder Rhythm).
- [ ] كل أسبوع يوجد recovery report — (Recovery Report).

---

## 4. `whatsapp_client_os` — نظام عملاء واتساب

| المعيار | المخرج المرتبط |
|---|---|
| لا يوجد طلب أسرار داخل واتساب | Secure Portal Handoff Guide |
| كل نوع محادثة له flow | WhatsApp Flow Map |
| كل حالة حساسة لها human handoff | Human Handoff Policy |
| كل أسبوع يوجد review | Weekly WhatsApp Review |

- [ ] لا يوجد طلب أسرار داخل واتساب — (Secure Portal Handoff Guide).
- [ ] كل نوع محادثة له flow — (WhatsApp Flow Map).
- [ ] كل حالة حساسة لها human handoff — (Human Handoff Policy).
- [ ] كل أسبوع يوجد review — (Weekly WhatsApp Review).

---

## 5. `proposal_proof_os` — نظام العروض والإثبات

| المعيار | المخرج المرتبط |
|---|---|
| العرض واضح | Proposal Template |
| النطاق واضح | Scope/Out-of-scope |
| الدليل واضح | Proof Pack Template |
| المخاطر واضحة | Risk & Assumption Block |
| الخطوة التالية واضحة | Next-step Card |

- [ ] العرض واضح — (Proposal Template).
- [ ] النطاق واضح — (Scope/Out-of-scope).
- [ ] الدليل واضح — (Proof Pack Template).
- [ ] المخاطر واضحة — (Risk & Assumption Block).
- [ ] الخطوة التالية واضحة — (Next-step Card).

---

## 6. أثر القبول على الـ Pipeline

```txt
كل معايير النظام محقّقة + موافقة العميل
   → الحالة accepted
   → يتفعّل weekly_value_report (تقرير قيمة ملاحَظة فقط — لا وعود)
   → عند وجود دليل قيمة أو توسّع: renewal_candidate
```

- تُسجَّل بوابة `accepted` وفق `schemas/delivery_acceptance_gate.schema.json` (انظر `DELIVERY_ACCEPTANCE_GATES_AR.md`).
- تقارير القيمة تُدار في `reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md` (انظر `WEEKLY_VALUE_REPORTS_AR.md`).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
