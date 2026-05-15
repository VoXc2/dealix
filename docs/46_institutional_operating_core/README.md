# Layer 46 — Institutional Operating Core (SYSTEM 65)

النواة التشغيلية المؤسسية: المرحلة النهائية — Dealix يصبح النواة التي تشغّل
المؤسسة الوكيلية (the operating core of the agentic institution).

## القاعدة (Rule)

لا تقيس عدد الوكلاء. قِس **الاعتماد المؤسسي** (institutional dependency):
هل تعتمد المؤسسة على Dealix للتشغيل، القرار، التنسيق، الحوكمة، التنفيذ،
الذاكرة، المراقبة، والتحسين؟

## التنفيذ في الكود (Implementation)

- `auto_client_acquisition/institutional_dependency_os/` —
  `dependency_index.py`: مؤشر الاعتماد المؤسسي.
  - `InstitutionalDependencyDimensions` — عشرة إشارات 0–100، واحدة لكل
    نظام 56–65.
  - `institutional_dependency_index(dims) -> int` — مؤشر مرجّح 0–100.
  - `dependency_band(score)` — `tool` / `platform` / `infrastructure` /
    `institutional_operating_core`.
  - `dependency_blockers(dims)` — أي بُعد دون 70 يمنع ادّعاء «النواة التشغيلية».
- API: `GET/POST /api/v1/institutional-dependency`.

## كيف تعرف أنك وصلت؟ (Arrival test)

المؤشر ≥ 85 **وبلا blockers** ⇒ band = `institutional_operating_core`.
عندها لم تعد تبني AI startup — بل The Institutional Operating Infrastructure.

## الحواجز (Doctrine)

المؤشر تقييم ذاتي صادق للاعتماد، لا ادّعاء إثبات: بوابات `dependency_blockers`
وعتبات الـ band تحترم `no_fake_proof` و`no_unverified_outcomes`؛ وقصّ المدخلات
يحترم `no_silent_failures`.
