# Terraform Baseline

Enterprise rule: لا يوجد provisioning يدوي للموارد الأساسية.

## Scope

- network primitives
- managed databases
- observability backends
- secrets references (بدون تخزين أسرار فعلية داخل repo)

## Guardrails

- versioned modules only
- remote state with locking
- plan/apply عبر CI فقط
