# Dealix Capability Index — DCI

The DCI is Dealix’s official measure of an organization’s AI operating capability. It is the engine behind the Capability Diagnostic and the language Dealix uses with senior buyers.

## 1. Axes

- **Revenue**
- **Customer**
- **Operations**
- **Knowledge**
- **Data**
- **Governance**
- **Reporting**

## 2. Maturity levels (0–5)

| Level | Meaning |
| --- | --- |
| 0 | Absent — nothing exists |
| 1 | Manual — humans do it ad hoc |
| 2 | Structured — process documented, but no AI |
| 3 | AI-Assisted — AI used inside a workflow with humans |
| 4 | Governed Workflow — AI under runtime governance and approval |
| 5 | Optimized OS — operated as a product with proof and capital |

## 3. How the score is used

Instead of selling “AI services,” Dealix says:

> We measure your operating capability, identify the transformation gap, and start with the highest-value, provable opportunity.

Every Diagnostic Report shows:

- The current score per axis.
- The composite score.
- The transformation gap (see `TRANSFORMATION_GAP.md`).
- The recommended sprint and retainer path.

## 4. Example

```
Revenue Capability: 1/5
Data Capability: 2/5
Governance Capability: 0/5
Recommended: Revenue Intelligence Sprint + AI Governance Review
```

## 5. Calibration

- Each axis has 5–8 yes/no calibration questions per level.
- A level is achieved when ≥ 80% of its questions are confirmed.
- Calibration questions live in `capability_index.py`.

## 6. Operating discipline

- The DCI is owned by the Office of the Standard.
- Scores are recalibrated when the Dealix Method version changes.
- Cross-tenant DCI data is aggregated only with consent and only for benchmarks.
- The DCI is a **diagnostic instrument**, not a marketing badge.

## 7. Failure modes

- Inflating scores to win the next sprint — undermines later retainer pricing.
- Using the DCI as a sales gimmick rather than a diagnostic instrument.
- Allowing axes to drift in definition across BUs.
- Reporting a composite score without showing the per-axis decomposition.
