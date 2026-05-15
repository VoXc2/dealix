# human_ai_os — System 33: Human-AI Operating Model

## English

Delegation, escalation, explainability and a human oversight surface. The
future is human + AI co-intelligence — humans must be able to delegate,
escalate, understand decisions, and intervene.

- Delegations are always bounded — a positive TTL is mandatory
  (`no_unbounded_agents`).
- Escalations create an approval-gate ticket routed to a human.
- The oversight queue is the API surface for granting / rejecting pending
  control-plane actions.

## العربية

التفويض والتصعيد وقابلية التفسير وواجهة الإشراف البشري. المستقبل ذكاء مشترك
بين الإنسان والآلة. التفويضات محدودة دائمًا بمدة صلاحية موجبة؛ والتصعيد يُنشئ
تذكرة موافقة موجّهة لإنسان؛ وقائمة الإشراف هي واجهة منح أو رفض الإجراءات المعلّقة.

## API

`/api/v1/human-ai` — `POST /delegations`, `DELETE /delegations/{id}`,
`POST /escalations`, `GET /explain/{subject_id}`, `GET /oversight-queue`,
`POST /oversight/{ticket_id}/grant`, `POST /oversight/{ticket_id}/reject`.
