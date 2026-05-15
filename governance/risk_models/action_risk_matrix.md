# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead).

## مصفوفة مخاطر الإجراءات

تربط هذه المصفوفة أنواع الإجراءات الشائعة في Dealix بتصنيفها A/R/S وبمسار معالجتها. هي مرجع توجيهي؛ المصدر النهائي للتصنيف هو `dealix/classifications/__init__.py`، ومصفوفة الموافقات `auto_client_acquisition/governance_os/approval_matrix.py`.

### المصفوفة

| الإجراء | A | R | S | المسار |
|---|---|---|---|---|
| تلخيص بيانات داخلية | A0 | R0 | S1 | تنفيذ آلي بعد فحص السياسة |
| تصنيف فرصة | A0 | R0 | S2 | تنفيذ آلي بعد فحص السياسة |
| صياغة مسوّدة عرض | A0 | R0 | S2 | مسوّدة فقط؛ لا إرسال |
| إرسال بريد لعميل | A2 | R2 | S2 | موافقة مدير قبل الإرسال |
| إطلاق حملة تواصل | A3 | R2 | S3 | موافقة مزدوجة + تقييم مخاطر الحملة |
| تصدير بيانات شخصية S3 | A3 | R3 | S3 | موافقة مزدوجة إلزامية |
| حذف بيانات عميل | A3 | R3 | S3 | موافقة مزدوجة + توثيق الأساس |
| تعديل قاعدة سياسة | A3 | R2 | S1 | موافقة مالك الطبقة + قيد تدقيق |
| إنشاء/حذف مستأجر | A2 | R3 | S2 | موافقة موثَّقة |

### القواعد الحاكمة

- أي إجراء بمحور R3 أو S3 يتطلب موافقة بشرية بصرف النظر عن محور A.
- أي إجراء خارجي مواجِه للعميل يُعرض كمسوّدة فقط حتى الموافقة.
- الإجراء غير المدرج في المصفوفة يُصنَّف افتراضياً A2/R2/S2 ويُرفع للموافقة (fail-closed).
- الإجراءات المدرجة في `NEVER_AUTO_EXECUTE` لا تُنفَّذ آلياً مطلقاً.

### قائمة الجاهزية

- [x] أنواع الإجراءات الشائعة مصنّفة وموثّقة.
- [x] الإجراء غير المدرج يُعامل بأمان افتراضي.
- [x] R3/S3 يستوجب موافقة بشرية دائماً.
- [ ] توسيع المصفوفة لتغطية إجراءات التكامل الخارجي الجديدة (مُخطَّط).

### المقاييس

- نسبة الإجراءات المنفّذة المطابقة لمسار المصفوفة: 100% (هدف).
- عدد الإجراءات غير المدرجة المصنّفة افتراضياً.

### الحوكمة والتراجع

- تعديل المصفوفة يتطلب موافقة مالك الطبقة وقيد تدقيق.
- التراجع: استعادة الإصدار السابق من `approval_matrix.py` وإعادة تقييم الإجراءات المعلّقة.

انظر أيضاً: `governance/risk_models/risk_levels.md`، `governance/approval_rules/`.

---

# English

**Owner:** Governance Platform Lead.

## Action Risk Matrix

This matrix maps common Dealix action types to their A/R/S classification and handling path. It is a guidance reference; the authoritative source of classification is `dealix/classifications/__init__.py`, and the approval matrix `auto_client_acquisition/governance_os/approval_matrix.py`.

### The matrix

| Action | A | R | S | Path |
|---|---|---|---|---|
| Summarize internal data | A0 | R0 | S1 | Auto-execute after policy check |
| Classify an opportunity | A0 | R0 | S2 | Auto-execute after policy check |
| Draft a proposal | A0 | R0 | S2 | Draft-only; no send |
| Send a customer email | A2 | R2 | S2 | Manager approval before send |
| Launch an outreach campaign | A3 | R2 | S3 | Dual approval + campaign risk scoring |
| Export S3 personal data | A3 | R3 | S3 | Mandatory dual approval |
| Delete customer data | A3 | R3 | S3 | Dual approval + basis documentation |
| Change a policy rule | A3 | R2 | S1 | Layer owner approval + audit entry |
| Create/delete a tenant | A2 | R3 | S2 | Documented approval |

### Governing rules

- Any action with an R3 or S3 axis requires human approval regardless of the A axis.
- Any external, customer-facing action is presented draft-only until approval.
- An action not listed in the matrix is defaulted to A2/R2/S2 and raised for approval (fail-closed).
- Actions on the `NEVER_AUTO_EXECUTE` list never auto-execute.

### Readiness checklist

- [x] Common action types are classified and documented.
- [x] An unlisted action is treated with safe defaults.
- [x] R3/S3 always requires human approval.
- [ ] Extend the matrix to cover new external integration actions (planned).

### Metrics

- Share of executed actions matching their matrix path: 100% (target).
- Count of unlisted actions defaulted.

### Governance and rollback

- Changing the matrix requires the layer owner's approval and an audit entry.
- Rollback: restore the prior version of `approval_matrix.py` and re-evaluate pending actions.

See also: `governance/risk_models/risk_levels.md`, `governance/approval_rules/`.
