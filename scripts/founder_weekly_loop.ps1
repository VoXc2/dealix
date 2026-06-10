# Founder weekly loop — Windows (see founder_weekly_loop.sh)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$ApiBase = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }

function Invoke-Py { param([string[]]$Args) if (Get-Command python3 -EA SilentlyContinue) { & python3 @Args } else { & py -3 @Args } }

Write-Host "== Founder operating system =="
& "$PSScriptRoot\verify_founder_operating_system.ps1"

Write-Host "== GTM public surfaces (repo) =="
Invoke-Py scripts/verify_gtm_public_surfaces.py --skip-live

Write-Host "== Railway production config =="
$railwayArgs = @("scripts/verify_railway_production_config.py", "--api-base", $ApiBase)
if ($env:RAILWAY_UI_START_COMMAND) { $railwayArgs += @("--ui-start-command", $env:RAILWAY_UI_START_COMMAND) }
if ($env:RAILWAY_UI_PREDEPLOY) { $railwayArgs += @("--ui-predeploy", $env:RAILWAY_UI_PREDEPLOY) }
try { Invoke-Py $railwayArgs } catch { Write-Host "  (railway verify warning — continuing)" }

Write-Host "== Founder weekly metrics bundle =="
try { Invoke-Py scripts/founder_weekly_metrics_bundle.py --write } catch { Write-Host "  (metrics warning — continuing)" }

Write-Host "== Founder production gates =="
$gateArgs = @("scripts/run_founder_production_gates.py", "--api-base", $ApiBase)
if ($env:RAILWAY_UI_START_COMMAND) { $gateArgs += @("--ui-start-command", $env:RAILWAY_UI_START_COMMAND) }
if ($env:RAILWAY_UI_PREDEPLOY) { $gateArgs += @("--ui-predeploy", $env:RAILWAY_UI_PREDEPLOY) }
try { Invoke-Py $gateArgs } catch { Write-Host "  (production gates warning — continuing)" }

Write-Host "== Commercial launch readiness =="
Invoke-Py scripts/verify_commercial_launch_ready.py

Write-Host "== Strongest plan checklist =="
Invoke-Py scripts/founder_strongest_plan_status.py

Write-Host "== Comprehensive plan =="
Invoke-Py scripts/founder_comprehensive_plan_status.py

Write-Host "== CEO weekly retro =="
Invoke-Py scripts/founder_weekly_ceo_retro.py

Write-Host "== Dogfooding war room =="
Invoke-Py scripts/founder_dogfooding_war_room_sync.py

Write-Host "FOUNDER_WEEKLY_LOOP=PASS"
