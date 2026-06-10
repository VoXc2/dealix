# Maximum governed autonomous day (Windows)
# Usage:
#   powershell -File scripts/run_dealix_complete_autonomous_day.ps1
#   powershell -File scripts/run_dealix_complete_autonomous_day.ps1 -DryRun
#   powershell -File scripts/run_dealix_complete_autonomous_day.ps1 -Weekly -Evening
param(
    [switch]$DryRun,
    [switch]$SkipCommercialDay,
    [switch]$Evening,
    [switch]$Weekly,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$argsList = @()
if ($DryRun) { $argsList += "--dry-run" }
if ($SkipCommercialDay) { $argsList += "--skip-commercial-day" }
if ($Evening) { $argsList += "--evening" }
if ($Weekly) { $argsList += "--weekly" }
if ($Json) { $argsList += "--json" }

py -3 scripts/run_dealix_complete_autonomous_day.py @argsList
exit $LASTEXITCODE
