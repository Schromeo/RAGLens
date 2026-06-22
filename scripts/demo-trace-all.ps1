$ErrorActionPreference = "Stop"

Write-Host "RAGLens demo: generating local RAG traces..."
Write-Host "Collector: http://localhost:4319"
Write-Host ""

$env:RAGLENS_COLLECTOR_URL = "http://localhost:4319"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sdkPythonDir = Join-Path $repoRoot "sdk/python"

Set-Location $sdkPythonDir

python -m examples.local_rag_demo.run_demo trace-all

Write-Host ""
Write-Host "Done."
Write-Host "Open the RAGLens dashboard and inspect the generated traces."