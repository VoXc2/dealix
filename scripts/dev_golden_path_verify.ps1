# Quick golden-chain verification (Windows / PowerShell).
# Mirrors the Revenue OS smoke tests used in CI-style checks.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..
$env:APP_ENV = "test"
py -3 -m pytest tests/test_revenue_os_golden_chain_smoke.py -q --no-cov
