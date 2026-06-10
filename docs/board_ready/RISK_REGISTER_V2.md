# Risk Register v2 — Board

## R1–R12

- **R1** Agency trap  
- **R2** Premature SaaS  
- **R3** Governance incident  
- **R4** Weak proof  
- **R5** Founder bottleneck  
- **R6** Partner brand damage  
- **R7** Over-customization  
- **R8** Low margin projects  
- **R9** Model provider dependency  
- **R10** Saudi compliance / data trust gap  
- **R11** Agent over-permission  
- **R12** Proof claims without evidence  

## لكل risk

owner · likelihood · impact · early warning signal · control · response plan.

### مثال — R11

```text
Risk: Agent over-permission
Signal: agent يحتاج tools أكثر من هدفه
Control: Agent Card + Autonomy Level + Approval + Audit Log
Response: reduce permissions, add rule, update tests, review incident
```

**الكود:** `BoardRiskId` · `board_risk_entry_valid` — `board_ready_os/risk_register.py`

**صعود:** [`../institutional_scaling/RISK_REGISTER.md`](../institutional_scaling/RISK_REGISTER.md)
