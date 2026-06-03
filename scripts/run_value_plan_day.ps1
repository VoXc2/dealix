# Value Plan day — expand pool + snapshot + founder commercial loop
param(
    [switch]$Wave2,
    [switch]$SkipCommercialDay
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Invoke-DealixPy {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($env:PY) { & $env:PY @Args } else { & py -3 @Args }
}

Write-Host "== Dealix Value Plan Day =="

$expandArgs = @(
    "scripts/expand_commercial_ops_all.py",
    "--wave4",
    "--cycle-weeks", "28",
    "--enrich-warm"
)
if ($Wave2) {
    $expandArgs = @("scripts/expand_commercial_ops_all.py", "--wave2", "--enrich-warm")
}
Invoke-DealixPy @expandArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not $SkipCommercialDay) {
    & (Join-Path $PSScriptRoot "run_founder_commercial_day.ps1")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Invoke-DealixPy scripts/founder_paid_launch_gate.py
Write-Host "VALUE_PLAN_DAY=OK"
