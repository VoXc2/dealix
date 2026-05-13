# Control Plane

The Control Plane is the explicit architectural layer that exposes Dealix’s controls as a product surface.

## 1. Components

```
Dealix Control Plane
├─ Data Control
├─ AI Control
├─ Agent Control
├─ Workflow Control
├─ Claim Control
├─ Channel Control
├─ Audit Control
├─ Proof Control
└─ Capital Control
```

## 2. Why a plane, not a checklist

A plane is *alive*: it answers questions, enforces decisions at runtime, and exposes telemetry. A checklist is paper that ages.

## 3. What enterprise buyers actually want

Larger buyers do not buy AI outputs. They buy:

- Visibility — where does AI run, on what data, for what purpose?
- Accountability — who owns the action, the decision, the outcome?
- Auditability — can we reconstruct what happened, and prove it?
- Approval — can a human intervene before external action?
- Risk reduction — are unsafe actions blocked at runtime?
- Proof — what is the evidence of value?

The Control Plane is what makes those six demands satisfiable.

## 4. Why this is the right time

Research on agent safety has begun to address how AI agents may collect or expose sensitive data during execution, and proposes real-time monitoring of agents’ data practices against privacy policies. The implication is direct: Dealix must sell **runtime governance as a real product**, not as an attached document.

## 5. Operating discipline

- Every Dealix offer references the Control Plane components it exercises.
- A new component is added only after repeated demand.
- The plane’s vocabulary is stable across BUs.
- Telemetry from the plane feeds the Command Center.

## 6. Failure modes

- A “plane” that exists in slides but not in code.
- Components added by individual BUs without registration.
- Telemetry that never reaches a decision surface.
- Approval flows that exist but are bypassed in practice.

## 7. The principle

> The Control Plane is the product Dealix sells, even when the buyer thinks they’re buying a sprint.
