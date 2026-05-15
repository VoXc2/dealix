# العربية

## أدوات وكيل الدعم

تستند فئات الأدوات إلى `auto_client_acquisition/agent_governance/schemas.py` وحدود الأدوات في `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### أدوات مسموحة (allowed)

| الأداة | الوصف |
|---|---|
| `read` / `analyze` | قراءة وتحليل التذكرة وسياقها |
| `whatsapp.draft_reply` | صياغة مسودة رد WhatsApp — لا إرسال |
| `email.draft_reply` | صياغة مسودة رد بريد — لا إرسال |
| `ticket.create_draft` | إنشاء مسودة تذكرة |
| `ticket.update_draft` | تحديث مسودة تذكرة |
| `knowledge.search_internal` | البحث في المعرفة الداخلية |
| `queue_for_approval` | رفع مخرج للموافقة |

### أدوات تحتاج موافقة (requires_approval)

| الأداة | السبب |
|---|---|
| `whatsapp.send_message` | إرسال خارجي |
| `email.send_message` | إرسال خارجي |
| `refund_offer` | التزام مالي |
| `sla_commitment` | التزام تعاقدي |

### أدوات ممنوعة (forbidden)

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `export_pii_bulk` — مرفوضة دائماً عند حدود الأدوات.

---

# English

## Support agent tools

Tool categories are based on `auto_client_acquisition/agent_governance/schemas.py` and the tool boundary in `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### Allowed tools

| Tool | Description |
|---|---|
| `read` / `analyze` | Read and analyze the ticket and its context |
| `whatsapp.draft_reply` | Draft a WhatsApp reply — no send |
| `email.draft_reply` | Draft an email reply — no send |
| `ticket.create_draft` | Create a draft ticket |
| `ticket.update_draft` | Update a draft ticket |
| `knowledge.search_internal` | Search internal knowledge |
| `queue_for_approval` | Raise an output for approval |

### Tools requiring approval

| Tool | Reason |
|---|---|
| `whatsapp.send_message` | External send |
| `email.send_message` | External send |
| `refund_offer` | Financial commitment |
| `sla_commitment` | Contractual commitment |

### Forbidden tools

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `export_pii_bulk` — always rejected at the tool boundary.
