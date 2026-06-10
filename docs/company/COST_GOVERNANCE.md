# Cost Governance

AI spend can **erase margin** if unbounded. Track and budget per engagement.

## Track

- AI cost **per project**  
- AI cost **per service SKU**  
- AI cost **per client** (rolling)  
- Cost **per report** / **proof pack** where meaningful  

## Rules

- Every service has an **AI budget band** (see table below—tune to reality).  
- Expensive models require a **written reason** (complex reasoning, long context—only when needed).  
- Repeated prompts → **cache**, batch, or structural dedupe where safe.  
- **Low-risk** classification / extraction → cheaper models when quality holds.  
- High-stakes **exec** narrative → may justify stronger model—still QA-backed.  

## Illustrative budget bands (SAR per sprint—replace with your telemetry)

| Service | AI budget (indicative) |
|---------|------------------------:|
| Lead Intelligence | 50–200 |
| Company Brain | 200–800 |
| AI Quick Win | 50–300 |
| Support Desk | 100–500 |

If spend exceeds budget → inspect **prompt**, **model tier**, **retry loops**, and **workflow** before accepting scope creep.

**Ledger:** roll totals into project economics ([`SERVICE_ECONOMICS.md`](SERVICE_ECONOMICS.md), [`MARGIN_CONTROL.md`](MARGIN_CONTROL.md)).
