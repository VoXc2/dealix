# Rollback — التراجع

**EN.** Rollback is the eighth-hardest component to fake and the easiest to skip.
A layer cannot score `PASS` on the Rollback component
([`scoring_system.md`](scoring_system.md)) until rollback is **documented and
drilled**. This file defines what "drilled" means and how to run the drill.

**AR.** التراجع أصعب مكوّن في التزوير وأسهله في التجاهل. لا تنال أي طبقة `PASS`
على مكوّن التراجع حتى يكون التراجع **موثَّقًا ومُجرَّبًا**. تحدّد هذه الوثيقة معنى
«مُجرَّب» وكيفية إجراء التمرين.

Owner: Platform Engineer. Backs: Layer 5 (Workflow Engine), Release 1 + Release 5.

---

## 1. What "tested rollback" means — معنى «تراجع مُجرَّب»

A rollback claim is real only when **all four** hold:

1. **Documented path.** A written procedure to return to the last known-good
   state — for code, for schema, and for in-flight workflows.
2. **Drilled.** The procedure was actually executed at least once in a
   non-production environment, with the result recorded.
3. **Bounded.** A known recovery-time objective (RTO) — how long the rollback
   takes — and a known data-loss objective (RPO).
4. **Triggerable.** A clear, named owner can start it without a meeting.

Documentation without a drill scores **6 / 12.5** at most (`partial`). A drill
with a recorded result scores **12.5**.

---

## 2. The three rollback surfaces — أسطح التراجع الثلاثة

| Surface | What can go wrong | Rollback path |
|---------|-------------------|---------------|
| **Code / deploy** | Bad release breaks the API. | Redeploy the previous image tag. See `docs/ops/RELEASE_DAY_RUNBOOK.md`. |
| **Schema / migration** | A migration corrupts or locks data. | Alembic downgrade to the prior revision; restore from backup if the migration is destructive. `db/migrations/`. |
| **In-flight workflow** | A workflow run is half-done when a release is pulled. | Workflow checkpoint + idempotency so a run can be safely retried or abandoned. `auto_client_acquisition/workflow_os_v10/checkpoint.py`, `idempotency.py`, `retry_policy.py`. |

A release is not safe unless **all three** surfaces have a rollback path.

---

## 3. The rollback drill — تمرين التراجع

Run this once per release candidate, in staging. Record the result.

| # | Step | Recorded |
|---|------|----------|
| 1 | Deploy release candidate `N` to staging. | version, time |
| 2 | Start the proof workflow ([`cross_layer_validation.md`](cross_layer_validation.md)); pause it mid-run. | run id |
| 3 | Trigger the code rollback to release `N-1`. | start time |
| 4 | Confirm the API serves on `N-1`. | RTO measured |
| 5 | If `N` included a migration: run the Alembic downgrade. | revision, result |
| 6 | Confirm the paused workflow run is either safely resumable or cleanly abandoned (no partial CRM write, no half-sent offer). | run state |
| 7 | Confirm no cross-tenant data and no PII leaked during the rollback. | check |
| 8 | Record RTO, RPO, owner, and any surprises. | summary |

Pass all 8 → the Rollback component scores `12.5` for that release.

---

## 4. Release-gate rule — قاعدة بوابة الإصدار

From Release 5 onward (see
[`enterprise_readiness_model.md`](enterprise_readiness_model.md)):
**no release ships without a rollback plan, and the plan must have been drilled
within the last 90 days.** A stale drill (> 90 days) downgrades the component to
`partial`.

For Release 1, the acceptance criterion is simpler: **the drill has been
executed at least once.** That single drill is part of the 30-day proof workflow
([`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md), Week 4).

---

## 5. Residual gaps — الفجوات المتبقية

1. **No recorded drill yet.** `docs/ops/RELEASE_DAY_RUNBOOK.md` documents release
   day; confirm it contains an explicit rollback section, and run the §3 drill at
   least once to produce the first recorded result.
2. **In-flight workflow rollback unproven.** `workflow_os_v10` has `checkpoint`,
   `idempotency`, and `retry_policy` modules — but no evidence a paused run
   survives a deploy rollback cleanly. Step 6 of the drill closes this.
3. **RTO/RPO undefined.** No published recovery-time / data-loss objectives.
   Define them from the first drill's measurements.

---

## ملخص بالعربية

التراجع يُعدّ حقيقيًا فقط حين يكون موثَّقًا ومُجرَّبًا ومحدّد الزمن وقابلًا
للتشغيل فورًا. هناك ثلاثة أسطح للتراجع: الكود/النشر، المخطط/الترحيل، ومسار
العمل الجاري — ويجب أن يكون لكلٍّ منها مسار تراجع. التمرين من 8 خطوات يُجرى في
بيئة staging لكل مرشّح إصدار. من الإصدار 5: لا إصدار بلا خطة تراجع مُجرَّبة خلال
آخر 90 يومًا. للإصدار 1: يكفي تنفيذ التمرين مرة واحدة (الأسبوع 4 من خطة الـ30
يومًا).
