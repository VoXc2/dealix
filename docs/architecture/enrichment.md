# Enrichment chain

Wathq is tried first when a Saudi VAT/CR is available — it's the
authoritative source and short-circuits the slower paid vendors.

```mermaid
flowchart LR
    L[(Lead with company name<br/>+ domain or email)]
    L --> Q{Has VAT or CR?}
    Q -- yes --> W[Wathq lookup<br/>dealix/enrichment/wathq_client.py]
    W -- matched --> R[(Enrichment payload<br/>confidence=0.95)]
    W -- miss --> A
    Q -- no --> A[Apollo lookup<br/>dealix/enrichment/apollo_client.py]
    A -- matched --> R2[(Enrichment payload<br/>confidence=0.85)]
    A -- miss --> C[Clearbit lookup<br/>dealix/enrichment/clearbit_client.py]
    C -- matched --> R3[(Enrichment payload<br/>confidence=0.78)]
    C -- miss --> H[Heuristic only<br/>auto_client_acquisition/pipelines/scoring.py]
    R & R2 & R3 & H --> S[LeadScoreRecord]
```

Each client short-circuits when its env key is unset; the orchestrator
in `dealix/enrichment/__init__.enrich()` walks the chain top-to-bottom
and returns the first confident match.
