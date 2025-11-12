# Script para iniciar el simulador de telemetría V6.0

Write-Host "🐄 Iniciando Simulador CAMPORT V6.0 - Gravedad de Centroide..." -ForegroundColor Green
Write-Host ""
Write-Host "✨ Nuevas Características V6.0:" -ForegroundColor Cyan
Write-Host "  🧲 Gravedad de Centroide (atracción natural al centro)" -ForegroundColor White
Write-Host "  🌊 Migración automática a nuevos centros de geocerca" -ForegroundColor White
Write-Host "  📊 Movimiento proactivo (80% aleatorio + 20% atracción)" -ForegroundColor White
Write-Host ""
Write-Host "✨ Características V5.0 (Heredadas):" -ForegroundColor Cyan
Write-Host "  🚨 Sistema de Fugas Aleatorias (cada 60 segundos)" -ForegroundColor White
Write-Host "  🏠 Retorno Automático (después de 30 segundos)" -ForegroundColor White
Write-Host "  📊 Temperatura con 1 decimal (realista)" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Intervalo: 20 segundos | Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

Set-Location backend
.\venv\Scripts\Activate.ps1

# Usar V6.0 con gravedad de centroide (20% atracción por defecto)
python manage.py simulate_collars --interval 20 --gravity-factor 0.2
