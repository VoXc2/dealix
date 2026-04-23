# HANDOFF — Dealix AI CRO (Revenue OS)
**Updated:** 2026-04-21 · **Owner:** Sami Mohammed Assiri · sami.assiri11@gmail.com · +966 570 327 724

> **Status:** Full-loop operating product, deployed + tested end-to-end on LIVE DB.
> ✅ 4 new modules (state machine, action center, lead engine, playbooks) — self-tests green
> ✅ 5 evals all passing · ✅ end-to-end test green (signal → WON) · ✅ landing shows 12-stage Revenue Loop

---

## 1 · The shift from "capability collection" → "operating loop"

Before this session, Dealix was a set of loose modules (policy engine, opportunity graph, static schema). After the Full Product Audit, it is **one state machine** — `signal → enrich → score → decide_channel → draft → send → wait_reply → negotiate → approval → book → summarize → report → {won|lost|blocked}` — with a single Action Center queue, evidence-grounded leads, sector-specific playbooks, and an evaluation harness the owner can run before every deploy.

**Why this matters commercially:** The product is no longer sold as "AI that drafts emails" (commodity). It is sold as a **Revenue Operating System** — the first that speaks Saudi-native data sources (Wathq, Monsha'at, Etimad, Maroof, SAMA Sandbox, CMA Fintech Lab), has a policy gate that understands PDPL and Meta WhatsApp January-2026 restrictions, and keeps the human owner at every red line.

---

## 2 · Live architecture (what runs in production)

### Server
- **IP:** `188.245.55.180` (Ubuntu 24.04)
- SSH: `ssh -o StrictHostKeyChecking=no -i ~/.ssh/dealix_deploy root@188.245.55.180`
- **Postgres 16 + pgvector** active · DB `dealix` · user `dealix` · DSN `postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix`
- FastAPI on `127.0.0.1:8001` (systemd unit `dealix-api.service`)
- nginx serves `dealix.me` + `dashboard.dealix.me` (HTTPS via certbot)
- Python venv: `/opt/dealix/.venv` (asyncpg, fastapi, uvicorn installed)

### Code layout `/opt/dealix/ai_cro/`
| Module | Purpose | Tested |
|---|---|---|
| `workflow/revenue_loop.py` | 12-stage state machine · policy gate · idempotency · resume-after-approval | ✅ 5 self-tests |
| `action_center/action_center.py` | Approval queue (`queue()`, `item_timeline()`, `resolve_approval()`) + FastAPI router | ✅ live DB |
| `lead_engine/lead_engine.py` | Hybrid search (trigram + firmographic completeness + signal freshness) with evidence cards | ✅ live DB |
| `playbooks/sector_playbooks.py` | 4 playbooks: real_estate, construction, retail, fintech — signals, value bands, outreach order, guardrails, Arabic hooks, objection rebuttals | ✅ self-test |
| `policy_engine/policy_engine.py` | Verdict AUTO/APPROVE/BLOCK · tier thresholds · WhatsApp intent restrictions · content guards | ✅ 7 live scenarios |
| `opportunity_graph/schema.sql` + `graph_api.py` | 8 tables + `v_priority_opportunities` view · async API with Arabic normalizer | ✅ integration test |
| `observability/tracing.py` | OTel wrapper with stdout fallback | ready |
| `evals/eval_harness.py` | 5 evals: lead_relevance, draft_quality, negotiation_safety, approval_necessity, report_usefulness | ✅ 5/5 pass |
| `test_e2e.py` | End-to-end: loops the live AlAhliya opportunity from signal → WON | ✅ 6 steps green |

### Landing (LIVE)
- **URL:** https://dealix.me
- Hero: "أول Saudi AI Chief Revenue Officer — يقود إيراد شركتك بوكلاء ذكاء اصطناعي محكومين بقرارك"
- Section `#how` now shows the **12-stage Revenue Loop** (replacing the old 7 generic steps): Signal → Enrich → Score → Decide Channel → Draft → Policy Gate → Send → Negotiate → Approve → Book → Summarize → Report
- File on server: `/var/www/dealix/landing/index.html` (backup in same dir with `.bak-<timestamp>`)

---

## 3 · Revenue Loop — how every opportunity flows

```
SIGNAL  ──▶  ENRICH  ──▶  SCORE  ──▶  DECIDE_CHANNEL  ──▶  DRAFT
                                                            │
                                       ┌─── POLICY GATE ───┘
                                       │    (auto/approve/block)
                                       ▼
                                     SEND  ──▶  WAIT_REPLY  ──▶  NEGOTIATE
                                                                    │
                                                 ┌─── APPROVAL ◀────┘  (if >15% concession
                                                 │                       or enterprise tier
                                                 │                       or red-line content)
                                                 ▼
                                              BOOK  ──▶  SUMMARIZE  ──▶  REPORT
                                                                            │
                                                                            ▼
                                                                    WON / LOST / BLOCKED
```

**Guarantees built in:**
1. **Idempotency** — every transition hashes `(from, to, payload)`; replays short-circuit.
2. **Policy gate** — Policy Engine is injected via constructor; any state transition can force APPROVAL or BLOCKED.
3. **Resume** — after an APPROVAL interrupt, `resume_after_approval(state, decision, edits)` picks up the pending action with owner edits applied.
4. **Full audit** — every `history[]` entry records `{from, to, actor, at, payload}` and is JSON-serializable.

---

## 4 · Action Center — the owner's single queue

`/opt/dealix/ai_cro/action_center/action_center.py` replaces the "many dashboard screens" pattern with one ranked list. Each `ActionItem` carries:
- `kind`: `approval` (priority 95) · `first_move` (70) · `negotiation` · `meeting_prep`
- `company_name`, `title_ar`, `expected_value_sar`, `win_probability`, `weighted_value_sar`
- `evidence[]` — list of `{type, label_ar, source, url, confidence}` cards
- `timeline[]` — stage history from the state machine
- `next_action_label_ar` — exactly what button the owner sees
- `requires_owner_decision` — boolean that drives the approval badge

FastAPI router is mounted via `build_router(dsn)` — ready to wire into `/opt/dealix/main.py`.

---

## 5 · Lead Engine v2 — evidence-grounded, not keyword-grounded

Blended confidence: `0.5 * trigram_lex + 0.3 * firmographic_completeness + 0.2 * signal_freshness_bonus`.

`FIELD_WEIGHTS` for completeness: sector 0.15, region 0.10, size 0.15, CR 0.20, source_url 0.10, confidence 0.10.

Every returned `Lead` carries `evidence[]` cards citing real Saudi data sources. Arabic normalization reuses `normalize_ar()` from `graph_api.py` (strips diacritics, unifies alef/yaa, removes leading `ال`).

---

## 6 · Sector Playbooks — 4 verticals, Saudi-native

| Sector | Channel order | Pro threshold | Key signals |
|---|---|---|---|
| `real_estate` | LinkedIn → Email → WhatsApp → Call | 10,000 SAR | Sakani/Wafi listings, Baladia permits, Wathq shareholder change |
| `construction` | Email → LinkedIn → Call → WhatsApp | 15,000 SAR | Etimad tenders, Monsha'at programs, BOQ updates (stricter tier) |
| `retail` | WhatsApp → LinkedIn → Email → Call | 10,000 SAR | Maroof reviews, Salla/Zid store launches, new SKU surge |
| `fintech` | Email → LinkedIn → Call (NO WhatsApp) | 5,000 SAR | SAMA Sandbox, CMA Fintech Lab, PDPL compliance posture |

Each playbook ships with: 5 qualification signals, value bands, Arabic opening hooks, objection rebuttals, red flags, evidence URLs.

---

## 7 · Evaluation Harness — gate every deploy

`/opt/dealix/ai_cro/evals/eval_harness.py` — run with:
```bash
DEALIX_DSN='postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix' \
  /opt/dealix/.venv/bin/python -m ai_cro.evals.eval_harness
```

| Eval | What it checks | Threshold | Status |
|---|---|---|---|
| `lead_relevance` | Engine finds AlAhliya for "الأهلية", "أهلية", "AlAhliya" | 0.70 | ✅ 1.00 |
| `draft_quality` | Arabic %, numeric anchor, CTA, no forbidden promises, AI disclosure | 0.80 | ✅ 1.00 |
| `negotiation_safety` | Discount >15% requires approval · no regulatory promises · no fake refs · no impersonation | 1.00 | ✅ 1.00 |
| `approval_necessity` | Enterprise/NDA/impersonate correctly routed; small email = AUTO | 1.00 | ✅ 1.00 |
| `report_usefulness` | Has URL + number + concrete action + time horizon | 0.75 | ✅ 1.00 |

**Exit code 0 = ship. Non-zero = block deploy.**

---

## 8 · End-to-end integration test

`/opt/dealix/ai_cro/test_e2e.py` — runs against LIVE DB:

```
STEP 1 · Lead Engine resolved شركة الأهلية للعقارات (conf 0.39)
STEP 2 · Action Center queue returned first_move · "صفقة مجمع سكني الملك فهد"
STEP 3 · Policy: impersonate → BLOCK · 1.55M proposal → APPROVE
STEP 4 · Playbook real_estate loaded · 4 channels · 10K threshold
STEP 5 · Revenue Loop · 5 transitions → APPROVAL → resume → WON (12 total)
STEP 6 · v_priority_opportunities: 1 row · total weighted 1,550,000 SAR
```

---

## 9 · Ship-day checklist for the owner

1. SSH to server. `cd /opt/dealix`.
2. Run evals: `DEALIX_DSN=… /opt/dealix/.venv/bin/python -m ai_cro.evals.eval_harness` — must print `5/5 passed`.
3. Run E2E: `DEALIX_DSN=… /opt/dealix/.venv/bin/python -m ai_cro.test_e2e` — must print `E2E RESULT ✅`.
4. Restart API: `systemctl restart dealix-api`. Tail logs for 30 seconds.
5. Hit `https://dealix.me/status.html` — trust bar should reflect the newly live service.
6. Open an opportunity in the Action Center, simulate one approve + one reject to verify the audit log.

---

## 10 · Commercial positioning (still-in-effect invariants)

- **Launch NOW, best form possible** · delete blockers without hesitation · profit first.
- Pricing hidden from landing, revealed only in meetings.
- Arabic-first UI, RTL layout.
- Never use `browser_task` for GitHub / Salesforce — use connectors / CLI.
- Minimize tokens: CLI > MCP, `grep` before `read`, `edit` > `write`.
- Sender address: `sami.assiri11@gmail.com`.

---

## 11 · Citations (keep these URLs — they appear in evidence cards and the deck)

- HubSpot Breeze pay-per-task: https://www.hubspot.com/company-news/hubspots-customer-agent-and-prospecting-agent-now-you-pay-when-the-task-is-complete
- Salesforce Agentforce: https://www.salesforce.com/news/stories/agentforce-sales-announcement/
- LangGraph durable execution: https://docs.langchain.com/oss/javascript/langgraph/durable-execution
- OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- Wathq developer APIs: https://developer.wathq.sa/en/apis
- Monsha'at programs: https://www.monshaat.gov.sa/en/node/12768
- Meta WhatsApp business AI rules (2024): https://about.fb.com/news/2024/06/new-ai-tools-meta-verified-and-more-for-businesses-on-whatsapp/
- Meta WhatsApp general-AI ban (Jan 2026): https://economictimes.indiatimes.com/tech/artificial-intelligence/meta-bans-general-purpose-ai-chatbots-from-whatsapp-business-platform/articleshow/124683946.cms

---

## 12 · What's next (roadmap post-handoff)

1. **OpenAPI spec** for Action Center router → hand to Saas integrations.
2. **Wathq + Monsha'at live connectors** feeding the signal ingester.
3. **Weekly board report** cron (Friday 7am Riyadh) — pulls from `v_priority_opportunities` + `summarize` stages.
4. **Eval 6: cost per won deal** — ties agent actions to weighted value.
5. **Second policy tier** for government entities (Etimad rules + ZATCA invoicing).
