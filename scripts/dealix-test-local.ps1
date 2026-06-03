$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\.."
Set-Location $root

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " DEALIX LOCAL TEST" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

py -3 ".\dealix-v2\dealix_os\cli.py" doctor
py -3 ".\dealix-v2\dealix_os\cli.py" services
py -3 ".\dealix-v2\dealix_os\cli.py" governance-check "we guarantee sales and send WhatsApp automatically"

try {
    py -3 ".\dealix-v2\dealix_os\cli.py" score "paid B2B agency partner with monthly retainer and CRM data"
} catch {
    Write-Host "score command not available yet. Aider will add it in Phase 2." -ForegroundColor Yellow
}

Write-Host "DONE" -ForegroundColor Green
