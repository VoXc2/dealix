# Tenant Isolation

## Core rule
Every operational object must include `tenant_id`.

## Why
- Prevents cross-tenant data leakage.
- Enables tenant-scoped audit and control timelines.
- Aligns routing, approvals, safety, and value with customer boundary.

## Current enforcement
- Schema-level required `tenant_id` for control/mesh/contracts/safety/value/self-evolving objects.
- Dev/test fallback supports `tenant_id="default"` only for non-production flows.
