# Railway UI alignment — Windows wrapper for verify + optional prod smoke.
param(
    [switch]$WithSmoke,
    [string]$ApiBase = $(if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }),
    [string]$UiStartCommand = $env:RAILWAY_UI_START_COMMAND,
    [string]$UiPredeploy = $env:RAILWAY_UI_PREDEPLOY
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== Railway UI alignment (api.dealix.me) =="

$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue; $pyArgs = @("-3") } else { $pyArgs = @() }

$args = @("scripts/verify_railway_production_config.py", "--api-base", $ApiBase)
if ($UiStartCommand) { $args += @("--ui-start-command", $UiStartCommand) }
if ($UiPredeploy) { $args += @("--ui-predeploy", $UiPredeploy) }

& $py.Source @pyArgs @args
if ($LASTEXITCODE -ne 0) {
    Write-Host @"

FOUNDER_ACTION:
  1. Railway -> Deploy -> Start Command: CLEAR (or /app/start.sh only)
  2. Railway -> Deploy -> Pre-deploy: sh /app/scripts/railway_predeploy.sh
  3. Enable Wait for CI on main
"@
    exit $LASTEXITCODE
}

if ($WithSmoke) {
    Write-Host "== prod_smoke =="
    bash "$Root/scripts/prod_smoke.sh" $ApiBase
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host "RAILWAY_UI_ALIGNMENT=PASS"
