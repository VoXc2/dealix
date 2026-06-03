# Verify Founder Operating System (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
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
    Write-Host "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
    Write-Host "python not found (install py launcher or set PY)"
    exit 1
  }
}
if ($Py -eq "py" -and $PyArgs.Count -eq 0) { $PyArgs = @("-3") }
$Fail = 0

Write-Host "== 1/2 Founder commercial day dry-run =="
& (Join-Path $PSScriptRoot "run_founder_commercial_day.ps1") -DryRun
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host "`n== 2/2 pytest bundle =="
$tests = @(
  "tests/test_founder_revenue_day_script.py",
  "tests/test_targeting_rotation.py",
  "tests/test_outreach_drafts.py",
  "tests/test_generate_weekly_content_drafts.py",
  "tests/test_commercial_ops_digest.py"
)
& $Py @PyArgs -m pytest @tests -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if ($Fail -eq 0) {
  Write-Host "`nFOUNDER_OPERATING_SYSTEM_VERDICT=PASS"
  exit 0
}
Write-Host "`nFOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
exit 1
