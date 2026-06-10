# Governed founder full autopilot (Windows)
param(
    [ValidateSet("full", "morning", "evening", "weekly", "brief-only")]
    [string]$Mode = "full",
    [switch]$DryRun,
    [switch]$SkipMorning,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$argsList = @("--mode", $Mode)
if ($DryRun) { $argsList += "--dry-run" }
if ($SkipMorning) { $argsList += "--skip-morning" }
if ($Json) { $argsList += "--json" }

py -3 scripts/run_founder_full_autopilot.py @argsList
exit $LASTEXITCODE
