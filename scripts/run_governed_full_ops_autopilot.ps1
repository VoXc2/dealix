# Governed full-ops autopilot — morning / evening / weekly (draft-only)
param(
    [switch]$Morning,
    [switch]$Evening,
    [switch]$Full,
    [switch]$DryRun,
    [switch]$SkipGates,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$argsList = @("scripts/run_governed_full_ops_autopilot.py")
if ($Morning) { $argsList += "--morning" }
if ($Evening) { $argsList += "--evening" }
if ($Full) { $argsList += "--full" }
if ($DryRun) { $argsList += "--dry-run" }
if ($SkipGates) { $argsList += "--skip-gates" }
if ($Json) { $argsList += "--json" }
if (-not ($Morning -or $Evening -or $Full -or $DryRun)) { $argsList += "--morning" }

if ($env:PY) { & $env:PY @argsList } else { & py -3 @argsList }
exit $LASTEXITCODE
