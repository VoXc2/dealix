# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead).

## الغرض

التحكّم بالإصدارات يجعل كل وكيل قابلاً للمقارنة بين إصداراته (v1 مقابل v2)، ويضمن وجود إصدار مستقر معروف يمكن الرجوع إليه فوراً. لا يصل تغيير سلوك وكيل إلى الإنتاج دون مقارنة موثَّقة.

## نموذج الإصدار

- كل `agent.yaml` يحمل حقل `version` بصيغة دلالية (`MAJOR.MINOR.PATCH`).
- تغيير الأدوات أو الصلاحيات أو مستوى المخاطر = ترقية `MAJOR`.
- تغيير المطالبة (system prompt) = ترقية `MINOR`.
- تصحيح صياغة = ترقية `PATCH`.

## حلقات النشر

تستند إلى `auto_client_acquisition/secure_agent_runtime_os/deployment_rings.py`:

1. **حلقة داخلية** — تشغيل ظلّي، لا أثر على العميل.
2. **حلقة تجريبية** — عميل واحد متطوّع.
3. **حلقة عامة** — كل العملاء.

## المقارنة v1 مقابل v2

قبل ترقية الحلقة، يُجرى تقييم مقارن: نفس مجموعة اختبارات `evals.md`، نفس المدخلات، مقارنة المخرجات والمقاييس. الترقية مرفوضة إن انخفض أي مؤشر جودة.

## قائمة الجاهزية

- [x] كل وكيل يحمل `version` دلالية.
- [x] يوجد إصدار مستقر معلَّم لكل وكيل.
- [x] التغييرات تمر عبر حلقات النشر بالترتيب.
- [ ] لوحة مقارنة آلية v1/v2 لكل تقييم.

## المقاييس

- عدد الإصدارات النشطة لكل وكيل (هدف: 1 مستقر + ≤1 تجريبي).
- فرق الجودة بين v1 و v2.
- زمن التراجع إلى الإصدار المستقر السابق (هدف: أقل من 5 دقائق).

## خطافات المراقبة

- حدث `agent.version_deployed` و`agent.version_rolled_back` عبر `auto_client_acquisition/agent_observability/trace.py`.
- وسم كل أثر بـ `agent_version`.

## قواعد الحوكمة

- لا تصل ترقية `MAJOR` إلى الحلقة العامة دون تقييم مقارن ناجح.
- يبقى الإصدار المستقر السابق متاحاً 30 يوماً على الأقل بعد الترقية.
- التقاعد النهائي لإصدار يتطلب موافقة مالك المنصة.

## إجراء التراجع

أعد توجيه الحركة إلى الإصدار المستقر السابق المعلَّم، انقل الإصدار المعيب إلى `stopped`، وسجّل `agent.version_rolled_back`.

## درجة الجاهزية الحالية

**72 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

**Owner:** Agent Runtime Platform Lead.

## Purpose

Versioning makes every agent comparable across its versions (v1 vs v2) and guarantees a known stable version that can be rolled back to instantly. No agent behavior change reaches production without a documented comparison.

## Version model

- Every `agent.yaml` carries a `version` field in semantic form (`MAJOR.MINOR.PATCH`).
- A change to tools, permissions, or risk level = `MAJOR` bump.
- A change to the system prompt = `MINOR` bump.
- A wording fix = `PATCH` bump.

## Deployment rings

Based on `auto_client_acquisition/secure_agent_runtime_os/deployment_rings.py`:

1. **Internal ring** — shadow run, no customer impact.
2. **Pilot ring** — one volunteer customer.
3. **General ring** — all customers.

## v1 vs v2 comparison

Before a ring promotion, a comparative evaluation runs: the same `evals.md` test set, the same inputs, with output and metric comparison. A promotion is rejected if any quality indicator drops.

## Readiness checklist

- [x] Every agent carries a semantic `version`.
- [x] A tagged stable version exists for every agent.
- [x] Changes pass through deployment rings in order.
- [ ] Automated v1/v2 comparison board per evaluation.

## Metrics

- Active version count per agent (target: 1 stable + at most 1 pilot).
- Quality delta between v1 and v2.
- Time to roll back to the previous stable version (target: under 5 minutes).

## Observability hooks

- `agent.version_deployed` and `agent.version_rolled_back` events via `auto_client_acquisition/agent_observability/trace.py`.
- Every trace tagged with `agent_version`.

## Governance rules

- A `MAJOR` bump does not reach the general ring without a passing comparative evaluation.
- The previous stable version stays available for at least 30 days after a promotion.
- Final retirement of a version requires Platform Lead approval.

## Rollback procedure

Re-route traffic to the tagged previous stable version, move the faulty version to `stopped`, and record `agent.version_rolled_back`.

## Current readiness score

**72 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
