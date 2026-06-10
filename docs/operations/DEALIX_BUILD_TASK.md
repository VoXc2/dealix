# Dealix Full Local Build Task

You are the lead platform engineer for Dealix.

Build the full platform files locally inside this repository.

## Current state

Repo root:
C:\Users\samim\dealix

Known folders may include:
- dealix-builder-api
- dealix-v2
- scripts
- prompts
- docs
- .github/workflows

The user does not want long broken pasted scripts anymore.
The AI coding agent must directly edit and create files.

## Main goal

Create a working API-first Dealix platform skeleton.

Dealix is an Arabic-first AI Operations company for Saudi/MENA businesses.

Strategic path:

Sprint → Proof → Retainer → Module → Platform

## Allowed edit scope

You may edit only:

- dealix-builder-api
- dealix-v2
- scripts
- prompts
- docs
- .github/workflows
- README.md
- package files
- config files required for this platform

Do not edit unrelated legacy folders.

## Required provider support

Support three provider modes:

1. openrouter
2. openai
3. ollama

Use environment variables:

AI_PROVIDER=openrouter
AI_MODEL=openrouter/auto
AI_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=...

For Ollama local:

AI_PROVIDER=ollama
AI_MODEL=qwen2.5-coder:14b
AI_BASE_URL=http://127.0.0.1:11434/v1

Never hardcode API keys.

## Required API package

Create or upgrade:

dealix-builder-api

Use Node.js ESM.

Dependencies:
- express
- zod
- dotenv
- openai
- cors
- helmet

## Required CLI commands

Create:

scripts/dealix-builder.ps1
scripts/dealix-builder.sh

CLI must support:

- doctor
- plan "goal"
- founder-brief
- governance-check "text"
- governance-ai "text"
- score "opportunity text"
- client-pack --client "..." --sector "..." --problem "..." --service "..."
- campaign --segment "..." --pain "..." --offer "..."
- deal-room --client "..." --problem "..." --offer "..." --target "..." --floor "..."
- value --client "..." --service "..." --metric "..." --result "..."
- monthly-review
- partner-kit --partner "..." --type "..."
- proposal --client "..." --service "..." --problem "..."
- proof-pack --client "..." --service "..." --result "..."

Commands that must work without API key:
- doctor
- governance-check
- score
- client-pack
- value

Commands that may require AI key:
- plan
- founder-brief
- governance-ai
- campaign
- deal-room
- monthly-review
- partner-kit
- proposal
- proof-pack

## Required API endpoints

Create:

GET /builder/health
POST /builder/plan
POST /builder/founder-brief
POST /builder/governance-check
POST /builder/score-opportunity
POST /builder/campaign
POST /builder/deal-room
POST /builder/client-pack
POST /builder/ledger/value
POST /builder/monthly-review
POST /builder/partner-kit
POST /builder/proposal
POST /builder/proof-pack

## Required agents

Create:

- provider-client
- planner
- founder
- governance
- scorer
- growth
- dealroom
- client-pack
- ledger
- proposal
- proof-pack
- partner-kit
- monthly-review
- reporter

## Required safety

- Never write outside dealix-v2 from writer tools.
- Block path traversal.
- Never expose API keys in logs.
- Never create spam automation.
- Never promise guaranteed sales.
- External sending requires human approval.
- WhatsApp automation is restricted and requires compliance review.
- Personal data triggers PII review.
- Scraping triggers source/permission review.

## Required dealix-v2 files

Create or repair:

dealix-v2/
  README.md
  ledgers/
    VALUE_LEDGER.md
    CAPITAL_LEDGER.md
    PIPELINE_LEDGER.md
    GOVERNANCE_LEDGER.md
    RELATIONSHIP_LEDGER.md
    PARTNER_LEDGER.md
  clients/
    _template/
      CLIENT_PROFILE.md
      CAPABILITY_SCORECARD.md
      DEAL_ROOM.md
      EXPANSION_MAP.md
      PROOF_PACK_TEMPLATE.md
  services/
    lead_intelligence/offer.md
    ai_quick_win/offer.md
    company_brain/offer.md
    data_readiness/offer.md
    ai_governance/offer.md
    executive_reporting/offer.md
  growth/
    CONTENT_ENGINE.md
    CAMPAIGN_SYSTEM.md
  money/
    REVENUE_PORTFOLIO.md
    PRICING_RULES.md
  governance/
    RUNTIME_GOVERNANCE.md
    HUMAN_APPROVAL_MATRIX.md
  partners/
    PARTNER_STRATEGY.md
    WHITE_LABEL_KIT.md
  product/
    PLATFORM_PATH.md
    MODULE_BACKLOG.md
  founder/
    FOUNDER_OPERATING_CADENCE.md
    WEEKLY_REVIEW.md

## Required tests

Add Node tests:

- local governance flags guaranteed claims
- local governance flags WhatsApp
- local governance blocks autonomous external action
- opportunity scorer returns score and decision
- client-pack creates files inside dealix-v2
- provider client initializes without printing keys
- path traversal is blocked

## Required docs

Create:

- DEALIX_LOCAL_BUILD_GUIDE.md
- DEALIX_OPENROUTER_SETUP.md
- DEALIX_OLLAMA_SETUP.md
- DEALIX_API_REFERENCE.md
- DEALIX_NEXT_COMMANDS.md

## Required scripts

Create:

scripts/dealix-builder.ps1
scripts/dealix-builder.sh
scripts/dealix-builder-dev.ps1
scripts/dealix-builder-dev.sh
scripts/dealix-api-test.ps1
scripts/dealix-api-test.sh
scripts/dealix-local-doctor.ps1
scripts/dealix-run-aider-openrouter.ps1
scripts/dealix-run-aider-ollama.ps1

## Required CI

Create:

.github/workflows/dealix-ci.yml

CI:
- checkout
- setup node 20
- install
- run tests
- run CLI doctor
- run local governance-check
- run score command

## Validation commands

Run:

cd dealix-builder-api
npm install
npm test
node src/cli.js doctor
node src/cli.js governance-check "we guarantee sales and send WhatsApp automatically"
node src/cli.js score "paid B2B agency partner with monthly retainer and CRM data"
node src/cli.js client-pack --client "Demo Client" --sector "B2B Services" --problem "messy leads" --service "lead-intelligence"

Then return:
- changed files
- tests passed
- exact commands to run server
- exact commands to test API
- exact commands to commit

Important:
Make real file edits.
Do not only explain.
Replace broken files cleanly.
Do not ask questions.
If something is missing, make a reasonable default and continue.
