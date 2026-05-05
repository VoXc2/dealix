# Open Design Bridge Runbook

> Optional. Open Design is NOT a runtime dependency of Dealix.
> The founder may use it locally to prototype visual artifacts that
> Dealix DesignOps can later port. This doc documents the safe flow.

**Date:** 2026-05-05

---

## When to use Open Design

Use Open Design **only** when:

- You want a richer interactive prototyping UX than the native
  Dealix DesignOps generators provide
- The artifact is a **deck**, **landing page mockup**, or
  **multi-page visual** that Dealix's generators don't yet cover
  natively
- You will **manually port** the final, founder-approved design
  back into Dealix landing/ or templates

Do **NOT** use Open Design to:

- Send anything externally
- Process customer PII
- Run agent workflows that touch Dealix runtime data
- Replace Dealix's safety_gate / approval gates

---

## Local-only setup

```bash
# Install once
git clone https://github.com/nexu-io/open-design.git
cd open-design
corepack enable
pnpm install
pnpm tools-dev run web
```

The web app runs on `http://127.0.0.1:<port>`. **Localhost only.**

---

## Security warnings

| ⚠️ Warning | Why |
|---|---|
| Localhost only — never expose the daemon to LAN | Open Design's MCP daemon is meant for local agents; LAN exposure is an attack surface |
| Do NOT paste secrets into prompts | LLM backends can log/cache prompts |
| Do NOT import customer PII | PDPL — customer data shouldn't leave Dealix's redaction pipeline |
| Do NOT run as root / sudo | Standard hygiene |
| Do NOT mount Dealix `docs/proof-events/` into Open Design | Proof events contain redacted-but-still-internal data |

---

## Recommended Dealix → Open Design → Dealix flow

```
1. In Dealix:
   POST /api/v1/designops/build-brief
   → returns LockedBrief with content_sections + visual_direction

2. Founder copies the LockedBrief markdown into Open Design as a brief

3. Open Design generates a richer visual prototype (HTML/PDF/PPTX)

4. Founder reviews in Open Design's sandboxed preview

5. Founder exports the artifact (HTML/Markdown only — skip PDF/PPTX
   unless the customer specifically requested those formats)

6. Founder runs:
   POST /api/v1/designops/check-artifact
   { "manifest_or_text": "<paste exported HTML/Markdown>" }
   → returns SafetyGateResult — if NOT passed, fix and re-export

7. Manually port the approved sections into:
   - landing/ (for public pages)
   - docs/sales-kit/ (for proposals + decks)
   - docs/customers/<customer>/ (for per-customer artifacts — gitignored)
```

---

## What Open Design adds vs Dealix native

| Concern | Dealix DesignOps native | Open Design |
|---|---|---|
| Bilingual markdown | ✅ | ✅ |
| Bilingual HTML | ✅ | ✅ |
| PDF / PPTX | ⏳ deferred | ✅ |
| Live LLM iteration | ❌ no LLM by design | ✅ via BYOK |
| Visual sandbox preview | basic | rich |
| Forbidden-token gate | ✅ enforced | ❌ not aware of Dealix policy |
| PDPL alignment | ✅ baked in | ❌ founder responsibility |

If the founder uses Open Design, **the Dealix safety_gate (step 6
above) is mandatory** — Open Design won't catch `نضمن` /
`guaranteed` / cold-WhatsApp implications by itself.

---

## Future MCP bridge (deferred)

A future Dealix-↔-Open-Design MCP adapter would let Claude Code read
Dealix artifacts via `nexu-io/open-design`'s MCP without re-attaching.
Deferred until:

- Dealix DesignOps native generators ship the 6 core artifacts
- Founder uses Open Design at least 5 times manually first
- A real customer requests a format Dealix doesn't produce natively
- Security review of MCP daemon exposure is signed off

If/when that happens, see issue tracker for the bridge implementation.

---

## Default decision

**Don't run Open Design** until you have a concrete need. Dealix
DesignOps native generators (Mini Diagnostic / Proof Pack / Exec
Weekly / Proposal / Pricing / Customer Room Dashboard) cover the
first-customer path. Open Design is reserved for visual richness
that doesn't yet exist in Dealix — and even then, manual port is
the bridge, not a runtime dependency.

— Open Design Bridge Runbook v1.0 · 2026-05-05 · Dealix
