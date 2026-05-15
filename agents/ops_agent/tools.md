# العربية

## أدوات وكيل العمليات

تستند فئات الأدوات إلى `auto_client_acquisition/agent_governance/schemas.py` وحدود الأدوات في `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### أدوات مسموحة (allowed)

| الأداة | الوصف |
|---|---|
| `read` / `analyze` | قراءة وتحليل حالة العمليات |
| `task.create_draft` | إنشاء مسودة مهمة |
| `task.update_draft` | تحديث مسودة مهمة |
| `report.draft_internal` | صياغة تقرير حالة داخلي |
| `evidence.assemble_draft` | تجميع مسودة حزمة أدلة |
| `knowledge.search_internal` | البحث في المعرفة الداخلية |
| `queue_for_approval` | رفع مخرج للموافقة |

### أدوات تحتاج موافقة (requires_approval)

| الأداة | السبب |
|---|---|
| `email.send_message` | إرسال خارجي |
| `vendor_commitment` | التزام تعاقدي |
| `resource_allocation_change` | تغيير تشغيلي مؤثر |

### أدوات ممنوعة (forbidden)

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `export_pii_bulk` — مرفوضة دائماً عند حدود الأدوات.

---

# English

## Ops agent tools

Tool categories are based on `auto_client_acquisition/agent_governance/schemas.py` and the tool boundary in `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### Allowed tools

| Tool | Description |
|---|---|
| `read` / `analyze` | Read and analyze operations status |
| `task.create_draft` | Create a draft task |
| `task.update_draft` | Update a draft task |
| `report.draft_internal` | Draft an internal status report |
| `evidence.assemble_draft` | Assemble an evidence pack draft |
| `knowledge.search_internal` | Search internal knowledge |
| `queue_for_approval` | Raise an output for approval |

### Tools requiring approval

| Tool | Reason |
|---|---|
| `email.send_message` | External send |
| `vendor_commitment` | Contractual commitment |
| `resource_allocation_change` | Impactful operational change |

### Forbidden tools

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `export_pii_bulk` — always rejected at the tool boundary.
