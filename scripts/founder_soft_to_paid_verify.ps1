# Soft Launch PASS → Paid Launch readiness (no Moyasar claim until FOUNDER_ACTION)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

function Invoke-DealixPy {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($env:PY) { & $env:PY @Args } else { & py -3 @Args }
}

Write-Host "== founder_soft_to_paid_verify =="
Write-Host ""

Write-Host "== 1/3 Commercial strict (targeting >= 80) =="
Invoke-DealixPy scripts/verify_commercial_launch_ready.py --strict
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "== 2/3 Paid launch roadmap =="
Invoke-DealixPy scripts/verify_paid_launch_readiness.py
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "== 3/3 First paid Diagnostic pipeline =="
Invoke-DealixPy scripts/verify_first_paid_diagnostic_tracker.py

Write-Host ""
Write-Host "FOUNDER_SOFT_TO_PAID=ROADMAP_OK"
Write-Host "Next: docs/commercial/PAID_LAUNCH_AFTER_SOFT_PASS_AR.md"
Write-Host "Production: bash scripts/official_launch_verify.sh (Moyasar + Railway)"
