# Risk Register v2

Extends the institutional register with R11 and R12.

## 1. The twelve

- R1 Agency trap
- R2 Premature SaaS
- R3 Governance incident
- R4 Weak proof
- R5 Founder bottleneck
- R6 Partner brand damage
- R7 Over-customization
- R8 Low-margin projects
- R9 Model provider dependency
- R10 Saudi compliance / data trust gap
- R11 Agent over-permission
- R12 Proof claims without evidence

## 2. Each risk row

```
owner | likelihood | impact | early-warning signal | control | response plan
```

## 3. Worked example

```
Risk: Agent over-permission
Signal: agent needs more tools than purpose
Control: Agent Card + Autonomy Level + Approval Required + Audit Log
Response: reduce permissions, add rule, update tests, review incident
```

## 4. Typed surface

`institutional_scaling_os.risk_register.DOCTRINE_RISKS` and `board_ready_os.risk_register_v2` (this module is the same register surfaced under the board-ready namespace; see implementation).

## 5. The principle

> The board reads the same risk register every month; otherwise it is decorative.
