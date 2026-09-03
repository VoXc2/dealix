# Dealix L5 Approval Fingerprint Contract

## Authority

This file is the repository contract referenced by `AGENTS.md` for every L5 external effect. It does **not** grant approval and it does not create a new Approval Center. The existing canonical Governance/Approval owner remains the only authority source.

## Canonical ACTION_HASH

Every L5 approval is bound to exactly one material action:

```text
ACTION_HASH = sha256(action_type|target|environment|payload)[0:16]
```

Where `action_type` is the exact L5 class, `target` is the exact external destination/resource, `environment` is the exact execution environment, and `payload` is deterministic canonical material binding schema version, content/artifact, purpose, scope, provider, expiry, idempotency key and evidence references.

Any material change creates a different ACTION_HASH and therefore requires a new action-specific approval. Broad founder statements never substitute for a matching hash.

## Packet integrity is separate

Execution packets additionally carry a full 64-character `packet_integrity_sha256`. It includes `schema_version` and all material serialized packet fields. It is a tamper/version-drift checksum only; it is **not** the approval identity. The executor recomputes both packet integrity and ACTION_HASH before any provider side effect. Unsupported schema or any mismatch fails closed.

## Fresh authority requirement

A cached approval object is not execution authority. Immediately before a side effect, a provider-owned trusted adapter must re-resolve from the canonical Governance/Approval owner:

- current approval state and ACTION_HASH;
- current exact scope and expiry;
- freshness of the approval-state check itself;
- current suppression/channel eligibility/consent evidence as applicable;
- current runtime authority/kill switches;
- current sender/claim evidence as applicable.

If the canonical provider-owned resolver is missing, stale, revoked, expired, mismatched or ambiguous, the effect remains blocked. Action callers must not inject a resolver, approval snapshot, runtime switch set, token/service object or idempotency implementation to manufacture execution authority.

## Durable idempotency and reconciliation

Before a provider call, the trusted provider boundary must durably reserve the packet's `idempotency_key` against both ACTION_HASH and packet integrity.

- same key + same COMMITTED action: return the prior provider receipt; do not send again;
- same key + different action: reject;
- RESERVED or UNKNOWN: do not blindly retry;
- provider success: persist provider receipt and COMMITTED state;
- ambiguous provider result: transition to UNKNOWN and reconcile independently.

UNKNOWN has two audited terminal reconciliation paths:

1. **Confirmed delivered** → `UNKNOWN -> COMMITTED`, with provider/reconciliation evidence and the recovered receipt.
2. **Confirmed not delivered** → `UNKNOWN -> ABORTED`, with evidence. The old key stays closed; any retry must create a new idempotency key and obtain fresh exact-action authority.

For providers without a transactional idempotency primitive (including Gmail `messages.send`), Dealix does **not** claim mathematical exactly-once delivery. It uses durable at-most-once replay prevention plus an explicit UNKNOWN reconciliation boundary for crash/network ambiguity.

## Fleet exact-once boundary

Living Fleet dispatch and collect must serialize terminalization through the same per-role lock. A collector may never increment counters or move a pending job concurrently with synchronous dispatch terminalization. FORCE=0 owner transitions and concurrent dispatch/collect behavior require non-skipped acceptance tests.

## Merge/deploy boundary

L5/authority code must remain fail-closed during tests and exact-head verification. Independent review must complete on the current exact head before any merge decision. Hosted checks that execute no repository jobs are not acceptance evidence.
