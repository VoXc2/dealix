# Client Data Risk Review — Findings (2026-06-03)

Scope: data received from engaged clients (CRM/pipeline samples for the Sprint).

| Risk | Control | Status |
|------|---------|--------|
| Client PII in AI prompts | redact + minimize; no public-tool pasting | ✅ policy |
| Over-retention | 90-day post-engagement deletion | ✅ policy |
| Cross-border transfer | KSA residency preference | 🟡 vendor confirm |
| Secret leakage in samples | detectors block secrets in text | ✅ |
| Unauthorized access | founder-only + encryption | ✅ policy |
| No DPA with subprocessors | vendor DPAs | 🟡 TBD (`vendors.jsonl`) |

**Verdict:** Acceptable for pilot engagements under the data-handling checklist.
Before scaling: confirm hosting residency + sign vendor DPAs.
