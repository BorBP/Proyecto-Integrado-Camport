# CAMPORT V8.0 - Script de Inicio del Simulador
# Signos Vitales Realistas con Intervalos Independientes

Write-Host "================================================================" -ForegroundColor Green
Write-Host "   CAMPORT V8.0 - SIGNOS VITALES + INTERVALOS INDEPENDIENTES" -ForegroundColor Green  
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
cd backend
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Iniciando simulador V8.0..." -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Características V8.0:" -ForegroundColor White
Write-Host "  ✅ Intervalos independientes (Movimiento/Temp/BPM)" -ForegroundColor White
Write-Host "  ✅ Signos vitales con variación gradual" -ForegroundColor White
Write-Host "  ✅ Alertas inteligentes (solo con geocerca)" -ForegroundColor White
Write-Host "  ✅ Sistema de cooldown anti-spam" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Ejecutar simulador V8.0 con parámetros por defecto
# Puedes modificar los intervalos aquí:
python manage.py simulate_collars_v8 `
    --interval-movement 3 `
    --interval-temperature 5 `
    --interval-bpm 2 `
    --alert-cooldown-vitals 180 --alert-cooldown-perimeter 60

cd ..
