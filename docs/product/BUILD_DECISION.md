# Build Decision (Product)

**Golden rule:** do not build because it is “cool.” Build because it **repeated**, **paid**, or **reduced risk/time** at scale.

## Gate: 3 of 5

Build is justified only if **at least three** are true:

1. Repeated in **3+** projects (or same pattern 3+ times in ops)
2. A **customer paid** for the workflow / outcome it supports
3. **Reduces delivery time** materially
4. **Reduces governance** or quality risk
5. **Improves output quality** measurably

## Score (for prioritization among candidates)

| معيار | Weight |
|--------|--------|
| Repetition | 25 |
| Revenue impact | 20 |
| Time saved | 20 |
| Risk reduction | 15 |
| Quality improvement | 15 |
| Build simplicity | 5 |

| Band | Action |
|------|--------|
| **80+** | Build now |
| **60–79** | Backlog |
| **Below 60** | Do not build |

Log candidates in [`../company/FEATURE_CANDIDATE_LOG.md`](../company/FEATURE_CANDIDATE_LOG.md). Full rubric also in [`FEATURE_PRIORITIZATION.md`](FEATURE_PRIORITIZATION.md).

## Examples

| Idea | Verdict |
|------|---------|
| **Import preview** (Lead Intelligence) | Repeats, saves time, reduces errors, cross-service → **Build now** |
| **Full WhatsApp API** sending | High compliance / spam risk, approval-heavy, not MVP-critical → **Do not build now** |

## Decision record

- Feature name:
- 3-of-5 check: (which three)
- Score:
- Owner:
- Risk:
- Next action:
