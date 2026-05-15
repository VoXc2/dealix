# Platform Contracts (`/platform/*`)

This directory is the filesystem-level mirror of the Dealix Operational Dominance model.

- Runtime implementation lives in `auto_client_acquisition/operational_fabric_os/`.
- API observability lives in `api/routers/operational_fabric.py`.
- Canonical mapping for Systems 26–35 lives in `platform/contracts_manifest.json`.

## Why not Python package at repo root named `platform`?

Creating a Python package named `platform` at repo root can shadow Python's stdlib
`platform` module. Therefore, runtime Python code is placed under
`auto_client_acquisition/operational_fabric_os/` and mirrored here as contracts.
