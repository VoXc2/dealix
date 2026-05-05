# Open Design — Research & Integration Decision

**Date:** 2026-05-05
**Researcher:** Founder + Claude Code agent

---

## What Open Design is

[`nexu-io/open-design`](https://github.com/nexu-io/open-design) is a
local-first design runtime that turns natural-language briefs into
visual artifacts (HTML / PDF / PPTX / Markdown) using multiple
coding-agent backends (Claude Code, Codex, Cursor, Gemini, etc.).

Key concepts:

- **DESIGN.md** — single-file design-system contract per project
- **SKILL.md** — bundle that defines a generator's mode, inputs,
  output format, safety rules, example prompt
- **Sandboxed preview** — local-only render before export
- **BYOK** — bring-your-own-key for the LLM backend
- **Read-only MCP access** — Claude Code can `read` design artifacts
  via MCP without re-attaching them per call

Stock skills shipped: `saas-landing`, `dashboard`, `pricing-page`,
`docs-page`, `mobile-app`, `email-marketing`, `social-carousel`,
`finance-report`, `invoice`, `weekly-update`, `guizang-ppt`.

---

## Patterns useful for Dealix

| Pattern | Why it helps Dealix |
|---|---|
| `DESIGN.md` per project | Locks Dealix's Saudi-B2B visual identity once; every artifact inherits |
| `SKILL.md` per generator | Turns each Dealix service into a reusable generator (Mini Diagnostic, Proof Pack, etc.) |
| Discovery + locked brief | Forces the founder to provide context BEFORE generation — no hallucinated metrics |
| Visual directions | Deterministic palette/layout choices prevent random AI-slop |
| Sandboxed preview | Founder reviews artifact before any external send |
| Local-first runtime | No customer data leaves the machine without consent |
| Export layer | Markdown/HTML/PDF/PPTX outputs ready for sales decks + proof packs |

---

## Patterns we explicitly DO NOT copy

| Pattern | Why we skip |
|---|---|
| Vendoring large third-party JS bundles | License + supply-chain risk; we want pure Python + minimal frontend |
| Auto-running coding-agent backends inside Dealix | Excessive agency (OWASP LLM-08); founder runs Claude Code separately if at all |
| MCP daemon exposed beyond localhost | Network attack surface; we keep all design generation in-process |
| Auto-publish to remote channels | Violates "approval-first external action" rule |
| Generic SaaS-landing skill | Dealix has a specific landing-page system already; templated noise hurts SEO |

---

## Integration options considered

| # | Option | Cost | Risk | Verdict |
|---|---|---|---|---|
| 1 | Inspiration only — borrow patterns, no code | low | none | ✅ taken (Phase 1+2+3) |
| 2 | Local dev tool — clone + use Open Design separately | low | depends on founder OS | 🟡 documented as optional bridge (Phase 9) |
| 3 | MCP adapter — Dealix exposes artifacts to Open Design via MCP | medium | network surface, security | ⏳ deferred until Open Design bridge proves useful in practice |
| 4 | Native Dealix DesignOps OS | medium | none | ✅ taken (Phases 1–8) |

---

## Recommended path

**Native Dealix DesignOps OS + optional Open Design bridge later.**

Build:

1. `design-systems/dealix/DESIGN.md` (Phase 1) — locked visual identity
2. `design-skills/<skill>/SKILL.md` × 15 (Phase 2) — generator catalog
3. `auto_client_acquisition/designops/` (Phase 3-8) — Python module:
   - `safety_gate` (no fake proof, no guaranteed claims, no live send)
   - `brief_builder` (deterministic; asks before hallucinating)
   - `generators/` (Mini Diagnostic, Proof Pack, Exec Weekly, Proposal, Pricing, Customer Room Dashboard)
   - `exporter` (markdown/html/json — PDF deferred)
4. `docs/OPEN_DESIGN_BRIDGE_RUNBOOK.md` (Phase 9) — how the founder
   runs Open Design separately if they want a richer prototyping UX

---

## Hard rules baked into DesignOps

Every generated artifact carries these by default:

- ❌ No auto-send (`safe_to_send=False`)
- ❌ No guaranteed-revenue/ranking claim
- ❌ No fake customer name (placeholder only unless consent)
- ❌ No fake metrics (every number sourced from a real ProofEvent or labeled `~estimate`)
- ❌ No PII unless explicitly consented + redacted on export
- ❌ No external network call during generation
- ✅ Arabic primary, English secondary
- ✅ `approval_status="approval_required"` on every artifact
- ✅ `evidence_refs` populated from existing v5/v6 modules

---

## Existing Dealix assets we already have (don't re-build)

| Asset | Path |
|---|---|
| Landing site | `landing/` (30+ HTML pages, RTL, bilingual) |
| Service Activation Console | `landing/status.html` + `landing/assets/js/service-console.js` |
| Founder dashboard HTML | `landing/founder-dashboard.html` + JS |
| Existing proposal + pitch deck | `docs/sales-kit/` |
| Service matrix (canonical inputs) | `docs/registry/SERVICE_READINESS_MATRIX.yaml` |
| Diagnostic CLI generator | `scripts/dealix_diagnostic.py` (already produces bilingual MD) |
| Proof pack assembler | `scripts/dealix_proof_pack.py` + `proof_snippet_engine.render_pack` |
| Forbidden-claims regex | `tests/test_landing_forbidden_claims.py::FORBIDDEN_PATTERNS` |

DesignOps connects these into a typed registry + safety gate; it does
NOT duplicate them.

---

## Decision

**Build the native DesignOps OS now.** Open Design stays a separate
local dev tool the founder can opt into later via the bridge runbook —
never a runtime dependency of Dealix.

— DesignOps Research v1.0 · 2026-05-05 · Dealix
