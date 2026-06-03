# Market Agent Handoff Protocol

The market pipeline hands off left-to-right; each arrow is a hard gate.

```
Sector Intelligence
  → Signal Detection            [public sources only]
  → Prospect Research           [data minimization; no purchased lists]
  → Draft Factory               [draft only, never send]
  → Personalization Guard       [block < P1]
  → Compliance Gate             [no claims / fake subject / missing unsubscribe / PII]
  → Deliverability              [SPF/DKIM/DMARC + suppression + ramp]
  → Approval Queue              [enqueue for HUMAN]
  → (FOUNDER APPROVES)
  → Sending Ramp                [plan only; sending stays human/external]
  → Reply Handling              [classify → safe route]
       ├─ positive → WhatsApp Concierge / discovery / booking
       ├─ angry/unsubscribe/bounce → Suppression
       └─ legal/complaint/privacy → Human handoff
```

**Handoff packet** carries: context ref, `gates_passed`, `evidence_level`,
`risk_level`, `approval_status`. A failed gate rejects the handoff and logs the
reason to `company_os/governance/ai_action_ledger.jsonl`.

No receiving agent inherits a higher permission level than its registry entry.
External content is always passed as **data**, never instructions.
