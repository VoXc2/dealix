# العربية

## أدوات وكيل الحوكمة

تستند فئات الأدوات إلى `auto_client_acquisition/agent_governance/schemas.py` وقواعد `auto_client_acquisition/governance_os/rules/`.

### أدوات مسموحة (allowed)

| الأداة | الوصف |
|---|---|
| `read` / `analyze` | قراءة وتحليل طلب الإجراء وسياقه |
| `policy.evaluate` | تقييم الطلب مقابل قواعد السياسة (`ALLOW`/`ESCALATE`/`DENY`) |
| `escalation.route` | توجيه الإجراء عالي المخاطر للمُوافِق الصحيح |
| `audit.record_trace` | تسجيل أثر قرار قابل للتدقيق |
| `knowledge.search_internal` | البحث في قواعد السياسة الداخلية |
| `queue_for_approval` | رفع مخرج للموافقة |

### أدوات تحتاج موافقة (requires_approval)

| الأداة | السبب |
|---|---|
| `policy_rule_change` | تغيير قاعدة سياسة |
| `approval_matrix_change` | تغيير مصفوفة الموافقات |
| `agent_permission_change` | تغيير صلاحية وكيل |

### أدوات ممنوعة (forbidden)

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `send_email`, `export_pii_bulk` — مرفوضة دائماً. وكيل الحوكمة لا يملك أي أداة إرسال خارجي إطلاقاً.

---

# English

## Governance agent tools

Tool categories are based on `auto_client_acquisition/agent_governance/schemas.py` and the rules in `auto_client_acquisition/governance_os/rules/`.

### Allowed tools

| Tool | Description |
|---|---|
| `read` / `analyze` | Read and analyze the action request and its context |
| `policy.evaluate` | Evaluate a request against policy rules (`ALLOW`/`ESCALATE`/`DENY`) |
| `escalation.route` | Route a high-risk action to the correct approver |
| `audit.record_trace` | Record an auditable decision trace |
| `knowledge.search_internal` | Search internal policy rules |
| `queue_for_approval` | Raise an output for approval |

### Tools requiring approval

| Tool | Reason |
|---|---|
| `policy_rule_change` | Changing a policy rule |
| `approval_matrix_change` | Changing the approval matrix |
| `agent_permission_change` | Changing an agent permission |

### Forbidden tools

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `send_email`, `export_pii_bulk` — always rejected. The governance agent holds no external-send tool at all.
