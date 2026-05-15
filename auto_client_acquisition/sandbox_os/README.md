# sandbox_os — System 29: Enterprise Sandbox Engine

## English

Simulation environments, canary rollouts, staged execution and replay — so a
new workflow can be exercised before it ever touches production.

A sandbox run is **structurally** incapable of a live action: every step runs
through a deterministic stub executor and there is no provider import in this
module, so `no_live_send` / `no_live_charge` hold by construction. Live-style
action types (send / charge) are explicitly recorded as `live_blocked`.

## العربية

بيئات محاكاة وإطلاقات canary وتنفيذ مرحلي وإعادة تشغيل — حتى يُختبر أي سير
عمل جديد قبل أن يمسّ الإنتاج. تشغيل المحاكاة عاجز بنيويًا عن أي إجراء حيّ:
كل خطوة تمرّ عبر منفّذ وهمي حتمي ولا يوجد أي استيراد لمزوّد خدمة في هذه الوحدة.

## API

`/api/v1/sandbox` — `POST /sandboxes`, `POST /simulate`, `POST /canary`,
`POST /replay/{run_id}`, `GET /runs/{run_id}`.
