# Recommendation Engine

**Layer**: L12 — Decision Intelligence Engine

## Mission
توليد توصيات أولويات وإجراءات عالية الأثر.

## Inputs
state vectors, constraints, objective functions.

## Outputs
top-N recommendations with expected impact.

## Core KPIs
recommendation precision, realized impact delta, recommendation regret.

## Required Controls
actionability thresholding, safety gating, human override hooks.

## Readiness Exit Criteria
- KPI baselines محددة ومراقبة بشكل دوري.
- سياسات الحوكمة مفروضة runtime وليست optional.
- يوجد مسار rollback / escalation موثق وقابل للتجربة.
- Evidence Pack متاح للمراجعة التنفيذية والتدقيق.
