# Founder — run all production layer verifiers (strict) + manual gate card
param(
    [switch]$SkipPush,
    [switch]$SkipFrontendBuild
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Fail = 0

Write-Host ""
Write-Host "== Dealix complete layers (strict) ==" -ForegroundColor Cyan
Write-Host ""

py -3 scripts/sync_railway_generated_env.py
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

$goArgs = @("-File", (Join-Path $PSScriptRoot "run_production_go_live_full.ps1"), "-Strict")
if ($SkipPush) { $goArgs += "-SkipPush" }
if ($SkipFrontendBuild) { $goArgs += "-SkipFrontendBuild" }
powershell @goArgs
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host ""
Write-Host "== Founder production probe (strict) ==" -ForegroundColor Cyan
powershell -File (Join-Path $PSScriptRoot "founder_production_probe.ps1") -Strict
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host ""
Write-Host "== Manual gates (cannot automate from this machine) ==" -ForegroundColor Yellow
Write-Host '  1) gh auth login -s repo  ->  powershell -File scripts/push_main_with_gh.ps1'
Write-Host '  2) Railway API -> Deploy latest main  ->  /version + /api/v1/meta = 200'
Write-Host '  3) Railway Frontend + DNS dealix.me  ->  /ar = 200 (not GitHub.com)'
Write-Host '  4) Layer 5: first payment + proof in evidence_events_tracker.csv'
Write-Host "  doc: docs/ops/RAILWAY_ONE_SHOT_DEPLOY_AR.md"
Write-Host ""

if ($Fail -eq 0) {
    Write-Host "FOUNDER_COMPLETE_LAYERS_NOW=OK" -ForegroundColor Green
} else {
    Write-Host 'FOUNDER_COMPLETE_LAYERS_NOW=PARTIAL — see blockers above' -ForegroundColor Yellow
}
exit $Fail
