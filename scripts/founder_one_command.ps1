# Dealix founder — one command for maximum governed autonomous day (no external send).
# Usage: powershell -File scripts/founder_one_command.ps1 [-Evening] [-Weekly] [-SkipCommercialDay]

param(
    [switch]$Evening,
    [switch]$Weekly,
    [switch]$SkipCommercialDay,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$args = @("scripts/run_dealix_complete_autonomous_day.py")
if ($Evening) { $args += "--evening" }
if ($Weekly) { $args += "--weekly" }
if ($SkipCommercialDay) { $args += "--skip-commercial-day" }
if ($DryRun) { $args += "--dry-run" }

py -3 @args
exit $LASTEXITCODE
