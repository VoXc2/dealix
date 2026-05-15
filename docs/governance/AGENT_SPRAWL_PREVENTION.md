# Agent Sprawl Prevention

## Sprawl risks

- duplicate agents  
- unused agents  
- agents with excessive data access  
- agents without owners  
- agents exceeding scope  
- hidden AI cost  
- inconsistent outputs  

## Controls

1. Central agent inventory  
2. Owner for every agent  
3. Autonomy classification  
4. Approved tools only  
5. Data access limits  
6. Monitoring  
7. Retirement process  
8. Cost review  

## Rule

No agent can exist outside the inventory.

---

## Monthly Agent Review

| Agent | Used? | QA | Cost | Incidents | Decision |
|---|---|---:|---:|---:|---|
| RevenueAgent | Yes | 91 | Low | 0 | Keep |
| OldDraftAgent | No | — | Low | 0 | Retire |

## Rule

Any agent that is unused, has no owner, or duplicates another agent must be retired or merged.
