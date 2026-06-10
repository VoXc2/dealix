# Company ready verify — Windows wrapper
param(
    [switch]$DocsOnly,
    [switch]$SkipGoLive
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

$Fail = 0
$Required = @(
    "docs/company/DEALIX_COMPANY_READY_MASTER_AR.md",
    "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md",
    "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
    "docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md",
    "docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md",
    "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
    "scripts/run_founder_revenue_day.sh",
    "scripts/run_founder_commercial_day.sh",
    "scripts/verify_dealix_commercial_go_live.sh"
)

Write-Host "== Company ready: required docs =="
foreach ($f in $Required) {
    $p = Join-Path $Root $f
    if (Test-Path $p) { Write-Host "  ok: $f" }
    else { Write-Host "  MISSING: $f"; $Fail = 1 }
}

if ($DocsOnly) {
    if ($Fail -eq 0) { Write-Host "COMPANY_READY_VERDICT: PASS (docs-only)"; exit 0 }
    Write-Host "COMPANY_READY_VERDICT: FAIL (docs-only)"; exit 1
}

function Invoke-Python {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PyArgs)
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 @PyArgs
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python @PyArgs
    } else {
        throw "python not found"
    }
}

Write-Host ""
Write-Host "== Company ready: imports =="
Invoke-Python -c @"
from dealix.commercial_ops.digest import build_commercial_digest
from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator
get_default_orchestrator()
build_commercial_digest(skip_no_build=True)
"@
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host ""
Write-Host "== Company ready: pytest =="
Invoke-Python -m pytest tests/test_founder_commercial_digest.py tests/test_founder_commercial_day_script.py tests/test_generate_weekly_content_drafts.py tests/test_company_ready_verify.py tests/test_client_pack.py -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if (-not $SkipGoLive) {
    Write-Host ""
    Write-Host "== Company ready: founder go-live =="
    & "$Root\scripts\founder_go_live_verify.ps1"
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
}

Write-Host ""
if ($Fail -eq 0) {
    Write-Host "COMPANY_READY_VERDICT: PASS"
    Write-Host "Next: scripts/run_founder_revenue_day.ps1"
    exit 0
}
Write-Host "COMPANY_READY_VERDICT: FAIL"
exit 1
