# Founder evening — evidence reminder (Windows)
# Usage: powershell -File scripts/founder_evening.ps1
#        powershell -File scripts/founder_evening.ps1 -Append -Company "Agency X" -EventType message_sent_manual
param(
    [switch]$Append,
    [string]$Company = "",
    [string]$EventType = "message_sent_manual",
    [string]$Notes = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$argsList = @("scripts/founder_evening_evidence.py")
if ($Append) {
    $argsList += @("--append", "--event-type", $EventType, "--company", $Company)
    if ($Notes) { $argsList += @("--notes", $Notes) }
}
if ($env:PY) { & $env:PY @argsList } else { & py -3 @argsList }
exit $LASTEXITCODE
