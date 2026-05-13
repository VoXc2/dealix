# Productization Command

Do not build a feature until repetition has proven it. Productization Command is the gate that decides when something becomes a product.

## 1. The gate

A capability is allowed to graduate from manual to productized only when **all** are true:

- `manual_step_repeated >= 3`
- `time_cost >= 2 hours per project`
- `linked_to_paid_offer == true`
- `reduces_risk_or_improves_margin == true`
- `testable == true`
- `reusable == true`

## 2. The path

```
Manual
→ Template
→ Script
→ Internal Tool
→ Client Feature
→ SaaS Module
```

Each step is a documented promotion in the Capital Ledger.

## 3. Why each criterion exists

- **Repetition** — prevents speculative builds.
- **Time cost** — ensures the asset earns its maintenance bill.
- **Paid linkage** — ensures the build is tied to revenue, not vanity.
- **Risk/margin** — ensures alignment with the firm’s economic engine.
- **Testable** — prevents brittle automations.
- **Reusable** — prevents single-client features.

## 4. Operating discipline

- The productization ledger captures each promotion with its evidence.
- A failed promotion is allowed and recorded — assets can fall back a step.
- Major promotions (Internal Tool → Client Feature) require an Office of the Standard sign-off.
- The Intelligence OS proposes promotions automatically from reuse-count signals.

## 5. Anti-patterns

- “We have time this quarter” builds.
- Productizing one operator’s personal toolset without the rest of the firm needing it.
- Skipping the testable criterion for speed.
- Treating a single client’s feature request as a SaaS signal.

## 6. The principle

> No repeated demand, no product feature. No proof of value, no promotion to a higher step.
