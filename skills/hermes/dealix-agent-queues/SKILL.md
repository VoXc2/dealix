---
name: dealix-agent-queues
description: Show and reconcile Dealix logical-agent work queues under the Agentic Holding / sector-company / arm-pod architecture. Read-only by default; no fake busywork and no material external actions.
---

# Dealix Agent Queues — Agentic Holding

## Canonical topology

Read current authority before queue work:

1. `config/company/fresh_market_execution_policy.json`
2. `docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md`
3. `dealix/config/commercial_reset_2026_09_12.yaml` for commercial routing
4. current sector and arm registries
5. current Opportunity / Approval / Proof / Economic Truth state

The historical fixed-five permanent-agent invariant is deprecated.

Legacy names such as `dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer` and `dealix-content` may remain as compatibility aliases for older modules. They are not the full logical-agent fleet.

Canonical hierarchy:

`Dealix Group -> Shared Agent Services -> Sector Companies -> Arm Pods -> Specialists`

Logical agent count is separate from runtime worker count. Runtime workers are lazy and resource-governed.

## Queue layers

### Group queues

Examples:
- President / economic ordering
- Revenue
- Delivery
- Engineering
- Finance / Economic Truth
- Research / intelligence
- Security / risk / governance
- Procurement / B2G
- Partnerships
- Brand / content
- QA / proof
- Self-improvement

### Sector-company queues

For every active sector, route scoped work to roles such as sector CEO, strategy, market intelligence, research, sales, diagnostic, solution architecture, delivery, economics, compliance, content, partnerships, QA, proof and learning.

### Arm-pod queues

For every applicable canonical arm, use at least:
- `lead`
- `scout`
- `operator`
- `verifier`

Additional specialists require a parent, authority scope and evidence trail.

## Commercial Reset routing

For commercial work also load:

- `docs/commercial/COMMERCIAL_RESET_AGENT_PLAYBOOK_2026_09_12.md`
- `skills/hermes/dealix-commercial-reset/SKILL.md`

Machine-readable previews:

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/commercial/commercial_reset_agent_packet.py" --blueprint
"$PY" "$REPO/scripts/commercial/commercial_reset_agent_packet.py" --daily
```

These outputs are logical dispatch plans, not instructions to start one process per logical agent.

## Existing compatibility queues

The existing Founder OS queues remain valid compatibility surfaces until migrated under one canonical hierarchy:

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/founder_agent_queue_status.py"
sed -n '1,12p' /opt/dealix/company-os/founder-os/queues/ACTION_QUEUE.tsv
sed -n '1,10p' /opt/dealix/company-os/founder-os/queues/APPROVAL_QUEUE.tsv
```

Do not create a second scheduler or queue system merely because a legacy compatibility surface remains.

## Resource governor

The historical global `DEEP_WIP_MAX=3` is deprecated.

Queue dispatch must account for:
- CPU/RAM/swap/disk pressure;
- provider/model quotas and cost;
- worktree availability;
- risk and expected economic value;
- duration and contention domain;
- incident state.

Parallel repo writers use isolated worktrees. Read-only research may fan out more broadly.

## Output contract

Report:
- logical agent identity;
- parent namespace;
- queue item and business purpose;
- current evidence/state;
- authority scope;
- expected economic value;
- risk/cost class;
- runtime eligibility under resource governor;
- output/receipt path;
- next verified state.

No synthetic tasks. Do not start work just to keep agents busy.

Anything material/external remains an approval item unless exact action-bound authority is already proven.

Truth firewall:

- Research != Relationship
- Public contact != Consent
- Draft != Sent
- Quote != Invoice
- Invoice != Payment
- Delivery != Customer Value

## Forbidden

- duplicate Company Brain, scheduler, Approval Center, Proof Ledger, Economic Truth store or model router;
- process-per-logical-agent architecture;
- orphan agents/arms/sectors;
- uncontrolled paid-model spill;
- restoring paid diagnostics or public fixed-price authority;
- cold WhatsApp or mass/personal LinkedIn automation;
- fabricated proof, relationships, consent or compliance/government claims;
- material external actions from this read-only queue skill.
