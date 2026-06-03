# Print actionable blockers before PRODUCTION_LAYERS_VERDICT=PASS (no secrets)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== Production go-live blockers ==" -ForegroundColor Cyan

$ahead = git rev-list --count origin/main..HEAD 2>$null
if ($ahead -and [int]$ahead -gt 0) {
    Write-Host "  GIT: $ahead commit(s) ahead of origin/main - push required for /version + /api/v1/meta"
    git log origin/main..HEAD --oneline 2>$null | ForEach-Object { Write-Host "    $_" }
    Write-Host "  FIX: gh auth login -s repo  then  powershell -File scripts/push_main_with_gh.ps1"
} else {
    Write-Host "  GIT: in sync with origin/main"
}

py -3 scripts/railway_redeploy_checklist.py
$redeploy = $LASTEXITCODE

py -3 scripts/production_layers_verify.py --from-railway-env 2>&1 | Select-String -Pattern "verdict:|Layer |blocker|probe "
if (Test-Path (Join-Path $Root ".env.railway.generated")) {
    py -3 scripts/validate_railway_generated_env.py 2>&1 | Select-String -Pattern "FAIL|ok:|INCOMPLETE|complete"
}

try {
    $ar = Invoke-WebRequest -Uri "https://dealix.me/ar" -Method Head -UseBasicParsing -TimeoutSec 12
    $srv = $ar.Headers["Server"]
    Write-Host ("  FRONTEND: /ar -> {0} Server={1}" -f $ar.StatusCode, $srv)
    if ($srv -match "GitHub") {
        Write-Host "  FIX: docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
    }
} catch {
    Write-Host "  FRONTEND: /ar probe failed"
}

if ($redeploy -eq 0) {
    Write-Host "`nNEXT: powershell -File scripts/poll_production_trust_layer.ps1" -ForegroundColor Green
    Write-Host "      py -3 scripts/production_layers_verify.py --from-railway-env --write-cache --strict"
} else {
    Write-Host ""
    Write-Host 'NEXT: Railway API Deploy latest main, then poll script above' -ForegroundColor Yellow
}
