# control_plane_os — System 26: Organizational Control Plane

## English

The central control plane over every workflow run. A run can be registered,
monitored, paused, resumed, rolled back, traced, and re-routed in real time,
and the policies attached to it can be live-edited.

It is a governance + observability layer **over** workflows — it never executes
external actions itself. Rollbacks and policy edits are state-changing, so they
route through the approval gate (approval-first); the change applies only after
the ticket is granted (`finalize_rollback` / `finalize_policy_edit`).

This module also owns two shared pieces used by all of Systems 26-35:

- `ledger.py` — the append-only control-event ledger (`docs/control-events/`),
  the audit substrate behind `no_unaudited_changes`.
- `approval_gate.py` — the ledger-backed approval gate (submit/grant/reject).

## العربية

طبقة التحكم المركزية فوق كل تشغيل لسير عمل. يمكن تسجيل أي تشغيل ومراقبته
وإيقافه واستئنافه والتراجع عنه وتتبعه وإعادة توجيهه في الوقت الحقيقي، مع
إمكانية تعديل السياسات المرتبطة به مباشرةً.

هي طبقة حوكمة ومراقبة **فوق** سير العمل ولا تنفّذ أي إجراء خارجي بنفسها.
التراجع وتعديل السياسات إجراءات تغيّر الحالة، لذا تمرّ عبر بوابة الموافقة
(الموافقة أولًا)؛ ولا يُطبَّق التغيير إلا بعد منح التذكرة.

## API

`/api/v1/control-plane` — `POST /runs`, `GET /runs`, `GET /runs/{id}`,
`GET /runs/{id}/trace`, `POST /runs/{id}/pause|resume|rollback|reroute|policy-edit`,
`POST /runs/{id}/rollback/finalize`.
