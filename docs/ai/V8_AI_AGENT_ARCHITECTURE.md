# V8 AI Agent Architecture (Dealix)

## Goals
- Provider-agnostic
- Demo mode works without keys
- Deterministic fallback for all tasks
- Every output is a draft with review_status

## Components
- `scripts/lib/ai_router.py` — central router
- `scripts/lib/ai_safety.py` — output + flags check
- `business/ai/prompts/*.md` — versioned prompt files
- `business/ai/evals/*.json` — eval cases
- `scripts/run_ai_evals.py` — eval runner

## Tasks (10)
1. lead_scoring_explanation
2. weakness_hypothesis
3. outreach_draft_ar
4. outreach_draft_en
5. proposal_section_ar
6. proposal_section_en
7. objection_response_ar
8. objection_response_en
9. proof_report_summary
10. compliance_review

## Modes
- demo: deterministic templates
- production: provider call (when wired) → fallback to deterministic on error

## Safety Flags (mandatory)
- no_guarantee
- no_auto_send
- human_review_required
