# العربية

## ملف مخاطر وكيل الحوكمة

**مستوى المخاطر:** مرتفع (`high`).

سبب التصنيف المرتفع ليس قدرة تنفيذ — الوكيل لا ينفّذ شيئاً — بل أنه نقطة تحكّم حرجة: خطأ في تقييمه قد يسمح بإجراء كان يجب رفضه.

## مصادر المخاطر

- **تقييم خاطئ:** السماح بإجراء كان يجب رفضه. التخفيف: قواعد ثابتة في `auto_client_acquisition/governance_os/rules/`؛ الإجراءات الممنوعة مرفوضة بصرامة لا باجتهاد.
- **توجيه تصعيد خاطئ:** وصول الطلب لمُوافِق غير صحيح. التخفيف: مصفوفة `approval_matrix.py` حتمية.
- **تغيير قاعدة:** تعديل السياسة نفسها. التخفيف: `policy_rule_change` تحت `requires_approval_for` لـ `governance_lead`.

## ضوابط التخفيف

- `L0_read_only` — لا قدرة تنفيذ إطلاقاً.
- لا أداة إرسال خارجي — فصل صلاحيات مقصود.
- الإجراءات الممنوعة دائماً `DENY`، لا تُصعَّد.
- إيقاف فوري عبر مفتاح الإيقاف.

## المخاطر المتبقية

احتمال ثغرة في قاعدة سياسة لم تُغطِّ حالة جديدة — يخفّفه مراجعة `governance_lead` الدورية لتغطية القواعد وتسجيل كل تقييم.

## درجة الجاهزية الحالية

**73 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Governance agent risk profile

**Risk level:** high.

The high rating is not because of execution power — the agent executes nothing — but because it is a critical control point: an error in its evaluation could allow an action that should have been denied.

## Risk sources

- **Wrong evaluation:** allowing an action that should have been denied. Mitigation: fixed rules in `auto_client_acquisition/governance_os/rules/`; forbidden actions are denied strictly, not by discretion.
- **Wrong escalation routing:** a request reaching an incorrect approver. Mitigation: the deterministic `approval_matrix.py`.
- **Rule change:** modifying policy itself. Mitigation: `policy_rule_change` under `requires_approval_for` for `governance_lead`.

## Mitigation controls

- `L0_read_only` — no execution capability at all.
- No external-send tool — a deliberate separation of duties.
- Forbidden actions are always `DENY`, never escalated.
- Instant stop via the kill switch.

## Residual risk

A possibility of a gap in a policy rule that does not cover a new case — mitigated by periodic `governance_lead` review of rule coverage and recording of every evaluation.

## Current readiness score

**73 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
