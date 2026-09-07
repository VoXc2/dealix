# Dealix Capability Top-50 — 2026-09-07

## Mission
Expand the existing Dealix Capability Radar with a curated, evidence-oriented Top-50 of open-source tools/libraries that can improve Production Trust, reliability, AI evaluation, document/data handling, public-signal research, and founder leverage **without creating parallel company architecture**.

## Live base used for this expansion
- `main`: `8443836729cfa8eff79c0f4eb2c68bbacd4f17d8`
- #1529 Production Trust was merged before this expansion.
- The capability registry remains subordinate to `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`.

## Admission law
- `REJECT_DUPLICATE_BY_DEFAULT`.
- At most **one active OSS benchmark** at a time.
- No candidate may become a second Company Brain, Opportunity Graph, Approval Center, Proof Ledger, CRM truth store, scheduler, model router, observability truth store, or permanent agent fleet.
- External research is not relationship/consent/buyer intent.
- Scanner/eval/telemetry output is evidence only, never Verified Cash or Customer Proof.
- Missing tools are **not auto-installed** by the admission runner.
- All material L5 effects remain disabled: merge, Production deploy, DNS, Production DB/schema, secrets/identity, external customer send, public publish, spend/payment/refund, binding legal/commercial commitments, live voice activation.

## How to run
```bash
bash scripts/ops/run_capability_top50_admission_v1.sh audit
bash scripts/ops/run_capability_top50_admission_v1.sh pilot
```

`audit` reconciles current `origin/main`, checks GitHub source reachability, scans the current repo for likely duplication, records local tool availability, and creates durable receipts.

`pilot` adds bounded `--version` probes only for tools already present on the host. It still does not install missing tools.

## Priority interpretation
The Top-50 is not a shopping list. Decisions are intentionally mixed:
- `ADOPT_NOW*`: low-duplication, high-leverage capabilities that fit an existing owner.
- `PILOT_ISOLATED`: benchmark only in credential-scrubbed/non-production context.
- `DEFER*`: useful later, but not worth current complexity or duplicates an existing capability.
- `REJECT_DUPLICATE_DEFAULT`: do not admit without a measured gap and replacement/migration case.

## Highest-value immediate cluster
1. OSV-Scanner + Syft evidence normalization.
2. actionlint + zizmor for GitHub Actions contract/security checks.
3. Hurl + Playwright + Schemathesis for deterministic Web/API/front-door acceptance.
4. Ruff + uv + Hypothesis for faster local quality/verification.
5. Presidio + Docling for privacy-safe document-to-evidence preparation.
6. OpenTelemetry + Promptfoo/Phoenix only as bounded observability/eval layers.
7. changedetection.io/Crawl4AI only for public/official research signals, never automated relationship creation.

## Explicit non-goals
- Do not install all 50 in Production.
- Do not add another workflow engine because it is popular.
- Do not add another vector database as a parallel Company Brain.
- Do not add another model gateway unless the existing Dealix router has a measured gap.
- Do not use browser/crawler tools for LinkedIn automation, cold WhatsApp, consent bypass, or platform-control circumvention.

## Files
- `scripts/ops/run_capability_top50_admission_v1.sh`
