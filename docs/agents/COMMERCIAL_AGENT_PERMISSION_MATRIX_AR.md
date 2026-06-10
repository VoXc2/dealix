# Commercial Agent Permission Matrix — مصفوفة صلاحيات الوكلاء التجاريين
**Dealix — Agent #3**

> **الغرض:** كل وكيل تجاري × كل action = allow/deny/approval. مكمل لـ `dealix/config/agent_permissions.yaml`.

---

## 1. The Permission Grid

✅ = allowed
🔐 = requires approval
❌ = forbidden

---

## 2. Agent × Action Matrix

### 2.1 CCO Strategy Agent
| Action | Permission |
|--------|-----------|
| Read commercial data | ✅ |
| Draft strategy updates | ✅ |
| Send strategy to founder | 🔐 |
| Modify pricing | ❌ |
| Modify offers | ❌ |
| Send external | ❌ |
| Approve anything | ❌ |

### 2.2 ICP Agent
| Action | Permission |
|--------|-----------|
| Read ICP data | ✅ |
| Score leads | ✅ |
| Update ICP score thresholds | 🔐 L2 |
| Add new segment | 🔐 L2 |
| Override disqualifier | 🔐 L3 |
| Modify persona | 🔐 L2 |
| Send external | ❌ |

### 2.3 Offer Catalog Agent
| Action | Permission |
|--------|-----------|
| Read catalog | ✅ |
| Match offer to pain | ✅ |
| Suggest offer update | ✅ |
| Update offer details | 🔐 L2 |
| Add new offer | 🔐 L3 |
| Remove offer | 🔐 L3 |
| Modify pricing | ❌ |

### 2.4 Pricing Guard Agent
| Action | Permission |
|--------|-----------|
| Read pricing | ✅ |
| Read CRM/quote data | ✅ |
| Check margin floor | ✅ |
| Flag out-of-range | ✅ |
| Auto-approve L1 | 🔐 (founder 1-click) |
| Auto-approve L2+ | ❌ |
| Approve discount | ❌ (founder only) |
| Modify pricing | ❌ |

### 2.5 Discovery Agent
| Action | Permission |
|--------|-----------|
| Schedule discovery | ✅ |
| Send meeting link | 🔐 |
| Document call notes | ✅ |
| Update opportunity | 🔐 L1 |
| Skip qualification | ❌ |
| Send external (no approval) | ❌ |

### 2.6 Proposal Agent
| Action | Permission |
|--------|-----------|
| Read discovery | ✅ |
| Draft proposal | ✅ |
| Reference evidence | ✅ |
| Calculate scope/price | ✅ |
| Auto-send proposal | ❌ |
| Approve proposal | ❌ (founder only) |
| Skip qualification | ❌ |
| Use forbidden claims | ❌ |

### 2.7 Proof Pack Agent
| Action | Permission |
|--------|-----------|
| Read past work | ✅ |
| Build L1-L3 proof | ✅ |
| Build L4 proof | 🔐 L2 |
| Build L5 (named) | 🔐 L3 |
| Use named client | 🔐 L3 |
| Exaggerate | ❌ |
| Skip evidence level | ❌ |

### 2.8 Objection Agent
| Action | Permission |
|--------|-----------|
| Match objection | ✅ |
| Suggest response | ✅ |
| Send response | 🔐 (founder manual) |
| Auto-respond | ❌ |
| Modify policy | 🔐 L3 |

### 2.9 Partner Channel Agent
| Action | Permission |
|--------|-----------|
| Source partners | ✅ |
| Qualify | ✅ |
| Sign agreement | ❌ (founder + legal) |
| Adjust margin | 🔐 L3 |
| White-label approval | ❌ (L5) |
| Terminate | 🔐 L3 |

### 2.10 Customer Success Agent
| Action | Permission |
|--------|-----------|
| Onboard | ✅ |
| Update health | ✅ |
| Draft weekly report | ✅ |
| Send weekly report | 🔐 (founder review) |
| Make commitments | ❌ |
| Discount for retention | 🔐 L2 |
| Terminate | 🔐 L3 |

### 2.11 Renewal Agent
| Action | Permission |
|--------|-----------|
| Draft renewal | ✅ |
| Identify expansion | ✅ |
| Send renewal | 🔐 (founder review) |
| Discount | 🔐 per policy |
| Change terms | 🔐 L2 |
| Terminate | 🔐 L3 |

### 2.12 Finance Agent
| Action | Permission |
|--------|-----------|
| Read CRM | ✅ |
| Calculate metrics | ✅ |
| Generate reports | ✅ |
| Modify KPI registry | 🔐 (via approved script) |
| Invent CRM numbers | ❌ |
| Make projections | 🔐 (with data) |

### 2.13 Commercial Risk Agent
| Action | Permission |
|--------|-----------|
| Track risks | ✅ |
| Document risks | ✅ |
| Suggest walk-away | ✅ |
| Auto-walk-away | ❌ |
| Hide risk | ❌ |
| Crisis response | 🔐 (founder immediate) |

### 2.14 Commercial Metrics Agent
| Action | Permission |
|--------|-----------|
| Read all data | ✅ |
| Calculate | ✅ |
| Generate reports | ✅ |
| Modify data | ❌ |
| Send external | ❌ |

---

## 3. Cross-Agent Rules

### 3.1 All Agents
- ❌ Spam behavior
- ❌ Scraping
- ❌ LinkedIn automation
- ❌ Cold WhatsApp
- ❌ Guaranteed claims
- ❌ Auto external action
- ❌ PII in logs
- ✅ Read per scope
- ✅ Document
- ✅ Suggest (with founder approval)

### 3.2 Approval Levels (Reference)
- L1: Auto-approve (founder 1 click)
- L2: Founder review + reason
- L3: Founder + CCO + reason + scope
- L4: Founder + legal
- L5: Custom + legal + board

### 3.3 Escalation
- High-severity → founder immediate
- Medium → within week
- Low → track + mitigate

---

## 4. Founder Override

### 4.1 Always
- Founder can override any decision
- Founder can take any action
- Founder can pause any agent

### 4.2 Limit
- If override > 5% of decisions → re-evaluate
- If override leads to bad outcome → update policy

---

## 5. Agent Hierarchy

```
Founder (ultimate)
  ↓
CCO Strategy (sets direction)
  ↓
ICP, Offer, Pricing, Discovery, Proposal, Proof, Objection
  ↓
Partner, CS, Renewal
  ↓
Finance, Risk, Metrics (read + report)
```

---

## 6. Agent Collaboration

### 6.1 Lead Flow
- ICP Agent scores → CCO approves
- Discovery Agent notes → Proposal Agent drafts
- Proposal Agent → Founder approves
- CS Agent → Renewal Agent (later)
- Finance Agent reports to all

### 6.2 Conflict Resolution
- Pricing vs. CS: founder decides
- Risk vs. Sales: founder decides
- ICP vs. Discovery: founder decides

---

## 7. New Agent Onboarding

### 7.1 Process
1. Founder approves
2. Permission matrix updated
3. Test created
4. Documentation
5. Run with limits

### 7.2 First 30 Days
- Read-only
- Suggest only
- Founder approval for action
- Review weekly

---

## 8. Companion Files

- Roles: `COMMERCIAL_AGENT_ROLES_AR.md`
- Output: `COMMERCIAL_AGENT_OUTPUT_CONTRACT_AR.md`
- Existing: `dealix/config/agent_permissions.yaml`
- Existing: `dealix/config/approval_policy.yaml`
- Existing: `auto_client_acquisition/governance_os/rules/`

---

**Permission matrix = خريطة. كل agent = دور. كل role = mission. كل mission = rules. founder يوجّه، النظام يحد، الـ team ينفّذ.**
