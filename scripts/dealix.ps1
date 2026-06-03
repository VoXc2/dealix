param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$root = Resolve-Path "$PSScriptRoot\.."
$v2 = Join-Path $root "dealix-v2"

if (!(Test-Path $v2)) {
    Write-Host "dealix-v2 not found. Run Founder OS installer first." -ForegroundColor Red
    exit 1
}

Push-Location $v2
python -m dealix_os.cli @Args
$code = $LASTEXITCODE
Pop-Location
exit $code