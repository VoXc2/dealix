# عقد مخرجات الوكلاء (Agent Output Contract)

كل مخرج من أي وكيل في Dealix يجب أن يلتزم بهذا العقد. الهدف: قابلية المراجعة،
وعدم تجاوز الصلاحيات، وبقاء القرار النهائي بيد المؤسس.

## الحقول الإلزامية في كل مخرج

| الحقل | الوصف |
|------|-------|
| `summary` | ملخص واضح لما تم. |
| `business_impact` | الأثر التجاري المتوقع (بدون مبالغة أو ضمانات). |
| `files_touched` | قائمة الملفات التي تم إنشاؤها/تعديلها. |
| `evidence_level` | أحد: `none / assumption / anecdote / internal_data / verified / third_party_verified`. |
| `risk_level` | أحد: `low / medium / high / critical`. |
| `approval_required` | `true/false` — أي إجراء خارجي = `true` دائماً. |
| `tests_checks_run` | الاختبارات/الفحوصات التي شُغّلت (مثل `pytest`). |
| `rollback` | كيف يُتراجع عن التغيير بأمان. |
| `next_founder_action` | الإجراء التالي المطلوب من المؤسس. |

## قالب JSON موحّد

```json
{
  "agent": "Draft Factory Agent",
  "summary": "...",
  "business_impact": "...",
  "files_touched": ["company_os/revenue/outreach_queue.json"],
  "evidence_level": "internal_data",
  "risk_level": "high",
  "approval_required": true,
  "tests_checks_run": ["pytest tests/test_gtm_quality_gate.py"],
  "rollback": "revert commit / restore previous queue file",
  "next_founder_action": "مراجعة المسودات والموافقة قبل أي إرسال"
}
```

## قواعد صارمة

- ممنوع ادعاء نتائج مضمونة أو مبالغ فيها في `business_impact`.
- `approval_required = true` لأي إرسال خارجي أو تسعير نهائي أو التزام قانوني.
- المجهول يُعلَّم `TBD` ولا يُختلق.
- لا أسرار في المخرجات أو السجلات.
