# org_graph_os — System 30: Operational Memory Graph

## English

A graph of people, workflows, approvals, incidents, risks, departments and
agents — with dependency and relationship edges. For any incident it answers:
what caused it, who was affected, which workflows and agents are related, and
which risks resulted.

Plain in-memory adjacency in v1 — no graph database.

## العربية

رسم بياني للأشخاص وسير العمل والموافقات والحوادث والمخاطر والإدارات والوكلاء،
مع روابط الاعتماد والعلاقات. لأي حادثة يجيب: ما سببها، ومن تأثّر، وما سير
العمل والوكلاء المرتبطون، وما المخاطر الناتجة.

## API

`/api/v1/org-graph` — `POST /nodes`, `POST /edges`,
`GET /nodes/{id}/neighbors`, `GET /nodes/{id}/dependencies`,
`GET /incidents/{id}/impact`.
