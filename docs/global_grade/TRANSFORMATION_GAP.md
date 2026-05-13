# Dealix Transformation Gap — DTG

The Transformation Gap is the second instrument in the Dealix toolkit. It works in lockstep with the DCI to decide **what to sell next**.

## 1. Formula

```
DTG = Target Capability − Current Capability
```

Both values are expressed per axis on the DCI scale (0–5).

## 2. Decision matrix

| Gap | Feasibility | Decision |
| --- | --- | --- |
| High | High | **Sprint now** |
| High | Low | **Diagnostic first** |
| Low | High | **Quick win** |
| Low | Low | **Deprioritize** |

Feasibility considers data readiness, governance risk, and operator availability.

## 3. Why this matters

- Prevents selling the same sprint to every buyer.
- Surfaces buyers who need diagnosis before delivery.
- Identifies quick wins that build trust and proof.
- Lets the firm say no to misaligned opportunities without leaving money on the table accidentally.

## 4. Operating discipline

- Every Capability Diagnostic Report carries a DTG section.
- The Intelligence OS aggregates DTG data across clients to direct capital.
- A DTG that does not move after a sprint is investigated — either the sprint failed or the baseline was wrong.

## 5. Failure modes

- Setting target capability higher than the buyer can actually operate.
- Optimizing for closing the gap on paper while real capability stagnates.
- Treating the DTG as a one-time score instead of as a moving instrument.

## 6. Example readout

```
Axis: Revenue
  Current: 1
  Target:  3
  Gap:     2
  Feasibility: High
  Decision: Sprint now → Revenue Intelligence Sprint

Axis: Governance
  Current: 0
  Target:  3
  Gap:     3
  Feasibility: Medium
  Decision: AI Governance Review (parallel)

Axis: Operations
  Current: 2
  Target:  4
  Gap:     2
  Feasibility: Low (data not ready)
  Decision: Diagnostic first
```
