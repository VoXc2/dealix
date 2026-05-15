# العربية

## ملف مخاطر وكيل العمليات

**مستوى المخاطر:** منخفض (`low`).

## مصادر المخاطر

- **داخلي التوجّه:** لا إرسال خارجي، ما يخفّض المخاطر جوهرياً.
- **التزام مورّد:** قد يقترح التزاماً. التخفيف: `vendor_commitment` تحت `requires_approval_for`.
- **تغيير موارد:** قد يقترح إعادة تخصيص. التخفيف: `resource_allocation_change` تحت `requires_approval_for`.
- **حالة مهمة خاطئة:** تقرير غير دقيق. التخفيف: الاستناد إلى `ops_memory` فقط.

## ضوابط التخفيف

- لا أداة إرسال خارجي مفعّلة؛ `send_whatsapp` ضمن `forbidden_tools`.
- الإجراءات الممنوعة مرفوضة عبر `forbidden_actions.py`.
- إيقاف فوري عبر مفتاح الإيقاف.

## المخاطر المتبقية

احتمال تقرير حالة قديم إذا لم تُحدَّث `ops_memory` — يخفّفه مراجعة المالك الدورية.

## درجة الجاهزية الحالية

**80 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Ops agent risk profile

**Risk level:** low.

## Risk sources

- **Internal-facing:** no external send, which materially lowers risk.
- **Vendor commitment:** may propose a commitment. Mitigation: `vendor_commitment` under `requires_approval_for`.
- **Resource change:** may propose a reallocation. Mitigation: `resource_allocation_change` under `requires_approval_for`.
- **Wrong task status:** an inaccurate report. Mitigation: grounding in `ops_memory` only.

## Mitigation controls

- No external-send tool is enabled; `send_whatsapp` is in `forbidden_tools`.
- Forbidden actions are rejected via `forbidden_actions.py`.
- Instant stop via the kill switch.

## Residual risk

A possibility of a stale status report if `ops_memory` is not updated — mitigated by periodic owner review.

## Current readiness score

**80 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
