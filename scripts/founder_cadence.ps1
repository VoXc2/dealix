# Founder cadence — morning default, optional evening / weekly (Windows)
# Usage:
#   powershell -File scripts/founder_cadence.ps1
#   powershell -File scripts/founder_cadence.ps1 -Evening
#   powershell -File scripts/founder_cadence.ps1 -Weekly
param(
    [switch]$Evening,
    [switch]$Weekly,
    [switch]$Complete,
    [switch]$DryRun,
    [switch]$Full
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if ($Evening) {
    py -3 scripts/run_founder_strongest_ops.py --evening
    $args = @()
    if ($DryRun) { $args += "-DryRun" }
    & (Join-Path $PSScriptRoot "founder_evening.ps1") @args
    exit $LASTEXITCODE
}

if ($Complete) {
    $completeArgs = @()
    if ($DryRun) { $completeArgs += "--dry-run" }
    if ($Evening) { $completeArgs += "--evening" }
    if ($Weekly) { $completeArgs += "--weekly" }
    py -3 scripts/run_dealix_complete_autonomous_day.py @completeArgs
    exit $LASTEXITCODE
}

if ($Weekly) {
    py -3 scripts/run_founder_strongest_ops.py --weekly --run-checks
    py -3 scripts/founder_weekly_scorecard.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 scripts/founder_all_motions_pipeline.py --top-n 5
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 scripts/founder_comprehensive_plan_status.py
    exit $LASTEXITCODE
}

py -3 scripts/run_founder_strongest_ops.py --morning
py -3 scripts/run_full_commercial_ops_autopilot.py --execute --top-n 15
py -3 scripts/founder_dogfooding_war_room_sync.py
$morningArgs = @()
if ($DryRun) { $morningArgs += "-DryRun" }
if ($Full) { $morningArgs += "-Full" }
& (Join-Path $PSScriptRoot "founder_morning.ps1") @morningArgs
$morningRc = $LASTEXITCODE
py -3 scripts/founder_comprehensive_plan_status.py
if ($morningRc -ne 0) { exit $morningRc }
exit $LASTEXITCODE
