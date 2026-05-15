# assurance_contract_os — System 28: Assurance Contract Engine

## English

Every agent action is governed by an **assurance contract** declaring what the
agent may see / propose / execute and which preconditions must pass first.

- No contract registered → fail-closed `DENY` (`no_unbounded_agents`).
- An irreversible contract must carry a `rollback_plan` (`no_unverified_outcomes`).
- External or irreversible actions return `ESCALATE` — they go to approval,
  never auto-execute.

## العربية

كل إجراء لوكيل محكوم بعقد ضمان يحدّد ما يمكن للوكيل رؤيته واقتراحه وتنفيذه،
والشروط المسبقة الواجب تحققها. عدم وجود عقد يعني الرفض الافتراضي؛ والعقد غير
القابل للعكس يجب أن يتضمن خطة تراجع؛ والإجراءات الخارجية تُصعَّد للموافقة.

## API

`/api/v1/assurance-contracts` — `POST /contracts`, `GET /contracts`,
`GET /contracts/{id}`, `POST /evaluate`.
