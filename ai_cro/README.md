# Dealix AI CRO — Revenue Operating System

> **أول Saudi AI Chief Revenue Officer** — يقود إيراد شركتك بوكلاء ذكاء اصطناعي محكومين بقرارك.

هذا هو الـ Revenue Operating Loop: مسار واحد من `signal` إلى `report` — لا شاشات متفرقة.
كل مرحلة مُختبرة، وكل قرار حرج يرجع للمالك، وكل مخرج يُسجَّل.

---

## البنية (Architecture)

```
ai_cro/
├── workflow/             # State machine موحّد (12 مرحلة)
│   └── revenue_loop.py   # signal → enrich → score → decide → draft → send → … → WON
├── action_center/        # قائمة الموافقات الموحدة (بديل الشاشات المنفصلة)
│   └── action_center.py  # queue() · item_timeline() · resolve_approval() + FastAPI router
├── lead_engine/          # بحث هجين مع evidence cards
│   └── lead_engine.py    # trigram + firmographic completeness + signal freshness
├── playbooks/            # Playbooks القطاعية (4 قطاعات)
│   └── sector_playbooks.py  # real_estate · construction · retail · fintech
├── policy_engine/        # بوابة السياسات (auto / approve / block)
│   └── policy_engine.py  # PDPL · Meta WhatsApp restrictions · tier thresholds
├── opportunity_graph/    # مخطط + API لجرافة الفرص
│   ├── schema.sql        # 8 جداول + v_priority_opportunities
│   └── graph_api.py      # async API + Arabic normalizer
├── observability/        # OpenTelemetry wrapper
│   └── tracing.py
├── evals/                # Eval Harness — 5 evals
│   └── eval_harness.py   # lead_relevance · draft_quality · negotiation_safety · approval_necessity · report_usefulness
├── test_integration.py   # اختبار تكامل: يُنشئ شركة + فرصة في v_priority_opportunities
└── test_e2e.py           # اختبار end-to-end كامل ضد DB حي
```

---

## حلقة الإيراد (Revenue Loop)

```
SIGNAL → ENRICH → SCORE → DECIDE_CHANNEL → DRAFT
                                            │
                         ┌─── POLICY GATE ──┘
                         │   (auto/approve/block)
                         ▼
                       SEND → WAIT_REPLY → NEGOTIATE
                                              │
                         ┌─── APPROVAL ◀──────┘   (>15% discount
                         │                         أو enterprise tier
                         │                         أو red-line content)
                         ▼
                      BOOK → SUMMARIZE → REPORT → {WON | LOST | BLOCKED}
```

**ضمانات مدمجة:**
- **Idempotency** — كل transition يُهشَّم `(from, to, payload)`؛ الإعادات تُختصر.
- **Policy gate** — Policy Engine مُحقَّن عبر constructor؛ أي transition ممكن يفرض APPROVAL أو BLOCKED.
- **Resume** — بعد APPROVAL interrupt، `resume_after_approval(state, decision, edits)` يكمّل.
- **Audit كامل** — كل `history[]` يسجّل `{from, to, actor, at, payload}` بصيغة JSON.

---

## Playbooks القطاعية

| القطاع | ترتيب القنوات | عتبة Pro | إشارات رئيسية |
|---|---|---|---|
| `real_estate` | LinkedIn → Email → WhatsApp → Call | 10,000 SAR | Sakani/Wafi · Baladia permits · Wathq |
| `construction` | Email → LinkedIn → Call → WhatsApp | 15,000 SAR | Etimad tenders · Monsha'at · BOQ |
| `retail` | WhatsApp → LinkedIn → Email → Call | 10,000 SAR | Maroof · Salla/Zid · SKU surge |
| `fintech` | Email → LinkedIn → Call (لا WhatsApp) | 5,000 SAR | SAMA Sandbox · CMA Fintech Lab · PDPL |

---

## Quick Start

### التشغيل المحلي
```bash
export DEALIX_DSN='postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix'

# اختبارات الحلقة الذاتية
python -m ai_cro.workflow.revenue_loop

# اختبار Action Center ضد DB
python -m ai_cro.action_center.action_center

# اختبار Lead Engine ضد DB
python -m ai_cro.lead_engine.lead_engine

# اختبار Playbooks
python -m ai_cro.playbooks.sector_playbooks
```

### تشغيل Evals (يجب أن يطبع `5/5 passed`)
```bash
python -m ai_cro.evals.eval_harness
```

### اختبار end-to-end (يجب أن يطبع `E2E RESULT ✅`)
```bash
python -m ai_cro.test_e2e
```

---

## معايير القبول (Ship-day)

| الخطوة | المعيار |
|---|---|
| 1. SSH للسيرفر | `/opt/dealix` |
| 2. `eval_harness` | `5/5 passed` (exit 0) |
| 3. `test_e2e` | `E2E RESULT ✅` (exit 0) |
| 4. Restart API | `systemctl restart dealix-api` |
| 5. Status page | `https://dealix.me/status.html` — أخضر |
| 6. Audit log | موافقة + رفض يُسجَّلان |

---

## الخادم الحي (Production)

| المعلومة | القيمة |
|---|---|
| IP | `188.245.55.180` |
| OS | Ubuntu 24.04 |
| DB | Postgres 16 + pgvector · DB `dealix` |
| DSN | `postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix` |
| API | FastAPI on `127.0.0.1:8001` · systemd: `dealix-api.service` |
| Landing | `https://dealix.me` · file: `/var/www/dealix/landing/index.html` |
| Dashboard | `https://dashboard.dealix.me` |
| Python venv | `/opt/dealix/.venv` (asyncpg · fastapi · uvicorn) |

---

## Citations

- [HubSpot Breeze pay-per-task](https://www.hubspot.com/company-news/hubspots-customer-agent-and-prospecting-agent-now-you-pay-when-the-task-is-complete)
- [Salesforce Agentforce](https://www.salesforce.com/news/stories/agentforce-sales-announcement/)
- [LangGraph durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
- [OpenTelemetry GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Wathq APIs](https://developer.wathq.sa/en/apis)
- [Monsha'at programs](https://www.monshaat.gov.sa/en/node/12768)
- [Meta WhatsApp business AI (2024)](https://about.fb.com/news/2024/06/new-ai-tools-meta-verified-and-more-for-businesses-on-whatsapp/)
- [Meta WhatsApp general-AI ban (Jan 2026)](https://economictimes.indiatimes.com/tech/artificial-intelligence/meta-bans-general-purpose-ai-chatbots-from-whatsapp-business-platform/articleshow/124683946.cms)

---

## للتوثيق الكامل

- [HANDOFF_AI_CRO.md](../HANDOFF_AI_CRO.md) — وثيقة التسليم الرئيسية
- [ARCHITECTURE.md](../ARCHITECTURE.md) — المعمارية العامة للنظام
- [DAILY_EXECUTION_SCHEDULE_AR.md](../DAILY_EXECUTION_SCHEDULE_AR.md) — الجدول اليومي 90 يوم

---

**Owner:** Sami Mohammed Assiri · sami.assiri11@gmail.com · +966 570 327 724
