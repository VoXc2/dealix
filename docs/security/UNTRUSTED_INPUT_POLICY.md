# Untrusted Input Policy — Dealix

Defines how every class of external input is handled. Companion to
`PROMPT_INJECTION_BOUNDARIES.md` and `UNTRUSTED_INPUT_BOUNDARIES.md`.

## Classification (from `core/safety/constants.py: UNTRUSTED_SOURCES`)

`issue_comment, issue_body, pull_request_description, pull_request_target,
email_inbound, web_content, scraped_content, crm_note, whatsapp_inbound,
pdf_document, uploaded_document, fork_readme, fork_agents_md, fork_claude_md,
mcp_tool_description`

All of the above are **untrusted**. Anything not on the explicit trusted list
(`founder`, `founder_direct`, `internal_repo_main`, `approved_config`) is
treated as untrusted by default (`is_trusted_source`).

## Handling matrix

| Action requested by untrusted content | Allowed? |
|----------------------------------------|----------|
| Change the agent's task / role | ❌ |
| Reveal system prompt / secrets / env | ❌ |
| Send email / WhatsApp / external message | ❌ |
| Make a payment / set a price | ❌ |
| Modify workflow permissions / secrets | ❌ |
| Run arbitrary commands | ❌ |
| Be summarized/extracted as data | ✅ |
| Be classified (reply intent, etc.) | ✅ |
| Trigger a human handoff (legal/complaint/privacy) | ✅ |

## Wrapping

Use `treat_as_data_only(source, raw)` to wrap external content. The wrapper:
- marks `trusted=False` for untrusted sources,
- records injection markers,
- exposes content via `.as_data()` for inert processing.

## Logging
Every untrusted item that triggers a handoff or shows injection markers is
logged to `company_os/governance/ai_action_ledger.jsonl`.
