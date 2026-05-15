# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead).

## مستويات المخاطر

تصف هذه الوثيقة محاور تصنيف المخاطر الثلاثة المعرّفة في `dealix/classifications/__init__.py`. كل إجراء يُصنَّف على المحاور الثلاثة، ودرجة المخاطر النهائية هي أعلاها.

### المحور A — الموافقة (Approval)

| المستوى | الوصف | المتطلب |
|---|---|---|
| A0 | لا يتطلب موافقة | تنفيذ آلي مسموح |
| A1 | يتطلب مراجعاً واحداً | موافقة فردية موثَّقة |
| A2 | يتطلب مدير الفريق | موافقة المدير المعني |
| A3 | يتطلب موافقة مزدوجة | مالك الطبقة + المالك التجاري |

### المحور R — قابلية التراجع (Reversibility)

| المستوى | الوصف |
|---|---|
| R0 | عكوس فوري بلا أثر |
| R1 | عكوس بجهد محدود |
| R2 | عكوس جزئياً؛ بعض الأثر يبقى |
| R3 | غير عكوس؛ لا تنفيذ آلي مطلقاً |

### المحور S — الحساسية (Sensitivity)

| المستوى | الوصف |
|---|---|
| S0 | عام |
| S1 | داخلي |
| S2 | سرّي تجاري |
| S3 | بيانات شخصية تخضع لـ PDPL |

### الدرجة النهائية

درجة المخاطر النهائية = أعلى المحاور الثلاثة، لا متوسطها. مثال: إجراء A1/R3/S2 يُعامل عالي المخاطر بسبب R3. الإجراء غير المعروف يُصنَّف افتراضياً A2/R2/S2 (fail-closed).

### معاملة المستويات

- A0/R0–R1/S0–S1: قد يُنفَّذ آلياً بعد فحص السياسة.
- A1+ أو R2+ أو S2+: يُرفع للموافقة وفق المحور الأعلى.
- R3 أو S3 أو إدراج في `NEVER_AUTO_EXECUTE`: موافقة بشرية إلزامية؛ لا استثناء.

### قائمة الجاهزية

- [x] المحاور الثلاثة معرّفة في الكود.
- [x] الدرجة النهائية = أعلى المحاور.
- [x] المجهول يُصنَّف افتراضياً عند الحذر الأعلى.
- [ ] إعادة معايرة دورية للحدود بناءً على بيانات الحوادث (مُخطَّطة).

### الحوكمة والتراجع

- لا تخفيض مستوى يدوياً دون موافقة مالك الطبقة وقيد تدقيق.
- التراجع: استعادة الإصدار السابق من `dealix/classifications/__init__.py` وإعادة تصنيف الإجراءات المعلّقة.

انظر أيضاً: `governance/risk_models/action_risk_matrix.md`، `platform/governance/risk_engine.md`.

---

# English

**Owner:** Governance Platform Lead.

## Risk Levels

This document describes the three risk classification axes defined in `dealix/classifications/__init__.py`. Every action is classified on all three axes, and the final risk grade is the highest of them.

### Axis A — Approval

| Level | Description | Requirement |
|---|---|---|
| A0 | No approval required | Auto-execution allowed |
| A1 | One reviewer required | Documented single approval |
| A2 | Team manager required | Relevant manager's approval |
| A3 | Dual approval required | Layer owner + commercial owner |

### Axis R — Reversibility

| Level | Description |
|---|---|
| R0 | Instantly reversible with no trace |
| R1 | Reversible with limited effort |
| R2 | Partially reversible; some impact remains |
| R3 | Irreversible; never auto-executed |

### Axis S — Sensitivity

| Level | Description |
|---|---|
| S0 | Public |
| S1 | Internal |
| S2 | Commercially confidential |
| S3 | Personal data subject to PDPL |

### Final grade

The final risk grade = the highest of the three axes, not their average. Example: an A1/R3/S2 action is treated as high-risk because of R3. An unknown action is defaulted to A2/R2/S2 (fail-closed).

### Treatment by level

- A0 / R0–R1 / S0–S1: may auto-execute after a policy check.
- A1+, R2+, or S2+: raised for approval per the highest axis.
- R3, S3, or listing on `NEVER_AUTO_EXECUTE`: human approval is mandatory; no exception.

### Readiness checklist

- [x] The three axes are defined in code.
- [x] The final grade = the highest axis.
- [x] The unknown is defaulted to the upper bound of caution.
- [ ] Periodic recalibration of thresholds from incident data (planned).

### Governance and rollback

- No manual level downgrade without the layer owner's approval and an audit entry.
- Rollback: restore the prior version of `dealix/classifications/__init__.py` and re-classify pending actions.

See also: `governance/risk_models/action_risk_matrix.md`, `platform/governance/risk_engine.md`.
