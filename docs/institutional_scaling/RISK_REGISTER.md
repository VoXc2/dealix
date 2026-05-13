# Institutional Risk Register

Twelve canonical doctrine risks. Each has owner, likelihood, impact, early-warning signal, control, response plan.

## 1. The twelve risks

- R1 Agency trap
- R2 Premature SaaS
- R3 Governance incident
- R4 Weak proof
- R5 Founder bottleneck
- R6 Partner brand damage
- R7 Over-customization
- R8 Low-margin projects
- R9 Model provider dependency
- R10 Saudi compliance gap
- R11 Agent over-permission
- R12 Proof claims without evidence

## 2. Worked example

```
Risk: Agency trap
Signal: every project starts from scratch
Control: Service Catalog + Productization Ledger + Capital Review
Response: refuse custom scope or convert to productized sprint
```

## 3. Typed surface

`institutional_scaling_os.risk_register.DOCTRINE_RISKS` + `RiskEntry` dataclass.

## 4. Operating discipline

- Review quarterly.
- Promote a risk to monthly review when its signal fires.
- Retire a risk only when its control is fully operational.

## 5. The principle

> A risk without an owner is a risk that has already happened.
