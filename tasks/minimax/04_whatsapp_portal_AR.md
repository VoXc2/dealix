# MiniMax Sub-prompt 04 — WhatsApp-after-consent + Secure Client Portal (status binding, no rebuild)

> **Scope:** Document the existing WhatsApp + Client Portal surfaces, verify consent gate, list one-liner status of each.
> **Do not break:** `auto_client_acquisition/governance_os/no_cold_whatsapp.py`, `docs/wave8/CONSENT_RECORD_TEMPLATE.json`, the DSR template.
> **Branch:** `feature/minimax-factory-p0-hardening`

---

## 1. Objective

Both surfaces exist. The gap is **discoverability** — a new operator does not know which file holds which rule, or which test enforces which safety. This sub-prompt produces one doc per surface that ties rules + tests + UI + API together.

---

## 2. Files to Create

### 2.1 `docs/whatsapp/WHATSAPP_AFTER_CONSENT_MAP_AR.md`

Sections:
1. **Hard rule (one line):** No cold WhatsApp. Period.
2. **Consent gate** — where it lives (`auto_client_acquisition/governance_os/no_cold_whatsapp.py`), what record it requires (`docs/wave8/CONSENT_RECORD_TEMPLATE.json`).
3. **What triggers human handoff** — complaints, legal, pricing, privacy (list the 4 trigger keywords).
4. **Action card schema** — fields: `title`, `summary`, `reason`, `risk_level`, `options[]`, `approval_required`. Reference the existing schema file (search for it under `schemas/` or `auto_client_acquisition/.../`).
5. **Readiness scan** — script that scores a lead for WhatsApp readiness: `scripts/whatsapp_e2e_mock.py` (already exists).
6. **Test coverage** — `pytest tests/test_whatsapp_safety_gates.py` (already exists). Do not edit.
7. **Eval dataset** — `data/evals/whatsapp_safety_cases.jsonl` (already exists).
8. **What "after consent" means in practice** — short examples of 2 legitimate flows (existing client asking for renewal quote, warm lead who replied to an email saying "send me WhatsApp").
9. **Forbidden flows** — 3 examples of blocked flows (cold list, scraped numbers, purchased database, LinkedIn auto-DM).

### 2.2 `docs/client_portal/SECURE_CLIENT_PORTAL_MAP_AR.md`

Sections:
1. **Why a portal exists** — never exchange API keys / secrets over WhatsApp.
2. **Routes** — `/client/start`, `/client/upload`, `/client/permissions` (under `frontend/src/app/[locale]/client/` or `apps/web/...`). Search the repo to confirm the actual path; if absent, flag it as a real gap.
3. **Permission request flow** — client requests a permission (e.g. read CRM); system logs to `permission_requests` with `evidence_level` and `approval_required=true`.
4. **Upload flow** — files go to S3-compatible storage with presigned URL; never to chat. Cite the code.
5. **Redaction** — anything client-side that touches PII must go through the existing redaction layer.
6. **Test coverage** — search for `test_client_portal*` or `test_permission*` and list them.

### 2.3 `reports/whatsapp/WHATSAPP_CONSENT_AUDIT_LATEST.md` (stub if missing)

A short audit snapshot:
- Count of consent records on file.
- Count of cold-WhatsApp attempts blocked in the last 7 days (read from logs if available, else "N/A — no signal").
- Count of human handoffs triggered.
- Last DSR (Data Subject Request) processed.

### 2.4 `reports/client_portal/PORTAL_HEALTH_LATEST.md` (stub if missing)

A short health snapshot:
- Count of active client sessions.
- Top 3 permission requests by frequency.
- Last 5 upload events (anonymized).

---

## 3. Constraints

- No code changes. Docs and stubs only.
- No live API calls. Status docs can be hand-written for now; auto-writer comes in a later sub-prompt.
- If a referenced file does not exist, **say so explicitly** in the doc (e.g. "GAP: client portal route not found in frontend/ — flagged for follow-up"). Do not invent files.
- Both maps under 200 lines each.

---

## 4. Acceptance

```bash
test -f docs/whatsapp/WHATSAPP_AFTER_CONSENT_MAP_AR.md
test -f docs/client_portal/SECURE_CLIENT_PORTAL_MAP_AR.md
make whatsapp-safety
make privacy-guard
```
