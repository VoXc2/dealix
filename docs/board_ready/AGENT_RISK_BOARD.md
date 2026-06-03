# Agent Risk Board

لكل agent تُعرض للمجلس أو للعميل enterprise:

```text
agent_id
owner
purpose
autonomy_level
allowed_inputs
allowed_tools
forbidden_actions
last_audit
risk_level
incident_count
decommission_status
```

## قواعد المستويات

- **0–2:** مسموح في MVP  
- **3:** مسموح مع طابور موافقة  
- **4:** محدود داخليًا وبعد audit  
- **5:** Enterprise-only  
- **6:** ممنوع  

**لماذا؟** الوكلاء قد تتعامل مع بيانات خاصة وتتعرض لـ exfiltration أو prompt injection — بيئة تنفيذ تتبع التدفق وتفرض موافقات — [arXiv:2604.19657](https://arxiv.org/abs/2604.19657).

## مثال: R11 — Agent over-permission

```text
Risk:
Agent over-permission
Signal:
agent يحتاج tools أكثر من هدفه
Control:
Agent Card + Autonomy Level + Approval Required + Audit Log
Response:
reduce permissions, add rule, update tests, review incident
```

**الكود:** `agent_autonomy_board_allowed` — `board_ready_os/agent_risk_board.py`

**صعود:** [`../institutional_control/AGENT_CONTROL_PLANE.md`](../institutional_control/AGENT_CONTROL_PLANE.md)
