$ErrorActionPreference = "Stop"

Write-Host "Starting RAGLens collector and dashboard..."
Write-Host ""

$scriptDir = $PSScriptRoot
$collectorScript = Join-Path $scriptDir "start-collector.ps1"
$dashboardScript = Join-Path $scriptDir "start-dashboard.ps1"

$collectorProcess = Start-Process -FilePath "powershell" -ArgumentList @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", $collectorScript
) -PassThru

try {
    Start-Sleep -Seconds 2
    & $dashboardScript
}
finally {
    if ($collectorProcess -and -not $collectorProcess.HasExited) {
        Stop-Process -Id $collectorProcess.Id -Force
    }
}