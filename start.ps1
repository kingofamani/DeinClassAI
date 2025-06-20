# DeinClassAI System Startup Script (Windows PowerShell)
# Set UTF-8 encoding for console output
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Starting DeinClassAI System..." -ForegroundColor Green

# Check Docker
try {
    docker info | Out-Null
    Write-Host "Docker is running" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not running" -ForegroundColor Red
    exit 1
}

# Check docker-compose
try {
    docker-compose --version | Out-Null
    Write-Host "docker-compose is available" -ForegroundColor Green
} catch {
    Write-Host "Error: docker-compose not found" -ForegroundColor Red
    exit 1
}

# Check .env.litellm file
if (!(Test-Path ".env.litellm")) {
    Write-Host "Warning: .env.litellm file not found" -ForegroundColor Yellow
    Write-Host "Creating from template..." -ForegroundColor Yellow
    
    $response = Read-Host "Create .env.litellm file? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Copy-Item .env.litellm.example .env.litellm
        Write-Host "Created .env.litellm file" -ForegroundColor Green
    } else {
        Write-Host "Please create .env.litellm file manually" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Starting services..." -ForegroundColor Yellow

# Start all services
docker-compose --profile full up -d

# Wait for startup
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "Service Status Check:" -ForegroundColor Cyan

# PostgreSQL
$postgresStatus = docker-compose ps postgres
if ($postgresStatus -match "Up") {
    Write-Host "PostgreSQL Database: Running" -ForegroundColor Green
} else {
    Write-Host "PostgreSQL Database: Failed" -ForegroundColor Red
}

# LiteLLM
$litellmStatus = docker-compose ps litellm
if ($litellmStatus -match "Up") {
    Write-Host "LiteLLM Service: Running" -ForegroundColor Green
    Write-Host "  Management: http://localhost:4000" -ForegroundColor White
} else {
    Write-Host "LiteLLM Service: Failed" -ForegroundColor Red
}

# Open WebUI
$webuiStatus = docker-compose ps open_webui
if ($webuiStatus -match "Up") {
    Write-Host "Open WebUI: Running" -ForegroundColor Green
    Write-Host "  Student Interface: http://localhost:8080" -ForegroundColor White
} else {
    Write-Host "Open WebUI: Failed" -ForegroundColor Red
}

# Teacher Panel
$teacherStatus = docker-compose ps teacher_panel
if ($teacherStatus -match "Up") {
    Write-Host "Teacher Panel: Running" -ForegroundColor Green
    Write-Host "  Management Interface: http://localhost:5000" -ForegroundColor White
} else {
    Write-Host "Teacher Panel: Not started" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "DeinClassAI System startup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor Cyan
Write-Host "  Teacher Panel: http://localhost:5000" -ForegroundColor White
Write-Host "  Student AI: http://localhost:8080" -ForegroundColor White
Write-Host "  LiteLLM: http://localhost:4000" -ForegroundColor White
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  1. Open Teacher Panel to create student keys" -ForegroundColor White
Write-Host "  2. Students scan QR Code to setup" -ForegroundColor White
Write-Host "  3. Students use AI classroom" -ForegroundColor White
Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  Stop: docker-compose down" -ForegroundColor White
Write-Host "  Logs: docker-compose logs -f [service]" -ForegroundColor White

# Open browser
Write-Host ""
$openBrowser = Read-Host "Open Teacher Panel in browser? (y/N)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "http://localhost:5000"
} 