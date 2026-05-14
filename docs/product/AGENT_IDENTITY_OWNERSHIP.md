# Agent Identity & Ownership

Every agent must have:

## Identity

- agent_id  
- name  
- version  
- owner  
- workspace  
- service  
- capability  
- autonomy level  

## Permissions

- data access  
- tool access  
- action permissions  
- approval requirements  

## Lifecycle

- created  
- approved  
- active  
- monitored  
- deprecated  
- retired  

## Audit

- every run is logged  
- every blocked action is logged  
- every approval is logged  

---

## Agent Identity Table

| Agent | Owner | Capability | Autonomy | Data Access | Action Access | Status |
|---|---|---|---:|---|---|---|
| RevenueAgent | Delivery | Revenue | 2 | lead datasets | draft/recommend | Active |
| OutreachAgent | Delivery | Revenue | 2 | approved accounts | draft only | Active |
| ComplianceGuardAgent | Governance | Governance | 3 | metadata | block/escalate | Active |

## Rules

- Any agent without an owner is forbidden.  
- Any agent without permissions is forbidden.  
- Any agent without a lifecycle state is forbidden.  

See also: [`AI_AGENT_INVENTORY.md`](AI_AGENT_INVENTORY.md), [`AGENT_LIFECYCLE_MANAGEMENT.md`](AGENT_LIFECYCLE_MANAGEMENT.md).
