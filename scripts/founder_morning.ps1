# One-click founder morning - canonical commercial day (Windows)
# Usage: powershell -File scripts/founder_morning.ps1
#        powershell -File scripts/founder_morning.ps1 -DryRun
param(
    [switch]$DryRun,
    [switch]$WithBusinessNow,
    [switch]$Full
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== Dealix Founder Morning (governed) =="
Write-Host "Policy: drafts + approvals only - no cold WhatsApp / no LinkedIn auto-send"
Write-Host "Evening: powershell -File scripts/founder_evening.ps1 (evidence tracker)"
Write-Host ""

# Canonical: founder full autopilot (expand + morning core + brief queue)
$autopilot = Join-Path $PSScriptRoot "run_founder_full_autopilot.ps1"
if (Test-Path $autopilot) {
    if ($DryRun) {
        & $autopilot -DryRun
    } elseif ($Full) {
        & $autopilot -Mode full
    } else {
        & $autopilot -Mode morning
    }
    exit $LASTEXITCODE
}

$target = Join-Path $PSScriptRoot "run_founder_commercial_day.ps1"
if ($DryRun) {
    & $target -DryRun
} elseif ($Full) {
    & $target -Full
} elseif ($WithBusinessNow) {
    & $target -WithBusinessNow
} else {
    & $target
}
exit $LASTEXITCODE
