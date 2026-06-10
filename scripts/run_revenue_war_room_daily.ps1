# Daily Revenue War Room — ops snapshot + tracker reminder
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== Dealix Revenue War Room (daily) ==="
Write-Host "Tracker: docs/ops/REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml"
Write-Host "SOP: docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md"
Write-Host ""

$Base = if ($env:DEALIX_API_URL) { $env:DEALIX_API_URL } else { "http://localhost:8000" }

try {
    Write-Host "--- Public services catalog ---"
    Invoke-RestMethod -Uri "$Base/api/v1/public/services" | ConvertTo-Json -Depth 4
} catch {
    Write-Host "(API unreachable: $_)"
}

if ($env:DEALIX_ADMIN_API_KEY) {
    $Headers = @{ "X-Admin-API-Key" = $env:DEALIX_ADMIN_API_KEY }
    try {
        Write-Host "--- Founder ops dashboard ---"
        Invoke-RestMethod -Uri "$Base/api/v1/ops-autopilot/founder-dashboard" -Headers $Headers | ConvertTo-Json -Depth 5
    } catch { Write-Host "founder-dashboard: $_" }
    try {
        Write-Host "--- Sales pipeline ---"
        Invoke-RestMethod -Uri "$Base/api/v1/sales/pipeline" -Headers $Headers | ConvertTo-Json -Depth 4
    } catch { Write-Host "pipeline: $_" }
} else {
    Write-Host "(Set DEALIX_ADMIN_API_KEY for founder-dashboard + pipeline)"
}

Write-Host ""
Write-Host "UI: /ar/ops/founder · /ar/ops/sales · /ar/ops/evidence · /ar/approvals"
Write-Host "Done."
