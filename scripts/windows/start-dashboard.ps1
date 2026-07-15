$ErrorActionPreference = "Stop"

Write-Host "Starting SledTrace dashboard..."
Write-Host ""

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$dashboardDir = Join-Path $repoRoot "dashboard\web"

if (-not (Test-Path $dashboardDir)) {
    Write-Error "Dashboard directory not found: $dashboardDir"
}

Set-Location $dashboardDir

if (-not (Test-Path "node_modules")) {
    Write-Host "node_modules not found."
    Write-Host "Run npm install in the dashboard directory first:"
    Write-Host "  cd dashboard/web"
    Write-Host "  npm install"
    exit 1
}

npm run dev