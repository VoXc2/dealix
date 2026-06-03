# Dealix Company OS

The operating system that runs Dealix as a Saudi B2B Revenue company: how we find
demand, draft outreach, get founder approval, deliver, prove value, renew — and stay
safe while doing it.

**Founding principles:** Arabic-first · approval-first · proof-driven ·
privacy-aware · agent-assisted but never agent-uncontrolled. No external sends by
default; everything outbound is `dry_run=true`, `approval_required=true`,
`send_enabled=false`.

---

## Subsystems

| Area | Folder | What it holds |
|------|--------|---------------|
| Revenue | [`revenue/`](revenue) | Pipeline, prospects, outreach queue, proposals, objections, follow-ups |
| Commercial | [`commercial/`](commercial) | [ICP matrix](commercial/ICP_MATRIX.md) · [Product ladder](commercial/PRODUCT_LADDER.md) · [Pricing guardrails](commercial/PRICING_GUARDRAILS.md) |
| WhatsApp | [`whatsapp/`](whatsapp) | [Post-consent Client OS](whatsapp/WHATSAPP_CLIENT_OS.md) |
| Delivery | [`delivery/`](delivery) | P1 SOP, intake, success plan, proof-pack template |
| Customer Success | [`customer_success/`](customer_success) | [Health score](customer_success/CLIENT_HEALTH_SCORE.md) · [Renewal playbook](customer_success/RENEWAL_PLAYBOOK.md) |
| Governance | [`governance/`](governance) | [Permissions](governance/agent_permissions.md) · [Autonomy levels](governance/agent_autonomy_levels.md) · [Untrusted input](governance/untrusted_input_policy.md) · [Approval gates](governance/approval_gates.md) · PDPL, ledger, suppression |
| Security | [`security/`](security) | [Outbound safety](security/OUTBOUND_SAFETY_POLICY.md) · [Secrets handling](security/SECRETS_HANDLING_POLICY.md) |
| Finance | [`finance/`](finance) | Unit economics, invoices, revenue scorecard |
| Marketing | [`marketing/`](marketing) | LinkedIn posts, one-pagers, pitch deck |
| War Room | [`war_room/`](war_room) | Daily brief, weekly CEO brief, scorecard, [risks](war_room/RISKS.md) |

Shared contracts live in [`../schemas/`](../schemas); enforcement lives in
[`../scripts/`](../scripts) and [`../tests/`](../tests).

---

## How safety is enforced (not just documented)

| Control | Implementation |
|---------|----------------|
| Governance rules (G001–G007) | `scripts/governance_check.py` |
| Outbound / WhatsApp / claims gate | `scripts/safety_gate.py` (dry-run, report-only) |
| Data + rules in CI | `tests/` (pytest, stdlib-only) |
| CI gate | `.github/workflows/company-os-safety.yml` (least privilege, no secrets) |

Run locally:

```bash
python scripts/governance_check.py     # G001–G007 compliance
python scripts/safety_gate.py          # outbound safety (no sends)
python -m pytest tests/ -q             # full safety + data + schema suite
```

---

## The flow, end to end

```
Signal → Research → Draft (A2) → Approval queue (A3) → Founder approves (A4)
   → Send-ready (only if every outbound gate passes) → Reply handling
   → WhatsApp after consent → Proposal / Proof → Payment handoff (approval)
   → Delivery → Weekly value report → Renewal (evidence ≥ L3)
```

Every external or sensitive step is gated by a human. See
[`governance/approval_gates.md`](governance/approval_gates.md).

---

*Company OS v1 | 2026-06-03*
