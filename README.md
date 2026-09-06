<div align="center">

# Dealix — Governed AI Execution Platform for Saudi Business

**Turn company signals into governed execution and measurable proof.**

`Signal -> Decision -> Action -> Proof`

Saudi-first · Customer-specific · Approval/evidence bounded

**[العربية](README.ar.md)** · **English**

[Platform Truth](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md) · [Launch](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md) · [Production](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) · [Go-Live](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)

</div>

---

## What Dealix is

Dealix is a **governed AI execution platform for Saudi business**. It turns official/first-party company signals into evidence-backed priorities and decisions, prepares or controls execution within explicit authority boundaries, and records proof of what actually happened.

Under the market-facing layer, Dealix operates as one Saudi-first **AI Business Operating System / Company Machine**. Its twelve Operating Systems cover Command, Revenue, Proof, Client, Delivery, Support, Finance, Data, Governance, Academy, Partner and Venture. **Revenue + Proof + Command** remains core capability language, but it is not the current generic category headline.

Dealix is not a generic chatbot, CRM replacement, lead scraper, mass-outreach bot, uncontrolled agent fleet or guaranteed-revenue service.

Operating rule:

> AI explores, analyzes and recommends. Governed workflows execute. Material external actions require the applicable current authority and evidence.

## Canonical engagement path

1. **Execution Diagnostic** — identify one economically meaningful workflow, baseline, leakage, systems, owner, data boundary and proof criteria.
2. **Qualified Discovery + Customer-Specific Quote** — confirm scope, start conditions and customer-specific commercial terms.
3. **Outcome Sprint** — execute a bounded workflow against measurable acceptance criteria; duration and scope are customer-specific.
4. **Proof Review** — compare outcome with baseline and separate activity from verified value.
5. **Dealix Runtime** — recurring managed/platform execution only after the workflow demonstrates repeatable value.

There is **no public fixed-price table, no public checkout authority, and no guaranteed revenue/ROI/result claim**.

Internal compatibility IDs may retain historical names such as `free_mini_diagnostic` or `revenue_command_pilot_30d` until an accepted runtime migration changes them. Those IDs do not restore superseded market labels or public pricing authority.

## One Company Machine

Permanent owners remain exactly five:

- `dealix-pm` — President / portfolio / decisions / approvals / next action.
- `dealix-sales` — signals, account research, qualification, diagnostic, discovery and negotiation preparation.
- `dealix-delivery` — onboarding, execution, support, acceptance and proof preparation.
- `dealix-engineer` — reliability, integrations, trust gates and productization that improves Cash, Trust or Repeatability.
- `dealix-content` — evidence-safe founder/company/search/distribution assets.

Specialists are bounded workloads under these owners. Do not create a parallel Company OS, Company Brain, CRM, Opportunity Graph, Approval Center, Proof Ledger, scheduler, model router, truth store, control plane or permanent agent fleet.

## Truth firewall

Dealix never collapses these states:

- research != relationship
- public contact != consent
- lead != buyer intent
- draft != sent
- quote != invoice
- invoice != payment
- synthetic/demo != customer proof
- PR != production
- historical PASS != current exact-head PASS

## Communication / growth constraints

- No scraping as a growth shortcut.
- No cold WhatsApp automation.
- No mass/unapproved LinkedIn account automation.
- No external auto-send without the applicable current authority.
- No fake proof, fake relationships, identity deception or ban-evasion.
- Founder-quality messaging may be prepared as clearly from Dealix / on behalf of the founder.

## Quick start

```bash
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
make setup
cp .env.example .env
make run
```

Local API docs: `http://localhost:8000/docs`

Production-style verification:

```bash
make prod-verify
```

Useful checks:

```bash
make env-check
make api-contract-check
make security-smoke
make production-smoke
make dependency-inventory
make release-manifest
make test
make security
```

## Architecture model

| Plane | Responsibility |
|---|---|
| Decision | Agents, reasoning, synthesis and evidence assembly. |
| Execution | Deterministic workflows, retries, compensation and bounded commitments. |
| Trust | Policy, approval, audit, verification and proof. |
| Data | Operational truth, lineage, metrics and integrations. |
| Operating | CI/CD, Docker, release discipline, repo governance and runbooks. |

## Launch / production truth

Before any material commercial/public activation, use current evidence rather than README claims:

- [Platform Source of Truth](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md)
- [Launch Operator Runbook](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md)
- [Production Readiness Checklist](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [Commercial Go-Live Gate](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)
- [Domain Operations](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md)
- [No-overclaim register](dealix/registers/no_overclaim.yaml)
- [Saudi compliance register](dealix/registers/compliance_saudi.yaml)

Repository source, a green provider status or an older acceptance receipt does not by itself prove current production identity or commercial proof.

## Security / Saudi posture

Dealix is designed around least privilege, approval and evidence boundaries, secrets outside source control, provider/runtime verification and Saudi operating context. Compliance documentation is not a blanket legal certification; claims remain scoped to verified controls and evidence.

## License

MIT — see [LICENSE](LICENSE).
