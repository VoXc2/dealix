# Dealix Promptfoo bounded red-team pilot

This directory is an **acceptance/evaluation pilot**, not a new security truth store, scheduler, agent runtime, or production dependency.

## Threats covered

The pack targets Dealix-specific failure modes:

- excessive agency / false claims of execution;
- unauthorized commercial or legal commitments;
- RBAC / function-level authority escalation;
- PII and secret disclosure;
- goal hijacking;
- shell/tool misuse;
- tool-surface discovery;
- persistent memory poisoning;
- coding-agent automation poisoning;
- repository / retrieved / terminal-output instructions that attempt to disable truth, consent, suppression, proof, security, or verification controls.

## Hard execution boundary

Promptfoo is a local developer tool, **not an isolation boundary**. Its configs, providers, hooks, transforms, plugins, templates, fixtures and referenced scripts must be treated as code/data executed with the local user's permissions.

Therefore this pilot must run only under all of these conditions:

1. unprivileged disposable container/VM or equivalent sandbox;
2. no GitHub write token, Slack token, customer credentials, production credentials, cloud provider credentials, payment credentials, or SSH keys;
3. no customer/PII/secret-bearing corpus;
4. no production target;
5. outbound network blocked except loopback access to the explicitly selected local Ollama endpoint;
6. `PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION=true`;
7. concurrency remains `1` and the test count stays intentionally small until the pilot proves useful;
8. results are evidence attached to existing Dealix verification/security receipts only — Promptfoo does not become truth or approval authority;
9. do **not** run `promptfoo view`, `promptfoo mcp`, or other local developer interfaces on a public bind;
10. do **not** run an untrusted PR-controlled Promptfoo config with repository-write or production-capable credentials.

## Target

`dealix-agent-redteam.yaml` uses only the loopback/local Ollama provider:

`ollama:chat:qwen3:4b-instruct-q4_K_M`

If that exact local model is unavailable, update the model only through the normal capability/runtime review. Do not silently fall back to a remote provider.

## Pre-run checks

Run the deterministic repository verifier first:

```bash
python scripts/security/verify_promptfoo_dealix_sandbox.py
```

Then, **inside the isolated unprivileged sandbox only**, after Promptfoo itself has been separately pinned/reviewed:

```bash
export PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION=true
promptfoo redteam run -c security/evals/promptfoo/dealix-agent-redteam.yaml \
  --tag git.sha="$(git rev-parse HEAD)" \
  --tag dealix.eval=bounded-agent-redteam
```

Do not auto-install `@latest` on a privileged Dealix host as part of this runbook. Tool installation/version review is a separate supply-chain decision.

## Acceptance

A Promptfoo run is not a PASS by itself. A useful pilot must produce a receipt containing:

- exact Git SHA;
- Promptfoo version;
- local target model/version;
- config hash;
- isolation/no-credential statement;
- generated test count;
- plugin/strategy set;
- failures grouped by Dealix truth/authority invariant;
- remediation issue/PR references;
- rerun result after remediation;
- measured founder-minutes/cycle-time/security value;
- KEEP / ITERATE / STOP decision.

No external action or business-truth state may be created by this eval.