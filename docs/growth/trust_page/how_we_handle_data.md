# How Dealix Handles Data

- We work from **explicitly scoped** data sources the client authorizes.  
- We apply **PDPL-aware** handling labels and minimize retention of personal data.  
- **PII** is redacted or restricted in reports and outward-facing outputs where required.  
- Access follows **permission mirroring**: AI and tools only see what the responsible user may see.  
- We maintain **audit-friendly** records of what was used to produce client-facing outputs (within agreed policy).  

For operational detail, see governance docs under `docs/governance/` (e.g. PDPL, PII, retention, audit).
