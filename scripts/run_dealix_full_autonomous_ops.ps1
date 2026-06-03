# Maximum governed autonomous ops (expand + founder day + gates + report)
# Usage: powershell -File scripts/run_dealix_full_autonomous_ops.ps1
#        powershell -File scripts/run_dealix_full_autonomous_ops.ps1 -StatusOnly
param(
    [switch]$SkipExpand,
    [switch]$SkipFounderDay,
    [switch]$SkipGates,
    [switch]$StatusOnly
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

$argsList = @("scripts/run_dealix_full_autonomous_ops.py")
if ($SkipExpand) { $argsList += "--skip-expand" }
if ($SkipFounderDay) { $argsList += "--skip-founder-day" }
if ($SkipGates) { $argsList += "--skip-gates" }
if ($StatusOnly) { $argsList += "--status-only" }

if ($env:PY) { & $env:PY @argsList } else { & py -3 @argsList }
exit $LASTEXITCODE
