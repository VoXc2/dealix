# Dealix legacy Aider watchdog — governed migration HOLD
param(
    [ValidateSet(1, 2, 3)]
    [int]$Gear = 1,
    [switch]$NoCreditCheck
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "Dealix legacy Aider watchdog is disabled." -ForegroundColor Yellow
Write-Host "It must not select, restart, or persist a model/provider outside the canonical Dealix execution fabric." -ForegroundColor Yellow
Write-Host "Use Company Operator -> ResourceGovernor/Session Factory -> OpenCode instead." -ForegroundColor Cyan
Write-Host "Canonical policy: trusted non-DeepSeek capacity or HOLD; never an implicit provider/default fallback." -ForegroundColor Cyan
Write-Host ""

# Compatibility parameters are accepted only so old operator shortcuts fail
# closed with a deterministic migration signal instead of silently routing.
exit 64
