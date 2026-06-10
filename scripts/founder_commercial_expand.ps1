# Expand commercial ops — delegates to expand_commercial_ops_all + verification gates
# Usage: powershell -File scripts/founder_commercial_expand.ps1
#        powershell -File scripts/founder_commercial_expand.ps1 -Wave2
#        powershell -File scripts/founder_commercial_expand.ps1 -Wave3 -SkipGoLive
param(
    [switch]$Wave2,
    [switch]$Wave3,
    [switch]$Wave4,
    [switch]$Full,
    [int]$MinRows = 120,
    [switch]$SkipGoLive,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Invoke-DealixPy {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($env:PY) { & $env:PY @Args } else { & py -3 @Args }
}

Write-Host "== founder_commercial_expand (all angles) =="
if ($Full) { $Wave4 = $true }
Write-Host "  wave2=$Wave2 wave3=$Wave3 wave4=$Wave4 full=$Full min_rows=$MinRows dry_run=$DryRun"
Write-Host ""

$expandArgs = @(
    "scripts/expand_commercial_ops_all.py",
    "--cycle-weeks", "28",
    "--meetings", "10",
    "--touch-drafts", "15",
    "--enrich-warm"
)
if ($Wave4 -or $Full) {
    $expandArgs += "--wave4"
} elseif ($Wave3) {
    $expandArgs += "--wave3"
} elseif ($Wave2) {
    $expandArgs += "--wave2"
} else {
    $expandArgs += "--min-rows"
    $expandArgs += "$MinRows"
}
if ($DryRun) {
    $expandArgs += "--skip-import"
    $expandArgs += "--skip-war-room"
}

Write-Host "== 1/4 expand_commercial_ops_all =="
Invoke-DealixPy @expandArgs
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`n== 2/4 Expansion status =="
Invoke-DealixPy scripts/founder_expansion_status.py

Write-Host "`n== 3/4 Gates (strict + soft-to-paid + FE/BE) =="
Invoke-DealixPy scripts/verify_commercial_launch_ready.py --strict
if ($LASTEXITCODE -ne 0) { exit 1 }
Invoke-DealixPy scripts/verify_commercial_fe_be.py
if ($LASTEXITCODE -ne 0) { exit 1 }
& powershell -File scripts/founder_soft_to_paid_verify.ps1
if ($LASTEXITCODE -ne 0) { exit 1 }

if (-not $SkipGoLive) {
    Write-Host "`n== 4/4 Unified go-live =="
    & powershell -File scripts/verify_dealix_commercial_go_live.ps1
    if ($LASTEXITCODE -ne 0) { exit 1 }
} else {
    Write-Host "`n== 4/4 Unified go-live (skipped) =="
}

Write-Host ""
Write-Host "FOUNDER_COMMERCIAL_EXPAND=OK"
Write-Host "Morning: powershell -File scripts/founder_morning.ps1"
Write-Host "Evening: powershell -File scripts/founder_evening.ps1 -Append -Company '...' -EventType message_sent_manual"
