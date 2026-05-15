# العربية

## ملف مخاطر الوكيل التنفيذي

**مستوى المخاطر:** مرتفع (`high`).

## مصادر المخاطر

- **تأثير القرار:** المذكّرات تؤثر على قرارات استراتيجية. التخفيف: مسودة فقط، توصيات مبنية على أدلة، موافقة المؤسس.
- **مبالغة في الادعاء:** توقّع معروض كحقيقة. التخفيف: قاعدة `no_guaranteed_claims`؛ كل توقّع مُعلَّم "تقديري".
- **تسرّب بيانات سرية:** PII أو مؤشرات سرية في مذكّرة. التخفيف: `metrics.aggregate` فقط؛ نطاق `executive_memory` لا يحوي بيانات خام.
- **نشر خارجي:** مذكّرة تصل أطرافاً خارجية. التخفيف: `report.publish_external` تحت `requires_approval_for`.

## ضوابط التخفيف

- `L1_draft_only` — لا تنفيذ آلي.
- النشر والالتزام الاستراتيجي يُرفعان للمؤسس.
- الإجراءات الممنوعة مرفوضة عبر `forbidden_actions.py`.
- إيقاف فوري عبر مفتاح الإيقاف.

## المخاطر المتبقية

احتمال انحياز تحليلي في صياغة الخيارات — يخفّفه عرض المقايضات بوضوح ومراجعة المؤسس.

## درجة الجاهزية الحالية

**71 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Executive agent risk profile

**Risk level:** high.

## Risk sources

- **Decision impact:** memos influence strategic decisions. Mitigation: draft only, evidence-backed recommendations, founder approval.
- **Overclaim:** a forecast presented as fact. Mitigation: the `no_guaranteed_claims` rule; every forecast labeled "estimated".
- **Confidential data leak:** PII or confidential metrics in a memo. Mitigation: `metrics.aggregate` only; the `executive_memory` scope holds no raw data.
- **External publishing:** a memo reaching external parties. Mitigation: `report.publish_external` under `requires_approval_for`.

## Mitigation controls

- `L1_draft_only` — no auto-execution.
- Publishing and strategic commitments are raised to the founder.
- Forbidden actions are rejected via `forbidden_actions.py`.
- Instant stop via the kill switch.

## Residual risk

A possibility of analytical bias in framing options — mitigated by clear trade-off presentation and founder review.

## Current readiness score

**71 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
