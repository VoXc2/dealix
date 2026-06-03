# Master orchestrator: Launch Execution Railway plan (A–D).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$SkipBootstrap = $env:SKIP_BOOTSTRAP -eq "1"
$SkipVerify = $env:SKIP_VERIFY -eq "1"
$SkipWarm = $env:SKIP_WARM -eq "1"
$SkipRevenueDay = $env:SKIP_REVENUE_DAY -eq "1"
$AllowReplaceTop = if ($env:ALLOW_REPLACE_TOP) { $env:ALLOW_REPLACE_TOP } else { "1" }

Write-Host "=== A: Railway env check ==="
py -3 scripts/railway_launch_env_check.py
if ($LASTEXITCODE -ne 0) { Write-Host "Env check incomplete (expected until Railway vars set)" }

if (-not $SkipBootstrap -and $env:DATABASE_URL) {
    Write-Host "=== A4: Production bootstrap ==="
    & "$PSScriptRoot\railway_prod_bootstrap.ps1"
} else {
    Write-Host "SKIP bootstrap (set DATABASE_URL to run)"
}

if (-not $SkipVerify) {
    Write-Host "=== B: Official launch verify ==="
    & "$PSScriptRoot\official_launch_verify.ps1"
}

if (-not $SkipWarm) {
    Write-Host "=== C: Warm CSV validation ==="
    $warmArgs = @()
    if ($AllowReplaceTop -eq "1") {
        $warmArgs += "--max-replace-top", "99"
    }
    py -3 scripts/validate_warm_targeting_csv.py @warmArgs
    if ($env:DEALIX_API_BASE -and $env:DEALIX_ADMIN_API_KEY) {
        py -3 scripts/sync_war_room_targets_api.py
    }
}

if (-not $SkipRevenueDay) {
    Write-Host "=== D: Founder revenue day ==="
    & "$PSScriptRoot\run_founder_revenue_day.ps1"
}

Write-Host "LAUNCH_EXECUTION_RAILWAY=done"
