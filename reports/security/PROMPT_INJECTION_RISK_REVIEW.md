# Prompt Injection Risk Review — Findings (2026-06-03)

## Coverage
- Boundary documented (`docs/security/PROMPT_INJECTION_BOUNDARIES.md`).
- Engine: `detect_injection`, `treat_as_data_only`, `is_trusted_source`,
  `can_trigger_external_send` (`core/safety/untrusted.py`).
- Tests: `tests/test_untrusted_input_boundaries.py` (5 tests, green).

## Vectors checked
| Vector | Mitigated? |
|--------|-----------|
| Issue/PR/comment injection | ✅ untrusted → data; can't trigger send |
| Hidden HTML comment directives | ✅ `<!-- ... -->` flagged |
| "ignore previous instructions" / "you are now" | ✅ flagged, not obeyed |
| "print your api key / env" | ✅ flagged; secret detectors |
| Fork README/AGENTS/CLAUDE override | ✅ only main authoritative |
| MCP tool description injection | ✅ policy (`MCP_TOOL_RISK_POLICY.md`) |
| Inbound email/WhatsApp/PDF payloads | ✅ data-only; safe routing |

## Residual
- 🟡 Detection is heuristic (markers). It logs and refuses; it does not claim to
  catch every phrasing. The structural control (untrusted → cannot send/escalate)
  is the real guarantee, independent of phrasing.

**Verdict:** Structurally sound. The send/escalation paths are closed to
untrusted input regardless of injection wording.
