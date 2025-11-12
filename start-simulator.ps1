# Script para iniciar el simulador de telemetría V4.0

Write-Host "🐄 Iniciando Simulador CAMPORT V4.0 - Rebaño Completo..." -ForegroundColor Green
Write-Host ""
Write-Host "✨ Nuevas Características V4.0:" -ForegroundColor Cyan
Write-Host "  🐄 Simula TODO el rebaño en cada ciclo" -ForegroundColor White
Write-Host "  ⏱️  Movimiento LENTO y REALISTA (20 segundos)" -ForegroundColor White
Write-Host "  🔄 Consulta dinámica de geocercas EN VIVO" -ForegroundColor White
Write-Host "  📡 Reacciona automáticamente a cambios de asignación" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Intervalo: 20 segundos | Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

Set-Location backend
.\venv\Scripts\Activate.ps1

# Usar V4.0 con intervalo realista de 20 segundos
python manage.py simulate_collars --interval 20
