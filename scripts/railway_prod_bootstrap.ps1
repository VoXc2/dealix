# Railway production bootstrap — migrations + GTM seed
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = if ($env:PY) { $env:PY } else { "py -3" }

Write-Host "== Railway production bootstrap ==" -ForegroundColor Cyan
Write-Host @"

Required env (Railway + GitHub):
  API: DATABASE_URL, APP_SECRET_KEY, ENVIRONMENT=production, CORS_ORIGINS
  API: DEALIX_ADMIN_API_KEY, MOYASAR_*
  FE:  NEXT_PUBLIC_API_URL, NEXT_PUBLIC_DEALIX_ADMIN_API_KEY
  CI:  DEALIX_API_BASE, DEALIX_API_KEY

"@

if (-not $env:DATABASE_URL) {
    Write-Host "SKIP: DATABASE_URL not set" -ForegroundColor Yellow
    exit 0
}

if ($args -notcontains "--seed-only") {
    Write-Host "`n--- Alembic upgrade head ---"
    & $Py -m alembic upgrade head
}

Write-Host "`n--- Seed gtm_seed accounts ---"
& $Py scripts/seed_revenue_machine_candidates.py

if ($env:DEALIX_API_BASE -and $env:DEALIX_ADMIN_API_KEY) {
    Write-Host "`n--- War room import (default CSV) ---"
    $base = $env:DEALIX_API_BASE.TrimEnd("/")
    $body = '{"use_default_csv": true}'
    try {
        Invoke-RestMethod -Method Post -Uri "$base/api/v1/ops-autopilot/war-room/import-targets" `
            -Headers @{ "X-Admin-API-Key" = $env:DEALIX_ADMIN_API_KEY; "Content-Type" = "application/json" } `
            -Body $body
    } catch {
        Write-Host "  import skipped: $_" -ForegroundColor Yellow
    }
}

Write-Host "`nRAILWAY_BOOTSTRAP: OK" -ForegroundColor Green
