# Founder one-session close — technical + commercial + CEO master plan verify
param(
    [switch]$SkipPush,
    [switch]$SkipFrontendBuild,
    [switch]$SkipDeploy,
    [switch]$SkipCommercial,
    [switch]$PdplConfirm,
    [int]$PollMinutes = 12
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Fail = 0

Write-Host ""
Write-Host "== Founder One-Session Close ==" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== Phase A0: merge env from local .env ==="
py -3 scripts/apply_founder_closure_env.py
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host ""
Write-Host "=== Phase A1: production deploy + poll ==="
if ($SkipDeploy) {
    Write-Host "  skipped (-SkipDeploy)"
} else {
    $autoArgs = @("-File", (Join-Path $PSScriptRoot "autonomous_production_close.ps1"), "-PollMinutes", $PollMinutes)
    if ($SkipPush) { $autoArgs += "-SkipPush" }
    if ($SkipFrontendBuild) { $autoArgs += "-SkipFrontendBuild" }
    powershell @autoArgs
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
}

Write-Host ""
Write-Host "=== Phase B: commercial closure (intake-driven) ==="
if ($SkipCommercial) {
    Write-Host "  skipped (-SkipCommercial)"
} else {
    $commArgs = @("scripts/apply_founder_closure_commercial.py")
    if ($PdplConfirm) { $commArgs += "--pdpl-confirm" }
    py -3 @commArgs
    if ($LASTEXITCODE -ne 0) { Write-Host "  commercial closure partial" -ForegroundColor Yellow; $Fail = 1 }
}

Write-Host ""
Write-Host "=== Phase C: strict production verify ==="
$completeArgs = @("-File", (Join-Path $PSScriptRoot "founder_complete_layers_now.ps1"), "-SkipPush")
if ($SkipFrontendBuild) { $completeArgs += "-SkipFrontendBuild" }
powershell @completeArgs
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host ""
Write-Host "=== Phase D: CEO master plan ==="
py -3 scripts/run_ceo_master_plan_status.py
py -3 scripts/founder_comprehensive_plan_status.py
py -3 scripts/verify_first_paid_diagnostic_tracker.py

Write-Host ""
if ($Fail -eq 0) {
    Write-Host "FOUNDER_ONE_SESSION_CLOSE=OK" -ForegroundColor Green
} else {
    Write-Host "FOUNDER_ONE_SESSION_CLOSE=PARTIAL" -ForegroundColor Yellow
    Write-Host "  docs/ops/RAILWAY_ONE_SHOT_DEPLOY_AR.md"
    Write-Host "  docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
}
exit $Fail
