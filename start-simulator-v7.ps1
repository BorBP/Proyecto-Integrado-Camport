# CAMPORT V7.0 - Script de Inicio del Simulador
# Simulador con Random Walk Natural y Oveja Negra

Write-Host "==========================================" -ForegroundColor Green
Write-Host "   CAMPORT V7.0 - SIMULADOR NATURAL" -ForegroundColor Green  
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
cd backend
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Iniciando simulador V7.0..." -ForegroundColor Yellow
Write-Host "Características:" -ForegroundColor White
Write-Host "  - Random Walk puro (sin gravedad de centroide)" -ForegroundColor White
Write-Host "  - Oveja negra con tendencia a escapar" -ForegroundColor White  
Write-Host "  - Abstracción total de geocercas" -ForegroundColor White
Write-Host "  - Adaptabilidad dinámica" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Ejecutar simulador V7.0
python manage.py simulate_collars_v7 --interval 20

cd ..
