# Founder go-live verify — Windows wrapper
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

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

$Fail = 0

Write-Host "== Founder go-live: Business NOW =="
try {
  & "$Root\scripts\run_business_now.ps1"
  Write-Host "  business_now: PASS"
} catch {
  Write-Host "  business_now: FAIL"
  $Fail = 1
}

Write-Host ""
Write-Host "== Founder go-live: golden chain =="
Invoke-Python -m pytest tests/test_revenue_os_golden_chain_smoke.py -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 } else { Write-Host "  golden_chain: PASS" }

Write-Host ""
Write-Host "== Founder go-live: commercial autopilot docs =="
$commFiles = @(
  "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md",
  "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
  "docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md",
  ".github/workflows/daily-revenue-machine.yml",
  "scripts/run_founder_commercial_day.sh",
  "scripts/generate_weekly_content_drafts.py"
)
foreach ($f in $commFiles) {
  if (Test-Path (Join-Path $Root $f)) { Write-Host "  ok: $f" }
  else { Write-Host "  MISSING: $f"; $Fail = 1 }
}

Write-Host ""
Write-Host "== Founder go-live: revenue_ops_autopilot import =="
Invoke-Python -c "from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator; get_default_orchestrator()"
if ($LASTEXITCODE -ne 0) { $Fail = 1 } else { Write-Host "  orchestrator: PASS" }

Write-Host ""
Write-Host "== Founder go-live: integration truth summary =="
Invoke-Python -c @"
from dealix.business_now.integration_truth import build_integration_truth_summary
s = build_integration_truth_summary()
c = s.get('counts') or {}
print('  overall_status:', s.get('overall_status'))
print('  counts: green=%s yellow=%s red=%s' % (c.get('green',0), c.get('yellow',0), c.get('red',0)))
print('  yaml:', s.get('source_yaml'))
"@

Write-Host ""
if ($Fail -eq 0) {
  Write-Host "FOUNDER_GO_LIVE_VERDICT: PASS"
  Write-Host "Next: scripts/run_founder_commercial_day.ps1"
  exit 0
}
Write-Host "FOUNDER_GO_LIVE_VERDICT: FAIL"
exit 1
