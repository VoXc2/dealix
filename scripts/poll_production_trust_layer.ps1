# Poll api.dealix.me trust layer until /version and /api/v1/meta return 200 (post Railway deploy)
param(
    [int]$Attempts = 24,
    [int]$SleepSec = 15,
    [string]$ApiBase = "https://api.dealix.me"
)

$ErrorActionPreference = "Continue"
$ok = $false
for ($i = 1; $i -le $Attempts; $i++) {
    $version = $null
    $meta = $null
    try {
        $r = Invoke-WebRequest -Uri "$ApiBase/version" -UseBasicParsing -TimeoutSec 12
        $version = $r.StatusCode
    } catch {
        $version = $_.Exception.Response.StatusCode.value__
    }
    try {
        $r = Invoke-WebRequest -Uri "$ApiBase/api/v1/meta" -UseBasicParsing -TimeoutSec 12
        $meta = $r.StatusCode
    } catch {
        $meta = $_.Exception.Response.StatusCode.value__
    }
    Write-Host ("[{0}/{1}] version={2} meta={3}" -f $i, $Attempts, $version, $meta)
    if ($version -eq 200 -and $meta -eq 200) {
        $ok = $true
        break
    }
    Start-Sleep -Seconds $SleepSec
}
if ($ok) {
    Write-Host "PRODUCTION_TRUST_LAYER=READY" -ForegroundColor Green
    exit 0
}
Write-Host "PRODUCTION_TRUST_LAYER=NOT_READY" -ForegroundColor Yellow
Write-Host "  Push main + Railway Deploy latest (see scripts/railway_redeploy_checklist.py)"
exit 1
