# Autonomous production close — push, trigger Railway deploy via GH Actions, poll trust layer, strict verify
param(
    [switch]$SkipPush,
    [switch]$SkipFrontendBuild,
    [int]$PollMinutes = 12
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Fail = 0
$ApiBase = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }

function Test-TrustLayerLive {
    param([string]$Base)
    $ok = $true
    foreach ($path in @("/healthz", "/version", "/api/v1/meta")) {
        try {
            $r = Invoke-WebRequest -Uri "$Base$path" -UseBasicParsing -TimeoutSec 20
            if ($r.StatusCode -ne 200) { $ok = $false; Write-Host "  $path -> $($r.StatusCode)" }
            elseif ($path -eq "/healthz" -and $r.Content -notmatch '"version"') {
                $ok = $false
                Write-Host "  /healthz -> 200 but missing version in body"
            }
            else { Write-Host "  $path -> 200" }
        } catch {
            $code = $_.Exception.Response.StatusCode.value__
            Write-Host "  $path -> $(if ($code) { $code } else { 'error' })"
            $ok = $false
        }
    }
    return $ok
}

Write-Host "== autonomous_production_close ==" -ForegroundColor Cyan

py -3 scripts/sync_railway_generated_env.py

if (-not $SkipPush) {
    powershell -File (Join-Path $PSScriptRoot "push_main_with_gh.ps1")
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
}

$hasRailwayToken = $false
$secrets = gh secret list --repo VoXc2/dealix 2>$null
if ($secrets -match "RAILWAY_TOKEN") {
    $hasRailwayToken = $true
    Write-Host ""
    Write-Host "== Trigger GitHub Actions Railway deploy ==" -ForegroundColor Cyan
    gh workflow run "Deploy to Railway" --ref main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Start-Sleep -Seconds 8
        $runId = (gh run list --workflow=railway_deploy.yml --limit 1 --json databaseId -q ".[0].databaseId" 2>$null)
        if ($runId) {
            Write-Host "  watching run $runId ..."
            gh run watch $runId --exit-status 2>&1
        }
    }
} else {
    Write-Host ""
    Write-Host "RAILWAY_TOKEN missing on GitHub - add once:" -ForegroundColor Yellow
    Write-Host "  https://railway.app/account/tokens"
    Write-Host "  gh secret set RAILWAY_TOKEN --repo VoXc2/dealix"
    Write-Host "  Or connect Railway GitHub repo deploy on service linked to api.dealix.me"
    $Fail = 1
}

Write-Host ""
Write-Host "== Poll live trust layer (${PollMinutes} min max) ==" -ForegroundColor Cyan
$deadline = (Get-Date).AddMinutes($PollMinutes)
$liveOk = $false
while ((Get-Date) -lt $deadline) {
    if (Test-TrustLayerLive -Base $ApiBase) {
        $liveOk = $true
        break
    }
    Write-Host "  waiting 30s ..."
    Start-Sleep -Seconds 30
}
if (-not $liveOk) {
    Write-Host "  trust layer still not PASS on $ApiBase" -ForegroundColor Yellow
    $Fail = 1
}

$completeArgs = @("-File", (Join-Path $PSScriptRoot "founder_complete_layers_now.ps1"), "-SkipPush")
if ($SkipFrontendBuild) { $completeArgs += "-SkipFrontendBuild" }
powershell @completeArgs
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if ($Fail -eq 0 -and $liveOk) {
    Write-Host "AUTONOMOUS_PRODUCTION_CLOSE=OK" -ForegroundColor Green
} else {
    Write-Host "AUTONOMOUS_PRODUCTION_CLOSE=PARTIAL" -ForegroundColor Yellow
    Write-Host "  Blockers: RAILWAY_TOKEN and/or DNS dealix.me -> Railway Frontend (not GitHub Pages)"
}
exit $Fail
