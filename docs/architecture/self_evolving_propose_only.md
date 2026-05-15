# Self-Evolving (Propose-Only)

Self-evolving flow is explicitly gated:

1. Proposal is created in `proposed` state.
2. Apply request creates approval ticket.
3. Proposal cannot apply while unapproved.
4. Only approved proposals can transition to `applied`.

This keeps system evolution human-governed and auditable.
