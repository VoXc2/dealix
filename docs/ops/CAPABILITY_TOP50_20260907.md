# Dealix Capability Top-50 — 2026-09-07

## Mission
Expand the existing Dealix Capability Radar with a curated, evidence-oriented Top-50 of open-source tools/libraries that can improve Production Trust, reliability, AI evaluation, document/data handling, public-signal research, and founder leverage **without creating parallel company architecture**.

## Live reconciliation
- #1529 Production Trust is merged.
- Latest `main` observed while reconciling this PR: `2dedf0a7427d7894379751198cb27b999cdc6812`.
- The runner never pins that SHA; every execution fetches current `origin/main`.
- Live state always overrides this document.

## Admission law
- `REJECT_DUPLICATE_BY_DEFAULT`.
- At most **one active OSS benchmark** at a time.
- No candidate may become a second Company Brain, Opportunity Graph, Approval Center, Proof Ledger, CRM truth store, scheduler, model router, observability truth store, or permanent agent fleet.
- External research is not relationship/consent/buyer intent.
- Scanner/eval/telemetry output is evidence only, never Verified Cash or Customer Proof.
- Missing tools are **not auto-installed** by the admission runner.
- All material L5 effects remain disabled: merge, Production deploy, DNS, Production DB/schema, secrets/identity, external customer send, public publish, spend/payment/refund, binding legal/commercial commitments, live voice activation.

## Files
- `config/oss/capability_top50_v1.tsv` — the curated Top-50 registry.
- `scripts/ops/run_capability_top50_admission_v1.sh` — live reconciliation + audit/pilot runner.

## How to run
```bash
bash -n scripts/ops/run_capability_top50_admission_v1.sh
bash scripts/ops/run_capability_top50_admission_v1.sh audit
```

Optional bounded version probes for tools that are **already installed**:
```bash
bash scripts/ops/run_capability_top50_admission_v1.sh pilot
```

`audit` reconciles current `origin/main`, validates that the registry has exactly 50 unique candidates, checks public GitHub source reachability, scans current Dealix source for likely duplication/reference hits, records local tool availability, and writes JSON/TSV/SHA256 receipts.

`pilot` adds only bounded `--version` probes for tools already available on the host. It still does not install missing tools.

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
