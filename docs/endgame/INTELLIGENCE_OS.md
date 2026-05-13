# Intelligence OS

The Intelligence OS is the **brain of the firm**. It reads the operating signals across Dealix and decides what to scale, build, pilot, hold, kill, productize, raise prices on, or spin out as a venture.

## 1. Inputs

- Events from every OS (`core_os`, `governance_os`, `revenue_os`, `brain_os`, `operations_os`, `reporting_os`).
- The Capital Ledger.
- Business metrics (margin, retention, NPS, time-to-proof).
- Proof Packs.
- Client health signals.
- Governance events (blocks, escalations, drift).
- Sales notes and lost-deal reasons.
- Delivery results and QA scores.
- Partner signals.

## 2. Decisions

The decision engine emits structured recommendations:

- `SCALE` — invest more in the capability.
- `BUILD` — author a new module.
- `PILOT` — limited test under explicit kill criteria.
- `HOLD` — keep, do not invest.
- `KILL` — see `KILL_SYSTEM.md`.
- `RAISE_PRICE` — price the proof.
- `PRODUCTIZE` — promote a capital asset into a module.
- `OFFER_RETAINER` — convert proof into recurring revenue.
- `CREATE_BUSINESS_UNIT` — see `BUSINESS_UNITS.md`.
- `CREATE_VENTURE_CANDIDATE` — see `VENTURE_FACTORY.md`.

## 3. Example decisions

**Productization signal**

```
Manual proof writing repeated 5 times
+ takes 3 hours/project
+ used in every sprint
→ BUILD proof_pack.py
```

**Scaling signal**

```
Revenue Intelligence Sprint:
  win rate high
  proof score high
  2 retainers
  repeatable delivery
→ SCALE + RAISE_PRICE + CREATE_BUSINESS_UNIT (Dealix Revenue)
```

**Kill signal**

```
Capability:
  low margin
  high scope creep
  weak proof
  no retainer path
→ KILL
```

## 4. Modules

`auto_client_acquisition/intelligence_os/`

- `metrics_engine.py` — aggregate metrics from every OS.
- `decision_engine.py` — apply rules and produce structured decisions.
- `capital_allocator.py` — propose where time, money, and operator hours go next.
- `venture_signal.py` — surface venture candidates with maturity scores.

## 5. Cadence

- **Weekly:** delivery and governance metrics review.
- **Bi-weekly:** Capability Diagnostic conversion review.
- **Monthly:** Capital Ledger and Proof Library review.
- **Quarterly:** business unit and venture review.

## 6. Output: the decision log

The Intelligence OS writes every decision into an immutable log, with the inputs that justified it. Reversals are allowed and recorded; secret pivots are not.

## 7. Failure modes

- The OS recommends, but no one is accountable for executing.
- Decisions are made outside the OS in chat threads — the log goes stale.
- Metrics include only revenue; governance, proof, and capital are ignored.
- The capital allocator is treated as advisory, not as the actual budget.

## 8. Why this is non-negotiable

Without the Intelligence OS, Dealix becomes a labor shop that happens to use AI. With it, Dealix becomes a firm that **compounds**.
