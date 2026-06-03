# Production go-live full verify (strict) — steps 0–12
param(
    [switch]$Strict,
    [switch]$SkipPush,
    [switch]$SkipFrontendBuild
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Fail = 0
$ApiBase = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }

function Step-Fail {
    param([int]$Code)
    if ($Strict -and $Code -ne 0) { $script:Fail = 1 }
}

Write-Host ""
Write-Host "== Production go-live full ==" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== 0 Git push ==="
if ($SkipPush) {
    Write-Host "  skipped (-SkipPush)"
} else {
    powershell -File (Join-Path $PSScriptRoot "push_main_with_gh.ps1")
    Step-Fail $LASTEXITCODE
}

Write-Host ""
Write-Host "=== 1 P0 env files ==="
py -3 scripts/sync_railway_generated_env.py
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 2 Repo gates ==="
py -3 scripts/verify_railway_production_config.py --api-base $ApiBase
Step-Fail $LASTEXITCODE
py -3 scripts/railway_launch_env_check.py
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 3 Unit tests ==="
$env:APP_ENV = "test"
py -3 -m pytest tests/test_founder_production_layers.py tests/test_gtm_public_surfaces.py tests/test_official_launch_verify.py -q --no-cov
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 4 Frontend build ==="
if ($SkipFrontendBuild) {
    Write-Host "  skipped (-SkipFrontendBuild)"
} else {
    Push-Location (Join-Path $Root "frontend")
    npm run build
    $buildCode = $LASTEXITCODE
    Pop-Location
    Step-Fail $buildCode
}

Write-Host ""
Write-Host "=== 5 Layer map ==="
$layerArgs = @("scripts/production_layers_verify.py", "--from-railway-env", "--write-cache")
if ($Strict) { $layerArgs += "--strict" }
py -3 @layerArgs
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 6 Railway redeploy ==="
py -3 scripts/railway_redeploy_checklist.py --api-base $ApiBase
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 7 Webhooks ==="
py -3 scripts/webhook_setup_checklist.py --from-railway-env
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 8 Founder gates ==="
py -3 scripts/run_founder_production_gates.py --api-base $ApiBase
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 9 Paid launch ==="
$paidArgs = @("scripts/verify_paid_launch_readiness.py")
if ($Strict) { $paidArgs += "--strict" }
if (Test-Path (Join-Path $Root ".env.railway.generated")) { $paidArgs += "--from-railway-env" }
py -3 @paidArgs
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 10 Post-redeploy verify ==="
$postArgs = @("scripts/post_redeploy_verify_dealix.py", "--api-base", $ApiBase)
if ($env:DEALIX_ADMIN_API_KEY) { $postArgs += "--admin-key", $env:DEALIX_ADMIN_API_KEY }
py -3 @postArgs
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 11 Validate railway env files ==="
py -3 scripts/validate_railway_generated_env.py --from-railway-env
Step-Fail $LASTEXITCODE

Write-Host ""
Write-Host "=== 12 Live HTTP ==="
@("/healthz", "/version", "/api/v1/meta") | ForEach-Object {
    $path = $_
    try {
        $r = Invoke-WebRequest -Uri "$ApiBase$path" -UseBasicParsing -TimeoutSec 15
        Write-Host "  $ApiBase$path -> $($r.StatusCode)"
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        Write-Host "  $ApiBase$path -> $(if ($code) { $code } else { 'error' })"
    }
}
try {
    $ar = Invoke-WebRequest -Uri "https://dealix.me/ar" -Method Head -UseBasicParsing -TimeoutSec 15
    Write-Host "  https://dealix.me/ar -> $($ar.StatusCode)"
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    Write-Host "  https://dealix.me/ar -> $(if ($code) { $code } else { 'error' })"
}

Write-Host ""
if ($Fail -eq 0) {
    Write-Host "PRODUCTION_GO_LIVE_FULL=OK" -ForegroundColor Green
} else {
    Write-Host "PRODUCTION_GO_LIVE_FULL=PARTIAL" -ForegroundColor Yellow
    Write-Host "  docs/ops/PRODUCTION_LAYERS_GO_LIVE_AR.md"
    Write-Host "  docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
}
exit $Fail
