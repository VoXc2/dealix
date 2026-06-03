# Agent Registry — سجل الوكلاء الرسمي

> سجل رسمي لكل وكيل في Dealix: مستواه، وظيفته، ما يقرأ، ما يكتب، وما هو ممنوع منه.
> المصدر الآلي: `company_os/agents/agent_registry.json`.

---

## السجل

| Agent | المستوى | الوظيفة | يقرأ | يكتب | ممنوع |
|-------|--------:|---------|------|------|-------|
| Account Research Agent | L1 | يجمع معلومات عامة | web/public data | account_packs draft | secrets, private data |
| Need Detection Agent | L2 | يكتشف الاحتياج | account pack | recommended_need | external actions |
| System Router Agent | L2 | يختار النظام | catalog | recommendation | pricing override |
| Email Draft Agent | L3 | يكتب الإيميل | need card | draft | send |
| Call Brief Agent | L3 | يجهّز المتصل | account pack | call brief | automated calls |
| Proposal Agent | L3 | يجهّز Mini Proposal | account pack | proposal draft | send/contract |
| Delivery Agent | L4 | يجهّز التسليم | won pipeline | tasks/checklist | start without inputs |
| Founder Command Agent | L2 | يرفع القرار اليومي | reports | daily command | execute decisions |
| Internal Reporter Agent | L5 | تقارير داخلية | company_os data | reports/ (internal) | external/client-facing |

---

## الحقول الإلزامية لكل وكيل

كل سجل وكيل يجب أن يحتوي الحقول الثمانية (Workflow-First):

```txt
workflow, input_contract, output_contract, level,
quality_gate, audit_log, owner, stop_rule
```

بالإضافة إلى أعلام الأمان (كلها يجب أن تكون false إلا internal_only لوكلاء L5):

```txt
can_send_external, can_call, can_change_price,
can_contract, can_start_delivery
```

---

## التحقق الآلي

```bash
python dealix.py agent-audit
```

- `check_agent_governance.py`: يتأكد أن كل وكيل يحقّق الحقول الثمانية ومستوى صالح.
- `check_agent_permissions.py`: يتأكد أن لا وكيل يملك صلاحية إرسال/اتصال/تسعير/
  تعاقد/بدء تسليم، وأن وكلاء L5 داخليون فقط.

---

## قاعدة التعديل

```txt
لا يُضاف وكيل جديد إلا بعد تعريف:
workflow + input/output contract + level + quality gate + audit log + owner + stop rule.
أي وكيل بلا هذه الحقول يُرفض في الفحص (exit 1).
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
