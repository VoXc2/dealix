# Official launch verify (Windows)
param(
    [string]$ApiBase = $env:DEALIX_API_BASE,
    [string]$AdminKey = $env:DEALIX_ADMIN_API_KEY,
    [switch]$SkipFeBuild,
    [switch]$SkipGoLive
)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"
function Invoke-Python {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PyArgs)
    if ($env:PY) {
        & $env:PY @PyArgs
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 @PyArgs
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python @PyArgs
    } else {
        throw "python not found"
    }
}
$Fail = 0

Write-Host "== Official Launch Verify ==" -ForegroundColor Cyan

$crArgs = @()
if ($SkipGoLive) { $crArgs += "-SkipGoLive" }
if (Get-Command bash -ErrorAction SilentlyContinue) {
    $bashCr = @("$Root/scripts/company_ready_verify.sh")
    if ($SkipGoLive) { $bashCr += "--skip-go-live" }
    & bash @bashCr
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    if (-not $SkipGoLive) {
        & bash "$Root/scripts/founder_go_live_verify.sh"
        if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    }
} else {
    & (Join-Path $PSScriptRoot "company_ready_verify.ps1") @crArgs
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
}

Invoke-Python -m pytest tests/test_gtm_commercial_stack.py tests/test_official_launch_verify.py tests/test_client_pack.py -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if (-not $SkipFeBuild -and (Test-Path "$Root/frontend/package.json")) {
    Push-Location "$Root/frontend"
    if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" }
    npm run build --silent
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    Pop-Location
}

if ($ApiBase) {
    $base = $ApiBase.TrimEnd("/")
    try {
        Invoke-RestMethod -Uri "$base/health" -Method Get | Out-Null
        Write-Host "  health: PASS"
    } catch {
        Write-Host "  health: FAIL" -ForegroundColor Red
        $Fail = 1
    }
    if ($AdminKey) {
        foreach ($path in @(
            "/api/v1/ops-autopilot/marketing/social-today",
            "/api/v1/ops-autopilot/war-room/today-pack",
            "/api/v1/ops-autopilot/founder/daily-pack"
        )) {
            try {
                Invoke-RestMethod -Uri "$base$path" -Headers @{ "X-Admin-API-Key" = $AdminKey } | Out-Null
                Write-Host "  ${path}: PASS"
            } catch {
                Write-Host "  ${path}: FAIL" -ForegroundColor Red
                $Fail = 1
            }
        }
    }
}

if ($Fail -eq 0) {
    Write-Host "OFFICIAL_LAUNCH_VERDICT=PASS" -ForegroundColor Green
    exit 0
}
Write-Host "OFFICIAL_LAUNCH_VERDICT=FAIL" -ForegroundColor Red
exit 1
