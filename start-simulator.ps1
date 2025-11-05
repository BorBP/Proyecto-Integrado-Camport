# Script para iniciar el simulador de telemetría

Write-Host "📡 Iniciando Simulador de Telemetría..." -ForegroundColor Green
Write-Host ""
Write-Host "Este script simulará datos de telemetría para 5 animales" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

Set-Location backend
.\venv\Scripts\Activate.ps1

python simulator.py
