# Wire GitHub Actions secrets for production cadence (run once by founder)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$required = @(
    @{ Name = "RAILWAY_TOKEN"; Doc = "https://railway.app/account/tokens"; Required = $true },
    @{ Name = "DEALIX_API_BASE"; Doc = "https://api.dealix.me"; Required = $false },
    @{ Name = "DEALIX_ADMIN_API_KEY"; Doc = "Same as Railway ADMIN_API_KEYS"; Required = $false }
)

Write-Host "== GitHub Actions production secrets ==" -ForegroundColor Cyan
$list = gh secret list --repo VoXc2/dealix 2>$null
$missing = @()
foreach ($s in $required) {
    $present = $list -match $s.Name
    if ($present) {
        Write-Host "  OK  $($s.Name)" -ForegroundColor Green
    } else {
        Write-Host "  MISSING  $($s.Name) - $($s.Doc)" -ForegroundColor Yellow
        if ($s.Required) { $missing += $s.Name }
    }
}

Write-Host ""
Write-Host "Set missing secrets (one-time):" -ForegroundColor Cyan
Write-Host '  gh secret set RAILWAY_TOKEN --repo VoXc2/dealix'
Write-Host '  gh secret set DEALIX_ADMIN_API_KEY --repo VoXc2/dealix'
Write-Host '  gh variable set DEALIX_FRONTEND_BASE --repo VoXc2/dealix --body "https://dealix.me"'

Write-Host ""
Write-Host "Workflows enabled on push/dispatch:" -ForegroundColor Cyan
Write-Host "  .github/workflows/railway_deploy.yml"
Write-Host "  .github/workflows/railway_deploy_frontend.yml"
Write-Host "  .github/workflows/production_layers_verify.yml"
Write-Host "  .github/workflows/founder_commercial_daily.yml"

if ($missing.Count -gt 0) {
    Write-Host "GH_ACTIONS_PRODUCTION=INCOMPLETE" -ForegroundColor Yellow
    exit 1
}
Write-Host "GH_ACTIONS_PRODUCTION=OK" -ForegroundColor Green
exit 0
