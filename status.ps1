# DeinClassAI System Status Check
# Set UTF-8 encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "DeinClassAI System Status" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check service status
$services = @(
    @{Name="PostgreSQL Database"; Service="postgres"; Port="5432"}
    @{Name="LiteLLM Service"; Service="litellm"; Port="4000"}
    @{Name="Open WebUI"; Service="open_webui"; Port="8080"}
    @{Name="Teacher Panel"; Service="teacher_panel"; Port="5000"}
)

foreach ($svc in $services) {
    $status = docker-compose ps $svc.Service
    if ($status -match "Up") {
        Write-Host "$($svc.Name): Running" -ForegroundColor Green
        Write-Host "  URL: http://localhost:$($svc.Port)" -ForegroundColor White
    } else {
        Write-Host "$($svc.Name): Stopped" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Yellow
Write-Host "  Start: .\start.ps1" -ForegroundColor White
Write-Host "  Stop:  docker-compose down" -ForegroundColor White
Write-Host "  Logs:  docker-compose logs -f [service]" -ForegroundColor White 