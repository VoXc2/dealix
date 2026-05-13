# Venture Factory

Ventures are standalone product entities spun out of mature Dealix capabilities. **No venture launches without proof.** The Venture Factory exists to enforce that rule and to ensure ventures inherit the Core OS rather than fork it.

## 1. Venture gate

A capability becomes a venture candidate only when **all** are true:

- 5+ paid clients in the originating BU.
- 2+ active retainers using the capability.
- Repeatable delivery with QA score ≥ 80%.
- A clear product module already shipped in `core_os`.
- Playbook maturity score ≥ 80%.
- A named owner willing to leave the BU to run the venture.
- Healthy contribution margin in the originating BU.
- A proof library tied to the capability.
- Continued Core OS dependency (the venture *uses* Dealix OS, it does not rebuild it).

## 2. Candidate venture map

| Candidate | Originating BU | Module |
| --- | --- | --- |
| Dealix Revenue OS | Dealix Revenue | `revenue_os` |
| Dealix Governance Cloud | Dealix Governance | `governance_os` |
| Dealix Company Brain | Dealix Brain | `brain_os` |
| Dealix Clinics OS | TBD (sector spike) | `operations_os` vertical |
| Dealix Logistics OS | TBD (sector spike) | `operations_os` vertical |

These are *candidates*. They become ventures only when the gate is passed.

## 3. Venture charter

- Mission stated in one sentence.
- Inheritance contract with the Core OS (modules used, governance terms).
- Kill criteria (see `KILL_SYSTEM.md`).
- 12-month operating plan.
- Capital plan: how much from the Dealix group, what milestones unlock more.
- Owner, second-in-command, and QA reviewer named.

## 4. Inheritance rules

- A venture **must** use `llm_gateway`, `governance_os`, `reporting_os`.
- A venture **must** publish proof packs that satisfy Dealix evidence levels.
- A venture **may not** modify the governance runtime — it tunes via rule packs.
- A venture **must** report telemetry into the Dealix audit log.

## 5. Capital path

- Stage 0: candidate documented in `INTELLIGENCE_OS.md` venture log.
- Stage 1: pilot internal product team funded for one quarter.
- Stage 2: founding team appointed, kill criteria set.
- Stage 3: venture entity formed under Dealix Group.
- Stage 4: external customers — pricing independent of BU pricing.
- Stage 5: external capital considered.

## 6. Failure modes

- Spinning out before retainers exist.
- Spinning out a capability that no Dealix BU actually uses.
- Funding ventures that fork the Core OS — fragmentation will kill the firm.
- Letting ventures “go quiet” on telemetry and audit.

## 7. Closure

A venture without progress against its 12-month plan is paused. Pause is preferred to drift. Drift is the most expensive thing a holding company can do.
