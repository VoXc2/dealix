# Operational Health

**Layer**: L11 — Organizational State Engine

## Mission
تقديم لوحة صحة تشغيلية موحدة على مستوى المؤسسة.

## Inputs
service SLO, queue depth, workflow throughput, error budgets.

## Outputs
health index, degradation alerts, weekly health narrative.

## Core KPIs
overall health score, SLO compliance, error budget burn.

## Required Controls
golden signals coverage, degraded-mode playbooks, recovery verification.

## Readiness Exit Criteria
- KPI baselines محددة ومراقبة بشكل دوري.
- سياسات الحوكمة مفروضة runtime وليست optional.
- يوجد مسار rollback / escalation موثق وقابل للتجربة.
- Evidence Pack متاح للمراجعة التنفيذية والتدقيق.
