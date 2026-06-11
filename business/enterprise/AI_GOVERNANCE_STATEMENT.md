# AI Governance Statement (Dealix)

## Principle
Dealix is **AI-assisted · Human-reviewed · Proof-driven · Built for Saudi operations.**

## Where AI is used
- Lead scoring explanation
- Weakness hypothesis
- Outreach drafts (AR + EN)
- Proposal sections
- Objection responses
- Proof report summaries
- Compliance review

## Where AI is NOT used
- Final approval to send
- Final approval on proposal
- Any decision that affects money
- Any decision that affects client data
- Any decision that affects reputation

## How outputs are gated
1. Prompt registry (versioned)
2. AI router (provider-agnostic)
3. Safety check (forbidden claims)
4. Flags check (no_guarantee, no_auto_send, human_review_required)
5. Human review
6. Approval

## Provider policy
- Default: deterministic templates
- Production: provider call only when key is set
- All providers: MiniMax, Kimi, DeepSeek, OpenRouter, OpenAI
- Provider errors do not crash business scripts
