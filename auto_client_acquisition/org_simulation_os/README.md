# org_simulation_os — System 32: Organizational Simulation Engine

## English

Simulates workflows, failures, approval load, scale and incidents **before**
deployment, so failure modes surface in prediction rather than in production.

Workflow and failure scenarios delegate execution to `sandbox_os` — they never
touch production. Incident scenarios use the operational memory graph
(`org_graph_os`) to predict cascading impact. The engine produces predictions
and recommendations only.

## العربية

تحاكي سير العمل والإخفاقات وحمل الموافقات والتوسّع والحوادث **قبل** النشر،
حتى تظهر أنماط الفشل في التنبؤ لا في الإنتاج. سيناريوهات سير العمل والإخفاق
تُفوَّض إلى `sandbox_os` ولا تمسّ الإنتاج، وسيناريوهات الحوادث تستخدم رسم
الذاكرة التشغيلية لتوقّع الأثر المتسلسل.

## API

`/api/v1/org-simulation` — `POST /simulate`, `GET /results/{scenario_id}`,
`GET /scenarios`.
