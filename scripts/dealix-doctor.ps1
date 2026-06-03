$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " DEALIX DOCTOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nPowerShell:" -ForegroundColor Yellow
$PSVersionTable.PSVersion

Write-Host "`nGit:" -ForegroundColor Yellow
git --version

Write-Host "`nPython:" -ForegroundColor Yellow
python --version

Write-Host "`nAider:" -ForegroundColor Yellow
try {
    aider --version
} catch {
    Write-Host "Aider not found in PATH." -ForegroundColor Red
}

Write-Host "`nDealix CLI:" -ForegroundColor Yellow
& "$PSScriptRoot\dealix.ps1" doctor

Write-Host "`nGit status:" -ForegroundColor Yellow
git status --short

Write-Host "`nLarge tracked files:" -ForegroundColor Yellow
Get-ChildItem ".dealix\reports\large-tracked-files-*.txt" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 |
    ForEach-Object {
        Write-Host $_.FullName
        Get-Content $_.FullName
    }