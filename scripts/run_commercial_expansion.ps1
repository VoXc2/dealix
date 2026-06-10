# Full commercial expansion (default: wave4 + 28w + gates)
# Usage: powershell -File scripts/run_commercial_expansion.ps1
#        powershell -File scripts/run_commercial_expansion.ps1 -Wave3
#        powershell -File scripts/run_commercial_expansion.ps1 -SkipGates -WithFounderDay
param(
    [switch]$Wave2,
    [switch]$Wave3,
    [switch]$Wave4,
    [switch]$Full,
    [switch]$SkipGates,
    [switch]$SkipGoLive,
    [switch]$WithFounderDay,
    [int]$Meetings = 10,
    [int]$TouchDrafts = 20
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

$argsList = @(
    "scripts/run_commercial_expansion.py",
    "--meetings", "$Meetings",
    "--touch-drafts", "$TouchDrafts"
)
if ($Wave2) { $argsList += "--wave2" }
elseif ($Wave3) { $argsList += "--wave3" }
elseif ($Wave4 -or $Full) { $argsList += "--wave4" }
else { $argsList += "--full" }
if ($SkipGates) { $argsList += "--skip-gates" }
if ($SkipGoLive) { $argsList += "--skip-go-live" }
if ($WithFounderDay) { $argsList += "--with-founder-day" }

if ($env:PY) { & $env:PY @argsList } else { & py -3 @argsList }
exit $LASTEXITCODE
