# Unified official commercial launch gate (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"
$Fail = 0

$Py = $env:PY
$PyArgs = @()
if (-not $Py) {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    $Py = "py"
    $PyArgs = @("-3")
  } elseif (Test-Path "$env:LOCALAPPDATA\Python\bin\python.exe") {
    $Py = "$env:LOCALAPPDATA\Python\bin\python.exe"
  } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $Py = "python3"
  } else {
    Write-Host "DEALIX_COMMERCIAL_GO_LIVE_VERDICT=FAIL"
    Write-Host "python not found (install py launcher or set PY)"
    exit 1
  }
}
if ($Py -eq "py" -and $PyArgs.Count -eq 0) { $PyArgs = @("-3") }

Write-Host "== Dealix commercial go-live (unified) =="

Write-Host "`n== 1/4 Founder operating system =="
& (Join-Path $PSScriptRoot "verify_founder_operating_system.ps1")
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host "`n== 2/4 Commercial soft launch =="
$launchArgs = @("scripts/verify_commercial_launch_ready.py")
if ($env:DEALIX_VERIFY_WITH_API -eq "1") { $launchArgs += "--with-api" }
if ($env:DEALIX_VERIFY_WITH_FRONTEND_BUILD -eq "1") { $launchArgs += "--with-frontend-build" }
& $Py @PyArgs @launchArgs
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host "`n== 3/4 Company ready =="
& (Join-Path $PSScriptRoot "company_ready_verify.ps1") -SkipGoLive
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host "`n== 4/4 Daily ops dry-run =="
& $Py @PyArgs scripts/run_dealix_daily_ops.py --dry-run --skip-api
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if ($Fail -eq 0) {
  Write-Host "`nDEALIX_COMMERCIAL_GO_LIVE_VERDICT=PASS"
  Write-Host "DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS"
  Write-Host "Next: powershell -File scripts/run_founder_commercial_day.ps1"
  exit 0
}
Write-Host "`nDEALIX_COMMERCIAL_GO_LIVE_VERDICT=FAIL"
Write-Host "DEALIX_OFFICIAL_LAUNCH_VERDICT=FAIL"
exit 1
