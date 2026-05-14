# Company Brain — Answer Schema (reference)

```json
{
  "question": "What is the refund policy?",
  "answer": "Based on the available policy document...",
  "sources": [
    {
      "source_id": "DOC-001",
      "title": "Refund Policy",
      "section": "2.1",
      "last_updated": "2026-05-01"
    }
  ],
  "confidence": "high",
  "insufficient_evidence": false,
  "escalation_required": false
}
```

When `sources` is empty or evidence is insufficient, set `insufficient_evidence: true` and avoid fabricated specifics.
