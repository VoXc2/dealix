# Business NOW snapshot — Windows wrapper
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Py = Get-Command python -ErrorAction SilentlyContinue
if (-not $Py) { $Py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $Py) { throw "python not found" }
$Python = $Py.Source
if ($Py.Name -eq "py") { $Python = "py -3" }

Write-Host "== Business NOW: platform KPI signals =="
& $Python "$Root\scripts\populate_kpi_baselines_platform_signals.py"

Write-Host ""
Write-Host "== Business NOW: commercial registry status =="
& $Python "$Root\scripts\apply_kpi_founder_commercial.py" --status
if ($LASTEXITCODE -ne 0) { $LASTEXITCODE = 0 }

Write-Host ""
Write-Host "== Business NOW: generate snapshot =="
& $Python "$Root\scripts\generate_business_now_snapshot.py"

Write-Host ""
Write-Host "== Business NOW: commercial strategy doc =="
& $Python "$Root\scripts\generate_commercial_strategy_doc.py"

Write-Host ""
Write-Host "BUSINESS_NOW: OK"
Write-Host "UI: /ar/business-now"
Write-Host "API: GET /api/v1/business-now/snapshot"
