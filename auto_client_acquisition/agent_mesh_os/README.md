# agent_mesh_os — System 27: Agent Mesh Infrastructure

## English

Discovery, capability registry, routing, trust boundaries and inter-agent
governance for an ecosystem of agents (internal / partner / vendor / third-party).

Every agent can be discovered, governed, scored, isolated and monitored.
Autonomy is capped at the MVP ceiling (`AutonomyLevel.QUEUE_FOR_APPROVAL`) — no
mesh agent auto-executes (`no_unbounded_agents`). Routing skips isolated agents.

Builds on `agent_os` for the autonomy ladder; the mesh adds the capability
index, routing, trust tiers, scoring and isolation.

## العربية

اكتشاف الوكلاء وسجل القدرات والتوجيه وحدود الثقة وحوكمة التفاعل بين الوكلاء
لمنظومة وكلاء (داخلي / شريك / مورّد / طرف ثالث). كل وكيل يمكن اكتشافه وحوكمته
وتقييمه وعزله ومراقبته. سقف الاستقلالية لا يتجاوز "إدراج في قائمة الموافقة".

## API

`/api/v1/agent-mesh` — `POST /agents`, `GET /agents`, `GET /agents/{id}`,
`POST /route`, `POST /agents/{id}/isolate`, `PUT /agents/{id}/trust-boundary`,
`GET /agents/{id}/score`.
