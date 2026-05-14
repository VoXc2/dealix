# Secure Agent Runtime + Kill Switch

## Runtime Assurance Loop

Observe → Classify → Check Policy → Decide → Execute/Block/Escalate → Log Evidence → Update State.

## أربع حدود

Prompt Boundary، Tool Boundary، Data Boundary، Context Boundary.

## حالات التشغيل

SAFE، WATCH، RESTRICTED، ESCALATED، PAUSED، KILLED.

## Kill Switch

Soft Kill، Tool Kill، Client Kill، Agent Kill، Fleet Kill — أي أداة يجب أن تكون قابلة للإيقاف الفوري مع أثر مسجّل.

## حلقات النشر (Rings)

من sandbox محلي إلى عميل retainer بموافقات — لا قفزات بدون أدلة تغطية.

## تنفيذ

- `auto_client_acquisition/tool_guardrail_gateway/`، `auto_client_acquisition/safe_send_gateway/`، وثائق `docs/institutional_control/`

## روابط

- [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
