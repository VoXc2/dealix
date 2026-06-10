# Founder production smoke — Windows
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$ApiBase = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }

function Invoke-Py { param([string[]]$Args) if (Get-Command python3 -EA SilentlyContinue) { & python3 @Args } else { & py -3 @Args } }

Write-Host "== 1/4 Railway config-as-code =="
$railwayArgs = @("scripts/verify_railway_production_config.py", "--api-base", $ApiBase)
if ($env:RAILWAY_UI_START_COMMAND) { $railwayArgs += @("--ui-start-command", $env:RAILWAY_UI_START_COMMAND) }
if ($env:RAILWAY_UI_PREDEPLOY) { $railwayArgs += @("--ui-predeploy", $env:RAILWAY_UI_PREDEPLOY) }
Invoke-Py $railwayArgs

Write-Host "`n== 2/4 GTM public surfaces (repo) =="
Invoke-Py scripts/verify_gtm_public_surfaces.py --skip-live

Write-Host "`n== 3/4 Live curls =="
curl.exe -fsS "$ApiBase/healthz"; Write-Host ""
try { curl.exe -fsS "$ApiBase/version"; Write-Host "" } catch { Write-Host "WARN: /version not live yet" }
try { curl.exe -fsS "$ApiBase/api/v1/meta"; Write-Host "" } catch { Write-Host "WARN: /api/v1/meta not live yet" }
curl.exe -fsS "$ApiBase/health"; Write-Host ""

Write-Host "`n== 4/4 Unified production gates =="
$gateArgs = @("scripts/run_founder_production_gates.py", "--api-base", $ApiBase)
if ($env:RAILWAY_UI_START_COMMAND) { $gateArgs += @("--ui-start-command", $env:RAILWAY_UI_START_COMMAND) }
if ($env:RAILWAY_UI_PREDEPLOY) { $gateArgs += @("--ui-predeploy", $env:RAILWAY_UI_PREDEPLOY) }
Invoke-Py $gateArgs

Write-Host "FOUNDER_PRODUCTION_SMOKE=PASS"
