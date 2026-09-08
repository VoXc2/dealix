# Dealix Telegram Founder Proof Plane V1

## Purpose

Turn the existing canonical founder path into a high-signal CEO surface without creating a second truth store or approval authority:

`Company Machine -> durable proof envelope -> Telegram/OpenClaw projection -> founder decision -> existing Approval authority -> execution receipt`

Telegram remains a projection and decision surface. A Telegram message, button click, delivery receipt, or model response is never execution proof by itself.

## Why this layer exists

Dealix already defines the canonical founder path as:

`Telegram DM -> OpenClaw -> existing Dealix Company Machine -> durable receipt -> Founder brief`

The missing operational layer is a consistent proof envelope that can be rendered safely in Telegram while preserving exact source identity, evidence digests, trace correlation, truth class, authority state, and durable receipt integrity.

This V1 adds that envelope and renderer only. It does **not** send Telegram messages, activate new OpenClaw commands, change runtime config, merge main, deploy Production, change DNS/DB/secrets, send customer communications, publish, spend, charge, or grant new L5 authority.

## Founder message contract

Every rendered proof uses the existing concise sections:

- `MONEY`
- `DECISIONS`
- `RISKS`
- `APPROVALS`
- `NEXT_ACTION`

Header fields include:

- truth class;
- status;
- proof ID;
- trace ID prefix;
- exact source SHA prefix;
- durable envelope SHA-256 prefix.

The full envelope remains private under:

`/opt/dealix/control/proof/telegram-founder/`

Telegram receives the compact projection only.

## Proof envelope

The envelope uses a CloudEvents-shaped metadata subset for interoperability:

- `specversion=1.0`
- `id`
- `source`
- `type`
- `subject`
- `time`
- `datacontenttype`

Dealix-specific fields add:

- `proof_id`
- `trace_id`
- `source_sha`
- `truth_class`
- `status`
- `previous_envelope_sha256`
- evidence path + SHA-256 references
- authority defaults
- founder brief sections

The local hash chain is **tamper-evident only**. It is not described as a digital signature, non-repudiation, or an external trusted timestamp.

## Evidence rules

The builder accepts evidence only when all are true:

1. absolute path;
2. resolved path remains under `/opt/dealix/control/proof`;
3. regular file;
4. not a symlink;
5. not group/world writable.

Only evidence path + SHA-256 are stored in the Telegram envelope. Raw evidence content is not copied into Telegram.

## Approval transport design

Future approval buttons must be action-bound and server-backed.

Telegram `callback_data` must contain an opaque short token only. Never embed:

- target SHA;
- DNS record content;
- configuration values;
- customer data;
- secret values;
- legal/commercial terms.

The server-side pending approval record owns the actual action packet and must contain the exact action fingerprint, target, preconditions, expiry, rollback, and one-time decision state.

On button click, the existing approval authority must revalidate:

- exact founder identity;
- callback token existence;
- token unused;
- packet not expired;
- exact action fingerprint unchanged;
- source/target SHA or config still current;
- all preconditions still true.

A stale or ambiguous decision fails closed.

`approval click != execution proof`

After an approved material action is separately executed, only the resulting execution receipt may advance truth.

## OpenClaw hardening target

The contract records a proposed one-founder hardening target based on current OpenClaw guidance. It is **not automatically applied by this PR**:

- DM policy: explicit allowlist for the founder numeric Telegram ID;
- groups disabled;
- exact founder command allowlist;
- config writes disabled;
- bash/config/MCP/plugin/debug/restart commands disabled;
- elevated tools disabled;
- inline buttons restricted to DMs;
- exec approval prompts routed to DM only;
- short approval expiry;
- webhook secret required if Telegram webhook mode is ever used.

Runtime mutation remains a separate action because current live OpenClaw version/config must be reconciled first.

## Observability

Every proof has a 32-lowercase-hex trace ID compatible with W3C trace-id shape. Where existing OpenTelemetry tracing exists, adapters should carry the same trace ID rather than create a second observability database.

Do not log raw prompts, tool arguments, customer PII, secrets, or full evidence merely to improve trace richness.

## Source verification

Run on the exact candidate SHA:

```bash
python scripts/ops/verify_telegram_proof_plane_v1.py
pytest -q tests/test_telegram_proof_plane_v1.py
```

Example builder invocation in an isolated/non-production proof test:

```bash
python scripts/ops/build_telegram_founder_proof.py \
  --source-sha "$(git rev-parse HEAD)" \
  --truth-class HOLD \
  --status HOLD \
  --subject "Telegram proof-plane source acceptance" \
  --decision "Proof envelope source is present" \
  --risk "Runtime Telegram delivery is not proven" \
  --next-action "Run current VPS Founder Control acceptance"
```

Expected builder footer:

```text
TELEGRAM_SENT=false
L5_EXECUTED=false
```

## Runtime activation sequence

1. exact-head source verification;
2. current VPS OpenClaw/Telegram founder-control acceptance;
3. generate a local synthetic proof envelope;
4. verify file ownership/mode/digest/hash-chain behavior;
5. project one synthetic `INFO/HOLD` proof into the existing founder DM through the current OpenClaw messaging path;
6. verify delivery receipt and correlation to the durable envelope;
7. only then implement server-backed approval callbacks as a bounded follow-up;
8. run a non-material approval canary before any L5 packet is exposed through buttons.

## Non-claims

This V1 does not prove:

- current Telegram/OpenClaw runtime acceptance;
- live Telegram delivery;
- inline approval callback execution;
- Production parity;
- Production Green;
- customer send authority;
- payment authority;
- verified cash;
- customer proof.
